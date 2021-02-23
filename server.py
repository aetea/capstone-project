"Server for looksee app"

# =======================================
#        Imports & Initalise
# =======================================

# imports for working with API
import requests
from pprint import pprint

# imports for app server
from flask import Flask, request, render_template, jsonify, redirect
from model import db, connect_to_db, User, City, UserCity
from crud import connect_one_usercity, get_user_cities, get_city_users, \
update_status, update_current_local

app = Flask(__name__)   # create a Flask object called "app"

# =======================================
#         API functions 
# =======================================
#    move to another file? 

# fetch data from teleport API
def tp_search_city(city_name):
    """Get basic city info from Teleport API and save to db."""

    # send request to api endpoint, get Response object, turn into dict
    res = requests.get(f"https://api.teleport.org/api/cities/?search={city_name}&limit=1")
    res_dict = res.json()
    # pprint(res_dict)

    top_city_found = res_dict["_embedded"]["city:search-results"][0]
    top_city_link = top_city_found["_links"]["city:item"]["href"]

    ### get city info for top result
    res_city = requests.get(top_city_link)
    tele_city_dict = res_city.json()
    # pprint(tele_city_dict)

    # clean up response and make dict
    tele_city_more = tele_city_dict["_links"]

    # get city name from teleport
    tele_name = tele_city_dict["name"]
    # always get country and city_id from teleport
    tele_country = tele_city_more["city:country"]["name"]
    tele_city_id = tele_city_dict["geoname_id"]

    # handle errors: when no city details available
    # city may have no urban area, eg venice, kolkata
    try:
        tele_ua = tele_city_more["city:urban_area"]["name"]
    except:
        print("sorry! no city info available from teleport")
        # add to db (without ua) anyway?? 
        return None

    tele_ua = tele_city_more["city:urban_area"]["name"]

    ### add city info to db
    city_db_add = City(city_name=tele_name.lower(), urban_area=tele_ua.lower(), 
                    country=tele_country.lower(), teleport_id=tele_city_id)

    # TODO: also get ua-id and image? 
    print(f">> before trying to init this city: {city_db_add}")
    db.session.add(city_db_add)
    db.session.commit()

    print(f">> after db commit: {city_db_add}")

    return city_db_add


def tp_get_city_details(tele_city_id):
    """Get detailed info and scores about a city from Teleport API."""

    pass 


# check DB and populate from teleport API if necessary
def check_db(city_name):
    """Check if db contains city, if not populate basic info from Teleport API."""

    if City.query.filter_by(city_name=city_name).count() == 0:
        # if no record in db, ping teleport and add to db
        print("city not in db, adding basic info from Teleport")
        tp_search_city(city_name)    
    else:
        print("city is in db")

# =======================================
#           Flask Routes 
# =======================================

@app.route("/")
def index():
    """Show index.html template."""
    
    return render_template("index.html") 


@app.route("/city-info")
def city_info_blank():
    """Show blank city info page."""

    return render_template("city-info.html")


@app.route("/city-info/<city_name>")
def city_info(city_name):
    """Show city info page for a given city."""

    check_db(city_name)
    # FIXME: returns None if no city info found in teleport
    # show a better error msg

    city = City.query.filter_by(city_name=city_name).first()
    ada = User.query.get(1) 
    print("found a city object: {}".format(city))
    print(" * " * 15)

    # ## TODO: pass json of city instead of City object?
    # city_dict = city.make_dict()
    # jsonify(city_dict)

    return render_template("city-info.html", city=city, user=ada)


@app.route("/city-search")
def search_city():
    """Query db and return matching city."""

    # get city name from search form
    city_name = request.args.get("city-search") 

    return redirect(f"/city-info/{city_name}")


# TODO: (v2) add functionality to save as "lived here previously"
@app.route("/save-city", methods=["POST"])
def save_city(): 
    """Create usercity connection between given user and city."""

    # grab user from $post
    # grab city from $post 
    # connect_userid = request.form.get("user")
    connect_userid = 1 #FIXME: handle real user
    connect_cityid = request.form.get("save-btn")

    print(f"connecting user:{connect_userid} to city:{connect_cityid}...")

    # make usercity record 
    connect_one_usercity(connect_userid, connect_cityid) 

    # get usercity record from server
    try:
        UserCity.query.filter((UserCity.user_id==connect_userid) & 
                              (UserCity.city_id==connect_cityid)).one()
    except:
        print("usercity creation failed.")
    else:
        usercity = UserCity.query.filter((UserCity.user_id==connect_userid) & 
                              (UserCity.city_id==connect_cityid)).one()
        city_name = usercity.city.city_name

    return redirect(f"/city-info/{city_name}")


@app.route("/api/city")
def city_api():
    """Return city information only."""

    city_name = request.args.get("cname")
    print(" * " * 15)
    print("got a city_name: {}".format(city_name))

    # check or populate db for city basics
    check_db(city_name)

    # get city object from db
    city = City.query.filter_by(city_name=city_name).first()
    print("found a city object: {}".format(city))
    print(" * " * 15)

    city_dict = city.make_dict()

    return jsonify(city_dict)


# =======================================
#          Main Server Function 
# =======================================

if __name__ == "__main__":
    connect_to_db(app)  # creates relationship btwn flask obj and db 
    app.run(host='0.0.0.0', debug=True)
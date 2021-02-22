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
    """Use Teleport API to search for a city and get basic info to save to db."""

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

    # TODO: also get ua-id and image? 
    tele_name = tele_city_dict["name"]
    tele_ua = tele_city_more["city:urban_area"]["name"]
    tele_country = tele_city_more["city:country"]["name"]
    tele_city_id = tele_city_dict["geoname_id"]

    ### add city info to db
    # FIXME: city name from API is title case, db has lowercase --> make consistent
    city_db_add = City(city_name=tele_name.lower(), urban_area=tele_ua.lower(), 
                       country=tele_country.lower(), teleport_id=tele_city_id)

    print(f">> before trying to init this city: {city_db_add}")
    db.session.add(city_db_add)
    db.session.commit()

    print(f">> after db commit: {city_db_add}")

    return city_db_add


def tp_get_city_details(tele_city_id):
    """Use Teleport API to get detailed info and scores about a city."""

    pass 

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

    city = City.query.filter_by(city_name=city_name).first()
    ada = User.query.get(1)

    return render_template("city-info.html", city=city, user=ada)


@app.route("/city-search")
def search_city():
    """Query db and return matching city."""

    # get city name from search form
    city_name = request.args.get("city-search")

    # query db/api for city info
    # city = City.query.filter_by(city_name=city_name).first()

    # return render_template("city-info.html", 
    #                         cityname=city_name, 
    #                         cityinfo=city)

    return redirect(f"/city-info/{city_name}")


@app.route("/save-city", methods=["POST"])
def save_city(): 
    """Create usercity connection between given user and city."""

    # grab user from $post
    # grab city from $post 
    connect_userid = request.form.get("user")
    connect_cityid = request.form.get("cityId")

    print(f"connecting user:{connect_userid} to city:{connect_cityid}...")

    # make usercity record 
    connect_one_usercity(connect_userid, connect_cityid) 

    # get usercity record from server
    try:
        UserCity.query.filter((UserCity.user_id==connect_userid) & 
                              (UserCity.city_id==connect_cityid)).one()
    except:
        print("usercity creation failed.")
        confirm = "fail"
    else:
        confirm = "success"

    return confirm


@app.route("/api/city")
def city_api():
    """Return city information only."""

    city_name = request.args.get("cname")
    print(" * " * 15)
    print("got a city_name: {}".format(city_name))

    # check if db has city
    if City.query.filter_by(city_name=city_name).count() == 0:
        # if no, ping teleport and add to db
        print("city not in db, sending to teleport for basics")
        tp_search_city(city_name)    
    else:
        print("city is in db")

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
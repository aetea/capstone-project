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
update_status, update_current_local, delete_user_city

app = Flask(__name__)   # create a Flask object called "app"

# =======================================
#         API functions 
# =======================================
#    move to another file? 



# fetch data from teleport API
def get_city_api(city_name):
    """Get basic city info from Teleport API and save to db if necessary."""
    # returns City object 

    # ? cleanup: make this a separate function ...
    ### get city info from API
    # 1. send request to api endpoint, get Response object, turn into dict
    print("*** fetching from teleport API ***")
    res = requests.get(f"https://api.teleport.org/api/cities/?search={city_name}&limit=1")
    res_dict = res.json()

    # 2. get city info for top result and make dictionary
    top_city_found = res_dict["_embedded"]["city:search-results"][0]
    top_city_link = top_city_found["_links"]["city:item"]["href"]

    print("*** fetching from teleport API ***")
    res_city = requests.get(top_city_link)
    tele_city_dict = res_city.json()
    # ? cleanup: ... END separate function

    # 3. extract city basics from response
    # always get country and city_id from teleport
    tele_city_id = tele_city_dict["geoname_id"]
    tele_name = tele_city_dict["name"]
    tele_city_more = tele_city_dict["_links"]
    tele_country = tele_city_more["city:country"]["name"]

    ### handle error: skip if no details/urban area available 
    # eg venice, kolkata
    try:
        tele_ua = tele_city_more["city:urban_area"]["name"]
    except:
        print(f"found a match to {tele_name} in {tele_country}")
        print("but no detailed city info available from teleport :( sorry! ")
        # add to db (without ua) anyway?? 
        return None

    ### double check before adding City to db
    try:
        # look for tele_city_id in db
        City.query.filter_by(teleport_id=tele_city_id).one()
    except:
        # ? cleanup: make this a separate function 
        # add city info to db
        tele_ua = tele_city_more["city:urban_area"]["name"]
        city_found = City(city_name=tele_name.lower(), urban_area=tele_ua.lower(), 
                        country=tele_country.lower(), teleport_id=tele_city_id)

        print(f">> before trying to init this city: {city_found}")
        db.session.add(city_found)
        db.session.commit()
        print(f">> after db commit: {city_found}")
        # ? cleanup: ... END separate function
    else:
        city_found = City.query.filter_by(teleport_id=tele_city_id).one()

    return city_found


def tp_get_city_details(tele_city_id):
    """Get detailed info and scores about a city from Teleport API."""

    print("*** fetching from teleport API ***")

    pass 


# check DB and populate from teleport API if necessary
def get_city_db(city_name):
    """Check if db contains city, if not populate basic info from Teleport API."""

    cityname_query = City.query.filter_by(city_name=city_name)

    if cityname_query.count() == 0:
        # if none found in db, ping teleport and add to db if needed
        print("this city name not found in db, trying Teleport")
        city = get_city_api(city_name)  
    else:
        print("city name found in db")
        city = cityname_query.first()

    return city

# =======================================
#           Flask Routes 
# =======================================

@app.route("/")
def index():
    """Show index.html template."""
    
    return render_template("index.html") 

@app.route("/profile/<user_id>")
def profile(user_id):
    """Show profile for given user."""

    user = User.query.get(user_id)

    user_dict = user.make_dict()
    # user_json = jsonify(user_dict)

    return render_template("profile.html", user_dict=user_dict)


# @app.route("/city-info")
# def city_info_blank():
#     """Show blank city info page."""

#     return render_template("city-info.html")


@app.route("/city-info/<city_name>")
def city_info(city_name):
    """Show city info page for a given city.
    
    Should render city-info template, passing basic_info and tele_id as arguments
    """

    ada = User.query.get(1) 
    # city = City.query.filter_by(city_name=city_name).first()
    city = get_city_db(city_name)
    # returns None if no city info found in teleport

    print("found a city object: {}".format(city))
    print(" * " * 15)

    # city_dict = city.make_dict()
    # jsonify(city_dict)

    return render_template("city-info.html", city=city, user=ada)


@app.route("/city-search")
def search_city():
    """Query db and return matching city."""

    # get city name from search form
    city_name = request.args.get("city-search") 

    return redirect(f"/city-info/{city_name}")


@app.route("/api/city")
def city_api():
    """Return city information only."""

    city_name = request.args.get("cname")
    print(" * " * 15)
    print("got a city_name: {}".format(city_name))

    # check or populate db for city basics
    city = get_city_db(city_name)

    # get city object from db
    # city = City.query.filter_by(city_name=city_name).first()
    print("found a city object: {}".format(city))
    print(" * " * 15)

    city_dict = city.make_dict()

    return jsonify(city_dict)


# ========== Save / Unsave City ============

# TODO (v2) add functionality to save as "lived here previously"
@app.route("/save-city", methods=["POST"])
def save_city(): 
    """Create usercity connection between given user and city."""

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


@app.route("/unsave-city", methods=["POST"])
def unsave_city(): 
    """Function to remove a user's connection to a city."""

    rm_userid = 1 #FIXME: handle real user
    rm_cityid = request.form.get("unsave-btn")

    delete_user_city(rm_userid, rm_cityid)
    # -> removes matching usercity record (one or all? PLSCHECK) 

    q = UserCity.query
    uc = q.filter((UserCity.user_id==rm_userid) & 
                  (UserCity.city_id==rm_cityid))

    if uc.count() == 0:
        confirm = "success"
    else: 
        confirm = "failed"

    print(f"unsave city operation: {confirm}")

    return redirect(request.referrer)


# =======================================
#          Main Server Function 
# =======================================

if __name__ == "__main__":
    connect_to_db(app)  # creates relationship btwn flask obj and db 
    app.run(host='0.0.0.0', debug=True)
"Server for looksee app"

# =============================================
#              Imports & Initalise
# =============================================

# imports for working with API
import requests
from pprint import pprint

# imports for app server
from flask import Flask, request, render_template, jsonify, redirect
from model import db, connect_to_db, User, City, UserCity
from crud import add_city_db, connect_one_usercity, delete_user_city, \
                    get_user_cities, get_city_users, \
                    update_status, update_current_local

app = Flask(__name__)   # create a Flask object called "app"

# =============================================
#                 API functions 
# =============================================
#    move to another file? 


def search_w_scores_api(city_name):    #paris (france, texas?)
    """Get detailed info and scores about a city from Teleport API."""
    # fetch city basics+details in one step, using embed param 

    payload = {
        "search": city_name,
        "limit": 1,
        "embed": "city:search-results/city:item/city:urban_area/ua:scores"
    }

    print("*** fetching from teleport API ***")
    res = requests.get("https://api.teleport.org/api/cities/", params=payload)
    res_dict = res.json()

    return res_dict 


# fetch data from teleport API
def get_city_api(city_name):
    """Get basic city info from Teleport API and save to db if necessary."""
    # return City json ??

    print("HI from get_city_api...")

    res_dict = search_w_scores_api(city_name) 
    print("HI AGAIN from get_city_api...")

    if res_dict["count"] == 0:
        return None

    emb = "_embedded"
    city_item = res_dict[emb]["city:search-results"][0][emb]["city:item"]

    # 3. extract city basics from response
    # always get country and city_id from teleport
    tele_city_id = city_item["geoname_id"]
    tele_name = city_item["name"]

    city_item_links = city_item["_links"]
    tele_country = city_item_links["city:country"]["name"]

    ### handle error: skip if no details/urban area available 
    # eg venice, kolkata
    try:
        city_item_links["city:urban_area"]["name"]
    except:
        print(f"found a match to {tele_name} in {tele_country}")
        print("but no detailed city info available from teleport :( sorry! ")
        # add to db (without ua) anyway?? 
        return None
    else:
        # OK, get complete ua+scores data
        ua_dict = city_item[emb]["city:urban_area"]
        scores = ua_dict[emb]["ua:scores"]["categories"]

        # compile dictionary to pass to next function
        city_dict = {
            "tele_id": tele_city_id,
            "city_name": tele_name, 
            "country": tele_country,
            "urban_area": city_item_links["city:urban_area"]["name"],
            "urban_id": ua_dict["ua_id"],
            "scores": scores
        }

    ### double check before adding City to db and get city_id
    try:
        # look for tele_city_id in db
        City.query.filter_by(teleport_id=tele_city_id).one()
    except:
        # add city info to db
        city_id = add_city_db(city_dict)
    else: 
        city = City.query.filter_by(teleport_id=tele_city_id).first()
        city_id = city.city_id
        
    city_dict["city_id"] = city_id

    return city_dict


# =============================================
#                 Flask Routes 
# =============================================

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


@app.route("/city-info/<city_name>")
def city_info(city_name):
    """Show city info page for a given city.
    
    Should render city-info template, passing basic_info and tele_id as args
    """

    ada = User.query.get(1) # FIXME: handle real user
    city_dict = get_city_api(city_name)
    # returns None if no city info found in teleport

    print("fetched a city: {}".format(city_dict))
    print(" * " * 15)

    return render_template("city-info.html", city=city_dict, user=ada)


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

    city_dict = get_city_api(city_name) 

    print("found a city object: {}".format(city))
    print(" * " * 15)

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
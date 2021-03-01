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


def search_w_scores_api(city_name, limit=1):    #paris (france, texas?)
    """Get detailed info and scores about a city from Teleport API."""
    # fetch city basics+details in one step, using embed param 

    payload = {
        "search": city_name,
        "limit": limit,
        "embed": "city:search-results/city:item/city:urban_area/{ua:scores,ua:images}",
    }

    print("*** fetching from teleport API ***")
    res = requests.get("https://api.teleport.org/api/cities/", params=payload)
    res_dict = res.json()

    return res_dict 


def clean_search_res(res_dict):
    """Clean up response from Teleport API to get city basics."""

    # ? account for multiple results?
    # * do not clean urban areas -- need to check if available separately

    pass


def clean_urban_area(city_dict):
    """Clean up dictionary for a city:item from Teleport API."""

    pass


# fetch data from teleport API
def get_city_api(city_name):
    """Get basic city info from Teleport API and save to db if necessary.
    
    Returns dict containing city details from teleport + city_id from db."""
    # return City json ??

    print("HI from get_city_api...")

    res_dict = search_w_scores_api(city_name) 
    print("HI AGAIN from get_city_api...")

    if res_dict["count"] == 0:
        return None

    emb = "_embedded"
    first_city = res_dict[emb]["city:search-results"][0] 
    city_item = first_city[emb]["city:item"]

    # 3. extract city basics from response
    # always get country and city_id from teleport
    tele_city_id = city_item["geoname_id"]
    tele_name = city_item["name"]

    city_item_links = city_item["_links"]
    tele_country = city_item_links["city:country"]["name"]
    # ------------------ ooo -------------------
    print(f"[get_city_api] result basics from teleport: ")
    print(f"[get_city_api] {tele_name} in {tele_country} with id {tele_city_id}")

    ### handle error: skip if no details/urban area available 
    # eg venice, kolkata
    try:
        city_item_links["city:urban_area"]["name"]
    except:
        print(f"[get_city_api] found a match to {tele_name} in {tele_country}")
        print("but no detailed city info available from teleport :( sorry! ")
        # add to db (without ua) anyway?? 
        return None
    else:
        # OK, get complete ua+scores data
        ua_dict = city_item[emb]["city:urban_area"]
        scores_list = ua_dict[emb]["ua:scores"]["categories"]

        scores_dict = {}
        for cat in scores_list:
            score = float(cat["score_out_of_10"])
            scores_dict[cat["name"]] = round(score, 1)

        photo_1 = ua_dict[emb]["ua:images"]["photos"][0]
        img_link = photo_1["image"]["web"]

        # compile dictionary to pass to next function
        city_dict = {
            "tele_id": tele_city_id,
            "city_name": tele_name, 
            "country": tele_country,
            "urban_area": city_item_links["city:urban_area"]["name"],
            "urban_id": ua_dict["ua_id"],
            "scores": scores_dict,
            "img_link": img_link
        }

    ### double check before adding City to db
    try:
        # look for tele_city_id in db. if one only, continue
        City.query.filter_by(teleport_id=tele_city_id).one()
    except:
        # if none, add city info to db
        # if more than one, skip 
        if City.query.filter_by(teleport_id=tele_city_id).count() == 0:
            city_id = add_city_db(city_dict)
            
    # ------------------ ooo -------------------
    num_records = City.query.filter_by(teleport_id=tele_city_id).count()
    print(f"[get_city_api] found {num_records} city records in db")

    # get first record only, in case of duplicates
    city = City.query.filter_by(teleport_id=tele_city_id).first()
    print(f"[get_city_api] city from db is: {city}")
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


@app.route("/city-info/<country>/<city_name>")
def city_country_info(country, city_name):
    """Show city info page for a given city in a given country."""

    # get city details from teleport 

    return f"this works! received {country} and {city_name}"


@app.route("/city-info/<city_name>")
def city_info(city_name):
    """Check Teleport API for matching city and redirect/present city choices.
    
    Should render city-info template, passing city details as args
    """

    ada = User.query.get(1) # FIXME: handle real user
    city_dict = get_city_api(city_name)
    # returns city details from teleport + city_id from db
    # returns None if no city info found in teleport
    # -------------- ooo ---------------
    print("fetched a city: {}".format(city_dict))
    print(" * " * 15)

    # todo: enable multiple results

    return render_template("city-info.html", city=city_dict, user=ada)


@app.route("/city-search")
def search_city():
    """Get city name from search form."""

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
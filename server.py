"Server for looksee app"

# =============================================
#              Imports & Initalise
# =============================================

# for working with system folders
import os, random

# imports for working with API
import requests
from pprint import pprint

# imports for app server
from flask import Flask, request, render_template, redirect, session, \
                  jsonify, json
from werkzeug.security import generate_password_hash, check_password_hash
from model import db, connect_to_db, User, City, UserCity, Country
from crud import add_city_db, connect_one_usercity, delete_user_city, \
                    get_one_usercity, get_user_cities, get_city_users, \
                    update_status, update_current_local
import api_fx

app = Flask(__name__)   # create a Flask object called "app"
app.secret_key = "gjlrkejlkj64jgk39lkw"


# session["last_city"] = {
#     # "geoid": 0,
#     # "name": ""
# }


def pick_homepage_photo():
    """Pick a random image from bg-folder as homepage background."""

    bg_folder = os.getcwd() + "/static/backgrounds"
    bg_images = [f for f in os.listdir(bg_folder) if not f.startswith(".")]
    # * ^ don't use hidden files, like .DS_Store
    photo_url = random.choice(bg_images)

    return photo_url


def img_folder_exists(city_name):
    """Check if static has a folder with given city name."""

    city_name = city_name.lower()
    city_img_path = os.getcwd() + "/static/city-images/"

    return os.path.exists(city_img_path + city_name)


def city_images(city_name):
    """Get list of images from static folder to pass to city-info page."""

    city_img_path = os.getcwd() + "/static/city-images/"
    city_images = [f for f in os.listdir(city_img_path + city_name.lower()) 
                    if not f.startswith(".")]

    return city_images  # ["img1.jpg", "img2.jpg"]


# =============================================
#                 Flask Routes 
# =============================================

@app.route("/")
def index():
    """Show index.html template."""
    ada = User.query.get(1)
    bg_url = pick_homepage_photo()
    print(f"using {bg_url} this time")
    return render_template("index.html", user=ada, bg_url = bg_url) 


@app.route("/login", methods=["POST"])
def login():
    """Check login details provided."""
    email = request.form.get("email_field")
    user = User.query.filter_by(email=email)    # get User obj

    pw_entered = request.form.get("pw_field")
    result = check_password_hash(user.pw, pw_entered)

    if result == True:
        return "welcome!"
    else:
        # return str(result)
        return "please try again."


@app.route("/map")
def map():
    """Show map only page."""
    ada = User.query.get(1)
    
    return render_template("map-only.html", user=ada) 


@app.route("/profile/<user_id>")
def profile(user_id):
    """Show profile for given user."""

    user = User.query.get(user_id)

    user_dict = user.make_dict()
    # user_json = jsonify(user_dict)
    print(" * " * 15)
    print(f"passing a user_dict of type {type(user_dict)}")
    pprint(user_dict)

    return render_template("profile.html", user_dict=user_dict)


@app.route("/city-info/<country_iso>/<city_name>")
def city_country_info(country_iso, city_name):
    """Show city info page for a given city in a given country.
    
    Fetches city info from Teleport and Sherpa. Passes more or less details 
    depending on whether scores available. Also adds city to db if needed."""

    ada = User.query.get(1)

    # if url matches last city in session
    # there was an exact match or user picked one from last search
    if session.get("last_searched_city"):
        print("city found in session. try get_city_details with geoid from session.")

    # if not, user came here directly - get geoid from teleport 
    geoid = api_fx.search_city_country(city_name, country_iso)
    print(f"got geoid {geoid} from city country search")
    
    if not geoid: 
        return "no city found; no geoid obtained :( what to show?"

    # * from here onwards, tele_id is present, city is known
        
    print("ok to continue, getting city details...")
    city_dict = api_fx.tele_city_details(geoid)   # either basic/scores dict
    print(f"got this city dict {city_dict}")

    # if basic dict, render "no results/not enough info page"
    if city_dict.get("urban_area") == None:
        return "[ERROR] found that city in teleport, but no detailed info :("

    # add to db if not yet there
    # todo: make this another func(geoid) -> return City
    db_cities = City.query.filter_by(teleport_id=geoid)
    if db_cities.count() == 0:
        print("no matching city records found in db, adding now.")
        city = add_city_db(city_dict)  
    else: 
        num_records = db_cities.count()
        print(f"[get_city_api] found {num_records} city records in db")

    # get first record only, in case of duplicates
    city = City.query.filter_by(teleport_id=geoid).first()
    # todo ---- end new function ----
    print(f"got this city from db: {city}")
    city_dict["city_id"] = city.city_id

    # get country alerts from sherpa - using countryiso 
    iso = city.country_code
    sc = api_fx.sherpa_country_request(iso)["data"][0] # [1st country]
    sr = api_fx.sherpa_restrictions(iso)["data"]  # []
    sp = api_fx.sherpa_procedures(iso)["data"]  # []
    sp_high = api_fx.filter_procedures_sev(sp, 2) # get procedures with min sev3

    saved = [False]
    for uc in ada.user_cities: 
        if city_dict["city_id"] == uc.city.city_id:
            saved = [True, uc.user_status]      # user_status = future/past/current

    # get city photos 
    city_img_list = []
    if img_folder_exists(city_name):
        city_img_list = city_images(city_name)
        print(city_img_list)
    
    print(" * " * 15)
    print(f"RENDER CITY-INFO, passing city_dict: {city_dict}")
    
    return render_template("city-info.html", city=city_dict, user=ada, 
                            saved=saved, local=None, img_list=city_img_list,
                            sherpac=sc, sherpar=sr, sherpap=sp_high)


@app.route("/city-search")
def search_city():
    """Get city name from search form, count results from Teleport API 
    and redirect."""
    
    ada = User.query.get(1)

    # get city name from search form
    city_name = request.args.get("city-search") 

    # ask teleport for top 5 cities  
    tele_res = api_fx.tele_search_cityname(city_name)

    if not tele_res: 
        # return render_template("not-found.html")
        return "[BETTER_ERROR] uh-oh nothing found from teleport."

    # else: check list, count exact matches for city_name
    exact_matches = []
    for idx, res_city in enumerate(tele_res): 
        if res_city["match"] == "exact":
            exact_matches.append(idx)
    print(f"{len(exact_matches)} exact matches found.")

    # if 1 exact, move forward with that city:
    if len(exact_matches) == 1:
        # get country_iso from db first
        city = tele_res[exact_matches[0]] 
        cname = city["tele_name"]
        country_iso = city["iso"]
        return redirect(f"/city-info/{country_iso}/{cname}") 

    # else render page for city-picker, show all cities
    else:
        return render_template("search-results.html", results=tele_res, user=ada)


# ========== Save / Unsave City ============

@app.route("/save-city", methods=["POST"])
def save_city(): 
    """Create usercity connection between given user and city."""

    connect_userid = 1 #FIXME: handle real user
    connect_cityid = request.form.get("save-city")
    past_local = request.form.get("past_local")
    print(f"form values cityid is {connect_cityid}, past_local is {past_local}")

    status = "past_local" if past_local == "true" else "future"  
    # * check past_local as string because value is coming from js 

    print(f"connecting user:{connect_userid} to city:{connect_cityid} as {status}")

    # make usercity record 
    usercity = update_status(connect_userid, connect_cityid, status)
    confirm = "success" if usercity else "failed"

    return confirm


@app.route("/unsave-city", methods=["POST"])
def unsave_city(): 
    """Function to remove a user's connection to a city."""

    rm_userid = 1 #FIXME: handle real user
    rm_cityid = request.form.get("unsave-city")
    hidden_info = request.form.get("user-id")

    delete_user_city(rm_userid, rm_cityid)
    # -> removes matching usercity record (one or all? PLSCHECK) 

    try:
        get_one_usercity(rm_userid,rm_cityid)
    except:
        confirm = "success"
    else: 
        confirm = "failed"

    print(f"unsave city operation: {confirm}")
    return confirm

    # return redirect(request.referrer)


# =======================================
#          Main Server Function 
# =======================================

if __name__ == "__main__":
    connect_to_db(app)  # creates relationship btwn flask obj and db 
    app.run(host='0.0.0.0', debug=True)
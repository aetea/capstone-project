"Server for looksee app"

# =============================================
#              Imports & Initalise
# =============================================

# imports for working with API
import requests
from pprint import pprint

# imports for app server
from flask import Flask, request, render_template, jsonify, redirect, session 
from model import db, connect_to_db, User, City, UserCity, Country
from crud import add_city_db, connect_one_usercity, delete_user_city, \
                    get_user_cities, get_city_users, \
                    update_status, update_current_local
import api_fx

app = Flask(__name__)   # create a Flask object called "app"
app.secret_key = "gjlrkejlkj64jgk39lkw"


# session["last_city"] = {
#     # "geoid": 0,
#     # "name": ""
# }

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


@app.route("/city-info/<country_iso>/<city_name>")
def city_country_info(country_iso, city_name):
    """Show city info page for a given city in a given country.
    
    Fetches city info from Teleport and Sherpa. Passes more or less details 
    depending on whether scores available. Also adds city to db if needed."""

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
        return "[BETTER_ERROR] found that city in teleport, but no detailed info :("

    # add to db if not yet there
    db_cities = City.query.filter_by(teleport_id=geoid)
    if db_cities.count() == 0:
        print("no matching city records found in db, adding now.")
        city = add_city_db(city_dict)  
    else: 
        num_records = db_cities.count()
        print(f"[get_city_api] found {num_records} city records in db")

    # get first record only, in case of duplicates
    city = City.query.filter_by(teleport_id=geoid).first()
    print(f"got this city from db: {city}")
    city_dict["city_id"] = city.city_id

    # get country alerts from sherpa - using countryiso 
    iso = city.country_code
    sc = api_fx.sherpa_country_request(iso)["data"][0] # [1st country]
    sr = api_fx.sherpa_restrictions(iso)["data"]  # []
    sp = api_fx.sherpa_procedures(iso)["data"]  # []
    # pass adict=alerts, 
    ada = User.query.get(1)

    return render_template("city-info.html", city=city_dict, user=ada,  
                            sherpac=sc, sherpar=sr)
    # todo clear session["last_city"] on city-info page to prevent locking user in


@app.route("/city-search")
def search_city():
    """Get city name from search form, count results from Teleport API 
    and redirect."""

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
        return render_template("search-results.html", results=tele_res)
        # return "many results found. show all results here for user to pick."


# @app.route("/api/city")
# def city_api():
#     """Return city information only."""

#     city_name = request.args.get("cname")
#     print(" * " * 15)
#     print("got a city_name: {}".format(city_name))

#     city_dict = api_fx.get_city_api(city_name) 

#     print("found a city object: {}".format(city_dict))
#     print(" * " * 15)

#     return jsonify(city_dict)


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
    # uc = UserCity.query.filter((UserCity.user_id==connect_userid) & 
    #                           (UserCity.city_id==connect_cityid))
    
    # if uc.count() == 1: 
        # print("save success!")
    # else:
    #     print("usercity creation error")
    
    # return redirect(f"/city-info/{iso}/{cname}")
    return redirect(request.referrer)


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
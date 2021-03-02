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
import api_fx

app = Flask(__name__)   # create a Flask object called "app"

# =============================================
#                 API functions 
# =============================================
#    move to another file? 


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
    city_dict = api_fx.get_city_api(city_name)
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

    city_dict = api_fx.get_city_api(city_name) 

    print("found a city object: {}".format(city_dict))
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
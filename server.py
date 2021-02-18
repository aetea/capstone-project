"Server for looksee app"

from flask import Flask, request, render_template, jsonify, redirect
from model import connect_to_db, City
from crud import connect_one_usercity, get_user_cities, get_city_users, \
update_status, update_current_local

app = Flask(__name__)

# route for home page -- root directory
    # return index.html 

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

    return render_template("city-info.html", city=city)


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


@app.route("/api/city")
def city_api():
    """Return city information only."""

    city_name = request.args.get("cname")
    print(" * " * 15)
    print("got a city_name: {}".format(city_name))

    # check if db has city
    if City.query.filter_by(city_name=city_name).count():
        print("city is in db")

    # get city object from db
    city = City.query.filter_by(city_name=city_name).first()
    print(" * " * 15)
    print("found a city object: {}".format(city))
    print(" * " * 15)

    # if no city object from db, get from API 

    # add city info from api to db

    ### turn city info into dict
    # city_dict = {
    #     "city_name": city.city_name,
    #     "country": city.country
    # }
    city_dict = city.make_dict()

    return jsonify(city_dict)



if __name__ == "__main__":
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
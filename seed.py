"""Script to seed the database."""

import os 
import json
# from random import choice, randint 
# from datetime import datetime 

import crud 
from model import db, connect_to_db, User, City, UserCity, Country, Follow 
import server 
import api_fx


# ====== MAKE TEST DATA FUNCTIONS =======

def make_test_users():
    """Create some users for testing."""
    test_fnames = ['ada', 'bey', 'cat', 'dory', 'emma', 'finn']

    for name in test_fnames:
        email = f'{name}@test.tst'
        user = User(first_name=name, last_name='test', email=email)
        db.session.add(user)

    db.session.commit()

    print("*** Success: Added some users ***")


def make_test_countries():
    """Make fake countries.""" 

    countries = {
        'USA': 'United States',
        'GBR': 'United Kingdom',
        'FRA': 'France', 
        'TWN': 'Taiwan',
        'JPN': 'Japan', 
        'KOR': 'Korea (Republic of)'
    }

    for iso, name in countries.items():
        country_to_add = crud.add_country(iso, name)
        db.session.add(country_to_add)

    db.session.commit()

    print("*** Success: Added some countries ***")


def make_test_cities():
    """Create some cities for testing."""
    cities = {
        'San Francisco': {'ccode': 'USA', 'tid': 5391959, 'urban_area': 'Bay Area'},
        'London': {'ccode':'GBR', 'tid': 2643743}, 
        'Paris': {'ccode': 'FRA', 'tid': 2988507},
        'Taipei': {'ccode': 'TWN', 'tid': 1668341}
    }

    for c, cinfo in cities.items():
        city = City(city_name=c, urban_area=cinfo.get('urban_area'), 
                    teleport_id=cinfo.get('tid'), country_code=cinfo['ccode'])
        db.session.add(city)

    db.session.commit()

    print("*** Success: Added some cities ***")


def connect_bey_fans():
    """Make several users fans of userid=2 for testing."""
    # TODO: update to give emma fans & have bey follow someone
    
    q = db.session.query(User)
    fans = q.filter(User.user_id != 2).limit(3).all()

    bey = User.query.filter(User.first_name == 'bey').first()
    bey.fans=[]     # clear any prior bey.fans
    bey.fans.extend(fans)

    db.session.add(bey)
    db.session.commit()

    print("*** Success: Added some fans ***")
    print(f"-- bey.fans = {bey.fans}")


def connect_users_cities():
    """Create connections between users and cities for testing."""

    # give ada current and future cities
    ada = User.query.get(1)
    taipei = City.query.filter_by(city_name='taipei').first()
    london = City.query.filter_by(city_name='london').first()

    ada_taipei = UserCity(user_status='curr_local', tenure='mid', user=ada, city=taipei)
    ada_london = UserCity(user_status='future', user=ada, city=london)

    db.session.add(ada_taipei, ada_london)
    db.session.commit()

    # give finn current, past and future cities
    finn = User.query.get(6)
    sf = City.query.filter_by(city_name='san francisco').first() 

    finn_sf = UserCity(user_status='curr_local', tenure='new', user=finn, city=sf)
    finn_london = UserCity(user_status='past_local', tenure='long', user=finn, city=london)
    finn_taipei = UserCity(user_status='future', user=finn, city=taipei)

    finn.user_cities.extend([finn_sf, finn_london, finn_taipei])
    db.session.add(finn)
    db.session.commit() 


# ======================================
#               MAIN SCRIPT 
# ======================================


os.system('dropdb looksee')
os.system('createdb looksee') 

connect_to_db(server.app)
db.create_all()  # setup tables


# add real countries
# ==================
res_country_dict = api_fx.sherpa_all_countries()
countries = res_country_dict["data"]

# for each country item in response, 
# add a record to country db table
for c in countries:
    ccode = c["attributes"]["isoAlpha3"]
    cname = c["attributes"]["countryName"]
    cadd = crud.add_country(ccode, cname)
    db.session.add(cadd)

db.session.commit()


# populate tables with test data
# ==============================
make_test_users()
# make_test_countries()
make_test_cities()
connect_users_cities()
connect_bey_fans()


# ======================================
#        ~~~~~ PSEUDOCODE ~~~~ 
# ======================================

# start with a fresh db 
# connect to db (model)
# create all tables (model)

# load json data from external source (api/file)
# convert into dict and extract datapoints wanted 
# use datapoints to create db records 
#     - supply as arguments to crud functions 
# <---- YOU ARE HERE 🌼 ---->
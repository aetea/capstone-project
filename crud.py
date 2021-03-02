from model import db, connect_to_db, User, City, UserCity, Country, Follow

# =========================================
#       Create Functions 
# =========================================

def make_some_users(n):
    """Make n test users"""

    new_users = []
    alphabet = 'abcdefghijklmnopqrstuvwxyz'

    for num in range(n):
        first_name = alphabet[num]*2
        email = f'{first_name}@test.tst'
        
        user = User(first_name=first_name, last_name='test', email=email)
        new_users.append(user)


def add_city_db(city_basics_dict):
    """Add city and basic info to db."""
    # todo clean this up, make arguments more explicit
    # todo return city object instead for consistency

    # city_to_add = City(city_name=tele_name.lower(), urban_area=tele_ua.lower(), 
    #                     country=tele_country.lower(), teleport_id=tele_city_id)

    country_name = city_basics_dict["country_name"]
    print(f"[crud.add_city_db] got country_name {country_name}")
    db_country = Country.query.filter_by(name=country_name).one()
    ccode = db_country.isocode3
    print(f"country table says isocode for that country is {ccode}")

    city_to_add = City(city_name=city_basics_dict["city_name"],
                        urban_area=city_basics_dict["urban_area"],
                        country_code=ccode,
                        teleport_id=city_basics_dict["tele_id"]
                        )

    print(f">> before trying to init this city: {city_to_add}")
    db.session.add(city_to_add)
    db.session.commit()
    print(f">> after db commit: {city_to_add}")

    city_id = city_to_add.city_id

    return city_id


def add_country(iso3, name):
    """Add a new country to db."""

    country = Country(isocode3=iso3, name=name)
    # db.session.add(country)
    # db.session.commit()

    return country 


# ========= Connect Functions ===========


def connect_one_usercity(userid, cityid, status="future"):
    """Function to create a single UserCity connection, given IDs."""
    # do not use if needing to bundle connection with other changes
    print(" * " * 15)
    print("now running crud.py...")

    user = User.query.get(userid)
    print(f"User object found is {user}")
    city = City.query.get(cityid)
    print(f"City object found is {city}")

    user.user_cities.append(
        UserCity(user_status = status, city=city)
    )

    print(" * " * 15)
    print(f"last usercity before commit: {user.user_cities[-1]}")
    db.session.add(user)
    db.session.commit()
    print(f"last usercity after commit {user.user_cities[-1]}")
    print(" * " * 15)


# =========================================
#       Read Functions 
# =========================================

def get_user_cities(user, status="all"):
    """Get city connections for a user, optionally filter by status."""
    # returns [uc.city_id, uc.city_name, uc.user_status]
    
    all_uc = user.user_cities
    usercities = [ (uc.city.city_id, uc.city.city_name, uc.user_status) # c below
                    for uc in all_uc
    ] 

    if status != "all":
        usercities = [ c for c in usercities if c[2]==status ]

    return usercities 


def get_city_users(city, status="all"):
    """Get all users connected to a city, optionally filter by status."""

    all_uc = city.user_cities 
    users = [ (uc.user.user_id, uc.user.first_name, uc.user.last_name, uc.user_status) 
                    for uc in all_uc
    ]

    if status != "all":
        # filter users by user_status
        # allow searching by "local" to get past_local and curr_local
        users = [ u for u in users if u[3].find(status) != -1 ]

    return users 


# =========================================
#       Update Functions 
# =========================================

def update_status(user, city, new_status):
    """Update user status for a given city."""

    q = UserCity.query
    uc = q.filter ((UserCity.user==user) & (UserCity.city==city))

    if uc.count() == 0:
        print(f"before update: no record")
        connect_one_usercity(user, city, new_status) 
    else:
        uc = uc.one()
        print(f"before update: {uc}")
        uc.user_status = new_status

    db.session.add(user)
    db.session.commit() 

    return f"after update: {uc}"


def update_current_local(user, city):
    """Update user's current location to given city."""

    q = UserCity.query
    # update existing curr_local city to past_local
    uc = q.filter((UserCity.user==user) & (UserCity.user_status=='curr_local'))
    uc.one().user_status = 'past_local'

    # make given city curr_local city 
    # ---------------------
    uc_new = q.filter((UserCity.user==user) & (UserCity.city==city))
    # check if given city exists in user_cities
    if uc_new.count() == 1:
        uc_new.one().user_status = 'curr_local'
    else:
        connect_one_usercity(user, city, status='curr_local')

    # should be a single transaction - do not commit if not all successful
    # FIXME: commit goes thru even if updating past_local fails
    db.session.add(user)
    db.session.commit()


def update_teleport_id(city, tid):
    """Update teleport_id from API response."""

    pass


# =========================================
#       Delete Functions 
# =========================================

def delete_user_city(user_id, city_id):
    """Delete user connection to a city.""" 

    q = UserCity.query
    uc = q.filter((UserCity.user_id==user_id) & 
                  (UserCity.city_id==city_id)) 

    uc.delete()    # no need to do db.session.add(user) -- will error
    db.session.commit()


# =========================================
#       Main Function 
# =========================================

if __name__ == "__main__":
    # make a Flask app (alternatively, can import from server.py)
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print("Connected to DB!")

    # ----- if new empty db ------
    # -- should use seed.py instead 

    # db.create_all()
    # if User.query.count() == 0:
    #     make_test_users()
    # if City.query.count() == 0:
    #     make_test_cities()
    # if UserCity.query.count() == 0:
    #     connect_users_cities()
    # if Follow.query.count() == 0:
    #     connect_bey_fans()
from model import db, connect_to_db, User, City, UserCity, Follow

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


def make_test_users():
    """Create some users for testing."""
    test_fnames = ['ada', 'bey', 'cat', 'dory', 'emma', 'finn']

    for name in test_fnames:
        email = f'{name}@test.tst'
        user = User(first_name=name, last_name='test', email=email)
        db.session.add(user)

    db.session.commit()

    print("*** Success: Added some users ***")


def make_test_cities():
    """Create some cities for testing."""
    cities = {
        'san francisco': {'country': 'united states', 'urban_area': 'bay area'},
        'london': {'country':'united kingdom'}, 
        'paris': {'country': 'france'},
        'taipei': {'country': 'taiwan'}
    }

    for c, cinfo in cities.items():
        city = City(city_name=c, urban_area=cinfo.get('urban_area'), country=cinfo['country'])
        db.session.add(city)

    db.session.commit()

    print("*** Success: Added some cities ***")


def add_city_db(city_basics_dict):
    """Add city and basic info to db."""

    # city_to_add = City(city_name=tele_name.lower(), urban_area=tele_ua.lower(), 
    #                     country=tele_country.lower(), teleport_id=tele_city_id)

    city_to_add = City(city_name=city_basics_dict["name"].lower(),
                        urban_area=city_basics_dict["urban_area"].lower(),
                        country=city_basics_dict["country"].lower(),
                        teleport_id=city_basics_dict["tele_id"]
                        )

    print(f">> before trying to init this city: {city_to_add}")
    db.session.add(city_to_add)
    db.session.commit()
    print(f">> after db commit: {city_to_add}")

    city_id = city_to_add.city_id

    return city_id


# ========= Connect Functions ===========

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
    db.create_all()
    print("Connected to DB!")

    if User.query.count() == 0:
        make_test_users()
    if City.query.count() == 0:
        make_test_cities()
    if UserCity.query.count() == 0:
        connect_users_cities()
    if Follow.query.count() == 0:
        connect_bey_fans()
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

# ========= Connect Functions ===========

def make_bey_fans():
    """Make several users fans of userid=2."""
    # TODO: update to give emma fans & have bey follow someone
    
    q = db.session.query(User)
    bey_fans = q.filter(User.user_id != 2).limit(3).all()

    bey = User.query.filter(User.first_name == 'bey').first()
    bey.fans=[]     # clear any prior bey.fans
    bey.fans.extend(bey_fans)

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


def connect_one_usercity(user, city):
    """Function to create a single UserCity connection."""
    # TBD if needed
    pass 

# =========================================
#       Read Functions 
# =========================================

def get_user_cities(user, status="all"):
    """Get city connections for a user, optionally filter status."""
    
    all_uc = user.user_cities
    usercities = [ (uc.city.city_id, uc.city.city_name, uc.user_status) # c below
                    for uc in all_uc
    ] 

    if status != "all":
        usercities = [ c for c in usercities if c[2]==status ]

    return usercities 


def get_city_users(city, status="all"):
    """Get all users connected to a city, optionally filter status."""

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

def update_user_city(user, city, new_status):
    """Update user status for a given city."""
    pass 


def update_teleport_id(city, tid):
    """Update teleport_id from API response."""


    pass


# =========================================
#       Delete Functions 
# =========================================

def delete_user_city(user, city):
    """Delete user connection to a city."""
    pass 


# =========================================
#       Main Function 
# =========================================

if __name__ == "__main__":
    # make a Flask app (alternatively, can import from server.py)
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print("Connected to DB!")

    # TODO: split these into function to run once only after creating db
    # db.create_all()
    # print("Created all tables!")

    # # create basic objects 
    # make_test_users()
    # make_test_cities()

    # # create connections between objects 
    # make_bey_fans()

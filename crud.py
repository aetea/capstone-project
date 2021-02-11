from model import db, connect_to_db, User, City, UserCity, Follow

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

    test_fnames = ['ada', 'bey', 'cat', 'dory', 'emma', 'finn']

    for name in test_fnames:
        email = f'{name}@test.tst'
        user = User(first_name=name, last_name='test', email=email)
        db.session.add(user)

    db.session.commit()


def make_test_cities():

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


def make_bey_fans():
    """Make several users fans of userid=2."""
    
    q = db.session.query(User)
    bey_fans = q.filter(User.user_id != 2).limit(3).all()

    bey = User.query.filter(User.first_name == 'bey').first()
    bey.fans.extend(bey_fans)


if __name__ == '__main__':
    # make a Flask app (alternatively, can import from server.py)
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print('Connected to DB!')
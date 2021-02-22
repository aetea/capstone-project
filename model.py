"""Models for city research app"""

from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    # username = db.Column(db.String)     
    # ~~~ ASK> optional username? or use another table for usernames
    # current_city = db.Column(db.String, nullable=False) 
    # ~~~ ASK> should I have this column or just use user_to_cities table? 

    # ------ Relationships ------
    # user_cities = a list of UserCity objects ### RELATIONSHIP

    fans = db.relationship('User', # fan profile in users table
                            secondary='follows', 
                            primaryjoin=('User.user_id==Follow.follow_target'),
                            secondaryjoin=('User.user_id==Follow.follower'),
                            backref='idols')

    def __repr__(self):
        return f'<User user_id={self.user_id} first_name={self.first_name} '\
                f'last_name={self.last_name} email={self.email}>'


class Follow(db.Model):
    """A follow connection between users."""

    __tablename__ = 'follows'

    fid = db.Column(db.Integer, autoincrement=True, primary_key=True)
    follower = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    follow_target = db.Column(db.Integer, db.ForeignKey('users.user_id'))


    def __repr__(self):
        return f'<Follow fid={self.fid} follower_id = {self.follower} '\
                f'target_id={self.follow_target}>'


class City(db.Model): 
    """A city."""

    __tablename__ = 'cities' 
    
    city_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    city_name = db.Column(db.String, nullable=False)
    urban_area = db.Column(db.String)
    country = db.Column(db.String, nullable=False)
    teleport_id = db.Column(db.Integer)    # geoname_id in teleport API

    # user_cities = a list of UserCity objects ### RELATIONSHIP

    def __repr__(self):
        return f'<City city_id={self.city_id} city_name={self.city_name} '\
                f'urban_area={self.urban_area} country={self.country} '\
                f'teleport_id={self.teleport_id}>'


    def make_dict(self):
        """Convert object to a dictionary for JS."""

        dict = {
            "cityId": self.city_id, 
            "cityName": self.city_name, 
            "urbanArea": self.urban_area, 
            "country": self.country, 
            "teleId": self.teleport_id
        }

        return dict


class UserCity(db.Model):
    """A connection between a user and a city."""

    __tablename__ = 'user_cities'

    connect_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    city_id = db.Column(db.Integer, db.ForeignKey('cities.city_id'))
    user_status = db.Column(db.String, nullable=False)  # past_local, curr_local, future
    tenure = db.Column(db.String)   # new (<1yr), short (1-3yrs), 
                                    # mid (3-5yrs), long (>5yrs)

    user = db.relationship('User', backref='user_cities')
    city = db.relationship('City', backref='user_cities')

    def __repr__(self):
        return f'<UserCity connect_id={self.connect_id} '\
                f'{self.user.first_name} {self.user.last_name}<->'\
                f'{self.city.city_name} '\
                f'user_id={self.user_id} city_id={self.city_id} '\
                f'user_status={self.user_status} tenure={self.tenure}>' 


# =======================================
#          Helper Functions
# =======================================
# - create app and db connection for testing/debugging

def connect_to_db(app):
    """Connect this database to a Flask app."""

    # Configure to use db=looksee
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///looksee'
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = app
    db.init_app(app)


if __name__ == '__main__':
    # make a Flask app (alternatively, can import from server.py)
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print('Connected to DB!')

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

    # user_cities = a list of UserCity objects ### RELATIONSHIP

    def __repr__(self):
        return f'<User user_id={self.user_id} first_name={self.first_name} last_name={self.last_name} email={self.email}>'


class City(db.Model): 
    """A city."""

    __tablename__ = 'cities' 
    
    city_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    city_name = db.Column(db.String, nullable=False)
    urban_area = db.Column(db.String)
    country = db.Column(db.String, nullable=False)
    teleport_id = db.Column(db.Integer) 

    # user_cities = a list of UserCity objects ### RELATIONSHIP

    def __repr__(self):
        return f'<City city_id={self.city_id} city_name={self.city_name}'\
                f'urban_area={self.urban_area}, country={self.country}'\
                f'teleport_id={self.teleport_id}>'

class UserCity(db.Model):
    """A connection between a user and a city."""

    __tablename__ = 'users_to_cities'

    connect_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    city_id = db.Column(db.Integer, db.ForeignKey('cities.city_id'))
    user_status = db.Column(db.String, nullable=False)  # past_local, curr_local, future
    tenure = db.Column(db.String)   # new (<1yr), short (1-3yrs), 
                                    # mid (3-5yrs), long (>5yrs)

    user = db.relationship('User', backref='user_cities')
    city = db.relationship('City', backref='user_cities')

    def __repr__(self):
        return f'<UserCity connect_id={self.connect_id}'\ 
                f'user_id={self.user_id} city_id={self.city_id}'\
                f'user_status={self.user_status} tenure={self.tenure}>' 

class Follow(db.Model):
    """A follow connection between users."""

    __tablename__ = 'follows'

    fid = db.Column(db.Integer, autoincrement=True, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey=('users.user_id'))
    follow_target = db.Column(db.Integer, db.ForeignKey=('users.user_id'))

    follower = db.relationship('User', backref='following')
    follow_target = db.relationship('User', backref='followers')

    def __repr__(self):
        return f'<Follow fid={self.fid} follower_id = {self.follower_id}'\ 
                f'follow_target={self.follow_target}>'


# =======================================
# Helper Functions
# - create app and db connection for testing/debugging

def connect_to_db(app):
    """Connect this database to a Flask app."""

    # Configure to use db=looksee
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///looksee'
    app.config['SQLALCHEMY_ECHO'] = True
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = app
    db.init_app(app)


if __name__ == '__main__':
    # make a Flask app (alternatively, can import from server.py)
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print('Connected to DB!')
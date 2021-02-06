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

    def __repr__(self):
        return f'<City city_id={self.city_id} city_name={self.city_name}'\
                f'urban_area={self.urban_area}, country={self.country}'\
                f'teleport_id={self.teleport_id}>'

class UserCity(db.Model):
    """A connection between a user and a city."""

    __tablename__ = 'users_to_cities'

    connection_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    city_id = db.Column(db.Integer, db.ForeignKey('cities.city_id'))
    user_status = db.Column(db.String, nullable=False)  # past_local, curr_local, future
    tenure = db.Column(db.String)   # new (<1yr), short (1-3yrs), 
                                    # mid (3-5yrs), long (>5yrs)

    def __repr__(self):
        return f'<UserCity connection_id={self.connection_id}'\ 
                f'user_id={self.user_id} city_id={self.city_id}'\
                f'user_status={self.user_status} tenure={self.tenure}>' 

                
#this module defines the tables(models) for the database
from railway import db
class Train(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    train_name = db.Column(db.String)
    train_number = db.Column(db.String)
    starting_date = db.Column(db.Date)
    starting_time = db.Column(db.Time)
    ending_date = db.Column(db.Date)
    ending_time = db.Column(db.Time)

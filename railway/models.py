#this module defines the tables(models) for the database
from railway import db
class Train(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    train_name = db.Column(db.String)
    train_number = db.Column(db.String)
    starting_date = db.Column(db.Date,nullable =False)
    starting_time = db.Column(db.Time,nullable=False)
    ending_date = db.Column(db.Date,nullable=False)
    ending_time = db.Column(db.Time,nullable=False)
    left_seats = db.Column(db.Integer) 
    ticket_price = db.Column(db.Integer,nullable= False)
    booked_seats = db.relationship('Booked_seats',backref = 'train',lazy=True)
    unbooked_seats = db.relationship('Unbooked_seats',backref = 'train',lazy=True) 
    #lazy = True : enforces that the select query is executed when the property is first accessed

class Passenger(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    ticket_id = db.Column(db.Integer)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(length =1))
    seat = db.relationship('Booked_seat',backref = 'passenger',lazy = True)

class Booked_seat(db.Model):
    train_id = db.Column(db.Integer,db.ForeignKey('train.id'),primary_key = True) #foreign key to Train
    compartment_no = db.Column(db.Integer,primary_key = True)
    seat_no = db.Column(db.Integer,primary_key =True) 
    passenger_id = db.Column(db.Integer,db.ForeignKey('passenger.id')) #foreign key to Passenger

class Unbooked_seat(db.Model):
    train_id = db.Column(db.Integer,db.ForeignKey('train.id'),primary_key = True) #foreign key to Train
    compartment_no = db.Column(db.Integer,primary_key = True)
    seat_no = db.Column(db.Integer,primary_key =True) 


class Booked_ticket(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    booked_by_user = db.Column(db.Integer,db.ForeignKey('user.id'))  # foreign key
    status = db.Column(db.String)

class User(db.Model):
    id = db.Column(db.Integer,primary_key =True)
    username = db.Column(db.String)
    hash_password = db.Column(db.String)
    email_id = db.Column(db.String)
    budget = db.Column(db.Integer)
    booked_tickets = db.relationship('booked_tickets',backref='user',lazy=True)

#To-do : After testing is done, code nullable,Unique and lenght properties according to the business logic 

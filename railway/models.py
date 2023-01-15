#this module defines the tables(models) for the database
from railway import db,bcrypt,login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
class Train(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    train_name = db.Column(db.String)
    train_number = db.Column(db.Integer)
    starting_date = db.Column(db.Date,nullable =False)
    starting_time = db.Column(db.Time,nullable=False)
    ending_date = db.Column(db.Date,nullable=False)
    ending_time = db.Column(db.Time,nullable=False)
    left_seats = db.Column(db.Integer)
    number_of_compartments = db.Column(db.Integer)
    compartment_size = db.Column(db.Integer) 
    ticket_price = db.Column(db.Integer,nullable= False)
    booked_seats = db.relationship('Booked_seat',backref = 'train',lazy=True)
    unbooked_seats = db.relationship('Unbooked_seat',backref = 'train',lazy=True) 
    def add(self):
        db.session.add(self)
        db.session.commit()
        for i in range(self.number_of_compartments):
            for j in range(self.compartment_size):
                new_seat = Unbooked_seat(
                    train_id = self.id,
                    compartment_no = i+1,
                    seat_no = j+1
                )
                db.session.add(new_seat)
        db.session.commit()
    
    def search(t_name,t_no,date):
        search_trains = []
        trains = Train.query.all()
        for trn in trains:
            if t_name:
                if trn.train_name!=t_name:
                    continue
            if t_no:
                if trn.train_number!=int(t_no):
                    continue
            if date:
                if trn.starting_date.strftime('%Y-%m-%d')!=date:
                    continue
            search_trains.append(trn)
        return search_trains
    def __repr__(self):
        return f"{self.id} {self.train_name} {self.train_number} {self.starting_date} {self.starting_time} {self.ending_date} {self.ending_time}"

    #lazy = True : enforces that the select query is executed when the property is first accessed
class Passenger(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    ticket_id = db.Column(db.Integer,db.ForeignKey('booked_ticket.id'))
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(length =1))
    seat = db.relationship('Booked_seat',backref = 'passenger',lazy = True)
    def add(self):
        db.session.add(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Booked_seat(db.Model):
    train_id = db.Column(db.Integer,db.ForeignKey('train.id'),primary_key = True) #foreign key to Train
    compartment_no = db.Column(db.Integer,primary_key = True)
    seat_no = db.Column(db.Integer,primary_key =True) 
    passenger_id = db.Column(db.Integer,db.ForeignKey('passenger.id')) #foreign key to Passenger
    def add(self):
        db.session.add(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        unbooked_seat = Unbooked_seat(
            train_id = self.train_id,
            compartment_no = self.compartment_no,
            seat_no = self.seat_no
        )
        db.session.add(unbooked_seat)
        db.session.commit()

class Unbooked_seat(db.Model):
    train_id = db.Column(db.Integer,db.ForeignKey('train.id'),primary_key = True) #foreign key to Train
    compartment_no = db.Column(db.Integer,primary_key = True)
    seat_no = db.Column(db.Integer,primary_key =True)
    def book(self,new_passenger):
        db.session.delete(self)
        db.session.commit()
        booked_seat = Booked_seat(
            train_id = self.train_id,
            compartment_no =self.compartment_no,
            seat_no=self.seat_no,
            passenger_id = new_passenger.id 
        ) 
        booked_seat.add()


class Booked_ticket(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    booked_by_user = db.Column(db.Integer,db.ForeignKey('user.id'))  # foreign key
    status = db.Column(db.String)
    passengers = db.relationship('Passenger',backref = 'ticket',lazy = True)
    def add(self):
        db.session.add(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key =True)
    username = db.Column(db.String)
    hash_password = db.Column(db.String)
    email_address = db.Column(db.String)
    budget = db.Column(db.Integer,default = 1500)
    booked_tickets = db.relationship('Booked_ticket',backref='user',lazy=True)
    # properties for password
    def get_password(self):
        return self.hash_password

    def set_password(self,password):
        self.hash_password = bcrypt.generate_password_hash(password)
        return self.hash_password
    password = property(get_password,set_password)

    def check_password(self,attempted_password):
        return bcrypt.check_password_hash(self.hash_password,attempted_password)

    def add(self):
        db.session.add(self)
        db.session.commit()


#To-do : After testing is done, code nullable,Unique and lenght properties according to the business logic 

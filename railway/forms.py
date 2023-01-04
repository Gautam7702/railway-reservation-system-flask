from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField, SubmitField,DateField,TimeField,IntegerField
from wtforms.validators import DataRequired,NumberRange,ValidationError,Length,Email,EqualTo
from datetime import datetime
from railway.models import Train,User


class add_train(FlaskForm):
    def date_validation(self,given_date):
        today_date = datetime.now().date()
        if given_date.data < today_date:
            raise ValidationError(f'Train {given_date.label.text} is invalid')
    def validate_starting_time(self,starting_time):
        cur_datetime = datetime.now()     
        # given_datetime = datetime()
        starting_dt = datetime.combine(self.starting_date.data,starting_time.data)
        ending_dt = datetime.combine(self.ending_date.data,self.ending_time.data)
        if ending_dt<starting_dt:
            raise ValidationError("Journey start date and time must be before journey end date and time")
        if starting_dt   < cur_datetime:
            raise ValidationError('Train has timestamp before current time.')
    def validate_train_name(self,train_name):
        train = Train.query.filter_by(train_name= train_name.data,train_number = self.train_number.data,starting_date = self.starting_date.data,starting_time=self.starting_time.data).first()
        if train:
            raise ValidationError(train)
            # raise ValidationError(f"Train with name {self.train_name.data} ,number {self.train_number.data},date {self.starting_date.data} and time {self.starting_time.data} already exists ")

    train_name = StringField(label = 'Train Name',validators=[DataRequired()])
    train_number = IntegerField(label = 'Train Number',validators=[DataRequired(),NumberRange(min=1,max=10000)])
    starting_date = DateField(label='Journey Start date ',validators=[DataRequired(),date_validation])
    ending_date =  DateField(label='Journey End date ',validators=[DataRequired(),date_validation])
    starting_time = TimeField(label= 'Journey Start time',validators = [DataRequired()])
    ending_time =  TimeField(label= 'Journey Start time',validators = [DataRequired()])
    number_of_compartments = IntegerField(label = 'Number of Compartments',validators=[DataRequired(),NumberRange(min=1,max=1000)])
    compartment_size = IntegerField(label = 'Size of Compartments',validators=[DataRequired(),NumberRange(min=1,max=20)])
    ticket_price = IntegerField(label = 'Ticket price',validators=[DataRequired()])
    submit = SubmitField(label ='Add Train')


class search_train(FlaskForm):
    def validate_date(self,given_date):
        today_date = datetime.now().date()
        if given_date.data < today_date:
            raise ValidationError(f'Train {given_date.label.text} is invalid')

    train_number = IntegerField(label = 'Train Number',validators=[NumberRange(min=1,max=10000)])
    train_name = StringField(label = 'Train Name',validators=[])
    date = DateField(label='Journey Start date ',validators=[])
    submit = SubmitField(label ='Search Train')
     

class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')

    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')

class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')

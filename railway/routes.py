#This module define the routes of the application
from railway import app
from flask import render_template

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/book-tickets',methods = ['GET','POST'])
def book_tickets_page():
    return render_template('book_tickets.html')

@app.route('/add_train',methods = ['GET','POST'])
def add_train_page():
    return render_template('add_train.html')

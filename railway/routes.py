#This module define the routes of the application
from railway import app
from flask import render_template,request,flash,redirect
from railway.forms import add_train,search_train
from railway.models import *
@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/search-tickets',methods = ['GET','POST'])
def search_tickets_page():
    if request.method == "POST":
        return redirect('/book-tickets/' + request.form.get("train_id"))
    form = search_train()
    train_name = request.args.get('train_name')
    train_number = request.args.get('train_number')
    train_date = request.args.get('date')
    search_result = Train.search(train_name,train_number,train_date)
    return render_template('search_tickets.html',form=form,search_result = search_result)

@app.route('/book-tickets/<train_id>',methods = ['GET','POST'])
def book_tickets_page(train_id):
    return train_id


@app.route('/add_train',methods = ['GET','POST'])
def add_train_page():
    form = add_train()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_train = Train(
                train_name = form.train_name.data,
                train_number = form.train_number.data,
                starting_date = form.starting_date.data,
                starting_time = form.starting_time.data,
                ending_date = form.ending_date.data,
                ending_time = form.ending_time.data,
                number_of_compartments = form.number_of_compartments.data,
                compartment_size = form.compartment_size.data,
                ticket_price = form.ticket_price.data,
                left_seats = form.compartment_size.data*form.number_of_compartments.data
            )
            new_train.add()
            flash(f'Train {form.train_name.data} running on {form.starting_date.data} has been successfully added!',category = 'sucess')
        if form.errors != {}: #If there are not errors from the validations
            for err_msg in form.errors.values():
                flash(err_msg, category='danger')
        return render_template('add_train.html',form=form)
        
    return render_template('add_train.html',form=form)

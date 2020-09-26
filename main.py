import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donor, Donation
import model

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('all'))

@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)

@app.route('/donations/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        try:
            requested_donor = Donor.select().where(Donor.name == request.form['donor_name']).get()
        except Donor.DoesNotExist:
            return render_template('create.jinja2', error='User does not exist!')
        donation = Donation(donor=requested_donor, value=request.form['donation_amount'])
        donation.save()
        return redirect(url_for('home'))
    return render_template('create.jinja2')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)

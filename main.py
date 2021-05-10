import requests
from flask import Flask, render_template, redirect, url_for, request, send_file, make_response, current_app
import dload
import pdfkit
from flask_pymongo import PyMongo
import os
import qrcode
import string
import random
import base64
from flask_mail_sendgrid import MailSendGrid
from flask_mail import Message
from dotenv import load_dotenv
from pathlib import Path

app = Flask(__name__)
img_folder = os.path.join('static', 'images')
app.config['UPLOAD_FOLDER'] = img_folder

dotenv_path = Path('sendgrid.env')
load_dotenv(dotenv_path=dotenv_path) 
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
app.config['MAIL_SENDGRID_API_KEY'] = os.getenv('SENDGRID_API_KEY')
mail = MailSendGrid(app)

# Global variables 
name = ''
srcstate = ''
srcdist = ''
deststate = ''
destdist = ''
mobile = ''
doj = ''
email = ''

# Connecting to MongoDB
mongodb_client = PyMongo(app, uri="mongodb://localhost:27017/E-Pass")
db = mongodb_client.db

# Homepage
@app.route('/')
def registration_form():
   return render_template('form.html')

# Core Logic
@app.route('/register',methods = ['POST', 'GET'])
def input_registration_details():

    fname = request.form['firstname']
    lname = request.form['lastname']
    global name 
    name = fname + " " + lname
    global srcstate
    srcstate = request.form['srcstate']
    global srcdist
    srcdist = request.form['srcdist']
    global deststate
    deststate = request.form['deststate']
    global destdist
    destdist = request.form['destdist']
    global mobile
    mobile = request.form['mobile']
    global doj
    doj = request.form['doj']
    global email
    email = request.form['email']
    
    json = dload.json("https://api.covid19india.org/v4/data.json")
    confirmed_cases = json[deststate]['districts'][destdist]['total']['confirmed']
    recovered_cases = json[deststate]['districts'][destdist]['total']['recovered']
    ratio = (recovered_cases / confirmed_cases) * 100;
    
    # If recovery rate is > 30%
    if(ratio > 30):
        
        # Insert into DB
        obj_id = id_generator()
        dictionary = {'_id': obj_id, 'name': name, 'email': email, 'mobile': mobile, 'srcstate': srcstate, 'srcdist': srcdist, 'deststate': deststate, 'destdist': destdist, 'doj': doj}
        tmp = db.Tokens.insert_one(dictionary)
        
        img = qrcode.make(obj_id)
        img.save(img_folder + '/x.png')
        full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'x.png')

        # Converting image to base64
        with open("static/images/x.png", "rb") as img_file:
        	my_string = base64.b64encode(img_file.read())
        my_string = my_string.decode("utf-8")
        res = "data:image/png;base64,"
        res += my_string
        rendered_page = render_template('epasstemplate.html', name=name, email=email, srcdist=srcdist, srcstate=srcstate, deststate=deststate, destdist=destdist, doj=doj, mobile=mobile, res=res)

        options = {"enable-local-file-access": None, "load-error-handling": "ignore", "load-media-error-handling": "ignore"}
        pdfkit.from_string(rendered_page, 'static/PDFs/epass.pdf', options=options) # Save locally for sending as attachment

        send_mail(email)

        return render_template('epass.html', name=name, email=email, srcdist=srcdist, srcstate=srcstate, deststate=deststate, destdist=destdist, doj=doj, mobile=mobile, qrcode=full_filename)

    return render_template('rejected.html')

# Download PDF
@app.route('/download', methods = ['POST', 'GET'])
def download():

    # Converting image to base64
    with open("static/images/x.png", "rb") as img_file:
        my_string = base64.b64encode(img_file.read())
    my_string = my_string.decode("utf-8")
    res = "data:image/png;base64,"
    res += my_string
    rendered_page = render_template('epasstemplate.html', name=name, email=email, srcdist=srcdist, srcstate=srcstate, deststate=deststate, destdist=destdist, doj=doj, mobile=mobile, res=res)
    
    options = {"enable-local-file-access": None, "load-error-handling": "ignore", "load-media-error-handling": "ignore"}
    pdf = pdfkit.from_string(rendered_page, False, options=options)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename = epass.pdf'

    return response

# Verify page
@app.route('/verify', methods = ['POST', 'GET'])
def verify():
    return render_template("verify.html")

# Verify QR Code Page
@app.route('/verifycode', methods = ['POST', 'GET']) 
def verifycode():
    txt = request.form['text']
    tmp = db.Tokens.find({"_id": txt})
    tmp = list(tmp)
    if len(tmp) != 0:
        return render_template("verified.html")
    return render_template("verificationfailed.html")

# Send mail
def send_mail(email):
	msg = Message("ePass", sender='abhishek.bodapati@gmail.com', recipients=[email])
	msg.body = "PFA"
	with current_app.open_resource("static/PDFs/epass.pdf") as fp:
		msg.attach("epass.pdf","application/pdf", fp.read())
	mail.send(msg)

def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

if __name__ == '__main__':
   app.run(debug = True)

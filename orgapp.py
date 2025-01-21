from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import json
from flask_mail import Mail, Message

# Load configuration from JSON
with open('config.json', "r") as c:
    params = json.load(c)["params"]

local_server = True

app = Flask(__name__, static_folder='static')

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['gmail_user'],
    MAIL_PASSWORD=params['gmail_pass']
)
mail = Mail(app)

if local_server:
    app.config["SQLALCHEMY_DATABASE_URI"] = params['local_uri']
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = params['prod_uri']
db = SQLAlchemy(app)

class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(120), unique=True, nullable=False)
    message = db.Column(db.String(120), unique=False, nullable=False)

class Posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    resource_name = db.Column(db.String(80), unique=False, nullable=False)
    subheading = db.Column(db.String(80), unique=False, nullable=False)
    description = db.Column(db.String(120), unique=False, nullable=False)
    shared_by = db.Column(db.String(120), unique=False, nullable=False)
    date = db.Column(db.String(120), unique=False, nullable=False)
    slug = db.Column(db.String(120), unique=False, nullable=False)
    img_file = db.Column(db.String(120), unique=False, nullable=False)

@app.route("/")
def hello():
    posts = Posts.query.filter_by().all()
    return render_template("index.html", params=params , posts=posts)

@app.route("/about")
def about():
    return render_template("about.html", params=params)

#n3xt commit

@app.route("/dashboard" , methods = ['GET' , 'POST'])
def dashboard():
    if request.method =='POST':
        pass
        #redirect to admin portal
    else:

       return render_template("dashboard.html", params=params)

@app.route("/post/<string:post_slug>",methods=['GET'])
def postfunc(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()
   # print(f"Requested Slug: {post_slug}")

    return render_template("post.html", params=params , post=post)

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        '''add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')

        entry = Contacts(name=name, email=email, phone=phone, message=message)
        db.session.add(entry)
        db.session.commit()
        #this is for sending messages the down ones
        try:
            msg = Message('New Message from ResourceShare: ' + name, 
                          sender=email,  # Sender will be the user who submitted the form
                          recipients=[params['gmail_user']])  # Recipient is you
            msg.body = message + "\n" + phone
            mail.send(msg)
        except Exception as e:
            print(f"Error sending email: {e}")

    return render_template("contact.html", params=params)

if __name__ == '__main__':
    app.run(debug=True)  # Enable debugging

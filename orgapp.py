from flask import Flask, render_template, request, session , redirect
from flask_sqlalchemy import SQLAlchemy
import json , os , datetime, math
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename


# Load configuration from JSON
with open('config.json', "r") as c:
    params = json.load(c)["params"]

local_server = True

app = Flask(__name__, static_folder='static')
app.secret_key = 'super-secret-key'  # Add a secret key for session handling
app.config['UPLOAD_FOLDER'] = params['upload_location']

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

# Database models
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
    shared_by = db.Column(db.String(120), unique=False, nullable=True)
    date = db.Column(db.String(120), unique=False, nullable=True)
    slug = db.Column(db.String(120), unique=False, nullable=False)
    img_file = db.Column(db.String(120), unique=False, nullable=False)

@app.route("/")
def hello():
    posts = Posts.query.filter_by().all()
    posts_per_page = int(params['no_of_posts'])
    last = math.ceil(len(posts) / posts_per_page)  # Calculate the total number of pages
    
    # Get the 'page' parameter from the request
    page = request.args.get('page')
    if not page or not page.isnumeric():
        page = 1
    else:
        page = int(page)
    
    # Calculate start and end index for the current page
    start = (page - 1) * posts_per_page
    end = start + posts_per_page
    paginated_posts = posts[start:end]  # Get the posts for the current page

    # Determine prev and next links
    prev = "#" if page <= 1 else f"/?page={page - 1}"
    next = "#" if page >= last else f"/?page={page + 1}"

    return render_template("index.html", params=params, posts=paginated_posts, prev=prev, next=next)


@app.route("/about")
def about():
    return render_template("about.html", params=params)

@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    if 'user' in session and session['user'] == params['admin-user']:
        posts = Posts.query.all()
        return render_template('dashboard.html' , params=params , posts=posts)
    if request.method == 'POST':
        username = request.form.get('uname')
        userpass = request.form.get('pass')
        # Redirect to admin portal
        if username == params['admin-user'] and userpass == params['admin-pass']:
            session['user'] = username
            posts = Posts.query.all()
            return render_template('dashboard.html' , params=params ,posts=posts)
           # pass  # Handle invalid login (logic can be added later)
    return render_template("login.html", params=params)

@app.route("/post/<string:post_slug>", methods=['GET'])
def postfunc(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()
    return render_template("post.html", params=params, post=post)

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        '''Add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')

        entry = Contacts(name=name, email=email, phone=phone, message=message)
        db.session.add(entry)
        db.session.commit()

        # Send email notification
        try:
            msg = Message(
                'New Message from ResourceShare: ' + name,
                sender=email,  # Sender will be the user who submitted the form
                recipients=[params['gmail_user']]  # Recipient is you
            )
            msg.body = message + "\n" + phone
            mail.send(msg)
        except Exception as e:
            print(f"Error sending email: {e}")

    return render_template("contact.html", params=params)



#edit options 

@app.route("/edit/<string:sno>", methods=['GET', 'POST'])
def edit(sno):
    if 'user' in session and session['user'] == params['admin-user']:
        if request.method == 'POST':
            box_title = request.form.get('title')
            subheading = request.form.get('subheading')
            slug = request.form.get('slug')
            content = request.form.get('content')
            img_file = request.form.get('img_file')
            shared_by = request.form.get('shared_by')
            date = request.form.get('date')
            
            if sno == '0':  # Handling adding a new post
                post = Posts(resource_name=box_title, subheading=subheading, description=content, slug=slug, img_file=img_file , shared_by=shared_by , date=date)
                db.session.add(post)
                db.session.commit()
                return redirect('/dashboard')  # Redirect after adding new post
            
            else:  # Handling editing an existing post
                post = Posts.query.filter_by(sno=sno).first()
                if post:
                    post.resource_name = box_title
                    post.subheading = subheading
                    post.description = content
                    post.slug = slug
                    post.img_file = img_file
                    db.session.commit()
                    return redirect('/edit/'+sno)  # Redirect after editing post
    post=Posts.query.filter_by(sno=sno).first()
    return render_template('edit.html', params=params , post=post , sno=sno)

@app.route("/upload", methods=['GET', 'POST'])
def uploader():
    if 'user' in session and session['user'] == params['admin-user']:
        if request.method == 'POST':
            f = request.files['file1']
            if f:
                filename = secure_filename(f.filename)
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return 'File uploaded successfully'
            else:
                return 'No file uploaded'
    return redirect('/dashboard')  # Redirect if not authenticated

@app.route("/logout")
def logout():
    session.pop('user')
    return redirect("/dashboard")

@app.route("/delete/<string:sno>", methods=['GET', 'POST'])
def delete(sno):
    if 'user' in session and session['user'] == params['admin-user']:
        post= Posts.query.filter_by(sno=sno).first()
        db.session.delete(post)
        db.session.commit()
    return redirect("/dashboard")

if __name__ == '__main__':
    app.run(debug=True)

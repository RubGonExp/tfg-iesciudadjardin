from flask import Flask,render_template,request,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

with open('config.json', 'r') as c:
    params = json.load(c)["params"]

local_server = params["local_server"]
db = SQLAlchemy()

app = Flask(__name__, template_folder='template')

if local_server:
    app.config["SQLALCHEMY_DATABASE_URI"] = params["dev_uri"]
else:
    private_ip_address = params["PRIVATE_IP_ADDRESS"]
    dbname = params["DBNAME"]
    project_id = params["PROJECT_ID"]
    instance_name = params["INSTANCE_NAME"]
    password = params["PASSWORD"]

    app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+mysqldb://root:{password}@{private_ip_address}/{dbname}"

db.init_app(app)

class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone_num = db.Column(db.String(12),  nullable=False)
    mes = db.Column(db.String(120), nullable=False)
    date = db.Column(db.DateTime)
   
class Posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(25), nullable=False)
    content= db.Column(db.String(120), nullable=False)
    date = db.Column(db.DateTime)

# Set up models

def create_table():
    with app.app_context():
        # Create the table in the database
        db.create_all()

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template("about.html")

@app.route('/contact', methods=['GET','POST'])
def contact():    
    if(request.method=="POST"):
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get("message")

        entry = Contacts(name=name,email=email,phone_num=phone,mes=message,date=datetime.now())
        db.session.add(entry)
        db.session.commit()

    return render_template('contact.html',params=params)


@app.route('/post/<string:post_slug>',methods=['GET'])
def post_route(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html',params=params,post=post)
    
#After first insertion , comment out the below line
create_table()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)


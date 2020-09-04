from flask import Flask, render_template, request, flash
from models import Pic, db_init, db
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:7Pillars@localhost/Picshare'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db_init(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload")
def upload():
    pic = request.files['pic']

    if not pic: 
        flash("Image not uploaded")
        return 400

    filename = secure_filename(pic.filename)
    mimetype = pic.mimetype 
    pic = Pic(img=pic.read(), mimetype=mimetype, name=filename)
    db.session.add(pic)
    db.session.commit()

    flash('Image succesfully uploaded!!')
    return 200

@app.route("/<int>:id")
def get_pic(id):
    pic = Pic.query.filter_by(id=id).first()
    if not pic:
        flash("No such image exists")
        return 404
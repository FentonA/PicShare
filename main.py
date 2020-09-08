from flask import Flask, render_template, request, flash, Response, redirect
from models import Pic, db_init, db
from werkzeug.utils import secure_filename
import base64

app = Flask(__name__)
app.secret_key = b'=N1B8-+ydFaEJ'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///img.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db_init(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=['POST'])
def upload():
    pic = request.files['pic']

    if not pic: 
        return "Image not uploaded"

    filename = secure_filename(pic.filename)
    mimetype = pic.mimetype 
    img_string = base64.b64encode(pic.read())
    img = Pic(img=img_string, mimetype=mimetype, name=filename)
    db.session.add(img)
    db.session.commit()

    return redirect('/Images')

@app.route("/<int:id>")
def get_img(id):
    img = Pic.query.filter_by(id=id).first()
    img_string = base64.b64encode(img.img)
    if not img:
        return "Image doesn't exist"
    return Response(img_string, mimetype=img.mimetype)



@app.route("/Images")
def get_pics():
    data = Pic.query.order_by(Pic.id).all()
    return render_template('gallery.html', galleries=data)

if __name__ == "__main__":
    app.run()
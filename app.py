from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///urls.db'

db = SQLAlchemy(app) 

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url_string = db.Column(db.String(500), nullable=False)
    desc = db.Column(db.String(200))
    # def __repr__(self):
    #     return "<Task %r>" % self.id

@app.route('/')
def index():
    urls = URL.query.all()
    return render_template("index.html", urls=urls)

@app.route("/save_url", methods=['POST'])
def post_url():
    content = URL(url_string=request.form["url"])
    desc =  URL(desc=request.form["desc"])
    db.session.add(content)
    db.session.add(desc)
    db.session.commit()

    return redirect(url_for("index"))

@app.route('/<int:id>')
def reroute(id):
    info = URL.query.get_or_404(id)
    return redirect("https://" + info.url_string, code=302)
    

if __name__ == '__main__':
    app.run(debug=True)
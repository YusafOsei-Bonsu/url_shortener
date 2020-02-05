from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import requests
from sqlalchemy import text 

app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///urls.db'

db = SQLAlchemy(app) 

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url_string = db.Column(db.String(500), nullable=False)
    description = db.Column(db.String(200))


@app.route('/')
def index():
    urls = URL.query.all()
    print(urls)
    print(type(urls))
    return render_template("index.html", urls=urls)

@app.route("/save_url", methods=['POST'])
def post_url():
    x = request.form['url']
    y = request.form['description']
    if (len(x) == 0 or len(y) == 0 ):
        return 'Sorry you must enter a URL with a description'
    else:
        content = URL(url_string=request.form["url"], description=request.form["description"]) 
        db.session.add(content)
        db.session.commit()

        return redirect(url_for("index"))

@app.route('/<int:id>')
def reroute(id):
    info = URL.query.get_or_404(id)
    new_url = info.url_string
    if (not ('https://' in new_url)):
        new_url = 'https://' + new_url
    
    return redirect(new_url, code=302)

@app.route('/_co_uk')
def get_co_uk():
    sql = text("select id, url_string, description from url where url_string like '%.co.uk%'")
    x = db.engine.execute(sql)
    result = [row for row in x]
    print(result)
    print(type(result))
    return render_template('index.html', urls=result, show_co_uk=1)

@app.route('/com')
def get_com():
    sql = text("select id, url_string, description from url where url_string like '%.com%'")
    x = db.engine.execute(sql)
    result = [row for row in x]
    print(result)
    print(type(result))
    return render_template('index.html', urls=result, show_com=1)

@app.route('/net')
def get_net():
    sql = text("select id, url_string, description from url where url_string like '%.net%'")
    x = db.engine.execute(sql)
    result = [row for row in x]
    print(result)
    print(type(result))
    return render_template('index.html', urls=result, show_net=1)

@app.route('/org')
def get_org():
    sql = text("select id, url_string, description from url where url_string like '%.org%'")
    x = db.engine.execute(sql)
    result = [row for row in x]
    print(result)
    print(type(result))
    return render_template('index.html', urls=result, show_org=1)


if __name__ == '__main__':
    app.run(debug=True)
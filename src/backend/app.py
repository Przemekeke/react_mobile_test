from dataclasses import field
from distutils.log import debug
from email.policy import default
from this import d
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config['SQLALCHEMY_DATABESE_URI'] = 'mysql://pmarciniak:12345678:@localhost:3306/flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Articles(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    body = db.Column(db.Text(100))
    date = db.Column(db.DateTime, default = datetime.datetime.now)

    def __init__(self, title, body) -> None:
        super().__init__()
        self.title = title
        self.body = body

class ArticleSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'body', 'date')

article_schema = ArticleSchema()
article_schema = ArticleSchema(many=True)

@app.route('/get', methods = ['GET'])
def get_articles():
    return jsonify({"Hello": "Worlds"})

@app.route('/add', methods = ['POST'])
def add_article():
    title = request.json['title']
    body = request.json['body']

    articles = Articles(title, body)
    db.session.add(articles)
    db.session.commit()
    return article_schema.jsonify(articles)


if __name__ == "__main__":
    app.run(debug=True)
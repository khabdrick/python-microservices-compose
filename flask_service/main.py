from flask import Flask, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint #u8sed to make sure user_id and article_id is unique
from dataclasses import dataclass # used to define a clas that encapsulate data
import requests
from producer import publish

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://khabdrick1:secure-password@flask_db/likes'

db = SQLAlchemy(app)

@dataclass
class Article(db.Model):
    id: int
    title: str
    details: str
    timestamp: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(200))
    details = db.Column(db.String(1000))
    timestamp = db.Column(db.String(200))


@dataclass
class BlogUser(db.Model):
    # get's data for liked article. Make sure a user is only able to like once.
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    article_id = db.Column(db.Integer)

    UniqueConstraint('user_id', 'article_id', name='user_article_unique')


@app.route('/api/articles')
def index():
    return jsonify(Article.query.all())


@app.route('/api/article/<int:id>/like', methods=['POST'])
def like(id):
    req = requests.get('http://172.30.0.2:8000/user')
    
    userID = req.json()

    try:
        blogUser = BlogUser(user_id=userID['id'], article_id=id)
        db.session.add(blogUser)
        db.session.commit()
        publish('article_liked', id)

    except:
        abort(400, 'You already liked this article')

    return jsonify({
        'message': 'success'
    })



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
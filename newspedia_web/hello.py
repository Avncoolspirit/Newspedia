from flask import Flask,jsonify, make_response
from keyword_extraction import extract_keyword as ek, extract_subs, subs_between_time
import sqlite3
from flask import g

DATABASE = 'test.db'

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()




def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    get_db().commit()
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

with app.app_context():
    for user in query_db('select * from state'):
        print (user[0], 'has the id', user[1])



# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# db = SQLAlchemy(app)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)

#     def __repr__(self):
#         return '<User %r>' % self.username

# db.session.add(User(username="Flask", email="example@example.com"))
# db.session.commit()

# users = User.query.all()
# for users in Query:
#     print(users.id)


tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
    ]

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route("/")
def index():
    return "Index!"

@app.route("/hello")
def hello():
    return "Hello World!"

@app.route("/members")
def members():
    return "Members"

@app.route("/api/v1.0/update_time/<int:videoid>/<int:time>/")
def updateTime(videoid,time):
    query_db('UPDATE state SET video_id = ?, time = ? where id  = 1' ,(videoid,time))
    return "Success!"
    


@app.route("/api/v1.0/get_recos/<string:videoid>/<int:time>/")
def getMember(videoid,time):
    string_test =""
    state = query_db('select * from state')
    subs_to_extract = extract_subs(videoid+'.srt')
    snap = subs_between_time(subs_to_extract,int(state[0][2])-2,int(state[0][2]))
    string_test = ' '.join(snap)
    return jsonify({'videoid':videoid,'time_elased':state[0][2],'keywords':ek(string_test)})

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})


if __name__ == "__main__":
    app.run('0.0.0.0')

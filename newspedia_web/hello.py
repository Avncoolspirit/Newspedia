from flask import Flask,jsonify, make_response
from keyword_extraction import extract_keyword as ek, extract_subs, subs_between_time
app = Flask(__name__)

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

@app.route("/api/v1.0/get_recos/<string:videoid>/<int:time>/<int:time>")
def getMember(videoid,time):
	string_test =""
	if int(videoid) == 1 :
		subs_to_extract = extract_subs('sub1.srt')
		snap = subs_between_time(subs_to_extract,int(time)-2,int(time))
		string_test = ' '.join(snap)
	return jsonify(ek(string_test))

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})


if __name__ == "__main__":
    app.run()

import chatterbot
from flask import Response, jsonify, Flask, request
from chatterbot import ChatBot
from pymongo import MongoClient, message
from flask import jsonify
import json
from chatterbot.trainers import ChatterBotCorpusTrainer
from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

def Convert(lst):
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dct


mongodb_uri = 'mongodb+srv://User_1:Qwerty@cluster0.q5slf.mongodb.net/bktlist?retryWrites=true&w=majority'

print(chatterbot.__file__) 
client = MongoClient(mongodb_uri)
bugs = client.bktlist.Bugs
feedback = client.bktlist.feedback
announcement = client.bktlist.announcement
admin = client.bktlist.admin

english_bot = ChatBot("English Bot", 
                     storage_adapter = "chatterbot.storage.MongoDatabaseAdapter",
                     database = 'bktlist',
                     database_uri = mongodb_uri)
trainer = ChatterBotCorpusTrainer(english_bot)
# trainer.train("chatterbot.corpus.english")
trainer.load()

app = Flask(__name__)

app.config['SECRET_KEY']  = '5791628bb0b13ce0c676dfde280ba245'

@app.route('/health-check', methods=['GET'])
def health():
    return Response("I'm healthy. Thanks for asking. -Sonali", status=200)

@app.route('/chatbot', methods=['POST'])
def chatbot():
    userText = request.get_json()
    return jsonify(reply=str(english_bot.get_response(userText['msg'])))

@app.route('/bugs', methods=['GET', 'POST'])
def bugs_():
    if request.method == 'POST':
        userText = request.get_json()
        bug = bugs
        bug.insert(userText)
        return "Bug sucessfully registered"
    if request.method == 'GET':
        bug = bugs
        return json.dumps(list(bug.find({})), cls=JSONEncoder)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback_():
    if request.method == 'POST':
        userText = request.get_json()
        feedbacks = feedback
        feedbacks.insert(userText)
        return "Feedback sucessfully registered"
    if request.method == 'GET':
        feedbacks = feedback
        return json.dumps(list(feedbacks.find({})), cls=JSONEncoder)

@app.route('/announcement', methods=['GET', 'POST'])
def announcement_():
    if request.method == 'POST':
        userText = request.get_json()
        announce = announcement
        announce.insert(userText)
        return "Feedback sucessfully registered"
    if request.method == 'GET':
        announce = announcement
        return json.dumps(list(announce.find().sort([('_id',-1)]).limit(5)), cls=JSONEncoder)

@app.route('/login', methods=['POST'])
def login_():
    users=admin
    user_id_pass = request.get_json()
    login_user = users.find_one({'username': user_id_pass['username']})
    if login_user:
        if login_user['password']==user_id_pass['password']:
            return jsonify(messgae = 'Valid Admin', status = "true")

    return jsonify(message = 'Invalid username or password.. Please go back and try again.', status = "false")


@app.route('/register', methods=['POST', 'GET'])
def register_():
    if request.method == 'POST':
        users = admin
        user_id_pass = request.get_json()
        existing_user = users.find_one({'username' : user_id_pass['username']})

        if existing_user is None:
            users.insert(user_id_pass)
            return jsonify(message = 'Admin Created', status = "true")

        return jsonify(message = 'That username already exists! Please go back and register again', status = "false")


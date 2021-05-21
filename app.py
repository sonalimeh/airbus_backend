import chatterbot
from flask import Response, jsonify, Flask, request
from chatterbot import ChatBot
from pymongo import MongoClient
from flask import jsonify
import json
from chatterbot.trainers import ChatterBotCorpusTrainer
from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


mongodb_uri = 'mongodb+srv://User_1:Qwerty@cluster0.q5slf.mongodb.net/bktlist?retryWrites=true&w=majority'

print(chatterbot.__file__) 
client = MongoClient(mongodb_uri)
bugs = client.bktlist.Bugs
feedback = client.bktlist.feedback
announcement = client.bktlist.announcement

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

@app.route('/chatbot', methods=['GET'])
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
        return json.dumps(list(announce.find({})), cls=JSONEncoder)

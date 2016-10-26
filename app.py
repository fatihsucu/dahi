from bson import ObjectId
from dahi.bot import Bot
from dahi.context import Context
from dahi.document import Document
from dahi.documents import Documents
from dahi.knowledgebase import KnowledgeBase
from dahi.statement import Statement
from flask import Flask, Blueprint, request, jsonify, send_from_directory
from pymongo import MongoClient

# TODO: a config file required for flask app
api = Blueprint("api", __name__, url_prefix="/api/v1")
ui = Blueprint("ui", __name__, static_folder="static/")

# TODO: move the db initialization into a separate module
db = MongoClient("mongodb://192.168.2.209")["dahi"]
docs = Documents(db["docs"])
kb = KnowledgeBase(db, 1)
botId = 12


@ui.route('/index')
def send_index():
    return ui.send_static_file("index.html")


@ui.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('static/css', path)


@ui.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


@api.route("/docs/")
def getDocs():
    kb = KnowledgeBase(db, 1)
    d = Bot(kb).knowledgeBase.getAll()
    # TODO: improve this jsonify operation, make it less verbose
    a = [i.toJson() for i in d]
    return jsonify({"docs": a})


@api.route("/docs/", methods=["POST"])
def insertDoc():
    question = request.form["question"]
    answer = request.form["answer"]
    onMatch = answer
    doc = Document(ObjectId(), humanSay=Statement(question), botSay=Statement(answer), onMatch=onMatch)
    bot = Bot(kb)
    bot.learn(doc)

    # TODO: every response must be in a standard format. restfulApi doc needed.
    return jsonify(doc.toJson())


@api.route("/answer")
def getAnswer():
    queryStatement = Statement(request.args["q"])

    userId = 3
    bot = Bot(kb)

    context = Context(123)
    responseStatement = bot.respond(context, queryStatement)

    context.insert(queryStatement)
    context.insert(responseStatement)
    return jsonify(responseStatement.toJson())


def run():
    app = Flask(__name__)
    app.register_blueprint(api)
    app.register_blueprint(ui)
    app.debug = True
    app.run()

if __name__ == "__main__":
    run()

from bson import ObjectId
from dahi.bot import Bot
from dahi.context import Context
from dahi.document import Document
from dahi.documents import Documents
from dahi.storages import Mongo
from dahi.knowledgebase import KnowledgeBase
from dahi.statement import Statement
from flask import Flask, Blueprint, request, jsonify, send_from_directory, render_template
from flask import request, abort
import functools
from pymongo import MongoClient

app = Flask(__name__)


def jsonize_request():
    if request.method != 'GET':
        datatype = request.headers.get("Content-Type", None)
        print(request.json)
        if not datatype:
            abort(404)
        elif "application/x-www-form-urlencoded" in datatype:
            data = dict(request.form)
            for each in data.keys():
                data[each] = data[each][0]
        elif "application/json" in datatype:
            data = dict(request.json)
        else:
            return {}
        return data
    else:
        data = dict(request.args.items())
        return data


def jsonizeRequest(f):
    @functools.wraps(f)
    def wrapper(*args, **kwds):
        data = jsonize_request()
        kwds['data'] = data
        return f(*args, **kwds)

    return wrapper

storage = Mongo("mongodb://172.25.1.77/dahi")
#context = contexts.Builder(storage).create(meta={})
accountid = "58ac69c6eb29aa3a897b97ac"
result = []
kb = KnowledgeBase(storage, accountid)

@app.route("/")
def index():
    question = request.args.get("questionText", None)
    answer = request.args.get("answerText", None)
    if question and answer:
        bot = Bot(kb)
        bot.learn(Document(
            humanSay=Statement(question),
            botSay=Statement(answer)
            )
        )
    qas = kb.getAll()
    response = [qa.toJson() for qa in qas]
    return render_template('index.html', qas=response)


@app.route("/test", methods=["GET"])
def learn():
    try:
        question = request.args.get("questionText", None)
        if question:
            bot = Bot(kb)
            answer = bot.respond(Statement(question))
            answer =  answer.botSay.text
            result.append({"asked": question, "answer": answer})
    except:
        pass
    return render_template('test.html', qas=result)


def run():
    app.run("0.0.0.0")

if __name__ == "__main__":
    run()

from pymongo import MongoClient

from dahi import bots, contexts, storages
from dahi.contexts import ContextNotFoundError
from dahi.document import Document
from dahi.knowledgebase import KnowledgeBase
from dahi.statement import Statement
from dahi.storages import Mongo

storage = Mongo("mongodb://192.168.2.209/dahi")
contextId = "57960e326bb20030900eb6d4"

try:
    context = contexts.Builder(storage).get(contextId)
except ContextNotFoundError:
    context = contexts.Builder(storage).create(meta={})

bot = bots.Builder(storage).create(meta={})
bot.knowledgeBase.truncate()

bot.learn(Document(
    humanSay=Statement("kredi karti nedir"),
    botSay=Statement("kredi karti nedir dedin")))

bot.learn(Document(
    humanSay=Statement("kredi faizi"),
    botSay=Statement("kredi faizi dedin")))

bot.learn(Document(
    humanSay=Statement("kredi karti"),
    botSay=Statement("kredi karti dedin")))

bot.learn(Document(
    humanSay=Statement("Selam"),
    botSay=Statement("Merhaba")))

bot.learn(Document(
    humanSay=Statement("Selam, tuvalet nerede?"),
    botSay=Statement("Az ilerde sagdaki duvar")))

print(bot.respond(context, Statement("Selam")))
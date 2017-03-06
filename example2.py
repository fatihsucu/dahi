from dahi import bots, contexts
from dahi.contexts import ContextNotFoundError
from dahi.document import Document
from dahi.knowledgebase import KnowledgeBase
from dahi.nlu import MatchNotFound
from dahi.statement import Statement
from dahi.storages import Mongo

storage = Mongo("mongodb://172.25.1.77/dahi")
botId = "57e9095c102ee808b06f0ae1"
storage.db.drop_collection("bots")
storage.db.drop_collection("docs")

questionAnswers = [
    {
        "question": "How can I get my private hire licence?",
        "answer": "In order to become a partner driving on the platform, you need to obtain a private hire licence (previously known as a PCO licence) for London from TfL (Transport for London), which can take an average of 6-8 weeks to obtain. To help you through this process you can attend one of our Ignition licence guidance sessions. For more information on this and how to book a session please visit t.uber.com/private-hire-booking."
    },
    {
        "question": "What are the benefits of obtaining your private hire licence with the help of Uber's Ignition programme?",
        "answer": "In addition to having a dedicated team to provide the information you need to help submit your application successfully, we will provide the topographical guidance and assessment totally free of charge.You can now also complete your enhanced DBS background check in office as well as register for a medical check! Please remember there is no requirement to drive on the Uber platform once you have your licence, but we are happy to assist you in the process regardless."
    },
    {
        "question": "I tried to book an appointment for the Ignition session, but they are all booked up. What do I do?",
        "answer": "We now offer sessions 6 days a week, so there should be lots of availability. Simply re-visit the booking website and select the next most convenient session for you."
    },
    {
        "question": "What do I need to bring to the Ignition session?",
        "answer": "Please bring the following to the one day licensing session:"
    },
    {
        "question": "Do you know the way of Los Angeles",
        "answer": "Here is the way of LA. Please click here"
    },
    {
        "question": "Do you know way of New York",
        "answer": "Here is the way of NY. Please click here"
    },
    {
        "question": "How much does the whole process cost?",
        "answer": "15$ is the total cost of whole process"
    },
    {
        "question": "What is your age?",
        "answer": "I am X years old."
    },
    {
        "question": "Do you love me?",
        "answer": "I love all world but not you."
    },
    {
        "question": "I need some help",
        "answer": "I am here just say it"
    },
    {
        "question": "I want to be your friend",
        "answer": "Ok you can of course"
    },
    {
        "question": "I want to refund",
        "answer": "I don't handle refunds, sorry for that. Please send an email to team@botego.com with your account information."
    },
    {
        "question": "I want to delete my chats",
        "answer": "Deleting chats is a premium feature and you can do so by clicking the menu icon on top right side of the chat screen."
    },
    {
        "question": "Kredi karti basvurusu nasil yapilir?",
        "answer": "Kredi karti basvusuru icin asagidaki adimlari izleyebilirsiniz."
    }
]

bot = bots.Builder(storage).create(botId=botId, meta={})

print("Bot learning these questions")
print("===================================")
print("                                   ")
for item in questionAnswers:
    print(" @  {}".format(item["question"]))
    bot.learn(Document(
            humanSay=Statement(item["question"]),
            botSay=Statement(item["answer"])))


# bot2 = bots.Builder(storage).get(botId=bot2Id)
#
# bot1 = bots.Builder(storage).create(botId=bot1Id, meta={})
# bot2 = bots.Builder(storage).create(botId=bot2Id, meta={})

# bot1.learn(Document(
#     botSay=Statement("bot 1 elma dedin"),
#     humanSay=Statement("elma")))

# print(context)
# try:
#     print(bot2.respond(context, Statement(text="elma")))
# except MatchNotFound:
#     print("bot 2 match not found")

def run():
    while True:
        print("                                    ")
        text = raw_input("Type Your question please :")
        print("                                    ")
        if text == "show_synos":
            print(bot.matcher.model.synonyms)
        if text == "q":
            return
        try:
            print(bot.respond(Statement(text=text)).botSay)
        except MatchNotFound:
            print("Couldn't find any match for {}".format(text))


if __name__ == "__main__":
    run()
    KnowledgeBase(storage, botId).remove(docID="57ee51816bb2003008fcd4c2")

from flask import Flask, render_template, jsonify, request
from flask_pymongo import PyMongo

# import os
import openai

openai.api_key = "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"

app = Flask(__name__)


app.config["MONGO_URI"] = "mongodb+srv://tyagianiket6:FruaBgc1kkv0SsXJ@cluster0.l34lh.mongodb.net/chatgpt"

mongo = PyMongo(app)

@app.route("/")
def hello_world():
    chats = mongo.db.chats.find({})
    myChats = [chat for chat in chats]
    print(myChats)
    return render_template("index.html", context={"myChats": myChats})

@app.route("/api", methods=["GET", "POST"])
def qa():
    if request.method == "POST":
        # print(request.json)
        question = request.json.get("question")
        chat = mongo.db.chats.find_one({"question": question})
        # print(chat)
        if(chat):
            data = {"question": question, "answer": f"{chat['answer']}"}
            return jsonify(data)
        else:
            response = openai.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=question,
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
            )
            # print(response)
            generated_text = response.choices[0].text.replace('\\n', '\n')  # Accessing the generated text
            data = {"question": question, "answer": generated_text}
            mongo.db.chats.insert_one({"question": question, "answer": generated_text})
            return jsonify(data)
    data = {"result": "Hello welcome to my api"}
    return jsonify(data)


app.run(debug=True)
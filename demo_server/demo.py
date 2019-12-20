from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/_func/', methods=['POST'])
def _func():
    data = json.load(open("output.json"))
    return data

if __name__ == "__main__":
    app.run(debug=True, port=4621)

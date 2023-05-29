from flask import Flask, request
import json
import auto_reply
import traceback
import logging


app = Flask(__name__)


@app.route('/')
def home():
    return 'Home Page Route API'


@app.route('/webhook', methods=['GET', 'POST'])
def req():
    request_data = request.get_data()
    try:
        data = json.loads(request_data)
        auto_reply.reply_comment(data['entry'][0]['changes'])
    except Exception as error:
        logging.error(traceback.format_exc())
    return request.args.get('hub.challenge', 'Hahah')


if __name__ == '__main__':
    app.run(debug=True)
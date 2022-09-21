import os
import sys
from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from fsm import TocMachine
from utils import send_text_message

import configparser

load_dotenv()

machine = TocMachine(
    states=["user", "help", 
            "new", "hot", "search", "name",
            "taiwan", "usa", "week",
            "hot_drama", "type_drama", "hot_taiwan",
            "china", "hongkong", "japan", "korea", "america", "england",
            ],
    transitions=[
        {
            "trigger": "advance",
            "source": "user",
            "dest": "help",
            "conditions": "is_going_to_help",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "new",
            "conditions": "is_going_to_new",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "hot",
            "conditions": "is_going_to_hot",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "search",
            "conditions": "is_going_to_search",
        },

        {
            "trigger": "advance",
            "source": "search",
            "dest": "name",
            "conditions": "is_going_to_name",
        },

        {
            "trigger": "advance",
            "source": "user",
            "dest": "taiwan",
            "conditions": "is_going_to_taiwan",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "usa",
            "conditions": "is_going_to_usa",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "week",
            "conditions": "is_going_to_week",
        },

        {
            "trigger": "advance",
            "source": "user",
            "dest": "hot_taiwan",
            "conditions": "is_going_to_hot_taiwan",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "hot_drama",
            "conditions": "is_going_to_hot_drama",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "type_drama",
            "conditions": "is_going_to_type_drama",

        },
        {
            "trigger": "advance",
            "source": "type_drama",
            "dest": "china",
            "conditions": "is_going_to_china",
        },
        {
            "trigger": "advance",
            "source": "type_drama",
            "dest": "hongkong",
            "conditions": "is_going_to_hongkong",
        },
        {
            "trigger": "advance",
            "source": "type_drama",
            "dest": "japan",
            "conditions": "is_going_to_japan",
        },
        {
            "trigger": "advance",
            "source": "type_drama",
            "dest": "korea",
            "conditions": "is_going_to_korea",
        },
        {
            "trigger": "advance",
            "source": "type_drama",
            "dest": "america",
            "conditions": "is_going_to_america",
        },
        {
            "trigger": "advance",
            "source": "type_drama",
            "dest": "england",
            "conditions": "is_going_to_england",
        },

        {
            "trigger": "advance",
            "source": ["china", "hongkong", "japan", "korea", "america", "england"],
            "dest": "type_drama",
            "conditions": "is_going_to_back",
        },

        {
            "trigger": "advance",
            "source": "name",
            "dest": "search",
            "conditions": "is_going_to_back",
        },

        {
            "trigger": "advance",
            "source": ["china", "hongkong", "japan", "korea", "america", "england"
                        , "name"],
            "dest": "help",
            "conditions": "is_going_to_home",
        },

        {
            "trigger": "go_back", 
            "source": [ "help", 
                        "new", "hot",
                        # "movie", "tv", "search_movie",
                        "taiwan", "usa", "week",
                        "hot_drama", "hot_taiwan",
                        # "china", "hongkong", "japan", "korea", "america", "england"
                        ], 
            "dest": "user"
        }
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")

# read config
config = configparser.ConfigParser()
config.read("config.ini")

# get channel_secret and channel_access_token from your environment variable
# channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
# channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)

# get channel_secret and channel_access_token from your environment variable
channel_access_token = config['line_bot']['Channel_Access_Token']
channel_secret = config['line_bot']['Channel_Secret']

# print(channel_access_token)
# print(channel_secret)

if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


# echo
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"

# main function
@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False:
            send_text_message(event.reply_token, "Not Entering any State")

    return "OK"

# draw the fsm img
@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")

if __name__ == "__main__":
    port = os.environ.get("PORT", 5000)
    app.run(host="0.0.0.0", port=port, debug=True)

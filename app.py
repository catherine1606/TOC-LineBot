import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message

load_dotenv()

machine = TocMachine(
    states=["user", "menu", "game1", "game2", "game3", "game4", "score", "answer", "search", "get_idiom", "not_search", "mean", "story"],
    transitions=[
        {
            "trigger": "advance",
            "source": "user",
            "dest": "menu",
            "conditions": "is_going_to_menu",
        },
        {
            "trigger": "advance",
            "source": "menu",
            "dest": "game1",
            "conditions": "is_going_to_game1",
        },
        {
            "trigger": "advance",
            "source": "game1",
            "dest": "game2",
            "conditions": "is_going_to_game2",
        },
        {
            "trigger": "advance",
            "source": "game2",
            "dest": "game3",
            "conditions": "is_going_to_game3",
        },
        {
            "trigger": "advance",
            "source": "game3",
            "dest": "game4",
            "conditions": "is_going_to_game4",
        },
        {
            "trigger": "advance",
            "source": "game4",
            "dest": "score",
            "conditions": "is_going_to_score",
        },
        {
            "trigger": "advance",
            "source": "score",
            "dest": "answer",
            "conditions": "is_going_to_answer",
        },
        {
            "trigger": "advance",
            "source": "score",
            "dest": "menu",
            "conditions": "is_going_to_menu",
        },
        {
            "trigger": "advance",
            "source": "answer",
            "dest": "get_idiom",
            "conditions": "is_going_to_get_idiom",
        },
        {
            "trigger": "advance",
            "source": "answer",
            "dest": "not_search",
            "conditions": "is_going_to_not_search",
        },
        {
            "trigger": "advance",
            "source": "menu",
            "dest": "search",
            "conditions": "is_going_to_search",
        },
        {
            "trigger": "advance",
            "source": "search",
            "dest": "menu",
            "conditions": "is_going_to_menu",
        },
        {
            "trigger": "advance",
            "source": "search",
            "dest": "get_idiom",
            "conditions": "is_going_to_get_idiom",
        },
        {
            "trigger": "advance",
            "source": "search",
            "dest": "not_search",
            "conditions": "is_going_to_not_search",
        },
        {
            "trigger": "advance",
            "source": "not_search",
            "dest": "search",
            "conditions": "is_going_to_search",
        },
        {
            "trigger": "advance",
            "source": "not_search",
            "dest": "menu",
            "conditions": "is_going_to_menu",
        },
        {
            "trigger": "advance",
            "source": "get_idiom",
            "dest": "mean",
            "conditions": "is_going_to_mean",
        },
        {
            "trigger": "advance",
            "source": "mean",
            "dest": "story",
            "conditions": "is_going_to_story",
        },
        {
            "trigger": "advance",
            "source": "mean",
            "dest": "menu",
            "conditions": "is_going_to_menu",
        },
        {
            "trigger": "advance",
            "source": "get_idiom",
            "dest": "story",
            "conditions": "is_going_to_story",
        },
        {
            "trigger": "advance",
            "source": "story",
            "dest": "mean",
            "conditions": "is_going_to_mean",
        },
        {
            "trigger": "advance",
            "source": "story",
            "dest": "search",
            "conditions": "is_going_to_search",
        },
        {
            "trigger": "advance",
            "source": "story",
            "dest": "menu",
            "conditions": "is_going_to_menu",
        },
        {"trigger": "go_back", "source": ["menu", "game1", "game2", "game3", "game4", "score", "answer", "search", "get_idiom", "not_search", "mean", "story"], "dest": "user"},
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)
# machine.get_graph().draw("fsm.png", prog="dot", format="png")

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
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
            machine.state = "user"
            send_text_message(event.reply_token, "無效操作！\n請輸入「主選單」返回列表")

    return "OK"

if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
from flask import Flask, render_template, session
from uuid import uuid4

from boggle import BoggleWordList, BoggleBoard

SESS_BOARD_UUID_KEY = "board_uuid"

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

word_list = BoggleWordList()

# The boggle boards created, keyed by board uuid
boards = {}


@app.route("/")
def homepage():
    """Show board."""

    # get a unique identifier for the board we're creating
    uuid = uuid4()

    board = BoggleBoard()
    boards[uuid] = board

    # store the uuid for the board in the session so that later requests can
    # find it
    session[SESS_BOARD_UUID_KEY] = uuid

    return render_template(
        "index.html",
        board=board)

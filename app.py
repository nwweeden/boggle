from flask import Flask, render_template, session, request, jsonify
from uuid import uuid4
from flask_debugtoolbar import DebugToolbarExtension

from boggle import BoggleWordList, BoggleBoard

SESS_BOARD_UUID_KEY = "board_uuid"

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

debug = DebugToolbarExtension(app)

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

@app.route('/api/score-word', methods=['POST'])
def validate_word():
    # breakpoint()
    current_word = request.json['submit_word'] #what is a JSON bdoy??
    board = boards[session[SESS_BOARD_UUID_KEY]]

    check_word = word_list.check_word(current_word)
    check_on_board = board.check_word_on_board(current_word)

    if not check_word: 
        return jsonify({'result': "not-word"})
    if not check_on_board:
        return jsonify({'result': "not-on-board"})
    else:
        return jsonify({'result': "ok", 'word': f"{current_word}"})


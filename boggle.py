"""Code for the logic of boggle board and work search."""

from random import choice

LETTERS_BY_FREQ = (
        "EEEEEEEAAAAAAOOOOOIIIIUUU" +
        "RRRRSSSSTTTTLLLLNNN" +
        "BBCCDDFFGGHHKKMMPPYY" +
        "JVWXZ")


class BoggleWordList:
    """List of words for a Boggle game."""

    def __init__(self, dict_path="/usr/share/dict/words"):
        """Create a word list from a dictionary file on disk."""

        self.words = self.read_dict(dict_path)

    @staticmethod
    def read_dict(dict_path):
        """Read dictionary file at dict_path and return set of words."""

        dict_file = open(dict_path)
        words = {w.strip().upper() for w in dict_file}
        dict_file.close()
        return words

    def check_word(self, word):
        """Is word in word list?"""

        return word in self.words

    @classmethod
    def score_word(cls, word):
        """Calculate point totals for a word"""

        return len(word)


class BoggleBoard(list):
    """A board for Boggle, where it can find words on the board."""

    def __init__(self, board_size=5):
        """Create empty board and fill with random letters."""

        self.board_size = board_size

        board = []
        for y in range(board_size):
            board.append([choice(LETTERS_BY_FREQ) for x in range(board_size)])

        super().__init__(board)

    def __repr__(self):
        board_text = super().__repr__()
        return f"<BoggleBoard board_size={self.board_size} board={board_text}>"

    def check_word_on_board(self, word):
        """Can word be found in board? Returns True/False."""

        # Find starting letter --- try every spot on board and,
        # win fast, should we find the word at that place.

        for y in range(0, 5):
            for x in range(0, 5):
                if self._find_from(word, y, x, seen=set()):
                    return True

        # Tried every path from every starting square w/o luck. Sad panda.
        return False

    def _find_from(self, word, y, x, seen):
        """Can we find a word on board, starting at x, y?

        - word: word in all uppercase
        - y, x: coordinates to start search
        - seen: set of of (y,x) starting places already checked

        Returns True/False
        """

        # This is called recursively to find smaller and smaller words
        # until all tries are exhausted or until success.

        # if we're searching off the board, current recursion fails
        if x < 0 or x >= self.board_size or y < 0 or y >= self.board_size:
            return False

        # Base case: this isn't the letter we're looking for.
        if self[y][x] != word[0]:
            return False

        # Base case: we've used this letter before in this current path
        if (y, x) in seen:
            return False

        # Base case: we are down to the last letter --- so we win!
        if len(word) == 1:
            return True

        # Otherwise, this letter is good, so note that we've seen it,
        # and try of all of its neighbors for the first letter of the
        # rest of the word/

        # This next line is a bit tricky: we want to note that we've seen the
        # letter at this location. However, we only want the child calls of this
        # to get that, and if we used `seen.add(...)` to add it to our set,
        # *all* calls would get that, since the set is passed around. That would
        # mean that once we try a letter in one call, it could never be tried again,
        # even in a totally different path. Therefore, we want to create a *new*
        # seen set that is equal to this set plus the new letter. Being a new
        # object, rather than a mutated shared object, calls that don't descend
        # from us won't have this `y,x` point in their seen.
        #
        # To do this, we use the | (set-union) operator, read this line as
        # "rebind seen to the union of the current seen and the set of point(y,x))."

        seen = seen | {(y, x)}

        rest_of_word = word[1:]

        # Search every letter (horiz, vert, diagonal) from here
        for dx in [-1, 0, +1]:
            for dy in [-1, 0, +1]:
                # already on the center letter, so don't use that
                if dx == dy == 0:
                    continue

                if self._find_from(rest_of_word, y + dy, x + dx, seen):
                    return True

        # Couldn't find the next letter, so this path is dead
        return False

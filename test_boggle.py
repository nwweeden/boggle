from string import ascii_uppercase
from unittest import TestCase
from boggle import BoggleWordList, BoggleBoard

TEST_DICTIONARY_PATH = "./test_dictionary.txt"


class BoggleWordListTestCase(TestCase):
    """Tests about the BoggleWordList."""

    def test_word_list(self):
        """Test that word list creation works, and check_word function works."""
        word_list = BoggleWordList()

        
        self.assertFalse(len(word_list.words) == 0, False)
        self.assertTrue(word_list.check_word('PUREE'), True)


class BoggleBoardTestCase(TestCase):
    """Tests about the BoggleBoard."""

    def test_initializer(self):
        """Test board was created successfully."""

        board = BoggleBoard(3)

        self.assertTrue(
            all(
                all(cell in ascii_uppercase for cell in row) for row in board
            ))

        # Make sure each row is a separate list, now a copy of another row!
        self.assertTrue(board[0] is not board[1])

    def test_check_word_on_board(self):
        """Is word on board?"""

        board = BoggleBoard(3)

        # fill board with exact setup so we can test word finding
        board[0] = ['C', 'X', 'X']
        board[1] = ['A', 'T', 'X']
        board[2] = ['D', 'O', 'G']

        self.assertTrue(board.check_word_on_board("CAT"))
        self.assertTrue(board.check_word_on_board("DOG"))
        self.assertFalse(board.check_word_on_board("PET"))

#!/usr/bin/python

import unittest
from ticktacktoe import Painter
from ticktacktoe import Prompter
from StringIO import StringIO
from mock import patch, Mock

class PainterTestCase(unittest.TestCase):

    def setUp(self):
        data = [
            [1,2,3],
            [1,2,3],
            [1,2,3],
        ]
        self.board = Mock(data=data)

    def test_init(self):
        p = Painter('board')
        self.assertTrue(isinstance(p, Painter))

    @patch('sys.stdout', new_callable=StringIO)
    def test_paint_board(self, m_stdout):
        p = Painter(self.board)
        p()
        expected = ('\n    A | B | C\n  ------------\n1 | 1 | 2 | 3\n  '
                    '|---|---|---\n2 | 1 | 2 | 3\n  |---|---|---\n'
                    '3 | 1 | 2 | 3\n  |---|---|---\n')
        self.assertEqual(m_stdout.getvalue(), expected)


class PrompterTestCase(unittest.TestCase):

    @patch('sys.stdin', StringIO('users_input'))
    def test_get_input(self):
        p = Prompter()
        player = Mock(name='Fred')
        got = p.get_input(player)
        self.assertEqual('users_input', got)

    def test_validate_input_bad1(self):
        p = Prompter()
        self.assertEqual(None, p.validate_input('X'))

    def test_validate_input_bad2(self):
        p = Prompter()
        self.assertEqual(None, p.validate_input('A4'))

    def test_validate_input_bad2(self):
        p = Prompter()
        self.assertEqual(None, p.validate_input('D1'))

    def test_validate_input_good1(self):
        p = Prompter()
        self.assertEqual((0,0), p.validate_input('A1'))

    def test_validate_input_good2(self):
        p = Prompter()
        self.assertEqual((0,2), p.validate_input('A3'))

    def test_validate_input_good3(self):
        p = Prompter()
        self.assertEqual((1,0), p.validate_input('B1'))

    def test_validate_input_good4(self):
        p = Prompter()
        self.assertEqual((1,2), p.validate_input('B3'))

    def test_validate_input_good6(self):
        p = Prompter()
        self.assertEqual((2,0), p.validate_input('C1'))

    def test_validate_input_good6(self):
        p = Prompter()
        self.assertEqual((2,2), p.validate_input('C3'))

    @patch('ticktacktoe.Prompter.get_input')
    @patch('ticktacktoe.Prompter.validate_input')
    def test_prompt_first_attempt_ok(self, m_vi, m_gi):
        p = Prompter()
        player = Mock(name='name')
        m_gi.return_value = 'a1'
        m_vi.return_value = (0, 0)
        self.assertEqual((0, 0), p.prompt(player))
        m_gi.assert_called_once_with(player)
        m_vi.assert_called_once_with('a1')

    @patch('ticktacktoe.Prompter.get_input')
    @patch('ticktacktoe.Prompter.validate_input')
    def test_prompt_first_attempt_ok(self, m_vi, m_gi):
        p = Prompter()
        player = Mock(name='name')
        m_gi.return_value = 'get_input'
        m_vi.side_effect = [None, (0, 0)]
        self.assertEqual((0, 0), p.prompt(player))
        self.assertEqual(2, len(m_vi.call_args_list))



from pymysql import NULL
from gameServer.utils import generate_error_reply_JSON, generate_success_reply_JSON, validate_card_serial_number
import unittest


class TestGenerateSuccessReplyJSON(unittest.TestCase):
    def test_generate_success_reply_JSON(self):
        self.assertEqual(generate_success_reply_JSON(), '{"success": 1}')


class TestGenerateErrorReplyJSON(unittest.TestCase):
    def test_generate_error_reply_JSON(self):
        self.assertEqual(generate_error_reply_JSON("reply message"), '{"success": 0, "desc": "reply message"}')
        self.assertEqual(generate_error_reply_JSON(""), '{"success": 0, "desc": ""}')

class ValidateCardSerialNumber(unittest.TestCase):
    def test_validate_card_serial_number(self):
        self.assertEqual(validate_card_serial_number("zdfgg00001233412"), None)
        self.assertEqual(validate_card_serial_number("zdfgg0000123adsdas34234234234234243412"), "Serial number is too long (max is 20 chars)")
        self.assertEqual(validate_card_serial_number(""), "Serial number can't be empty and has to be a string")
        self.assertEqual(validate_card_serial_number(None), "Serial number can't be empty and has to be a string")


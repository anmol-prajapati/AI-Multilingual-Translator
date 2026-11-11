"""Tests for the logic that does NOT need the model (validation, script check, splitting).
Run from the project folder:  python -m unittest discover tests -v
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import translator  # noqa: E402


class TestValidation(unittest.TestCase):
    def test_empty(self):
        with self.assertRaises(ValueError):
            translator.validate_input("   ", "en", "hi")

    def test_same_language(self):
        with self.assertRaises(ValueError):
            translator.validate_input("Hello", "en", "en")

    def test_english_samples(self):
        for t in ["Hello, how are you?", "India is a beautiful country."]:
            self.assertEqual(translator.validate_input(t, "en", "hi"), t)

    def test_hindi_samples(self):
        for t in ["मेरा नाम अनमोल है।", "आप कैसे हैं?"]:
            self.assertEqual(translator.validate_input(t, "hi", "en"), t)

    def test_wrong_script(self):
        with self.assertRaises(ValueError):
            translator.validate_input("आप कैसे हैं?", "en", "hi")
        with self.assertRaises(ValueError):
            translator.validate_input("Hello", "hi", "en")

    def test_too_long(self):
        with self.assertRaises(ValueError):
            translator.validate_input("a" * 2001, "en", "hi")

    def test_split(self):
        self.assertEqual(translator.split_sentences("Hi. How are you?"), ["Hi.", "How are you?"])
        self.assertEqual(len(translator.split_sentences("नमस्ते। आप कैसे हैं?")), 2)


if __name__ == "__main__":
    unittest.main()

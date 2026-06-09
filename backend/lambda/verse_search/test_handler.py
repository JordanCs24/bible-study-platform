import unittest
from handler import normalize_query, parse_verse_reference

class TestNormalizeQuery(unittest.TestCase):
    
    def test_strips_whitespace(self):
        self.assertEqual(normalize_query("  john 3:16  "), "John 3:16")
    
    def test_handles_caps(self):
        self.assertEqual(normalize_query("JOHN 3:16"), "John 3:16")
    
    def test_handles_missing_space(self):
        self.assertEqual(normalize_query("john3:16"), "John 3:16")
    
    def test_handles_number_prefix(self):
        self.assertEqual(normalize_query("1chronicles 3:5"), "1 Chronicles 3:5")

class TestParseVerseReference(unittest.TestCase):

    def test_single_verse(self):
        result = parse_verse_reference("John 3:16")
        self.assertEqual(result['book'], 'John')
        self.assertEqual(result['chapter'], '3')
        self.assertEqual(result['verse_start'], '16')
        self.assertEqual(result['type'], 'single_verse')

    def test_verse_range(self):
        result = parse_verse_reference("John 3:16-20")
        self.assertEqual(result['book'], 'John')
        self.assertEqual(result['chapter'], '3')
        self.assertEqual(result['verse_start'], '16')
        self.assertEqual(result['verse_end'], '20')
        self.assertEqual(result['type'], 'range')

    def test_whole_chapter(self):
        result = parse_verse_reference("John 3")
        self.assertEqual(result['book'], 'John')
        self.assertEqual(result['chapter'], '3')
        self.assertEqual(result['type'], 'chapter')

    def test_number_prefix_book(self):
        result = parse_verse_reference("1 John 3:16")
        self.assertEqual(result['book'], '1 John')
        self.assertEqual(result['chapter'], '3')
        self.assertEqual(result['verse_start'], '16')

if __name__ == '__main__':
    unittest.main()
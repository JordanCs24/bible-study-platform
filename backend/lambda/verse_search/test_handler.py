import unittest
from handler import normalize_query, parse_verse_reference, get_verse_from_s3

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
        
class TestS3Lookup(unittest.TestCase):

    def test_john_3_16(self):
        print("TESTING John 3:16\n")
        parsed = parse_verse_reference("John 3:16")
        result = get_verse_from_s3(parsed)
        print(result)
        print('\n\n')
        self.assertEqual(result['statusCode'], 200)
        
    def test_john_3_16_20(self):
        print("TESTING John 3:16-20\n")
        parsed = parse_verse_reference("John 3:16-20")
        result = get_verse_from_s3(parsed)
        print(result)
        print('\n\n')
        self.assertEqual(result['statusCode'], 200)
    
    def test_john_3(self):
        print("TESTING John 3\n")
        parsed = parse_verse_reference("John 3")
        result = get_verse_from_s3(parsed)
        print(result)
        print('\n\n')
        self.assertEqual(result['statusCode'], 200)
    
    def test_jonh_3(self):
        print("TESTING Jonh 3\n")
        parsed = parse_verse_reference("Jonh 3")
        result = get_verse_from_s3(parsed)
        print(result)
        print('\n\n')
        self.assertEqual(result['statusCode'], 404)
        
    def test_john_3(self):
        print("TESTING Chronicals 3:13\n")
        parsed = parse_verse_reference("Chronicals 3:13")
        result = get_verse_from_s3(parsed)
        print(result)
        print('\n\n')
        self.assertEqual(result['statusCode'], 404)

if __name__ == '__main__':
    unittest.main()
    
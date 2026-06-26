import json
import os

RAW_FOLDER = "./data/Bible-kjv"


BOOK_ORDER = [
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy",
    "Joshua", "Judges", "Ruth", "1 Samuel", "2 Samuel",
    "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles", "Ezra",
    "Nehemiah", "Esther", "Job", "Psalms", "Proverbs",
    "Ecclesiastes", "Song of Solomon", "Isaiah", "Jeremiah", "Lamentations",
    "Ezekiel", "Daniel", "Hosea", "Joel", "Amos",
    "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk",
    "Zephaniah", "Haggai", "Zechariah", "Malachi",
    "Matthew", "Mark", "Luke", "John", "Acts",
    "Romans", "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians",
    "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians", "1 Timothy",
    "2 Timothy", "Titus", "Philemon", "Hebrews", "James",
    "1 Peter", "2 Peter", "1 John", "2 John", "3 John",
    "Jude", "Revelation"
]

def book_name_to_filename(book_name):
    return book_name.replace(" ", "") + ".json"


book_id_lookup = {book_name: index + 1 for index, book_name in enumerate(BOOK_ORDER)}

#" For every book 0 to 65 (covers 66 books), go into the given book and access the chapters, 
# retrieve it, then verses, then retrieve every verse in the verses array. 
# Given each variable respectfully we will put the data into the file 
# then we will do it over again. "

with open("verses.jsonl", "w", encoding="utf-8") as output_file:
    # loop through all 66 books here
    for book in BOOK_ORDER:
        book_file = book_name_to_filename(book)
        # inside the loop: read each book's file, then loop chapters, then loop verses, then write each verse
        filepath = os.path.join(RAW_FOLDER, book_file)
        with open(filepath, "r", encoding="utf-8") as f:
            book_data = json.load(f)
            chapters = book_data['chapters']
            for chapter in chapters:    # loops through each chapter object
                verses = chapter['verses']
                for verse in verses:       # loops through each verse object inside the current chapter
                    # here, you have access to:
                    #   chapter["chapter"]   (the chapter number, as a string)
                    #   verse["verse"]       (the verse number, as a string)
                    #   verse["text"]        (the verse text)
                    record = {
                        "book_id": book_id_lookup[book],
                        "book": book,
                        "chapter": int(chapter["chapter"]),
                        "verse": int(verse["verse"]),
                        "text": verse["text"]
                    }
                    output_file.write(json.dumps(record) + "\n")
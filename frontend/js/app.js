const BOOKS = {
  oldTestament: [
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy",
    "Joshua", "Judges", "Ruth", "1 Samuel", "2 Samuel",
    "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles", "Ezra",
    "Nehemiah", "Esther", "Job", "Psalms", "Proverbs",
    "Ecclesiastes", "Song of Solomon", "Isaiah", "Jeremiah", "Lamentations",
    "Ezekiel", "Daniel", "Hosea", "Joel", "Amos",
    "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk",
    "Zephaniah", "Haggai", "Zechariah", "Malachi"
  ],
  newTestament: [
    "Matthew", "Mark", "Luke", "John", "Acts",
    "Romans", "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians",
    "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians", "1 Timothy",
    "2 Timothy", "Titus", "Philemon", "Hebrews", "James",
    "1 Peter", "2 Peter", "1 John", "2 John", "3 John",
    "Jude", "Revelation"
  ]
};

let currentTranslation = "kjv";

function setTranslation(translation) {
  currentTranslation = translation;
  document.getElementById("btn-kjv").classList.remove("active");
  document.getElementById("btn-web").classList.remove("active");
  document.getElementById("btn-" + translation).classList.add("active");
}

function handleSearch() {
  const query = document.getElementById("search-input").value.trim();
  if (!query) return;
  showResults([
    {
      reference: "John 3:16",
      text: "For God so loved the world, that he gave his only begotten Son..."
    }
  ]);
}

function showResults(verses) {
  const container = document.getElementById("results-container");
  if (verses.length === 0) {
    container.innerHTML = "<p class='placeholder-text'>No results found.</p>";
    return;
  }
  container.innerHTML = verses.map(verse => `
    <div class="verse-card">
      <div class="verse-reference">${verse.reference}</div>
      <div class="verse-text">${verse.text}</div>
    </div>
  `).join("");
}

function browseBook(book) {
  document.getElementById("search-input").value = book;
  handleSearch();
}

function buildBookButtons() {
  const oldDiv = document.getElementById("old-testament-books");
  const newDiv = document.getElementById("new-testament-books");

  BOOKS.oldTestament.forEach(book => {
    const btn = document.createElement("button");
    btn.className = "book-btn";
    btn.textContent = book;
    btn.onclick = () => browseBook(book);
    oldDiv.appendChild(btn);
  });

  BOOKS.newTestament.forEach(book => {
    const btn = document.createElement("button");
    btn.className = "book-btn";
    btn.textContent = book;
    btn.onclick = () => browseBook(book);
    newDiv.appendChild(btn);
  });
}

buildBookButtons();
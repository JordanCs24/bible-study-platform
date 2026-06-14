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

const API_URL = 'https://bx0ddxpgwl.execute-api.us-east-1.amazonaws.com'

let currentTranslation = "kjv";
let selectedBookBtn = null;

function setTranslation(translation) { // Sets the translation based on what the user wants
  currentTranslation = translation;
  document.getElementById("btn-kjv").classList.remove("active");
  document.getElementById("btn-web").classList.remove("active");
  document.getElementById("btn-" + translation).classList.add("active");
}
/**
 * if data.error → show error
  `else if data.text → single verse
  else if data.verses → range or chapter`
 */
function displayResults(data) {
  const container = document.getElementById("results-container");
  if (data.error) {
    container.innerHTML =`
    <div class="verse-card">
      <div class="verse-text">${data.error}</div>
    </div>
  `
  } else if (data.text) {
    container.innerHTML = `
    <div class="verse-card">
      <div class="verse-reference">${data.reference}</div>
      <div class="verse-text">${data.text}</div>
    </div>`;

  } else if (data.verses) {
    const verseText = data.verses.map(verse => `<sup class="verse-number">${verse.verse}</sup> ${verse.text} `).join("");
  
    container.innerHTML = `
      <div class="verse-card">
        <div class="verse-reference">${data.reference}</div>
        <div class="verse-text">${verseText}</div>
      </div>
    `;
  }
}

async function handleSearch() {
  const query = document.getElementById("search-input").value.trim();
  if (!query) return;
  
  // show the user something is happening
  document.getElementById("results-container").innerHTML = 
    "<p class='placeholder-text'>Searching...</p>";
  
  try {
    const response = await fetch(`${API_URL}/search?q=${encodeURIComponent(query)}`);
    const data = await response.json();
    displayResults(data);
  } catch (error) {
    document.getElementById("results-container").innerHTML = 
      "<p class='placeholder-text'>Something went wrong. Please try again.</p>";
  }
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

function browseBook(book,btnElement) {
    console.log("book:", book, "btnElement:", btnElement);
    if (selectedBookBtn) {
        selectedBookBtn.classList.remove("selected");
    }
    selectedBookBtn = btnElement;
    selectedBookBtn.classList.add("selected");
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
    btn.onclick = () => browseBook(book, btn);
    oldDiv.appendChild(btn);
  });

  BOOKS.newTestament.forEach(book => {
    const btn = document.createElement("button");
    btn.className = "book-btn";
    btn.textContent = book;
    btn.onclick = () => browseBook(book, btn);
    newDiv.appendChild(btn);
  });
}

buildBookButtons();
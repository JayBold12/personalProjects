from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox
)
import sys
import requests

#1A: Word look up
def ask_for_word() -> str:
    word = input("What word would you like to look for? ")
    return word

def check_word(word: str) -> bool:
    valid_word = word.isalpha()
    if not valid_word:
        return False
    else:
        return True

def get_word_data(word: str) -> dict:
    url = "https://wordsapiv1.p.rapidapi.com/words/" + word

    headers = {
        "x-rapidapi-key": "1fa7bdd31fmshd2a2a893ef40af8p16b589jsne6bf3037ff65",
        "x-rapidapi-host": "wordsapiv1.p.rapidapi.com"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # This will raise if status code is not 2xx
        data = response.json()
        return data
    except (requests.exceptions.RequestException):
        word_data_ERROR()

def invalid_word_ERROR():
    print("This is an invalid word")

def word_data_ERROR() -> str:
    print("Either the word is not in the database or the app failed obtain the word from the database")
    return

#1B: Definitions
def get_word(word_data: dict) -> str:
    word = word_data["word"]
    return word

def get_definitions(word: str):
    url = f"https://wordsapiv1.p.rapidapi.com/words/" + word + "/definitions"

    headers = {
        "x-rapidapi-key": "1fa7bdd31fmshd2a2a893ef40af8p16b589jsne6bf3037ff65",
        "x-rapidapi-host": "wordsapiv1.p.rapidapi.com"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # This will raise if status code is not 2xx
        data = response.json()["definitions"]
        return data
    except (requests.exceptions.RequestException):
        word_data_ERROR()

#1C: Pronunciations
#1D: Synonyms/ Antonymns
def get_synonyms(word: str) -> list:
    url = f"https://wordsapiv1.p.rapidapi.com/words/" + word + "/synonyms"

    headers = {
        "x-rapidapi-key": "1fa7bdd31fmshd2a2a893ef40af8p16b589jsne6bf3037ff65",
        "x-rapidapi-host": "wordsapiv1.p.rapidapi.com"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # This will raise if status code is not 2xx
        data = response.json()['synonyms']
        return data
    except (requests.exceptions.RequestException):
        word_data_ERROR()

def get_antonyms(word: str) -> list:
    url = f"https://wordsapiv1.p.rapidapi.com/words/" + word + "/antonyms"

    headers = {
        "x-rapidapi-key": "1fa7bdd31fmshd2a2a893ef40af8p16b589jsne6bf3037ff65",
        "x-rapidapi-host": "wordsapiv1.p.rapidapi.com"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # This will raise if status code is not 2xx
        data = response.json()['antonyms']
        return data
    except (requests.exceptions.RequestException):
        word_data_ERROR()
#1E: Word of the Day
#1F: Offline
#1G: Light/ Dark UI
#1H: Word usage
#1I: AI explain like I am five
#1J: Multilingual integrataion
#1K: Word origin
#1L: Word frequency
#1M: Notification

class DictionaryApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bold Dictionary")
        self.setGeometry(100, 100, 600, 400)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.word_input = QLineEdit()
        self.word_input.setPlaceholderText("Enter a word: ")
        layout.addWidget(self.word_input)

        self.search_btn = QPushButton("Search")
        self.search_btn.clicked.connect(self.search_word)
        layout.addWidget(self.search_btn)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        self.setLayout(layout)

    def search_word(self):
        word = self.word_input.text().strip().lower()

        if not word.isalpha():
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid word.")
            return
        
        word_data = get_word_data(word)
        if not word_data:
            QMessageBox.critical(self, "Error", "Word not found or API failed.")
            return
        
        definitions = get_definitions(word)
        synonyms = get_synonyms(word)
        antonyms = get_antonyms(word)

        self.output.clear()
        self.output.append(f"<h2>{word.capitalize()}</h2>")

        if definitions:
            self.output.append("<b>Definitions:</b>")
            for idx, d in enumerate(definitions, 1):
                self.output.append(f"{idx}. {d.get('definition', 'N/A')}")
        else:
            self.output.append("No definitions found.")

        if synonyms:
            self.output.append(f"<br><b>Synonyms:</b> {', '.join(synonyms)}")
        if antonyms:
            self.output.append(f"<br><b>Antonyms:</b> {', '.join(antonyms)}")

def main():
    app = QApplication(sys.argv)
    window = DictionaryApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

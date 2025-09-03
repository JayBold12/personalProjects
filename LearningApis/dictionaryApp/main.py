import requests

def partOfSpeechErrorCode(part:str) -> str:
    
    print(f"The {part} part of speech does not exist for this word")
    print("Try again with another part of speech: (noun, pronoun, verb, adjective, adverb, preposition, conjunction, interjection)")

def askForWord() -> str:
    word = input("What word would you like to search? ")
    return word

def askForPartOfSpeech() -> str:
    part = input("What part of speech? ")
    speechParts = {"noun", "pronoun", "verb", "adjective", "adverb", "prepostion", "conjunction", "interjection"}
    if part not in speechParts:
        partOfSpeechErrorCode(part)
    else:
        return part

def findDef(word:str, part:str) -> list:
    url = "https://api.dictionaryapi.dev/api/v2/entries/en/" + word
    response = requests.get(url)
        
    if response.status_code == 200:
        data = response.json()[0]["meanings"]
        finder = None
        for i in range(len(data)):
            if data[i]['partOfSpeech'] == part:
                finder = data[i]
                break
        if finder == None:
            partOfSpeechErrorCode(part)
        else:
            definitions = []
            for i in range(len(finder["definitions"])):
                definitions.append(finder["definitions"][i]["definition"])
            return(definitions)
    else:
        return("Failed to retrieve definition(s)")

def main():
    word = askForWord()
    part = askForPartOfSpeech()
    if part:
        definitions = findDef(word, part)
        if definitions != None:
            for i in range(len(definitions)):
                print(str(i+1) + ': ' + definitions[i])
    
if __name__ == "__main__":
    main()

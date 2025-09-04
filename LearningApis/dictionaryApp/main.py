import requests
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import io
import random
import exceptions

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

def getPhonetics(word: str):
    # Get the audio URL from the dictionary API
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)

    if response.status_code == 200:
        try:
            phonetics = response.json()[0]["phonetics"]
            audio_url = next((p["audio"] for p in phonetics if p.get("audio")), None)

            if audio_url:
                # Stream the audio into memory
                audio_response = requests.get(audio_url)
                if audio_response.status_code == 200:
                    audio_data = io.BytesIO(audio_response.content)

                    # Initialize pygame mixer
                    pygame.mixer.init()
                    pygame.init()

                    # Load music from memory and play
                    pygame.mixer.music.load(audio_data)
                    pygame.mixer.music.play()

                    # Keep script alive until playback finishes
                    while pygame.mixer.music.get_busy():
                        pygame.time.Clock().tick(10)
                else:
                    print("Failed to stream audio.")
            else:
                print("No audio URL found for this word.")
        except Exception as e:
            print("Error while processing audio:", e)
    else:
        print("Failed to retrieve phonetics")

def getSynonyms(word:str, part:str) -> list:
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
            synonyms = []
            for i in range(len(finder["definitions"])):
                synonyms.extend(finder["definitions"][i]["synonyms"])
            if len(synonyms) < 1:
                return []
            else:
                return(synonyms)
    else:
        return("Failed to retrieve synonymns(s)")
    
def getAntonyms(word:str, part:str) -> list:
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
            antonyms = []
            for i in range(len(finder["definitions"])):
                antonyms.extend(finder["definitions"][i]["antonyms"])
            if len(antonyms) < 1:
                return []
            else:
                return(antonyms)
    else:
        return("Failed to retrieve antonyms(s)")
        
def main():
    word = askForWord()
    part = askForPartOfSpeech()
    if part:
        definitions = findDef(word, part)
        if definitions != None:
            for i in range(len(definitions)):
                print(str(i+1) + ': ' + definitions[i])
        synonyms = getSynonyms(word, part)
        antonyms = getAntonyms(word, part)
    audio = getPhonetics(word)
    
if __name__ == "__main__":
    main()

import json
import requests
import os
from typing import Dict, List, Any
from constants import *
from decorators import *

def main():
    decks = get_decks()
    for deck in decks:
      translate_deck(deck)

def translate_deck(deck_path):
    with open(deck_path) as file:
        anki_json = json.load(file)
    list_of_notes : List[Dict[str, Any]] = anki_json["notes"]
    translate_notes(list_of_notes)
    save_json(anki_json, deck_path)

@run_in_threads
def translate_notes(notes):
    for note in notes:
      try:
          translate_note(note)
      except Exception as e:
          print_red(f"Error while translating {note['fields'][WORD]}" + e.__str__())

@note_logger
def translate_note(note: Dict[str, Any]):
    fields : List[str] = note["fields"]
    for key, value in MAPPINGS.items():
      if fields[value] == "" or OVERWRITE:
        fields[value] = translate_word(fields[key])

def remove_tags(text: str):
    return text.replace("<b>", "").replace("</b>", "")

def translate_word(word: str) -> str:
    url=f"{API_URL}{word}" 
    res = requests.get(url)
    if (res.status_code != 200): raise Exception(f"Error while translating {word}")
    data = res.json()
    return data[0][0][0]
    
def save_json(json_data, to = ANKI_DECK_NAME):
    print(f"Saving json to {to}")
    with open(to, 'w') as outfile:
        json.dump(json_data, outfile, indent=4, ensure_ascii=False)

def print_red(text):
    print(f"{RED_TEXT}{text}{RESET_TEXT_COLOR}")

def get_decks():
  decks = []
  for root, dirs, files in os.walk(f"anki cards/{ANKI_DECK_NAME}"):
    for file in files:
      if file.endswith(".json"):
        decks.append(os.path.join(root, file))
        if (ANKI_DECK_NAME != ""): break

  return decks

if __name__ == "__main__":
    main()

"""
-- json format --

{
  "__type__": string,
  "children": array,
  "crowdanki_uuid":string 
  "deck_config_uuid": string,
  deck_configurations: array,
  "desc": string,
  "dyn": integer,
  "extendNew": integer,
  "extendRev": integer,
  "media_files": array,
  "name": string,
  "newLimit": integer,
  "newLimitToday": integer,
  "note_models": array,
  "notes": [
        {
            "__type__": "Note",
            "fields": [
                "1000BEW_B01_U01_001", -- id
                "cry", -- word 
                "[krái]", -- pronunciation
                "v.", -- part of speech
                "to show sadness", -- definition
                "He <b>cries</b> when he is sad.", -- example
                "He {{c1::cries}} when he is sad.", -- cloze
                "<img src=\"1000BEW_B01_U01_001.webp\">", -- img
                "[sound:1000BEW_B01_U01_001.word.mp3]", -- sound word 
                "[sound:1000BEW_B01_U01_001.example.mp3]", --sound example
                "", -- word translation
                "Він плаче, коли йому сумно.", -- cloze translation
                "" -- question definition translation
            ],
            "guid": "M$:|1aI;)7",
            "note_model_uuid": "75f537fe-5c67-11ee-8412-e3d31f772a01",
            "tags": []
        },
  ],
  "reviewLimit": null,
  "reviewLimitToday": null
}
"""

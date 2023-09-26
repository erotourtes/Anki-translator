import json
import requests
from typing import Dict, List, Any
from constants import *
from decorators import *

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

def main():
  anki_json = json.load(open(ANKI_JSON_PATH))
  list_of_notes : List[Dict[str, Any]] = anki_json["notes"]
  list_of_notes = list_of_notes[:100]

  translate_notes(list_of_notes)
  save_json(anki_json)

@run_in_threads
def translate_notes(notes):
    for note in notes:
        if should_translate(note["fields"]):
            try:
                translate_note(note)
            except Exception as e:
                print_red(f"Error while translating {note['fields'][WORD]}" + e.__str__())
        else:
            print_red(f"Note {note['fields'][WORD]} is already translated")

@note_logger
def translate_note(note: Dict[str, Any]):
    fields : List[str] = note["fields"]
    fields[TRANSLATE_WORD] = translate_word(fields[WORD])
    fields[TRANSLATE_CLOZE] = translate_word(remove_tags(fields[EXAMPLE]))
    fields[TRANSLATE_DEFINITION] = translate_word(fields[DEFINITION])


def should_translate(fields: List[str]):
    return fields[TRANSLATE_WORD] == "" or fields[TRANSLATE_CLOZE] == "" or fields[TRANSLATE_DEFINITION] == ""

def remove_tags(text: str):
    return text.replace("<b>", "").replace("</b>", "")

def translate_word(word: str) -> str:
    url=f"{API_URL}{word}" 
    res = requests.get(url)
    if (res.status_code != 200): raise Exception(f"Error while translating {word}")
    data = res.json()
    return data[0][0][0]
    
    
def save_json(json_data, to = ANKI_JSON_PATH):
    print(f"Saving json to {to}")
    with open(to, 'w') as outfile:
        json.dump(json_data, outfile, indent=4, ensure_ascii=False)

def print_red(text):
    print(f"{RED_TEXT}{text}{RESET_TEXT_COLOR}")

if __name__ == "__main__":
    main()

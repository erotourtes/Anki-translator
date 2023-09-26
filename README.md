# Anki deck translator
Use [CrowdAnki](https://ankiweb.net/shared/info/1788670778) for exporting decks as `JSON`

To configure the fields you want to translate, navigate to the `constants.py` and change the constants you need.

## Variables
- FROM_LANGUAGE = "en"
- TO_LANGUAGE = "uk"

- ANKI_DECK_NAME = ""
  > specify path to your anki deck  
    Example: ANKI_DECK_NAME = "1000_Basic_English_Words"  
    otherwise it will translate all the decks in the "anki cards" folder"  

- WORD = 1
  > specify the index of the field to translate in the json `fields` array
- TRANSLATE_WORD = 2
  > Specify the index of the field in which the translation will be placed in the json `fields` array.
- MAPPINGS = { WORD: TRANSLATE_WORD, }
  > Map your `WORD` and `TRANSLATE_WORD`  
  > Example: 
    ```json
    "notes": [
          ... 
          {
              "__type__": "Note",
              "fields": [
                  "1000BEW_B01_U01_001", -- id, index 0
                  "fun", -- WORD, index 1
                  "", -- TRANSLATE_WORD, index 2
              ],
              ...
          },
    ],
    ```

- OVERWRITE = False
  > to overwrite fields

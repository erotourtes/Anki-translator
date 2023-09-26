FROM_LANGUAGE = "en"
TO_LANGUAGE = "uk"

# specify path to your anki deck
# Example: ANKI_DECK_NAME = "1000_Basic_English_Words"
# otherwise it will translate all the decks in the "anki cards" folder"
ANKI_DECK_NAME = ""

WORD = 1                    # <-> TRANSLATE_WORD
DEFINITION = 4              # <-> TRANSLATE_DEFINITION
EXAMPLE = 5                 # <-> TRANSLATE_EXAMPLE
TRANSLATE_WORD = 10
TRANSLATE_EXAMPLE = 11
TRANSLATE_DEFINITION = 12

# redeclare this constant if you want to change the order of fields in your anki deck
MAPPINGS = {
  WORD: TRANSLATE_WORD,
  DEFINITION: TRANSLATE_DEFINITION,
  EXAMPLE: TRANSLATE_EXAMPLE,
}

OVERWRITE = False


################# DON'T RECOMMENDED TO CHANGE #################

NUMBER_OF_THREADS = 10

RED_TEXT = "\033[91m"
RESET_TEXT_COLOR = "\033[0m"

API_URL=f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={FROM_LANGUAGE}&tl={TO_LANGUAGE}&dt=t&q="

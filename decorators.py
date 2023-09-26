import threading
from constants import NUMBER_OF_THREADS, WORD

def run_in_threads(func):
    def wrapper(*args, **kwargs):
        list_of_notes = args[0]
        chunk_size = len(list_of_notes) // NUMBER_OF_THREADS

        threads = []
        for i in range(NUMBER_OF_THREADS):
            start = i * chunk_size
            end = start + chunk_size
            if i == NUMBER_OF_THREADS - 1:
              end = len(list_of_notes)

            slice = list_of_notes[start:end]
            t = threading.Thread(target=func, args=(slice,))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
    return wrapper

def note_logger(func):
    def wrapper(*args, **kwargs):
        fields = args[0]['fields']
        word = fields[WORD]
        print(f"Translating {word}")
        func(*args, **kwargs)
        print(f"END of translating {word}")
    return wrapper

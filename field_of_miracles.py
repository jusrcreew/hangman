"""Функции и глобальное состояние игры «Виселица на поле чудес».

Вся работа с консолью, файлами, сравнениями и литералами живёт здесь;
main.py только управляет ходом игры, вызывая эти функции.
"""

import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
WORDS_FILE = BASE_DIR / "data" / "words.txt"
GALLOWS_DIR = BASE_DIR / "gallows"
GALLOWS_PATTERN = "stage_*.txt"

ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
HIDDEN_MARK = "■"
YES_ANSWERS = ("д", "да", "y", "yes")

DRUM_SECTORS = (100, 150, 200, 250, 300, 350, 400, 500, 600, 750, 1000, "Банкрот")
BANKRUPT = "Банкрот"

WORDS = []
UNUSED_WORDS = []

SECRET = ""
DESCRIPTION = ""
OPENED = set()
USED = []
MISTAKES = 0
MAX_MISTAKES = 0
SCORE = 0
SECTOR = 0
PLAYING = True


def normalize(text):
    return text.strip().lower().replace("ё", "е")


def load_words():
    """Читает словарь «слово: описание» из data/words.txt."""
    WORDS.clear()
    with open(WORDS_FILE, encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#") or ":" not in line:
                continue
            word, description = line.split(":", 1)
            WORDS.append((normalize(word), description.strip()))
    if not WORDS:
        raise SystemExit(f"В файле {WORDS_FILE} нет ни одного слова.")


def gallows_files():
    return sorted(GALLOWS_DIR.glob(GALLOWS_PATTERN))


def greet():
    print("=" * 50)
    print("  ВИСЕЛИЦА НА ПОЛЕ ЧУДЕС")
    print("=" * 50)
    print("Крутите барабан и называйте буквы.")
    print("Можно назвать слово целиком — но за ошибку достроят виселицу.")
    print(f"Ошибок до проигрыша: {len(gallows_files())}.")


def session_active():
    return PLAYING


def pick_word():
    if not UNUSED_WORDS:
        UNUSED_WORDS.extend(WORDS)
        random.shuffle(UNUSED_WORDS)
    return UNUSED_WORDS.pop()


def start_round():
    global SECRET, DESCRIPTION, MISTAKES, MAX_MISTAKES, SCORE
    SECRET, DESCRIPTION = pick_word()
    OPENED.clear()
    USED.clear()
    MISTAKES = 0
    MAX_MISTAKES = len(gallows_files())
    SCORE = 0
    print()
    print("-" * 50)
    print(f"Новый раунд! Задание: {DESCRIPTION}")
    print(f"В слове {len(SECRET)} букв.")


def is_won():
    return set(SECRET) <= OPENED


def is_lost():
    return MISTAKES >= MAX_MISTAKES


def round_continues():
    return not is_won() and not is_lost()


def masked_word():
    return " ".join(letter if letter in OPENED else HIDDEN_MARK for letter in SECRET)


def show_board():
    print()
    print(f"Слово:  {masked_word()}")
    print(f"Задание: {DESCRIPTION}")
    print(f"Очки: {SCORE}   Ошибки: {MISTAKES}/{MAX_MISTAKES}")
    if USED:
        print(f"Уже называли: {', '.join(USED)}")


def spin_drum():
    global SECTOR
    SECTOR = random.choice(DRUM_SECTORS)
    input("Нажмите Enter, чтобы крутить барабан...")
    if drum_is_bankrupt():
        print("Барабан остановился на секторе «Банкрот»!")
    else:
        print(f"Сектор {SECTOR} на барабане!")


def drum_is_bankrupt():
    return SECTOR == BANKRUPT


def go_bankrupt():
    global SCORE
    SCORE = 0
    print("Все очки сгорели. Крутите барабан ещё раз.")


def ask_answer():
    return normalize(input("Ваша буква или слово целиком: "))


def is_invalid(answer):
    return not answer or any(char not in ALPHABET for char in answer)


def report_invalid(answer):
    if not answer:
        print("Вы ничего не ввели.")
    else:
        print(f"«{answer}» — это не русская буква и не слово. Попробуйте ещё раз.")


def is_already_used(answer):
    return answer in USED


def report_already_used(answer):
    print(f"«{answer}» уже называли. Выберите другое.")


def is_word_attempt(answer):
    return len(answer) > 1


def is_correct_word(answer):
    return answer == SECRET


def open_whole_word():
    global SCORE
    hidden = set(SECRET) - OPENED
    OPENED.update(SECRET)
    SCORE += SECTOR * len(hidden)


def report_word_guessed():
    print(f"Абсолютно верно! Это слово «{SECRET.upper()}»!")


def letter_in_word(letter):
    return letter in SECRET


def open_letter(letter):
    global SCORE
    USED.append(letter)
    OPENED.add(letter)
    SCORE += SECTOR * SECRET.count(letter)


def report_hit(letter):
    count = SECRET.count(letter)
    print(f"Есть такая буква! «{letter.upper()}» встречается {count} раз(а). "
          f"+{SECTOR * count} очков.")


def register_miss(answer):
    global MISTAKES
    USED.append(answer)
    MISTAKES += 1


def report_miss(letter):
    print(f"Нет такой буквы «{letter.upper()}»!")


def report_wrong_word(answer):
    print(f"Нет, это не «{answer.upper()}».")


def draw_gallows():
    """Отрисовывает фрагмент виселицы, соответствующий числу ошибок."""
    stage_file = gallows_files()[MISTAKES - 1]
    print(stage_file.read_text(encoding="utf-8"))


def report_win():
    print()
    print(f"Слово:  {masked_word()}")
    print(f"ПОБЕДА! Вы отгадали слово «{SECRET.upper()}» и набрали {SCORE} очков!")


def report_loss():
    print(f"Вы проиграли. Загаданное слово: «{SECRET.upper()}».")


def ask_play_again():
    global PLAYING
    PLAYING = normalize(input("Сыграем ещё раз? (д/н): ")) in YES_ANSWERS


def say_goodbye():
    print("Спасибо за игру! До встречи на Поле чудес!")
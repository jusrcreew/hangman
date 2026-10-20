import field_of_miracles as fm

fm.load_words()
fm.greet()

while fm.session_active():
    fm.start_round()

    while fm.round_continues():
        fm.show_board()
        fm.spin_drum()

        if fm.drum_is_bankrupt():
            fm.go_bankrupt()
            continue

        answer = fm.ask_answer()

        if fm.is_invalid(answer):
            fm.report_invalid(answer)
        elif fm.is_already_used(answer):
            fm.report_already_used(answer)
        elif fm.is_word_attempt(answer):
            if fm.is_correct_word(answer):
                fm.open_whole_word()
                fm.report_word_guessed()
            else:
                fm.register_miss(answer)
                fm.report_wrong_word(answer)
                fm.draw_gallows()
        elif fm.letter_in_word(answer):
            fm.open_letter(answer)
            fm.report_hit(answer)
        else:
            fm.register_miss(answer)
            fm.report_miss(answer)
            fm.draw_gallows()

    if fm.is_won():
        fm.report_win()
    else:
        fm.report_loss()

    fm.ask_play_again()

fm.say_goodbye()
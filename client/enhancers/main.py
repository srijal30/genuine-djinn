from message_processer import AutoCorrecter, AutoTranslater

if __name__ == "__main__":
    m = AutoTranslater()
    m.add_new_message("Hello, world! How are you?")
    m.add_new_message("I dropped my spaghetti.")
    m.add_new_message("Linux is better than Windows and Mac.")
    print(m.messages)
    print(m.translated_messages)

    c = AutoCorrecter()
    text = (
        "In Greek mythology, Python was the serpent, sometimes represented as a medieval-style dragon, "
        "living at the center of the earth, believed by the ancient Greeks to be at Delphi."
    )
    autocorrected_entities_message = c.autocorrect_entities(text)
    autocorrected_string_message = c.autocorrect_string(text)
    print("Sending message: ", text)
    print("Autocorrected entities: ", autocorrected_entities_message)
    print("Autocorrected string: ", autocorrected_string_message)

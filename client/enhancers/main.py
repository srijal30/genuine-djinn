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
    autocorrected_message = c.autocorrect(text)
    print("Sending message: ", text)
    print("Autocorrected: ", autocorrected_message)

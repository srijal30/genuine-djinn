from message_processer import MessageProcesser

if __name__ == "__main__":
    m = MessageProcesser()
    m.add_new_message("Hello, world! How are you?")
    m.add_new_message("I dropped my spaghetti.")
    m.add_new_message("Linux is better than Windows and Mac.")
    print(m.messages)
    print(m.translations)



class Message:
    def __init__(self, prefix):
        self.text = prefix

    def set_text(self, text):
        return self.text + text


def danger_message(text):
    message = Message('🔴 ')
    print(message.set_text(text))


def info_message(text):
    message = Message('🔵 ')
    print(message.set_text(text))


def warning_message(text):
    message = Message('🟡 ')
    print(message.set_text(text))


def success_message(text):
    message = Message('🟢 ')
    print(message.set_text(text))

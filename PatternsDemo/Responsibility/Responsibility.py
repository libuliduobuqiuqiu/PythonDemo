# -*- coding: utf-8 -*-
# 责任链模式

class Event:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Widget:
    def __init__(self, parent=None):
        self.parent = parent

    def handle(self, event):
        method_name = f"handle_{event}"

        if hasattr(self, method_name):
            method = getattr(self, method_name)
            method(event)
        elif self.parent:
            self.parent.handle(event)
        elif hasattr(self, "handle_default"):
            self.handle_default(event)


class MainWindow(Widget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def handle_close(self, event):
        print(f"MainWindow: {event}")

    def handle_default(self, event):
        print(f"MainWindow: Default {event}")


class SendDialog(Widget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def handle_paint(self, event):
        print(f"SendDialog: {event}")


class MsgText(Widget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def handle_down(self, event):
        print(f"MsgText: {event}")


if __name__ == "__main__":
    md = MainWindow()
    sd = SendDialog(md)
    msg = MsgText(sd)

    for e in ("close", "paint", "down"):
        event = Event(e)
        print('\nSending event -{}- to MainWindow'.format(event))
        md.handle(event)
        print('Sending event -{}- to SendDialog'.format(event))
        sd.handle(event)
        print('Sending event -{}- to MsgText'.format(event))
        msg.handle(event)
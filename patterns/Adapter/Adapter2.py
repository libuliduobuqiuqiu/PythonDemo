# -*- coding: utf-8 -*-
# 适配器模式

class Computer:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"I'm a {self.name} computer."

    def execute(self):
        return "Execute a program"


class Human:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"My name is {self.name}"

    def speak(self):
        return "Speak loudly."


class Synthesizer:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"I am a {self.name} synthesizer."

    def play(self):
        return "Play a game"


class HumanAdapter(Human):
    def __init__(self, name):
        """通过继承方式实现适配器模式"""
        super().__init__(name)

    def execute(self):
        return self.speak()


class SynthesizerAdapter(Synthesizer):
    def __init__(self, name):
        """通过继承方式实现适配器模式"""
        super().__init__(name)

    def execute(self):
        return self.play()


if __name__ == "__main__":
    objs = [Computer("XiaoMi"), HumanAdapter("Leijun"), SynthesizerAdapter("Synthe")]

    for obj in objs:
        print(f"{str(obj)}:{obj.execute()}")
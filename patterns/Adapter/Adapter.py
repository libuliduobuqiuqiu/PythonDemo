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


class Adapter:
    def __init__(self, obj, adapter_method):
        # 使用__dict__属性，实现适配器模式
        self.obj = obj
        self.__dict__.update(adapter_method)

    def __str__(self):
        return str(self.obj)


if __name__ == "__main__":
    objs = [Computer("XiaoMi")]
    man = Human("Leijun")
    synth = Synthesizer("Synth")

    # 统一使用execute适配不同对象的方法，这样可以在不修改原有对象的基础上扩展功能
    m_adapter = Adapter(man, {"execute": man.speak})
    s_adapter = Adapter(synth, {"execute": synth.play})
    objs.append(m_adapter)
    objs.append(s_adapter)

    for obj in objs:
        print(f"{str(obj)}:{obj.execute()}")

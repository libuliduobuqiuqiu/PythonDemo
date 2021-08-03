# -*- coding: utf-8 -*-
# 建造者模式
import uuid


class Computer:
    def __init__(self, serial):
        self.serial = serial

        self.cpu = None
        self.mem = None
        self.disk = None
        self.system = None

    def __str__(self):
        computer_info = f"Serial: {self.serial}, Cpu: {self.cpu}, Mem: {self.mem}, " \
                        f"Disk: {self.disk}, System: {self.system}."
        return computer_info


class ComputerBuilder:
    def __init__(self):
        random_uuid = uuid.uuid1()
        self.computer = Computer(random_uuid)

    def set_cpu(self, cpu_info):
        self.computer.cpu = cpu_info

    def set_mem(self, mem_info):
        self.computer.mem = mem_info

    def set_disk(self, disk_info):
        self.computer.disk = disk_info

    def set_system(self, system_info):
        self.computer.system = system_info


class HardwareEngineer:
    def __init__(self):
        self.builder = None

    def construct_builder(self, cpu_info, mem_info, disk_info, system_info):
        self.builder = ComputerBuilder()
        construct_step = (self.builder.set_cpu(cpu_info),
                          self.builder.set_mem(mem_info),
                          self.builder.set_disk(disk_info),
                          self.builder.set_system(system_info))
        [step for step in construct_step]

    @property
    def computer(self):
        print(self.builder.computer)


if __name__ == "__main__":
    computer_info = ("Intel xen", "8 GB", "128GB SSD", "Linux 2.4")
    enginner = HardwareEngineer()
    enginner.construct_builder(*computer_info)
    enginner.computer
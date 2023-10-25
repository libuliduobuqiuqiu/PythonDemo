# -*- coding: utf-8 -*-

from netmiko import ConnectHandler, ssh_dispatcher


def connect_device(host: str, username: str, password: str, cmd: str) -> str:
    device_info = {
        "device_type": "autodetect",
        "host": host,
        "username": username,
        "password": password,
        "port": 22
    }
    print(device_info)
    device_connector = ConnectHandler(**device_info)
    output = device_connector.send_command(cmd)
    return output


if __name__ == "__main__":
    from setting import HOST, USERNAME, PASSWORD
    output = connect_device(HOST, USERNAME, PASSWORD, "df -h")
    print(output)

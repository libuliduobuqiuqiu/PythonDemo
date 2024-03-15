# -*- coding: utf-8 -*-

from paramiko import AutoAddPolicy

import paramiko

# from setting import F5_USERNAME, F5_PASSWORD


class F5Client:
    def __init__(self, host: str, username: str, password: str):
        self._host = host
        self._username = username
        self._password = password

        self._client = None
        self._sftp_client = None

    def __del__(self):
        if self._sftp_client:
            self._sftp_client.close()

        if self._client:
            self._client.close()

    def open(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())
        # 连接服务器
        client.connect(
            hostname=self._host,
            port=22,
            username=self._username,
            password=self._password,
        )
        self._client = client

    def open_sftp(self):
        if not self._client:
            self.open()

        if self._client:
            sftp_client = paramiko.SFTPClient.from_transport(
                self._client.get_transport()
            )
            self._client.open_sftp()
            self._sftp_client = sftp_client

    def put(self, local_path: str, remote_path: str):
        try:
            if self._sftp_client:
                self._sftp_client.put(local_path, remote_path)
            else:
                raise Exception("未打开SFTP通道")

        except Exception as e:
            raise Exception(f"SFTP连接传输文件失败:{str(e)}")

    def send_command(self, cmd: str):
        stdin, stdout, stderr = self._client.exec_command(command=cmd)
        out = stdout.read()

        if not out:
            err = stderr.read()
            return "", str(err, encoding="utf-8")
        else:
            return str(out, encoding="utf-8"), ""


if __name__ == "__main__":
    import re

    with open("D://vlan.txt", "r") as f:
        content = f.read()

    regex = "net vlan (\S+) {\s*?interfaces {([\s\S]*?)}\s*?}"
    vlan_list = re.findall(regex, content)

    for vlan_item in vlan_list:
        vlan_name = vlan_item[0]
        vlan_interfaces = vlan_item[1]

        regex = "(\S+) {"
        interfaces = re.findall(regex, vlan_interfaces)
        print(vlan_name, interfaces)

    with open("D://trunk.txt", "r") as f:
        trunk_content = f.read()

    regex = "net trunk (\S+) {\s*?interfaces {([\s\S]*?)}\s*?}"
    trunk_list = re.findall(regex, trunk_content)

    for trunk_item in trunk_list:
        trunk_name = trunk_item[0]
        trunk_interfaces = trunk_item[1]

        interfaces = trunk_interfaces.split()
        print(trunk_name, interfaces)

    # client.open_sftp()

    # crt_name = "wl2_123456.crt"
    # key_name = "wl2_123456.key"
    # remote_path = "/config/filestore/files_d/Common_d/certificate_d/"
    # local_path1 = "D:\\wl2_123456.key"
    # local_path2 = "D:\\wl2_123456.key"
    # client.put(local_path1, remote_path+crt_name)
    # client.put(local_path2, remote_path+key_name)

    # crt_cmd = f"tmsh create sys file ssl-cert wl2_123456 source-path file:{remote_path+crt_name}"
    # key_cmd = f"tmsh create sys file ssl-key wl2_123456 source-path file:{remote_path+key_name}"
    # client.send_command(crt_cmd)
    # client.send_command(key_cmd)

    # crt_name = "wl2_123456"
    # key_name = "wl2_123456"
    # profile_name = "all.ccuat.cmbchina.cn_client"
    # profile_cmd = "tmsh create ltm profile client-ssl %s { key %s cert %s passphrase 123456}" % (profile_name, key_name, crt_name)
    # print(client.send_command(profile_cmd))

    # print(client.send_command(f"tmsh list ltm profile client-ssl {profile_name}"))

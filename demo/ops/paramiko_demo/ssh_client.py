# -*- coding: utf-8 -*-

from paramiko import SSHClient, SFTPClient, Transport
from paramiko import AutoAddPolicy


def connect_server_by_sshclient(hostname: str, username: str, password: str, port=22):
    with SSHClient() as client:
        client.set_missing_host_key_policy(AutoAddPolicy())
        # 连接服务器
        client.connect(
            hostname=hostname, port=port, username=username, password=password
        )

        command = "df -h"
        stdin, stdout, stderr = client.exec_command(command)
        result = stdout.read()
        print(result.decode("utf8"))


def connect_server_by_transport(hostname: str, username: str, password: str, port=22):
    with Transport((hostname, port)) as transport:
        transport.connect(username=username, password=password)

        ssh_client = SSHClient()
        ssh_client._transport = transport
        command = "free -m"
        stdin, stdout, stderr = ssh_client.exec_command(command)

        result = stdout.read()
        print(result.decode("utf8"))

        sftp_client = SFTPClient.from_transport(transport)
        locate_path = "C:\\test.txt"
        remote_path = "/root/test.txt"
        sftp_client.put(locate_path, remote_path)

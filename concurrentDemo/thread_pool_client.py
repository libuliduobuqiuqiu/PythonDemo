# coding: utf-8
"""
    :date: 2023-10-24
    :author: linshukai
    :description: About Thread Pool Socket Client
"""
import concurrent.futures
from socket import AF_INET, SOCK_STREAM, socket
from concurrent.futures import ThreadPoolExecutor
import random
import string
import time


def multi_thread_client(address):

    random_string = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(30))
    print("Send: ", random_string)
    client = socket(AF_INET, SOCK_STREAM)
    client.connect(address)
    time.sleep(random.randint(0, 10))

    client.send(random_string.encode('ascii'))
    msg = client.recv(8192)
    print("Got From:", msg)


if __name__ == "__main__":

    with ThreadPoolExecutor(128) as executor:
        all_task = [executor.submit(multi_thread_client, ("localhost", 8992)) for _ in range(10)]

    concurrent.futures.wait(all_task)
    print("end...")

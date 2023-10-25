# coding: utf-8
"""
    :date: 2023-10-25
    :author: linshukai
    :description: About Argparse Demo
"""

import argparse
import getpass
import os


def search_files(dir_name, o_files):
    all_files = [filename for filename in os.listdir(dir_name) if os.path.isfile(os.path.join(dir_name, filename))]

    with open(o_files, "w+") as f:
        for file in all_files:
            f.write(os.path.join(dir_name, file) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find All Files of Directory.")

    parser.add_argument("-d", dest="dirname", metavar="DirectoryName", help="Search Directory Path", action="store")
    parser.add_argument("-o", dest="outfile", metavar="OutFile", help="Output File Path", action="store")

    args = parser.parse_args()
    print(args.dirname)
    print(args.outfile)

    user = input("Enter your username:")
    passwd = getpass.getpass()
    getpass.getuser()
    print(user,passwd)
    if user == 'root' and passwd == 'root':
        search_files(args.dirname, args.outfile)
        exit(0)

    print("login failed")

from bigsuds import BIGIP


if __name__ == "__main__":
    user = "admin"
    passwd = "admin"
    mip = "10.21.21.4"
    client = BIGIP(mip, user, passwd)
    view_info = client.Management.View.get_list()
    print(view_info)
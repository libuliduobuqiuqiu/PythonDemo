## 前言
>   在日常自动化运维场景，经常需要和Linux环境的设备连接进行交互操作，比如采集特定的系统信息，设备健康状况，后台进程任务等。根据目前现在开发工作场景，实际主要使用到paramiko，netmiko，napalm这三种模块。  
这几种模块可以构建成自动化运维框架底层设备交互层，从这篇文章从paramiko模块开始，将花费三篇文章梳理这三者之间的关联，以及适用于哪些不同的业务场景等问题；


## Paramiko

**适用场景**
> paramiko模块遵循SSH2协议纯Python实现的，提供客户端和服务器功能。日常主要通过ssh客户端连接设备，运行远程的shell命令或传输文件等；  

**核心功能**
> paramiko包含两个核心组件：SSHClient和SFTPClient，SSHClient可以方便进行SSH远程连接，SFTPClient通过SFTP协议进行SFTP文件传输；

**远程连接方式：**
1. 基于用户名密码连接；
2. 基于公钥密钥连接；

### SSHClient
> SSHClient的作用类似于Linux的ssh命令，是对SSH会话的封装，该类封装了传输（Transport），通道（Channel）及SFTPClient建立的方法（open_sftp)，通常用于执行远程命令。

**使用示例**

- 基于用户名和密码：
```python
import paramiko

ssh = paramiko.SSHClient()             
# 创建SSH对象
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# 允许连接不在know_hosts文件中的主机
ssh.connect(hostname='ip地址', port=22, username='root', password='@999')
# 连接服务器
stdin, stdout, stderr = ssh.exec_command('ls')
# 执行命令
result = stdout.read()
# 获取命令结果
print(result)

ssh.close()
# 关闭连接
```

- 公钥密钥：
```python
import paramiko
 
private_key = paramiko.RSAKey.from_private_key_file('/home/auto/.ssh/id_rsa')
# 创建SSH对象
ssh = paramiko.SSHClient()
# 允许连接不在know_hosts文件中的主机
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# 连接服务器
ssh.connect(hostname='c1.salt.com', port=22, username='wupeiqi', key=private_key)
# 执行命令
stdin, stdout, stderr = ssh.exec_command('df')
# 获取命令结果
result = stdout.read()
# 关闭连接
ssh.close()
```

### SFTPClient

> 通过SFTPClient类，可以使用基于SSH传输协议的SFTP协议。具体使用，通过创建成功的SSHClient对象打开一个SFTP会话，一个SFTPClient会话对象。操作会话对象上传、下载文件。

**使用示例：**

- 基于用户名和密码上传下载：

```python
import paramiko

transport = paramiko.Transport(('ip', 22))
transport.connect(username='root', password='SHIzhiming@999')

sftp = paramiko.SFTPClient.from_transport(transport)
# 将up.py 上传至服务器
# sftp.put('up.py', 'up.py')

#将服务器的文件 下载到本地 
sftp.get('up9.py', 'up_9.py')

transport.close()
```

- 基于公钥密钥：（和SSHClient类似）

```python
import paramiko
 
private_key = paramiko.RSAKey.from_private_key_file('/home/auto/.ssh/id_rsa')
 
transport = paramiko.Transport(('hostname', 22))
transport.connect(username='GSuser', pkey=private_key )
 
sftp = paramiko.SFTPClient.from_transport(transport)

# 将location.py 上传至服务器 /tmp/test.py
sftp.put('/tmp/location.py', '/tmp/test.py')

# 将remove_path 下载到本地 local_path
sftp.get('remove_path', 'local_path')
 
transport.close()
```

### Transport
> 这里额外介绍一下有关Transport方式的设备交互方式，Tranport方便的地方，你可以创建多个通道，然后在单个会话中多路复用；也可以创建单个通道绑定不同的客户端。

**使用示例：**
```python
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
```
备注：
- 创建指定设备的通道，建立连接，然后通过SSHClient和SFTPClient绑定通道，发送命令和传输文件；


## 总结
> 除了以上简单的登录，发送命令，传输文件任务在这基础上可以特定的增加类似WEB端命令交互功能等，在平时工作中接触到批量处理设备如：Fabric，Ansible，
底层也是基于paramiko模块实现的，所以可以将paramiko理解基础的SSH客户端库（当然也可以作为服务端，较少使用）；  
但是在后期需要兼容多种设备的自动化开发时发现，paramiko还是存在一定的局限性，如果需要设计一些类似如思科，Windows，非Unix设备的交互操作，paramiko都是不支持的，
所以这时候就需要使用Netmiko或者Napalm，关于Netmiko模块，我下一篇文章可以具体讲讲，感兴趣的点点关注；

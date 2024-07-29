准备建立连接的信息：
```python
info = {"device_type":"linux", "host":"","username":"root", "password":""}
```

 与设备建立SSH连接：
 ```python
from netmiko import ConnectHandler
device_connect = ConnectHandler(**info)
```

执行命令：
```python
device_connect.send_command("ifconfig")
```

常用方法：
- net_connect.send_command（）-在通道上发送命令，返回输出（基于模式）
- net_connect.send_command_timing（）-在通道上发送命令，返回输出（基于定时）
- net_connect.send_config_set（）-将配置命令发送到远程设备
- net_connect.send_config_from_file（）-发送从文件加载的配置命令
- net_connect.save_config（）-将运行配置保存到启动配置
- net_connect.enable（）-进入启用模式
- net_connect.find_prompt（）-返回当前路由器提示
- net_connect.commit（）-在Juniper和IOS-XR上执行提交操作
- net_connect.disconnect（）-关闭连接
- net_connect.write_channel（）-通道的低级写入
- net_connect.read_channel（）-通道的低级写入

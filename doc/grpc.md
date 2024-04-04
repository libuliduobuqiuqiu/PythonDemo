## 安装
grpc 安装
```shell
pip install grpcio
```
grpc tools 安装
```shell
pip install grpcio-tools
```
## 使用

根据protobuf生成grpc代码
```shell
python -m grpc_tools.protoc -I../../protos --python_out=. --pyi_out=. --grpc_python_out=. ../../protos/helloworld.proto
```
## 备注
可通过设置环境变量打印异常堆栈信息
```
GRPC_TRACE=all
GRPC_VERBOSITY=DEBUG
```

go grpc服务和python grpc服务互相调用
> https://zhuanlan.zhihu.com/p/607581611

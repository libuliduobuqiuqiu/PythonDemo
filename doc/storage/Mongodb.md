导语：
介绍Mongodb数据库的使用场景、基本类型、基本操作

## 安装pymongo库
> pip install pymongo


## 连接数据库
```python
# 第一种方式（使用属性）
client = pymongo.MongoClient(host="127.0.0.1",prot=27017,username="amdin", password="admin" )

# 第二种方式(使用MONGODB URI)
MONGODB_URI = "mongodb://admin:admin@127.0.0.1"
client = pymongo.MongoClient(MONGODB_URI)
```

## 指定数据库
```python
# 第一种方式
db = client["test"]

# 第二种方式
db = client.test
```

## 指定集合
> Mongodb数据库中的集合的概念类似与Mysql的表

```python
# 第一种方式
col = db.Address

# 第二种方式
col = db["Address"]
```

## 插入数据
```python
# 单条数据插入
person = {"name":"zhangsan", "address": "Villanuevatown, KS 93012"}
col.insert_one(person)
print(result.inserted_id)

# 批量数据插入
person = [{"name":"zhangsan", "address": "Villanuevatown, KS 93012"},{"name":"wangwu", "address": "Lake Alisonborough, MI 44016"}]
col.insert_many(person)
print(result.inserted_ids)
```
> inserted_id可获得插入数据后自动生成的_id，inserted_ids则是批量插入数据后的_id列表；

## 条件操作符
> 在讲讲有关删除，修改，查询等操作时，必须先了解相关Mongodb中条件操作符的语法


符号 | 含义
---|---
$lt | 小于
$gt | 大于
$lte | 小于等于
$gte | 大于等于
$ne | 不等于
$nin | 不在范围内
$in | 在范围内
$or | 至少满足一个条件

这里我们做个对比，方便理解：
```sql
# mysql查询
select * form Person where age > 18;
select * from Person where age between 18 and 30;

# mongodb查询
db.Person.find({"age": {"$gt": 18}})
db.Person.find({"age": {"$lt": 30, "$gt": 18}})
```

## 删除数据
remove()方法：
```python
result = col.remove({"name": "zhangsan"})
```
> 符合条件的数据都会一次性的删除，result是一个字典类似{'n': 12, 'ok': 1.0}，包含删除数据的数量和操作是否成功的标志；

delete_one()方法和delete_many方法：
```python
# 删除第一条符合条件的数据
col.delete_one({"name":"zhangsan"})

# 删除多条数据
result = col.delete_manay({"age": {"$gt": 30}})
print(result.deleted_count)
```
> deleted_count可以返回删除掉的记录数量，

## 更新数据

update()方法（官方不建议使用）:
```python
> 将符合条件的数据更新，只需要你指定条件和更新后的数据即可，这里需要注意的是
更新的数据更新的数据会覆盖原有的数据，即会移除所有忽略的键；

**更新插入数据（如果查找不到符合条件的数据则插入一条新的数据）**
```python
col.update(condition, {"$set": data}, upsert=True)
```
备注：
- condition为条件，data为更新插入的数据，upsert需为True（update+insert)

update_one()方法：
```python
result = col.update_one({"name":"zhangsan"}, {"$set":{"name": "wangwu"}})
print(result.matched_count, result.modified_count)
```
> update_one方法更新符合条件的第一条数据，需要注意的是，它不移除忽略的键，所以必须要使用$set操作符;<br>操作完成后返回的UpdateResult类型，如果想知道匹配了多少数据和更新了多少数据，可以分别调用matched_count和modified_count属性;

update_many()方法：
```python
result = col.update_many({"name":"zhangsan"}, {"$set":{"name": "wangwu"}})
```
> update_many方法批量更新符合条件的数据，需要注意的事项和update_one方法一样；


## 查询数据

find_one()方法和find()方法
```python
# 查询返回第一条符合条件的数据
result = col.find_one({"age": {"$gt": 30})

# 批量查询返回所有符合条件的数据
result = col.find({"age": {"$gt": 30})
```
> 可配合上面提到的条件操作符实现更多查询，批量查询返回的是一个Cursor类型，类似生成器，可通过遍历返回所有查询的结果，每个结果都是字典类型；

或查询
```python
result = client.read({"$or": [{"age": {"$lt": 20}},{"age": {"$gt": 70}}]})
```
> 小于20大于70

### 模糊查询

第一种方式：
```python
cond = {"name": {"$regex": "Peter"}}
result = col.find(cond)
```
第二种方式：
```python
cond = {"name": {"$regex": re.compile("Peter")}}
result = col.find(cond)
```
> 支持正则表达式
not list: $not

## 高级使用
**count()方法：**
```python
t_count = col.find({"name":"zhangsan"}).count()
print(t_count)
```
**sort()方法：**
```python
all_data = col.find({}).sort("name", pymongo.ASCENDING)
```
> pymongo.ASCENDING升序排列，pymongo.DESCENDING降序排列

**limit()方法和skip()方法**
```python
all_data = col.find().skip(2).limit(2)
```
> limit()方法限制返回结果，skip()方法偏移几个位置，即忽略前几个元素

**collections常用操作**
```python
# 查询所有的collections
collections_name = db.list_collection_names()

# 清空collection中的所有内容
col.remove()

# 删除collection
col.drop()

# 更改collection名字
col.rename("new_collections")
```

## 参考
> https://juejin.cn/post/6844903597465927694  
> https://blog.csdn.net/wzy0623/article/details/82870557  
> https://pymongo.readthedocs.io/en/stable/tutorial.html#making-a-connection-with-mongoclient

## 高级使用
pymongo文档：
> https://pymongo.readthedocs.io/en/stable/tutorial.html

### 问题代码
```python
def repeat_insert():
    from faker import Faker
    import random
    all_data = []
    f = Faker()
    client = MongoConnect("person")

    username = f.name()
    address = f.address()
    age = random.randint(0, 100)
    job = f.job()
    data = {"name": username, "address": address, "age": age, "job": job}
    all_data = [data for i in range(10)]
    client.insert(all_data)
```

### 实际场景
**在一个列表中有重复的字典，无法一次性全部插入到Mongodb中，插入会抛出异常：pymongo.errors.DuplicateKeyError: E11000 duplicate key error collection: test.person index: _id_ dup key.**

### 解决方法
根据网上查询资料显示，有可能是因为pymongo会给每个对象设置_id，如果同一个对象，会出现_id重复的情况，插入数据库后会因为_id重复的原因导致插入失败，所以只需要做一个浅拷贝，让all_data列表中的字典不是指向同一对象即可，修改后的代码：

```python
def repeat_insert():
    from faker import Faker
    import random
    all_data = []
    f = Faker()
    client = MongoConnect("person")

    username = f.name()
    address = f.address()
    age = random.randint(0, 100)
    job = f.job()
    data = {"name": username, "address": address, "age": age, "job": job}
    all_data = [data.copy() for i in range(10)]
    client.insert(all_data)
```

### 参考链接
> https://stackoverflow.com/questions/17529216/mongodb-insert-raises-duplicate-key-error

```python
from bson.json_util import dumps

cursor = db.collections.find({"Test": "Sample"})

for msg in cursor:
    json_msg = dumps(msg)
```

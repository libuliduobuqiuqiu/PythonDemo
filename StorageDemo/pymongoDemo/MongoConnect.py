# -*- coding: utf-8 -*-

from pymongo import MongoClient

from setting import AliyunSetting as setting
  
if __name__ == "__main__":
    MONGODB_URI = f"mongodb://{setting.MONGODB_USERNAME}:{setting.MONGODB_PASSWORD}@{setting.MONGODB_HOST}"
    client = MongoClient(MONGODB_URI, maxPoolSize = 200)
    db = client["test"]
    print("test")
    print(db.command("connections"))
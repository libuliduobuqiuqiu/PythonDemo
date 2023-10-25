# -*- coding: utf-8 -*-

from pymongo import MongoClient

from setting import MONGODB_HOST, MONGODB_USERNAME, MONGODB_PASSWORD
  
if __name__ == "__main__":
    MONGODB_URI = f"mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_HOST}"
    client = MongoClient(MONGODB_URI, maxPoolSize = 200)
    db = client["test"]
    print("test")
    print(db.command("connections"))
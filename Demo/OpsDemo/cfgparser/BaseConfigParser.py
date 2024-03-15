# -*- coding: utf-8 -*-

import json
import re


def parse_config(config: str):
    """
    将配置文件解析成字典格式
    :param config:
    :return:
    """

    config_item = config.splitlines()
    next_dict = {}              # 用于指向父节点的value字典
    line_dict = {}              # 保存每一行的节点信息
    result_items = []           # 保存已解析的数据
    parent_items = []           # 保存父节点路径
    result_flag = 0             # 保存树的深度

    for line in config_item:
        item_dict = {}
        next_items = {}
        line = line.strip()

        if not line:
            continue

        count_left = re.findall(r"{", line)
        count_right = re.findall(r"}", line)

        if count_left:
            item_name = re.findall(r"([\S\s]*){", line)[0].strip()

            if result_flag:
                line_dict = {item_name: {}}
                next_dict = line_dict[item_name]
                parent_items.append(item_name)
            else:
                item_dict = {item_name: {}}
            result_flag += len(count_left)

        if not count_left and not count_right and result_flag!=0:  # 不包含子节点的节点
            item = line.split()
            item_dict = {item[0]: " ".join(item[1:])}

        parent_dict = next_dict
        for item in parent_items[:result_flag]:             # 向包含子项的节点移动
            if next_items:
                for key, value in next_items.items():
                    if item == key:
                        parent_dict = value
            next_items = parent_dict

        if item_dict:
            next_items.update(item_dict)

            if count_left:
                parent_items.append("".join(item_dict.keys()))

        if count_right:
            result_flag -= len(count_right)
            if parent_items:
                parent_items.pop()

        if result_flag == 0:
            if line_dict:
                result_items.append(line_dict)
            line_dict = {}
            parent_items = {}
    return result_items

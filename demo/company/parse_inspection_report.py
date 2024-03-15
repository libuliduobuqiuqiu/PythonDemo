# coding: utf-8
"""
    :author: linshukai
    :date: 2023-12-14
    :description: Parse Adops Inspection Report
"""

import json


def parse_inspection():
    report_path = "/mnt/d/Company/report.json"

    with open(report_path, encoding="utf8") as f:
        content = f.read()

    record_list = json.loads(content)

    for records in record_list:
        print(records)
        for k, record in records.items():
            if k == "reports":
                print(json.dumps(records, indent=2, ensure_ascii=False))
                continue

            print(k, record)


if __name__ == "__main__":
    parse_inspection()

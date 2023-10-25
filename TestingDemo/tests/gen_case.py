# -*- coding: utf-8 -*-

import json

if __name__ == "__main__":
    flag = "12"
    # method = "create"
    method = "create"
    # method = "update"

    json_body = {
        "class": "deployments",
        "name": f"test_new_deploy{flag}_{method}",
        "deploy_schedule": "",
        "deploy_calendar": {"effect": "deny", "policies": ["? MON-FRI 00:00:00-23:59:59"]},
        "config": {
            "class": "adops.f5-bigip.slb",
            "project_id": "55",
            "group_id": "cb930d1f-1eca-11ed-a388-52540058c722",
            "MO1": {
                "class": "adops.slb.monitor",
                "method": method,
                "data": {
                    "name": f"test1_new_http{flag}",
                    "partition": "Common",
                    "type": "http",
                    "send_string": "hello,world",
                    "raw_configs": {
                        "defaults_from": "/Common/http",
                        "receive_string": "success"
                    },
                    "condition": True
                }
            },
            "MO2": {
                "class": "adops.slb.monitor",
                "method": method,
                "data": {
                    "name": f"test2_new_http{flag}",
                    "partition": "Common",
                    "type": "http",
                    "send_string": "hello,world",
                    "raw_configs": {
                        "defaults_from": "/Common/http",
                        "receive_string": "success"
                    },
                    "condition": True
                }
            },
            "Pool1": {
                "class": "adops.slb.pool",
                "method": method,
                "data": {
                    "name": f"test_new_pool{flag}",
                    "partition": "Common",
                    "full_path": "",
                    "load_balancing_method": "round-robin",
                    "monitors": [
                        f"/Common/test1_new_http{flag}"
                    ],
                    "availability_requirement_health_monitors": 0,
                    "raw_configs": {
                        "service_down_action": "none",
                        "slow_ramp_time": 10,
                        "priority_group": "Disabled",
                        "available_member": 1
                    }
                }
            },
            "Pool2": {
                "class": "adops.slb.pool",
                "method": "update",
                "data": {
                    "name": "test_new_pool7",
                    "partition": "Common",
                    "full_path": "/Common/test_new_pool7",
                    "load_balancing_method": "round-robin",
                    "monitors": [
                        f"/Common/test1_new_http{flag}",
                        f"/Common/test2_new_http{flag}"
                    ],
                    "availability_requirement_health_monitors": 0,
                    "raw_configs": {
                        "service_down_action": "none",
                        "slow_ramp_time": 10,
                        "priority_group": "Disabled",
                        "available_member": 1
                    }
                }
            }
            # "Pool3": {
            #     "class": "adops.slb.pool",
            #     "method": "create",
            #     "data": {
            #         "name": "test_new_pool8",
            #         "partition": "Common",
            #         "full_path": "",
            #         "load_balancing_method": "round-robin",
            #         "monitors": [
            #             "/Common/test1_new_http8"
            #         ],
            #         "availability_requirement_health_monitors": 0,
            #         "raw_configs": {
            #             "service_down_action": "none",
            #             "slow_ramp_time": 10,
            #             "priority_group": "Disabled",
            #             "available_member": 1
            #         }
            #     }
            # },
            # "VS1": {
            #     "class": "adops.slb.virtual_server",
            #     "method": "update",
            #     "data": {"name": "VS_linshukai_01",
            #              "availability": "unknown", "provider_name": "F5-BIGIP",
            #              "device_group_id": "cb930d1f-1eca-11ed-a388-52540058c722", "device_group_name": "10.21.21.97",
            #              "full_path": "/Common/VS_linshukai_01", "partition": "Common", "state": "enabled",
            #              "type": "layer7", "dest_address": "192.168.100.12", "protocol": "tcp", "port": 80,
            #              "virtual_address_id": "7fb1bfba-e1f4-46eb-a562-a2cbc65cfe05", "project_id": "56", "remark": "",
            #              "description": "",
            #              "raw_configs": {"address_status": "yes", "fallback_persistence": "", "irules": None,
            #                              "mask": "255.255.255.255", "persists": None, "policies": None,
            #                              "pool": "/Common/http_pool_cy", "profiles": [
            #                      {"context": "all", "full_path": "/Common/tcp",
            #                       "id": "d64f36c4-1eca-11ed-a388-52540058c722", "type": "tcp"}],
            #                              "service_down_immediate_action": "none", "snat_pool": "",
            #                              "source_address": "0.0.0.0/0", "source_address_translation": "none",
            #                              "vlans": None, "vlans_state": "disabled"}}
            # }
        }
    }

    print(json.dumps(json_body))

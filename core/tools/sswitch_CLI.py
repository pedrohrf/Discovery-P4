
import runtime_CLI

import sys
import os

from sswitch_runtime import SimpleSwitch

class SimpleSwitchAPI(runtime_CLI.RuntimeAPI):
    @staticmethod
    def get_thrift_services():
        return [("simple_switch", SimpleSwitch.Client)]

    def __init__(self, pre_type, standard_client, mc_client, sswitch_client):
        runtime_CLI.RuntimeAPI.__init__(self, pre_type,
                                        standard_client, mc_client)
        self.sswitch_client = sswitch_client


    def get_register_read(self, register_name, index):
        "Read register value: register_read <name> <index>"
        register = self.get_res("register", register_name, runtime_CLI.REGISTER_ARRAYS)
        try:
            index = int(index)
        except:
            print("Bad format for index")
        value = self.client.bm_register_read(0, register_name, index)
        return value

def get_Cli(thrift_ip, thrift_port, json):
    services = runtime_CLI.RuntimeAPI.get_thrift_services(runtime_CLI.PreType.SimplePreLAG)
    services.extend(SimpleSwitchAPI.get_thrift_services())
    standard_client, mc_client, sswitch_client = runtime_CLI.thrift_connect(thrift_ip, thrift_port, services)
    runtime_CLI.load_json_config(standard_client, json)
    return SimpleSwitchAPI(runtime_CLI.PreType.SimplePreLAG, standard_client, mc_client, sswitch_client)
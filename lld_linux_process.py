import json
from sys import argv
from zabbix_api import ZabbixAPI


hostname = argv[1]
## Essas Linhas precisams Ser alteradas
zapi = ZabbixAPI(server="")
zapi.login("", "")

def get_host_macros(hostname):

    macros_list = []

    filter = {
        "host": hostname
    }

    returned_list = zapi.host.get({"output": ["hostid","name"], "selectMacros": "extend", "filter": filter})

    for host in returned_list:
        for macro in host['macros']:
            macro_dict = {macro['macro']: macro['value']}
            macros_list.append(macro_dict)

    return macros_list
def construct_data_dict(value):
    data = {}
    process_name = value.split(",")[0].replace("\"","")
    process_qtd = value.split(",")[1]
    data["{#PROCESS_NAME}"] = process_name
    data["{#PROCESS_QTD}"] = process_qtd

    return data

def get_process_to_monitor():

    data = {}
    data_value = []

    macros_list = get_host_macros(hostname)

    for macro in macros_list:
        for key, value in macro.items():
            if '{$PROCESSMON.' in key:
                data_value.append(construct_data_dict(value))

    data["data"] = data_value
    print(json.dumps(data))

get_process_to_monitor()

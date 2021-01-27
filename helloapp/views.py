import os
from subprocess import Popen
from django.http import HttpResponse
from binspace.config import shared_storage_path


# Create your views here.
def on_demand(request, arg):
    tool_id = 1  # tool_id is the index of this tool in the list action_urls defined in binspace/config.py
    tool_folder_path = os.path.join(shared_storage_path, arg, 'tool'+str(tool_id))
    script_path = 'helloapp/scripts/helloapp_ondemand.sh'  # script_path is the file path of script
    command = ['/bin/bash', script_path, tool_folder_path]
    print("BinSpace Client: Get an on demand request. Run command " + ele for ele in command)
    Popen(command)
    response = HttpResponse('')
    return response


def on_submit(request, arg):
    sample_path = os.path.join(shared_storage_path, arg)
    script_path = 'helloapp/scripts/helloapp_onsubmit.sh'  # script_path is the file path of script
    command = ['/bin/bash', script_path, sample_path]
    print("BinSpace Client: Get an on submit request. Run command " + ele for ele in command)
    Popen(command)
    response = HttpResponse('')
    return response

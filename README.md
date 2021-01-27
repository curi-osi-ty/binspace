# BinSpace: A Workspace for Binary Analysis Tools

BinSpace is a management framework for binary analysis written in Django. It manages binaries and integrates binary analysis tools as workers, which can be activated by Django apps. BinSapce and tool workers communicate using a share directory structure. 

## Install Binspace
Requirement: python3 django
We suggest you install inside a Python virtual environment.
```
pip3 install django requests
```
Test it with:
```
python manage.py migrate
python manage.py runserver
```
Then it should start service at your localhost:8000.
## Add an analysis tool as an app. 
An helloapp is included, which demonstrates using the objdump utility to disassemble the uploaded binary. To use it, you need to unzip the helloapp-tools.zip file in the /tmp directory. 

Here are the steps of creating it. 

```
python manage.py startapp helloapp
```
Add your web app url path to `urlpatterns` list in binspace/urls.py:
```
urlpatterns += [
    path('myapp/', include('helloapp.urls')),
]
```
Add the tool name in `tools` list and the url in `action_urls` list in binspace/config.py.

Create helloapp/urls.py, define which function should be called: 
```
from django.urls import path
from helloapp import views

urlpatterns = [
    path('dump/<str:arg>', views.call_script),
]
```
Create helloapp/views.py, define the function to run your script:
```
import os
from subprocess import Popen
from django.http import HttpResponse
from binspace.config import shared_storage_path


# Create your views here.
def call_script(request, arg):
    tool_id = 1  # tool_id is the index of this tool in the list action_urls defined in binspace/config.py
    sample_path = os.path.join(shared_storage_path, arg, 'tool'+str(tool_id))
    script_path = '/tmp/helloapp-tool/script.sh'  # script_path is the file path of script
    command = ['/bin/bash', script_path, sample_path]
    Popen(command)
    response = HttpResponse('')
    return response
```




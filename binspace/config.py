# The names for each app. The first one must be NULL
tools = [
        'NULL',                         # by default, do not remove
        # Put your tool name here, e.g. 'Hello World App',
        'helloapp'
        ]

# The URLs for each app. The first one must be NULL
action_urls = [
        'NULL',                          # by default, do not remove
        # Put your tool's action url here accordingly, e.g. 'http://locahost:8000/helloapp/dump/',
        'http://127.0.0.1:8000/helloapp/dump/'
        ]

# The URLs for on submit actions. When a sample is uploaded, these URLs will be requested.
on_submit_urls = [
        # Put your tool's on_submit url here if any, e.g. 'http://locahost:8000/helloapp/file/'.
        'http://127.0.0.1:8000/helloapp/file/'
]

# The path where BinSpace stores all samples and reports
shared_storage_path = '/tmp/uploaded_samples/'

# The permission for storage folders of each samples
storage_permission = 0o755


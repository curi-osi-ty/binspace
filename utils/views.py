import os.path
import hashlib
import shutil
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from .forms import UploadSampleForm
from .models import Sample, Result, User
from django.shortcuts import redirect
import requests
from django.http import HttpResponse
from binspace.config import tools, action_urls, shared_storage_path

def index(request):
    num_of_users = User.objects.all().count()
    num_of_samples = Sample.objects.all().count()
    num_of_results = Result.objects.all().count()
    context = {
        'num_of_users': num_of_users,
        'num_of_samples': num_of_samples,
        'num_of_results': num_of_results,
    }
    return render(request, 'index.html', context=context)


def sample(request):
    # TODO User!
    # Currently, all users are set to demo
    try:
        current_user = User.objects.get(username='demo')
    except:
        current_user = User(username='demo', password='demo', email='demo@example.com', full_name='Demo')
        current_user.save()

    samples = Sample.objects.filter(user=current_user)
    return render(
        request,
        'sample.html',
        context={'num_of_samples': len(samples), 'my_samples': samples},
    )


def delete(request, id):
    # TODO User Permission Check!
    current_sample = Sample.objects.get(sid=id)
    results = Result.objects.filter(sample__sid=id)
    shared_sample_folder = os.path.join(shared_storage_path, current_sample.sha1sum)
    try:
        shutil.rmtree(shared_sample_folder)
    finally:
        results.delete()
        current_sample.delete()
        return redirect('/utils/sample.html')



def upload_file(request):
    if request.method == 'POST':
        form = UploadSampleForm(request.POST, request.FILES)
        if form.is_valid():
            # TODO User!
            # Currently, all users are set to demo
            current_user = User.objects.get(username='demo')
            
            uploaded_file = request.FILES['file']
            hasher = hashlib.sha1()
            for chunk in uploaded_file.chunks():
                hasher.update(chunk)
            instance = Sample(sha1sum=hasher.hexdigest(), filename=uploaded_file.name,
                              file=uploaded_file, user=current_user, uploaded_at=timezone.now())
            instance.save()
            # return HttpResponseRedirect('/success/url/')
            return HttpResponseRedirect('sample')
    else:
        form = UploadSampleForm()
    return render(request, 'upload.html', {'form': form})


class DisplayResult(object):
    tool = ''
    status = 'NA'
    latest_report_date = ''
    tool_id = 0
    report_path = '#'
    action_url = ''


def individual_sample(request, id):
    # TODO User Permission Check!
    current_sample = Sample.objects.get(sid=id)
    results = Result.objects.filter(sample__sid=id)
    num_of_results = results.count()
    results_of_tools = []
    shared_sample_folder = os.path.join(shared_storage_path, current_sample.sha1sum)
    for idx in range(1, len(tools)):
        result_entry = DisplayResult()
        result_entry.tool_id = idx
        result_entry.tool = tools[idx]
        result_entry.action_url = action_urls[idx] + current_sample.sha1sum
        if results.filter(tool=tools[idx]).count()!=0:
            latest_result = results.filter(tool=tools[idx]).latest('finished_at')

            result_entry.latest_report_date = latest_result.finished_at
            result_entry.report_path = latest_result.path
            shared_report_folder = os.path.join(shared_sample_folder, 'tool'+str(result_entry.tool_id))
            if os.path.exists(shared_report_folder):
                # We assume the tool generate a file caledd status.txt in the sample's folder
                status_path = os.path.join(shared_report_folder, 'status.txt')
                if os.path.exists(status_path):
                    fstatus = open(status_path, "r")
                    result_entry.status = fstatus.read()
                    fstatus.close()
                else:
                    # Somehow the scripts did not put the status file there
                    print("Error: status file not found! {}".format(status_path))
                    result_entry.status = 'Missing'
            else:
                # Somehow the scripts did not create the report folder
                print("Error: Report folder not found! {}".format(shared_report_folder))
                result_entry.status = 'Missing'
        results_of_tools.append(result_entry)

    context = {
        'sample_name': current_sample.filename,
        'uploaded_at': current_sample.uploaded_at,
        'num_of_available_reports': num_of_results,
        'report_of_tool': results_of_tools,
        'sample_hash': current_sample.sha1sum,
        'sample_uid': id,
    }
    return render(request, 'individual_sample.html', context=context)


def generate(request, tool_id, sample_id):
    if tool_id in range(1, len(action_urls)):
        current_sample = Sample.objects.get(sid=sample_id)
        assert (len(tools) == len(action_urls))
        # We just encode sample's sha1sum in the URL
        # If you want to send with more arguments,
        # you may modify the code below.
        url = action_urls[tool_id] + current_sample.sha1sum

        try:
            r = requests.get(url=url)
        except Exception as e:
            print("Error when getting url {}.\t{}".format(url, e))

        shared_sample_folder = os.path.join(shared_storage_path, current_sample.sha1sum)
        shared_report_folder = os.path.join(shared_sample_folder, 'tool' + str(tool_id))
        if not os.path.exists(shared_report_folder):
            os.mkdir(shared_report_folder)
        report_path = os.path.join(shared_report_folder, 'output.txt')
        instance = Result(sample=current_sample, finished_at=timezone.now(), tool=tools[tool_id], path=report_path)
        instance.save()
    response = redirect('sample')
    return response



def get_status(request, sha1, tool):
    response = HttpResponse(content_type="text/html")
    status_folder = os.path.join(shared_storage_path, sha1)
    tool_folder = os.path.join(status_folder, tool)
    status_file_path = os.path.join(tool_folder, 'status.txt')
    for line in open(status_file_path):
        response.write(line)
    return response


def get_result(request, sha1, tool):
    # response = HttpResponse(content_type="text/html")
    result_folder = os.path.join(shared_storage_path, sha1)
    tool_folder = os.path.join(result_folder, tool)
    result_file_path = os.path.join(tool_folder, 'output.txt')
    output = ''
    for line in open(result_file_path):
        output += line
    context = {
        'output_text': output,
    }
    return render(request, 'output.html', context=context)

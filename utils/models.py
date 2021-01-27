from django.db import models
from django.utils import timezone
from binspace.config import shared_storage_path, storage_permission, on_submit_urls
import hashlib
import os
import pathlib
import uuid
import requests


def send_on_submit_request(base_url, sha1sum):
    url = base_url + sha1sum
    try:
        r = requests.get(url=url)
        print("BinSpace: Sending a request to {}".format(url))
    except:
        print("BinSpace: Error when getting url {}".format(url))


def store_uploaded_file(instance, filename):
    hasher = hashlib.sha1()
    for chunk in instance.file.chunks():
        hasher.update(chunk)
    sample_sha1sum = str(hasher.hexdigest())
    shared_sample_folder = os.path.join(shared_storage_path, sample_sha1sum)
    pathlib.Path(shared_sample_folder).mkdir(mode=storage_permission, parents=True, exist_ok=True)
    for url in on_submit_urls:
        send_on_submit_request(url, sample_sha1sum)
    return os.path.join(shared_sample_folder, 'sample.bin')


class User(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    full_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username


class Sample(models.Model):
    sid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    filename = models.CharField(max_length=200)
    sha1sum = models.CharField(max_length=256)
    uploaded_at = models.DateTimeField(default=timezone.now)
    file = models.FileField(upload_to=store_uploaded_file)

    def __str__(self):
        return self.filename


class Result(models.Model):
    rid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sample = models.ForeignKey(Sample, on_delete=models.SET_NULL, null=True)
    tool = models.CharField(max_length=200)
    finished_at = models.DateTimeField(default=timezone.now)
    path = models.CharField(max_length=200)

    class Meta:
        ordering = ["-finished_at"]

    def __str__(self):
        return '%s (%s at %s)' % (self.sample.filename, self.tool, self.finished_at)

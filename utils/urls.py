from django.urls import path
from utils import views
from django.conf.urls import url

urlpatterns = [
    path('sample/<uuid:id>', views.individual_sample),
    path('delete/<uuid:id>', views.delete),
    path('generate/<int:tool_id>/<uuid:sample_id>', views.generate),
    path('status/<str:sha1>/<str:tool>', views.get_status),
    path('report/<str:sha1>/<str:tool>', views.get_result),
    url(r'^sample', views.sample, name='sample'),
    url(r'^upload', views.upload_file, name='upload'),
    url('', views.index, name='index'),
]

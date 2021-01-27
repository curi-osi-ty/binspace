from django.urls import path
from helloapp import views

urlpatterns = [
    path('dump/<str:arg>', views.on_demand),
    path('file/<str:arg>', views.on_submit),
]

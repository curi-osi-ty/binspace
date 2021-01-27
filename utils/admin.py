from django.contrib import admin

# Register your models here.
from .models import Sample, User, Result

admin.site.register(Sample)
admin.site.register(User)
admin.site.register(Result)

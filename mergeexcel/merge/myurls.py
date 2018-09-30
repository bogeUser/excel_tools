from django.conf.urls import url
from .views import *

urlpatterns = [
    url("^upload", upload, name="upload"),
    url("^download", download, name="download"),
    url("^sortfile",sortfile,name="sortfile"),
]

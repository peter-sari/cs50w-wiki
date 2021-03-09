from django.urls import path
from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("nosuchentry", views.nosuchentry, name="noSuchEntry"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("searching", views.searching, name="searching"),
    path("randomed", views.randomed, name="randomed"),
    path("create", views.create, name="create"),
    path("edit", views.edit, name="edit"),
    path("exists", views.exists, name="exists"),
    path("<str:entryname>", views.entryname, name="entryname")
]

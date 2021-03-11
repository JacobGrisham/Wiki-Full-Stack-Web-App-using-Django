from django.urls import include, path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="home"),
    path("search", views.search, name="search"),
    path("add/", views.create, name="create"),
    path("wiki/<str:title>", views.entry, name="title"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("wiki/", views.random_page, name="random")
]

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.load, name="load"),
    path("search", views.search, name="search"),
    path("newpage",views.new, name="newpage"),
    path("renderpage", views.renderpage, name="renderpage"),
    path("randompage", views.randompage, name="random"),
    path("editform/<str:name>", views.edit, name="editform"),
    path("editpage/<str:name>", views.editpage, name="edit"),
]

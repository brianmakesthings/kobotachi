from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:manga_id>/", views.chapter_list, name="chapter_list"),
]
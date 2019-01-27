from django.urls import path

from . import views

urlpatterns = [
    # path("", views.ProfileDetail.as_view(), name="profile"),
    path("edit/", views.ProfileEdit.as_view(), name="edit"),
    path("", views.home, name="home"),
]


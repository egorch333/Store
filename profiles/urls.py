from django.urls import path

from . import views


urlpatterns = [
    path("<int:pk>", views.ProfileDetail.as_view(), name="profile"),
    path("edit/<int:pk>", views.ProfileUpdate.as_view(), name="edit_profile"),
    path("edit-profile-anonym/", views.ProfileAnonymUpdate.as_view(), name="edit_profile_anonym"),
]
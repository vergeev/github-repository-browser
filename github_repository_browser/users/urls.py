from django.urls import path

from github_repository_browser.users.views import (
    user_redirect_view,
    user_detail_view,
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("<str:username>/", view=user_detail_view, name="detail"),
]

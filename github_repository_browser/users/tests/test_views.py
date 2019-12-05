import pytest
from django.conf import settings
from django.test import RequestFactory

from github_repository_browser.users.views import UserRedirectView

pytestmark = pytest.mark.django_db


class TestUserRedirectView:
    def test_get_redirect_url(
        self, user: settings.AUTH_USER_MODEL, request_factory: RequestFactory
    ):
        view = UserRedirectView()
        request = request_factory.get("/fake-url")
        request.user = user

        view.request = request

        assert view.get_redirect_url() == f"/users/{user.username}/"

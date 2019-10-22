from django.views.decorators.cache import cache_page
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, RedirectView, UpdateView
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from github import Github

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        github_client = Github(self.request.user.github_token)
        github_user = github_client.get_user()

        context['github_username'] = github_user.login
        context['github_avatar_url'] = github_user.avatar_url
        context['github_repositories'] = [
            {
                'name': repo.full_name,
                'url': repo.html_url,
            }
            for repo in github_user.get_repos()
        ]

        return context


user_detail_view = UserDetailView.as_view()
# Fetching Github info takes too long, better cache the response
user_detail_view = cache_page(settings.USER_INFO_CACHE_TIME)(user_detail_view)


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()

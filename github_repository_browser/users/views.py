from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.views.generic import DetailView, RedirectView
from django.contrib import messages
from django.http import Http404
from django.contrib.auth import logout
from django.utils.timezone import now


from github import Github

User = get_user_model()


class UserDetailView(UserPassesTestMixin, LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"

    def test_func(self):
        if self.request.user.is_superuser:
            return True

        if self.request.user.username != self.kwargs['username']:
            raise Http404()

        github_token = self.get_object().github_token
        if github_token.expires_at and github_token.expires_at < now():
            messages.add_message(
                self.request, messages.ERROR, 'Your Github token has expired. Please log in again.')
            logout(self.request)
            return False

        return True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        github_token = self.object.github_token
        github_client = Github(github_token.token)
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


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()

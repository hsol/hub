from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.views import RedirectURLMixin
from django.core.mail import send_mail
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import resolve_url
from django.urls import reverse
from django.utils.timezone import now
from django.views import View
from django.views.generic import TemplateView, FormView
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout

from core.forms import EmailLoginForm, EmailTokenProcessForm


class IndexView(TemplateView):
    template_name = "index.html"


class EmailVerifyTemplateView(TemplateView):
    template_name = "registration/email.tpl.html"


class LoginView(RedirectURLMixin, FormView):
    template_name = "registration/login.html"
    form_class = EmailLoginForm

    def get_initial(self):
        initial = super().get_initial()
        if redirect_to := self.request.GET.get("next"):
            initial["next"] = redirect_to

        return initial

    def get_redirect_url(self):
        return reverse("need_to_verify") + f"?email={self.request.POST.get('email')}"

    def form_valid(self, form: EmailLoginForm):
        email = form.cleaned_data["email"]
        token, _ = Token.objects.update_or_create(
            user=User.objects.get(email=email), defaults={"created": now()}
        )
        verify_path = reverse("verify") + f"?email={email}&token={token.key}"
        if redirect_to := form.cleaned_data.get("next"):
            verify_path += f"&next={redirect_to}"

        response = EmailVerifyTemplateView(request=self.request).render_to_response(
            {
                "email": email,
                "verify_path": verify_path,
                "first_name": token.user.first_name,
            }
        )
        send_mail(
            subject="[Hub] 이메일로 로그인해주세요.",
            message="",
            html_message=response.render().content.decode("utf-8"),
            from_email=settings.SERVER_EMAIL,
            recipient_list=[email],
        )

        return super().form_valid(form)


class NeedToVerifyView(TemplateView):
    template_name = "registration/need_to_verify.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.GET.get("email"):
            raise Http404

        return super().dispatch(request, *args, **kwargs)


class EmailVerifyView(RedirectURLMixin, FormView):
    template_name = "registration/token_verify.html"
    form_class = EmailTokenProcessForm

    def get_default_redirect_url(self):
        if self.next_page:
            return resolve_url(self.next_page)
        else:
            return resolve_url(settings.LOGIN_REDIRECT_URL)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = {
            "initial": self.get_initial(),
            "prefix": self.get_prefix(),
            "data": self.request.GET,
        }
        return kwargs

    def form_valid(self, form: EmailTokenProcessForm):
        token = Token.objects.get(key=form.cleaned_data["token"])
        login(self.request, token.user)
        token.delete()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class LogoutView(RedirectURLMixin, View):
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(self.get_success_url())

    def get_default_redirect_url(self):
        if redirect_to := self.request.GET.get("next"):
            return resolve_url(redirect_to)
        else:
            return resolve_url(settings.LOGIN_REDIRECT_URL)

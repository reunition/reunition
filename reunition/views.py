from allauth.account import app_settings
from allauth.account.views import LoginView, SignupView
from allauth.utils import get_form_class


class LoginSignupView(LoginView):

    def get_context_data(self, **kwargs):
        data = super(LoginSignupView, self).get_context_data(**kwargs)
        signup_form_class = get_form_class(
            app_settings.FORMS, 'signup', SignupView.form_class)
        data['signup_form'] = signup_form_class()
        return data


login_signup_view = LoginSignupView.as_view()

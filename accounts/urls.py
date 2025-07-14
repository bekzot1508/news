from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, \
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.views.generic import TemplateView

from .views import user_login, dashboard_view, user_register, SignUpView, edt_user, EditUserView

urlpatterns = [
    #path('login/', user_login, name="login"),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('logged_out/', TemplateView.as_view(template_name='registration/logged_out.html'), name='logged_out'),
    path('password-change/', PasswordChangeView.as_view(), name='password_change'),
    path('password-change-done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('profile/', dashboard_view, name='user_profile'),
    path('profile/edit/', edt_user, name='edt_user_information'),
    # path('profile/edit/', EditUserView.as_view(), name='edt_user_information'),
    path('signup/', user_register, name='user_register'),
    # path('signup/', SignUpView.as_view(), name='user_register'),
]
from django.urls import path
from authenticationapp.views import *

urlpatterns=[
    path("signup/",handlesignup,name='handlesignup'),
    path("login/",handlelogin,name='handlelogin'),
    path("logout/",handlelogout,name='handlelogout'),
    path('activate/<uidb64>/<token>',ActivateAccountView.as_view(),name='activate'),
    path('request-reset-email',RequestResetEmailView.as_view(),name="request-reset-email"),
    path('set-new-password/<uidb64>/<token>',SetNewPasswordView.as_view(),name="set-new-password"),
]
"""oouch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin, auth
from django.contrib.auth import backends
from django.urls import path
from django.conf.urls import url, include
from django.views.generic.base import TemplateView
from authorization import views as server_views
import oauth2_provider.views as oauth2_views
from django.views.generic.base import RedirectView
from django.conf import settings
from resources.views import HealthCheck, GetUser, GetSsh
from authorization.views import basic_auth_wrapper, authorize_wrapper
from django.contrib.auth.views import LoginView 


oauth2_endpoint_views = [
    url(r'^authorize/$', authorize_wrapper(oauth2_views.AuthorizationView.as_view()), name="authorize"),
    url(r'^token/$', oauth2_views.TokenView.as_view(), name="token"),
    url(r'^revoke-token/$', oauth2_views.RevokeTokenView.as_view(), name="revoke-token"),
]

# OAuth2 Application Management endpoints
oauth2_endpoint_views += [
    url(r'^applications/$', basic_auth_wrapper(oauth2_views.ApplicationList.as_view(),b'clarabibi4live',b'klaraboboissosupermegasecure!:D!', 'Oouch Admin Only'), name="list"),
    url(r'^applications/register/$', basic_auth_wrapper(oauth2_views.ApplicationRegistration.as_view(), b'develop', b'supermegasecureklarabubu123!', 'Oouch Development'), name="register"),
    url(r'^applications/(?P<pk>1)/.*$', basic_auth_wrapper(oauth2_views.ApplicationDetail.as_view(),b'clarabibi4live',b'klaraboboissosupermegasecure!:D!', 'Oouch Admin Only'), name="detail"),
    url(r'^applications/(?P<pk>\d+)/$', basic_auth_wrapper(oauth2_views.ApplicationDetail.as_view(), b'develop', b'supermegasecureklarabubu123!', 'Oouch Development'), name="detail"),
    url(r'^applications/(?P<pk>\d+)/delete/$', basic_auth_wrapper(oauth2_views.ApplicationDelete.as_view(), b'develop', b'supermegasecureklarabubu123!', 'Oouch Development'), name="delete"),
    url(r'^applications/(?P<pk>\d+)/update/$', basic_auth_wrapper(oauth2_views.ApplicationUpdate.as_view(), b'develop', b'supermegasecureklarabubu123!', 'Oouch Development'), name="update"),
]

# OAuth2 Token Management endpoints
oauth2_endpoint_views += [
    url(r'^authorized-tokens/$', basic_auth_wrapper(oauth2_views.AuthorizedTokensListView.as_view(),b'clarabibi4live',b'klaraboboissosupermegasecure!:D!', 'Oouch Admin Only'), name="authorized-token-list"),
    url(r'^authorized-tokens/(?P<pk>\d+)/delete/$', basic_auth_wrapper(oauth2_views.AuthorizedTokenDeleteView.as_view(),b'clarabibi4live',b'klaraboboissosupermegasecure!:D!', 'Oouch Admin Only'),
        name="authorized-token-delete"),
]

urlpatterns = [
    path('', TemplateView.as_view(template_name='authorization/home.html'), name='home'),
    path('home/', TemplateView.as_view(template_name='authorization/home.html'), name='home'),

    url(r'^accounts/login/$', RedirectView.as_view(url='/login/', permanent=True), name='login'),
    url(r'^login/$',  LoginView.as_view(template_name='authorization/login.html'), name='login'),
    url(r'^signup/$', server_views.signup, name='signup'),

    url(r'^api/hello', HealthCheck.as_view()),
    url(r'^api/get_user', GetUser.as_view()),
    url(r'^api/get_ssh', GetSsh.as_view()),

    url(r'^oauth/', include((oauth2_endpoint_views, "app"), namespace="oauth2_provider")),
]

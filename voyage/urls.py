"""voyage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework_swagger.views import get_swagger_view
from rest_framework_jwt.views import obtain_jwt_token

schema_view = get_swagger_view(title='Pastebin API')

localapp_urlpatterns = []
for app in settings.LOCAL_APPS:
    # Ignoring some unwanted app. Such apps usually don't have urls
    if app in ['core']:
        continue
    localapp_urlpatterns.append(url(r'^', include('%s.urls' % app)))

urlpatterns = [
    url(r'^apidoc/', schema_view),
    url(r'^admin/', admin.site.urls),
    url('grappelli/', include('grappelli.urls')),
    url(r'^api-token-auth/', obtain_jwt_token),
]

from django.contrib import admin
from django.contrib.admin import AdminSite
from django.http import HttpResponse
from django.shortcuts import render
# Register your models here.

from django.contrib.auth.models import User

class MyAdminSite(AdminSite):

    def custom_view(self, request):
        pass

    def get_urls(self):
        from django.conf.urls import url
        urls = super(MyAdminSite, self).get_urls()
        urls += [
            url(r'^custom_view/$', self.admin_view(self.custom_view))
        ]
        return urls

admin_site = MyAdminSite()
import json

from django.shortcuts import render
from oauth2_provider.views.generic import ProtectedResourceView
from django.http import HttpResponse


class HealthCheck(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        return HttpResponse('It works!')


class GetUser(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        username = request.user.username
        firstname = request.user.first_name
        lastname = request.user.last_name
        email = request.user.email

        data = {}
        data['username'] = username
        data['firstname'] = firstname
        data['lastname'] = lastname
        data['email'] = email

        json_data = json.dumps(data)

        return HttpResponse(json_data)


class GetSsh(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        ssh_server = request.user.profile.ssh_server
        ssh_user = request.user.profile.ssh_user
        ssh_key = request.user.profile.ssh_key

        data = {}
        data['ssh_server'] = ssh_server
        data['ssh_user'] = ssh_user
        data['ssh_key'] = ssh_key

        json_data = json.dumps(data)

        return HttpResponse(json_data)

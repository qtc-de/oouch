import base64
from django.http import HttpResponse, HttpRequest
from django.views.generic import CreateView
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .models import Profile
from django.contrib.auth.models import User

from authorization.forms import SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()

            user.profile.ssh_server = form.cleaned_data.get('ssh_server')
            user.profile.ssh_user = form.cleaned_data.get('ssh_user')
            user.profile.ssh_key = form.cleaned_data.get('ssh_key')

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')

            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/login/')
    else:
        form = SignUpForm()

    return render(request, 'authorization/signup.html', {'form': form})


def basic_auth_wrapper(maybe_view, username, password, realm):
    def basic_auth_or_view(request, *args, **kwargs):
        if 'HTTP_AUTHORIZATION' in request.META:
            auth = request.META['HTTP_AUTHORIZATION'].split()
            if len(auth) == 2:
                if auth[0].lower() == "basic":
                    uname, passwd = base64.b64decode(auth[1]).split(b':')
                    if uname == username and passwd == password:
                        return maybe_view(request, *args, **kwargs)

        # Either they did not provide an authorization header or
        # something in the authorization attempt failed. Send a 401
        # back to them to ask them to authenticate.
        response = HttpResponse()
        response.status_code = 401
        response['WWW-Authenticate'] = f'Basic realm="{realm}"'
        return response
    
    return basic_auth_or_view


# This is required to allow authorization using a simple get request
def authorize_wrapper(view):
    def get_to_post(request, *args, **kwargs):
        if request.method == 'POST':
            return view(request, *args, **kwargs)

        elif request.method == 'GET' and request.GET.get('allow'):
            post_request = HttpRequest()
            post_request.method = 'POST'
            post_request.META = request.META
            post_request.user = request.user

            try: 
                csrf_token = request.GET.get('csrfmiddlewaretoken')
                redirect_url = request.GET.get('redirect_uri')
                scope = request.GET.get("scope")
                client_id = request.GET.get("client_id")
                state = request.GET.get("client_id")
                response_type = request.GET.get("response_type")
                allow = request.GET.get("allow")
            except:
                response = HttpResponse()
                response.status_code = 500
                return response

            post_request.POST['csrf_token'] = csrf_token
            post_request.POST['redirect_uri'] = redirect_url
            post_request.POST['scope'] = scope
            post_request.POST['client_id'] = client_id
            post_request.POST['response_type'] = response_type
            post_request.POST['allow'] = allow

            return get_to_post(post_request, *args, **kwargs)
            
        elif request.method == 'GET' and not request.GET.get('allow'):
            return view(request, *args, **kwargs)

        else:
            response = HttpResponse()
            response.status_code = 500
            return response

    return get_to_post

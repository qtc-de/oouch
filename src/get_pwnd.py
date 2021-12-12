#!/usr/bin/python3
import re
import requests


def login_consumer(username, password):
    '''
    The following function performs a login into the consumer application. It is required to simoulate the 
    administrator how is visiting messages from the contact form. If such messages contain links, the administrator
    is expected to be logged in into the consumer application and to visit the corresponding link.

    Parameters:
        username                (String)                    Username for the administrator.

    Returns:
        session_cookie          (String)                    Session cookie for an administrator session.
    '''
    print(f'[+] Starting login on consumer application')
    # First we issue an request to obtain a initial session and the csrf token
    r = requests.get("http://consumer.oouch.htb:5000")

    # Session is parsed from the headers
    session_tmp = r.headers["Set-Cookie"].split("=")[1]
    session_tmp = session_tmp.split(";")[0]
    print(f'[+] Temporary Session-ID: {session_tmp}')

    # Csrf token is captured by regex
    csrf_regex = re.compile('name="csrf_token" type="hidden" value="([^"]+)"')
    csrf_token = csrf_regex.search(r.text).group(1)
    print(f'[+] CSRF Token: {csrf_token}')

    # When we prepare the login data
    data = {
                "csrf_token" : csrf_token,
                "username" : username,
                "password" : password,
                "submit" : "Sign In",
           }

    # And set the temporary session cookie
    cookies = {
                "session": session_tmp,
              }

    # Finally we peform the login request. We need to avoid redirects since we want the ne cookie from the 302 response
    r = requests.post("http://consumer.oouch.htb:5000/login", data=data, cookies=cookies,  allow_redirects=False)

    # Parse the session from the headers
    session = r.headers["Set-Cookie"].split("=")[1]
    print(f'[+] Admin cookie obtained: {session}')

    # And return it back to the client
    return session


def login_authorization(username, password):
    '''
    The following function performs a login into the authorization server. It is required to simoulate the 
    administrator how is visiting messages from the contact form. If such messages contain links, the administrator
    is expected to be logged in into the authorization application and to visit the corresponding link.

    Parameters:
        username                (String)                    Username for the administrator.

    Returns:
        session_cookie          (String)                    Session cookie for an administrator session.
    '''
    print(f'[+] Starting login on authorization application')
    # First we issue an request to obtain the csrf token
    r = requests.get("http://authorization.oouch.htb:8000/login/")

    # csrf token is parsed from the headers
    csrf_token = r.headers["Set-Cookie"].split("=")[1]
    csrf_token = csrf_token.split(";")[0]
    print(f'[+] CSRF Token: {csrf_token}')

    # When we prepare the login data
    data = {
                "csrfmiddlewaretoken" : csrf_token,
                "username" : username,
                "password" : password,
           }

    # And set the csrf token additionally as cookie
    cookies = {
                "csrftoken": csrf_token,
              }

    # Finally we peform the login request. We need to avoid redirects since we want the ne cookie from the 302 response
    r = requests.post("http://authorization.oouch.htb:8000/login/", data=data, cookies=cookies,  allow_redirects=False)

    # Since the endpoint issues two cookies, we have to use a regex for extraction
    cookie_regex = re.compile("sessionid=([^\s]+)")
    session = cookie_regex.search(r.headers["Set-Cookie"]).group(1)
    print(f'[+] Admin cookie obtained: {session}')

    # And return it back to the client
    return session


def sort_urls(filepath):
    '''
    This function takes the path to the file where the urls received by the contact form are stored. It sorts the urls into 
    three different groups according to their targets: 1. Consumer Application, 2. Authorization Server, 3. Other. It returns
    a list containing three different lists, that correspond to the above choices.

    Parameters:
        filepath                (String)                    Absolute path to the urls file

    Returns:
        urls                    (List[list[String]])        Three different list of targets
    '''
    # First of all we read all urls line by line
    with open(filepath, "r") as url_file:
        url_lines = url_file.readlines()

    # After the urls have been read in, we cleat the url file
    with open(filepath, "w") as url_file:
        pass

    # When we define regexes for the two different cases (thrid one will be all others)
    consumer_regex = re.compile('^(http://consumer.oouch.htb:5000/[^@]+|http://127.0.0.1:5000/[^@]+)')
    authorization_regex = re.compile('^http://authorization.oouch.htb:8000/[^@]+')

    other_urls = []
    consumer_urls = []
    authorization_urls = []

    url_lines = list(map( lambda x: x.strip(), url_lines))
    for url in url_lines:
        if consumer_regex.search(url):
            consumer_urls.append(url)
        elif authorization_regex.search(url):
            authorization_urls.append(url)
        else:
            other_urls.append(url)

    return [other_urls, consumer_urls, authorization_urls]


def visit_them(url_list, cookie_dict, timeout):
    '''
    This function takes a list of urls and lauches get requests against them. Furthermore, it includes cookies
    that can be specified as function arguments.

    Parameters:
        url_list                (list[String])              List of urls to visit
        cookie_dict             (dict)                      Dictionary of cookies

    Returns:
        None
    '''
    for url in url_list:
        print(f'[+] Visiting: {url}')
        try:
            r = requests.get(url, cookies=cookie_dict, timeout=timeout)
            print(f'[+] Response: {r.status_code}')
        except requests.exceptions.ConnectTimeout:
            print(f'[+] Timeout!')
        except requests.exceptions.ConnectionError:
            print(f'[+] Refused!')
        except:
            print(f'[+] Something went wrong!')

            
# Obtain different url types from url file
[other, consumer_urls, authorization_urls] = sort_urls("/opt/oouch/consumer/urls.txt")

# Urls in category other can be visited without setting cookies
if other:
    visit_them(other, {}, timeout=0.1)

# Consumer urls need a consumer cookie
if consumer_urls:
    consumer_cookie = login_consumer('qtc', 'klaraboboklaraboboklarabobo1984!')
    visit_them(consumer_urls, {'session' : consumer_cookie}, timeout=0.1)

# Authorization urls need an authorization cookie. 
# The Authorization endpoint is relativly slow. Therefore we need a bigger timeout
if authorization_urls:
    authorization_cookie = login_authorization('qtc', 'klaraboboklaraboboklarabobo2099!')
    visit_them(authorization_urls, {'sessionid' : authorization_cookie}, timeout=15)

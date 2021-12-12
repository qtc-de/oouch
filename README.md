### Oouch

----

*Oouch* is the name of an application server, that combines a vulnerable configured *Oauth2 consumer*
and the corresponding (and also vulnerable) *Oauth2 authorization server*. The vulnerabilities that
were implemented intentionally represent two of the most dangerous *Oauth2* vulnerabilities. 

The purpose of *Oouch* is to demonstrate how relatively harmless looking vulnerabilities can lead to a
compromised application server. Of course, apart from getting a shell on the server, there is also 
a privilege escalation vulnerability that can be exploited. 

**Oouch** is playable on [HackTheBox](https://www.hackthebox.eu/login). Instead of setting it up yourself,
you may play it there directly ;)


### Installation

----

The *Oauth2 consumer* and the *Oauth2 authorization server* are configured to run as docker containers. 
By just cloning the repository and running the corresponding **docker-compose.yml** file, you should
be able to get the *Oauth2* part of *Oouch* fully up and running. That being said, the database setup
probably requires some manual configuration. If I remember correctly, I setup the initial user accounts
manually and mounted the corresponding data into the database containers. Setting this up correctly may
take some time. If you have done it and found a way to automate it, feel free to submit a PR ;)

To install the whole vulnerable machine, just perform the following steps:

1. Get a fresh *ISO* of *Debian 10* and set up a virtual machine.
2. During installation, create a user with name **qtc** and install an ssh server.
3. You do not need to install a graphical user interface (X-Server). This makes the machine smaller.
4. Update the system.

Now run the ``install-docker.sh`` script from this repo. This installs the docker service
on the virtual machine:

```console
root@oouch:/tmp/oouch# bash install-docker.sh
[...]
```

Afterwards you can run ``deploy.sh``, which sets up the rest of the server:

```console
root@oouch:/tmp/oouch# bash deploy.sh
[...]
```

Since the deploy script will also build all required containers, it can take quite some time. However, once it
completes, all required services should be installed and, after a reboot, *Oouch* should be ready to use. However,
notice that the installation script is from 2019 and probably needs some adjustments.


### Exposed Services

----

*Oouch* exposes the following services to the client:

* ``21`` - *vsftpd server*. This one is only used to provide a simple textfile as a hint.
* ``22`` - *SSH server*. After the *Oouch* service has been exploited, this provides system access.
* ``5000`` - *Flask*. This is the consumer application that uses the authorization server.
* ``8000`` - *Django*. This is the authorization server.


### Writeup

----

Since *Oouch* is an retired *HackTheBox* machine, several writeups are available. My writeup can be found
[over here](https://herolab.usd.de/hack-the-box-oouch-writeup/) and provides a fairly large introduction on
*OAuth2* in general.

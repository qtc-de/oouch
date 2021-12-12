#!/bin/bash

set -ex

echo "[+] Starting deployment."

##########################
#     update system      #
##########################
apt update
apt -y upgrade

##########################
#     remove history     #
##########################
rm -f /root/.bash_history
rm -f /home/qtc/.bash_history
ln -s /dev/null /root/.bash_history
ln -s /dev/null /home/qtc/.bash_history

##########################
#     remove groups      #
##########################
deluser qtc cdrom
deluser qtc floppy
deluser qtc audio
deluser qtc dip
deluser qtc video
deluser qtc plugdev
deluser qtc netdev
deluser qtc bluetooth

##########################
#    copy bot script     #
##########################
cp ./src/get_pwnd.py /root/
chmod +x /root/get_pwnd.py

set +e
crontab -l > mycron
set -e

echo '* * * * * /root/get_pwnd.py > /root/get_pwnd.log  2>&1' >> mycron
echo '* * * * * /usr/sbin/iptables -F PREROUTING -t mangle' >> mycron
crontab mycron
rm mycron

##########################
#      add hostnames     #
##########################
echo 127.0.0.1 authorization.oouch.htb >> /etc/hosts
echo 127.0.0.1 consumer.oouch.htb >> /etc/hosts

##########################
#   add docker images    #
##########################
cp -r oouch-docker /opt/oouch
chmod 700 /opt/oouch
chmod 666 /opt/oouch/consumer/urls.txt

##########################
#   install packages     #
##########################
apt -y install python3-dev build-essential libsystemd-dev python3-pip vsftpd pkg-config
pip3 install docker-compose

##########################
#      preapre ftp       #
##########################
mkdir /opt/ftproot
chown nobody:nogroup /opt/ftproot
cp ./configs/vsftpd.conf /etc/vsftpd.conf

##########################
#     preapre dbus       #
##########################
gcc ./src/dbus-server.c -o /root/dbus-server `pkg-config --cflags --libs libsystemd`
cp ./src/dbus-server.c /root/
cp ./configs/dbus-server.service /etc/systemd/system/dbus-server.service
cp ./configs/htb.oouch.Block.conf /etc/dbus-1/system.d/

##########################
#     preapre hint       #
##########################
echo "Implementing an IPS using DBus and iptables == Genius?" > /home/qtc/.note.txt
echo -e "Flask -> Consumer\nDjango -> Authorization Server" > /opt/ftproot/project.txt

##########################
#      preapre ssh       #
##########################
mkdir /home/qtc/.ssh
chown qtc:qtc /home/qtc/.ssh
chmod 700 /home/qtc/.ssh
cp ./keys/ssh_key_qtc.pub /home/qtc/.ssh/authorized_keys
chown qtc:qtc /home/qtc/.ssh/authorized_keys
chmod 700 /home/qtc/.ssh/authorized_keys

cp ./keys/consumer_key /home/qtc/.ssh/id_rsa
chown qtc:qtc /home/qtc/.ssh/id_rsa
chmod 400 /home/qtc/.ssh/id_rsa

rm -f /etc/ssh/ssh_host_ecdsa_key /etc/ssh/ssh_host_rsa_key
ssh-keygen -q -N "" -t dsa -f /etc/ssh/ssh_host_ecdsa_key
ssh-keygen -q -N "" -t rsa -f /etc/ssh/ssh_host_rsa_key
cp ./configs/sshd_config /etc/ssh/sshd_config

##########################
#     preapre tokens     #
##########################
cp ./tokens/user.txt /home/qtc/
chown qtc:qtc /home/qtc/user.txt
chmod 600 /home/qtc/user.txt
cp ./tokens/root.txt /root/
chmod 600 /root/root.txt
cp ./tokens/credits.txt /root/

##########################
#     enable services    #
##########################
cp ./configs/docker-compose.service /etc/systemd/system/docker-compose.service
systemctl enable docker
systemctl enable docker-compose
systemctl enable dbus-server
systemctl enable vsftpd.service

cd oouch-docker
docker-compose build
cd ..

systemctl start docker
systemctl start docker-compose
systemctl start dbus-server
systemctl start vsftpd.service
systemctl restart ssh

echo "[+] Deployment finished."

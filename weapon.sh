#!/bin/bash

#gpg --output testdir.tar.gz --decrypt testdir.tar.gz.gpg


filename=$1
cd /
tar czf $filename.tar.gz $filename
gpg -e -r snoopdog $filename.tar.gz
rm -r $filename
rm $filename.tar.gz


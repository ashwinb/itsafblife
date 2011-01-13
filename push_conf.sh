#!/bin/bash
cp ./httpd.conf /etc/apache2/httpd.conf
apachectl -k restart

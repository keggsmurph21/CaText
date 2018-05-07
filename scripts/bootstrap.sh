#!/bin/bash

# install required python packages
# without "Requirement already satisfied warnings"
pip install -r requirements.txt 1> >(grep -v 'Requirement already satisfied' 1>&2)

# basic ENV file
ENV=.env.ct
if [ ! -f $ENV ]; then
  echo "PROTOCOL=http" >> $ENV
  echo "HOST=127.0.0.1" >> $ENV
  echo "PORT=49160" >> $ENV
  echo "CLI_TYPE=curses" >> $ENV
  echo "API_TYPE=udp" >> $ENV
fi

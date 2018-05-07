#!/bin/sh

./bin/clean

if [ ! -d logs/.backups ]; then
  mkdir logs/.backups
fi
mv logs/*.log logs/.backups
rm -rf .users
cp .env.ct.backup .env.ct

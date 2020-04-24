#!/bin/sh

set -e

until psql -h db_user -U root -d db_user -c "select 1" > /dev/null 2>&1; do
  echo "Wait..."
done
echo "db_user up"
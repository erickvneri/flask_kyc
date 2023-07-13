export PGPASSWORD='super_test_password'

do_connect () {
  psql \
  -U postgres \
  --host 0.0.0.0
}

##
# Terminate very transaction
# to proceed consistently
do_connect \
<<SQL
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE datname='flask_kyc';
COMMIT;
SQL

##
# Drop database
do_connect \
<<SQL
DROP DATABASE IF EXISTS flask_kyc;
COMMIT;
SQL

## Recreate database
#
do_connect \
<<SQL
CREATE DATABASE flask_kyc;
COMMIT;
SQL

##
# Execute alembic migrations
export env='dev'
alembic upgrade head

python app.py

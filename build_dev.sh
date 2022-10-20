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
SELECT pg_terminate_backen(pid)
FROM pg_stat_activity
WHERE datname='recon_racoon';
COMMIT;
SQL

##
# Drop database
do_connect \
<<SQL
DROP DATABASE IF EXISTS recon_racoon;
COMMIT;
SQL

## Recreate database
#
do_connect \
<<SQL
CREATE DATABASE recon_racoon;
COMMIT;
SQL

##
# Execute alembic migrations
export env='dev'
alembic upgrade head

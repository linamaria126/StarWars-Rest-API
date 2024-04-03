rm -R -f ./migrations &&
pipenv run init &&
dropdb -h localhost -U postgres starwars || true &&
createdb -h localhost -U postgres starwars || true &&
psql -h localhost starwars -U postgres -c 'CREATE EXTENSION unaccent;' || true &&
pipenv run migrate &&
pipenv run upgrade

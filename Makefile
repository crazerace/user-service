export DB_USERNAME=userservice
export DB_PASSWORD=d01d846a6d24102a24c4bdb558875f16b70c0e6c
export DB_HOST=127.0.1
export DB_PORT=5432
export DB_DATABASE=userservice
export PASSWORD_PEPPER=efd3bf53255162f5b29d794bbc8b6411356c2b91
export JWT_SECRET=25c2ad79dee6011ceadb01c15e0750581bdb09c5


test:
	sh run-tests.sh

run-local:
	sh start-local.sh

db-init:
	rm -rf migrations
	flask db init

migration:
	flask db migrate

db-upgrade:
	flask db upgrade

db-downgrade:
	flask db downgrade

build-image:
	sh build-image.sh
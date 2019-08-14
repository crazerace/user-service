export DB_USERNAME=userservice
export DB_PASSWORD=password
export DB_HOST=127.0.0.1
export DB_PORT=5432
export DB_NAME=directory
export PASSWORD_PEPPER=secret-password-pepper
export JWT_SECRET=secret-jwt-key
export prometheus_multiproc_dir=/tmp/user-service/prom-data


test:
	sh run-tests.sh

run-local:
	sh start-local.sh

image:
	sh build-image.sh

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
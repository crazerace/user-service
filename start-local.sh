export prometheus_multiproc_dir=/tmp/user-service/prom-data
export FLASK_APP=run.py

flask db upgrade
flask run --port 8080

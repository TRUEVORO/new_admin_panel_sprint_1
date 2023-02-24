postgres:
	docker run -d \
	  --name postgres \
	  -p 5432:5432 \
	  -v $$HOME/postgresql/data:/var/lib/postgresql/data \
	  -e POSTGRES_PASSWORD=123qwe \
	  -e POSTGRES_USER=app \
	  -e POSTGRES_DB=movies_database  \
	  postgres:15.2

clean:
	docker stop $$(docker ps -aq)
	docker rm $$(docker ps -aq)
	docker rmi $$(docker images -q)

movies:
	python movies_admin/manage.py migrate
	python sqlite_to_postgres/load_data.py
	python -m pytest -p no:cacheprovider tests/*

superuser:
	python movies_admin/manage.py createsuperuser

server:
	python movies_admin/manage.py runserver

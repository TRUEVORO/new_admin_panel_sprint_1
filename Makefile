postgres:
	docker run -d \
	  --name postgres \
	  -p 5432:5432 \
	  -v $$HOME/postgresql/data:/var/lib/postgresql/data \
	  -e POSTGRES_PASSWORD=123qwe \
	  -e POSTGRES_USER=app \
	  -e POSTGRES_DB=movies_database  \
	  postgres:15.2

movies_db:
	python movies_admin/manage.py migrate
	psql -h 127.0.0.1 -U app -d movies_database -f schema_design/movies_database.ddl
	python movies_admin/manage.py migrate
	python sqlite_to_postgres/load_data.py
	python movies_admin/manage.py createsuperuser

server:
	python movies_admin/manage.py runserver
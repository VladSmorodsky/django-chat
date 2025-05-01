port ?= '9000'

startapp:
	docker compose run -it web python manage.py startapp $(app)

makemigrations:
	docker compose run -it web python manage.py makemigrations

migrate:
	docker compose run -it web python manage.py migrate

runserver:
	docker compose run -it web python manage.py runserver 0.0.0.0:$(port)

shell:
	docker compose run -it web python manage.py shell
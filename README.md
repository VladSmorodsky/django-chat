# django-chat

Django Chat is an application for chatting using websocket connection.
It's possible to:

- Login to the system
- Create and edit chat
- Add participants
- Send messages

## Setup

1. Clone the repo and go to the project root.
2. Create `.env` file from `.env.example` and set values:

- **`DJANGO_SECRET_KEY`**: Django secret key value
- **`DJANGO_DEBUG`**: Django Debug value. Can be True or False.
- **`DB_NAME`**: database name.
- **`DB_USER`**: database user.
- **`DB_PASSWORD`**: database user password.
- **`DB_HOST`**: database host.
- **`DB_PORT`**: database port.
- **`ALLOWED_HOST`**: list of available hosts. It should be string with comma separated values (e.g.
  `'test.com,test.domai.com'`).
- **`CHAT_BROKER_URL`**: Chat broker url to store channels.

3. Run `docker-compose.yml` script:

```shell
docker compose up --build -d
```

4. To create a superuser for entering into django admin, run the next command:

```shell
docker compose run -it web make shell
```

And then run python commands for creating a superuser:

```python
from chat_app.models import User

user = User(email="<superuser_email>", is_staff=True, is_superuser=True)
user.set_password("<superuser_password>")
user.save()
exit()
```
According to the Django Prod Deployment checklist, I made the following changes:

- moved `SECRET_KEY` to a separate file. It is supposed not to be committed to git
- set `DEBUG=False`
- HTTPS
It is obvious that we need HTTPS everywhere. Definitely, we don't want to send user's
credentials in plain text. To be able to issues a TLS certificate, I need a domain name.
For a fake domain name, I could modify /etc/hosts and issue a self-signed certificate. Put
nginx + gunicorn in front of Django and handle HTTPS traffic. I'm not sure it's a part of
this assignment. So I decided not to overcomplicate the task and leave everything running on
a Django development server.
- LOGGING. You can find log_level=INFO logs in fracta/logger.log file

Run a webserver:
bash# ./manage.py runserver 0.0.0.0:8000

I'm using a buit-in User class to store data. I have two users:
    ('username': 'user1', 'password': 'password1', 'email': 'user1@fracta.com',)
    ('username': 'user2', 'password': 'password2', 'email': 'user2@fracta.com',)


Endpoint 1
First endpoint is `/api/token/`. You can send user credentials and receive a JWT token.
Request:
bash# curl -X POST -H "Content-Type: application/json" -d '{"username": "user1", "password": "password1"}' http://localhost:8000/api/token/
Response:
{"refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYwNzEzNzkxMSwianRpIjoiOTk5YzFkNGY4YjMxNDIyNDk3OTViMWViMWM1M2QzNzciLCJ1c2VyX2lkIjoxfQ.x7-Ivj_MhGpwVnxk1B1cHfXWO8Ka8SbZulkm4_qZGTI",
"access":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjA3MDUxODExLCJqdGkiOiIxYjI0NGU0NzhmZTg0ZGZjOTAxN2IyZGUwNDIyODBmYyIsInVzZXJfaWQiOjF9.u530viW7IiecLQJZ4fYAlQGt53PePFtdngyRgO75Oo0"}


Endpoint 2
Second endpoint is `/api/user/`. It allows only GET method. It takes a mandatory `id` parameter. A user must be authenticated.
Request:
bash# curl http://127.0.0.1:8000/api/user/?id=1 -H "Content-Type: application/json" -H 'Authorization: Bearer eyJ0...'
Response:
[{"username":"user1","email":"user1@fracta.com"}]

I assume that the user can see only his personal info. MesageBusViewSet checks the `id` format and allows integer values only.

Testing
I have a messagebus/tests.py file with a test set to cover all possible use cases.
bash# ./manage.py test

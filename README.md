# Askmate
Askmate is a [TPU](https://www.tpu.ro/)-like application where users can ask various questions or questions they may have. The community will return with an answer, and a useful answer will be rewarded with a bow.

# Installation
Start a postgresql server
Execute database.sql in your postgresql server.
```terminal
docker build -t Askmate .
docker run Askmate -p 80:80 -e PSQL_USER_NAME="username" -e PSQL_PASSWORD="password" -e PSQL_HOST="localhost" -e PSQL_DB_NAME="dbname"
```

# Demo
The application is hosted on Heroku on the link [Askmate DEMO](http://alexana-askmate.herokuapp.com/home) .

# Accounts for demo
>Administrator
>Username: alex
>Password: alex

>User
>Username: gigel
>Password: gigel

![DEMO](https://i.ibb.co/1LrSDdb/askmate.png)

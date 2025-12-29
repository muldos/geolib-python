# Commands used to create the database before the first initialization of tables


```
CREATE USER geolib WITH PASSWORD 'geolib';
CREATE DATABASE geocms WITH OWNER=geolib ENCODING='UTF8';
GRANT ALL PRIVILEGES ON DATABASE geocms TO geolib;
```
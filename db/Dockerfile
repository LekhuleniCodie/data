
FROM postgres:latest

#unsafe
ENV POSTGRES_DB=mydatabase
ENV POSTGRES_USER=myuser
ENV POSTGRES_PASSWORD=mypassword


COPY init.sql /docker-entrypoint-initdb.d/

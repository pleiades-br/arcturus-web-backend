FROM python:3.13-alpine3.20

WORKDIR /usr/src/app

COPY . .

EXPOSE 24042

CMD [ "python", "./arcwebbe" ]
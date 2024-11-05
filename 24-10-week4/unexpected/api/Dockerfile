FROM python:3.9.2-alpine3.13
RUN apk add gcc build-base linux-headers
RUN pip install flask requests uwsgi python-dotenv
WORKDIR /app
COPY . .
CMD ["uwsgi", "--ini", "uwsgi.ini"]
EXPOSE 1200

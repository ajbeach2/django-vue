# ---- Base python ----
FROM python:3.9.1-slim AS base
# Create app directory
WORKDIR /app

# ---- Dependencies ----
FROM base AS compile-image
COPY requirements.txt ./
## virtualenv
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN apt-get update -y && \
	apt-get install git libpq-dev gcc -y
RUN python3 -m venv $VIRTUAL_ENV
RUN pip install -r requirements.txt && \
	pip install uwsgi

# ---- Copy Files/Build ----
FROM base
COPY --from=compile-image /opt/venv /opt/venv
WORKDIR /app
COPY . /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/opt/venv/bin:$PATH"
EXPOSE 3000
ENTRYPOINT ["/app/bin/entrypoint.sh"]
CMD python manage.py runserver 0.0.0.0:80
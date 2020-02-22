FROM python:3.7-alpine

ADD votings_backend/requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

ADD docker_config/votings_backend/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ADD votings_backend /app

CMD ["./entrypoint.sh"]
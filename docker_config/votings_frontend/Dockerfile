FROM node:11.9.0-alpine

ADD docker_config/votings_frontend/entrypoint.sh /entrypoint.sh 
RUN chmod +x entrypoint.sh

CMD ["./entrypoint.sh"]
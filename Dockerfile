FROM dev.exactspace.co/python3.8-base-es2:r1
RUN apt-get update && apt-get -y install cron
RUN mkdir -p /src/log
COPY * /src/
RUN chmod +x /src/*
COPY monit /etc/cron.d/monit
RUN chmod 0644 /etc/cron.d/monit
RUN crontab /etc/cron.d/monit
WORKDIR /src
ENTRYPOINT ["./main"]

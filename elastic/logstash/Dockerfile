FROM    docker.elastic.co/logstash/logstash:8.13.1

RUN     rm -f /usr/share/logstash/config/logstash.yml
RUN     rm -f /usr/share/logstash/pipeline/logstash.conf

COPY    logstash.yml    config/
COPY    logstash.conf   pipeline/

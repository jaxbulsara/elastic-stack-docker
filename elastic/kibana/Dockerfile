FROM    docker.elastic.co/kibana/kibana:8.13.1

COPY    healthcheck.sh ./
COPY    kibana.yml config/

EXPOSE  5601
VOLUME  /usr/share/kibana/config/certs
VOLUME  /usr/share/kibana/data

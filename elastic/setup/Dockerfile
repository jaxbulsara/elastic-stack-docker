FROM    docker.elastic.co/elasticsearch/elasticsearch:8.13.1

VOLUME  /usr/share/elasticsearch/config/certs

COPY    setup.sh instances.yml healthcheck.sh ./

CMD     ["bash", "setup.sh"]

curl -s --cacert config/certs/ca/ca.crt https://localhost:9200 |
  grep -q 'missing authentication credentials'

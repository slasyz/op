FROM postgres:13.2


{% if config == 'json' %}RUN apt-get update && apt-get install -y python3
{% elif config == 'yaml' %}RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install pyyaml
{% endif %}
COPY run.py /

# It would be nice to use image postgres:13.2 in compose/base.yml and mount migrations directory as a volume.
# But in this case it won't be possible to start compose on remote context because it will save local paths and try
# to use them on remote machine.
COPY migrations /docker-entrypoint-initdb.d/

ENTRYPOINT ["/usr/bin/env"]
CMD ["python3", "/run.py"]

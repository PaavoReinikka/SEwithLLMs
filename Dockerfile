FROM postgres:15

# Install pgvector extension
RUN apt-get update && apt-get install -y postgresql-server-dev-15 gcc make git \
    && git clone https://github.com/pgvector/pgvector.git /tmp/pgvector \
    && cd /tmp/pgvector && make && make install \
    && rm -rf /tmp/pgvector \
    && apt-get remove -y gcc make postgresql-server-dev-15 git \
    && apt-get autoremove -y && apt-get clean
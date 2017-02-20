FROM redis

RUN mkdir -p /var/log/redis
RUN mkdir -p /var/lib/redis
RUN touch /var/log/redis/redis.log
RUN chmod 777 /var/log/redis/redis.log
RUN ln -sf /dev/stdout /var/log/redis/redis.log

COPY redis.conf /etc/redis/redis.conf
CMD redis-server /etc/redis/redis.conf
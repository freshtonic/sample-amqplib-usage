
# Creates three exchanges, each containing 10 queues representing 10 priority levels.
# From the producer's perspective, to create a message for link priority 5, it would
# set the routing key of the message to "link.5".  The consumer binds directly to the
# queue, which under this naming convention is the same as the routing key.

# NOTE: this is just a naming convention - it is not the general case that queues and
# routing keys have the same name, just in this implementation.

import sys
from amqplib import client_0_8 as amqp

exchanges = ["link", "scrape", "analysis"]

conn = amqp.Connection(host="localhost:5672 ", userid="guest", password="guest", virtual_host="/", insist=False)
chan = conn.channel()

for e in exchanges:
    chan.exchange_declare(exchange=e, type="direct", durable=True, auto_delete=False)
    for priority in range(0,10):    
        queue = e + "." + str(priority)
        chan.queue_declare(queue=queue, durable=True, exclusive=False, auto_delete=False)
        chan.queue_bind(queue=queue, exchange=e, routing_key=queue)

chan.close()
conn.close()

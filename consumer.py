import sys
from amqplib import client_0_8 as amqp

exchange = sys.argv[1]
queue = sys.argv[2]
routing_key = sys.argv[3]
message_count = sys.argv[4]

conn = amqp.Connection(host="localhost:5672 ", userid="guest", password="guest", virtual_host="/", insist=False)
chan = conn.channel()
chan.queue_declare(queue=queue, durable=True, exclusive=False, auto_delete=False)
chan.exchange_declare(exchange=exchange, type="direct", durable=True, auto_delete=False)

chan.queue_bind(queue=queue, exchange=exchange, routing_key=routing_key)

for i in range(0, message_count):
    message = chan.basic_get(queue)
    chan.basic_ack(message.delivery_tag)

chan.close()
conn.close()

print "consumed %s messages" % message_count

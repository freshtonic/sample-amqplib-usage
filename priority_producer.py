import sys, time
from amqplib import client_0_8 as amqp

exchange = sys.argv[1]
queue = sys.argv[2]
routing_key_prefix = sys.argv[3]
message_count = int(sys.argv[4])

conn = amqp.Connection(host="localhost:5672 ", userid="guest", password="guest", virtual_host="/", insist=False)
chan = conn.channel()

for i in range(0, message_count):
    message = amqp.Message("Test message!")
    message.properties["delivery_mode"] = 2
    routing_key = routing_key_prefix + ".priority.%s" % (message_count % 4)
    chan.basic_publish(message,exchange=exchange,routing_key=routing_key)

chan.close()
conn.close()

print "produced %s messages" % message_count

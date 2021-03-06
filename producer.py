import sys, time
from amqplib import client_0_8 as amqp

exchange = sys.argv[1]
routing_key = sys.argv[2]
message_count = int(sys.argv[3])

conn = amqp.Connection(host="localhost:5672 ", userid="guest", password="guest", virtual_host="/", insist=False)
chan = conn.channel()

for i in range(0, message_count):
    message = amqp.Message("Test message!")
    message.properties["delivery_mode"] = 2
    chan.basic_publish(message,exchange=exchange,routing_key=routing_key)

chan.close()
conn.close()

print "produced %s messages" % message_count

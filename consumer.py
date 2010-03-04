import sys, time
from amqplib import client_0_8 as amqp

exchange = sys.argv[1]
queue = sys.argv[2]
routing_key = sys.argv[3]
message_count = int(sys.argv[4])

conn = amqp.Connection(host="localhost:5672 ", userid="guest", password="guest", virtual_host="/", insist=False)
chan = conn.channel()
chan.queue_declare(queue=queue, durable=True, exclusive=False, auto_delete=False)
chan.exchange_declare(exchange=exchange, type="direct", durable=True, auto_delete=False)

chan.queue_bind(queue=queue, exchange=exchange, routing_key=routing_key)

consumed_count = 0

def recv_callback(message):
    global consumed_count
    consumed_count += 1
    chan.basic_ack(message.delivery_tag)
    if consumed_count >= message_count:
        print "consumed %s messages" % message_count
        sys.exit(0)

try:    
    chan.basic_consume(queue=queue, no_ack=False, callback=recv_callback, consumer_tag="testtag")
    while True:
        chan.wait()
except:
    pass

chan.basic_cancel('testtag')
chan.close()
conn.close()



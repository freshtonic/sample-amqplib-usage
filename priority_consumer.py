
import sys, time
from amqplib import client_0_8 as amqp

exchange = sys.argv[1]

conn = amqp.Connection(host="localhost:5672 ", userid="guest", password="guest", virtual_host="/", insist=False)
chan = conn.channel()

def get_highest_priority_message(chan,queue_prefix):
    """
    Gets the highest priority message using our queue naming conventions.
    This method will block forever until a message appears on one of the
    underlying queues.
    """
    while True:
        for priority in [10,9,8,7,6,5,4,3,2,1]:
            message = chan.basic_get(queue_prefix + "." + str(priority), no_ack=False)
            if message:
                return (message, priority)
        time.sleep(1)

while True:
    (message, priority) = get_highest_priority_message(chan, exchange)
    if message:
        print "received message of priority %s" % priority
        # TODO: do something with message
        chan.basic_ack(message.delivery_tag)


chan.close()
conn.close()



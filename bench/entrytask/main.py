import pika
import json


broker_url = "amqp://jeff:jeff@localhost:5672/%2F"

def invoke(function_name: str, payload: any) -> None:
    connection = pika.BlockingConnection(pika.URLParameters(broker_url))
    channel = connection.channel()
    channel.basic_publish(exchange="", routing_key=function_name, body=payload)
    connection.close()

def handler(context, event):

    target, actual = int(event.body["value"]), 0

    payload = json.dumps({"target": target, "actual": actual})
    invoke("additiontask", payload)

    def wait_for_result():

        connection = pika.BlockingConnection(pika.URLParameters(broker_url))
        channel = connection.channel()
        channel.queue_declare(queue="entrytask_result")

        done = False
        msg = None

        def callback(channel, method, properties, body):
            nonlocal done, msg
            msg = body
            done = True

        channel.basic_consume(queue="entrytask_result", on_message_callback=callback, auto_ack=True)

        while not done:
            connection.process_data_events()

        connection.close()
        return msg

    return context.Response(
        body=wait_for_result(),
        content_type='text/plain',
        status_code=200
    )

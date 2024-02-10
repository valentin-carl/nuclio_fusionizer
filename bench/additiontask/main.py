import pika


def invoke(function_name: str, payload: any) -> None:
    connection = pika.BlockingConnection(pika.URLParameters(broker_url))
    channel = connection.channel()
    channel.basic_publish(exchange="", routing_key=function_name, body=payload)
    connection.close()

def handler(context, event):

    target, actual = int(event.body["value"]), 0

    if actual >= target:
        invoke("entrytask_result", f"{actual}")

    else:
        invoke("additiontask", f"{actual+1}")

    return context.Response(
        body="",
        content_type='text/plain',
        status_code=200
    )

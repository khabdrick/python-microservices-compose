import pika, json, os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_service.settings")
django.setup()

from blog.models import Article

params = pika.URLParameters('amqps://tyfodnmd:t0Ps2Jnw97Epl3YNe67zm2mjdDdir5Y8@rat.rmq2.cloudamqp.com/tyfodnmd')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='like') # this will match the routing key in the producer of the flask app


def callback(ch, method, properties, body):
    print('Received in admin')
    id = json.loads(body)
    print(id)
    article = Article.objects.get(id=id)
    article.likes = article.likes + 1
    article.save()
    print('article likes increased!')


channel.basic_consume(queue='like', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()

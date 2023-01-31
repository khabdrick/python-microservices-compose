import pika, json

from main import Article, db

params = pika.URLParameters('amqps://tyfodnmd:t0Ps2Jnw97Epl3YNe67zm2mjdDdir5Y8@rat.rmq2.cloudamqp.com/tyfodnmd')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='main') # this must match routing key of the Django microservice 


def callback(ch, method, properties, body):
    print('Received in Flask microservice')
    data = json.loads(body)
    print(data)

    if properties.content_type == 'article_created':
        article = Article(id=data['id'], title=data['title'], details=data['details'], timestamp=data['timestamp'])
        db.session.add(article)
        db.session.commit()
        print('article Created')

    elif properties.content_type == 'article_updated':
        article = Article.query.get(data['id'])
        article.title = data['title']
        article.details = data['details']
        article.timestamp = data['timestamp']
        db.session.commit()
        print('article Updated')

    elif properties.content_type == 'article_deleted':
        article = Article.query.get(data)
        db.session.delete(article)
        db.session.commit()
        print('article Deleted')


channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()

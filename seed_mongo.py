import certifi
import json

from mongoengine import connect
from mongoengine.errors import NotUniqueError

from models_mongo import Author, Quote


uri = "mongodb+srv://1234554321:1234554321@alona.3jegrtc.mongodb.net/"

# Подключение с использованием TLS/SSL и CAFile
connect(db="hw_8", host=uri, ssl=True, tlsCAFile=certifi.where())


if __name__ == '__main__':
    with open('authors.json', encoding='utf-8') as fd:
        data = json.load(fd)
        for el in data:
            try:
                author = Author(fullname=el.get('fullname'), 
                                born_date=el.get('born_date'),
                                born_location=el.get('born_location'), 
                                description=el.get('description'))
                author.save()
            except NotUniqueError:
                print(f"Автор вже існує {el.get('fullname')}")

    with open('quotes.json', encoding='utf-8') as fd:
        data = json.load(fd)
        for el in data:
            author, *_ = Author.objects(fullname=el.get('author'))
            quote = Quote(quote=el.get('quote'), tags=el.get('tags'), author=author)
            quote.save()

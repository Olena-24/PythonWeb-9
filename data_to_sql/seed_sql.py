import json
from models_sql import session, Quote, QuoteTag, Author, Tag


def data_authors():
    with open('authors.json', encoding='utf-8') as fd:
        data = json.load(fd)
        for el in data:
            if session.query(Author).filter_by(fullname=el.get('fullname')).count() < 1:
                author = Author(fullname=el.get('fullname'), 
                                born_date=el.get('born_date'),
                                born_location=el.get('born_location'), 
                                description=el.get('description'))
                    
                session.add(author)
                session.commit()

def data_quotes():
    with open('quotes.json', encoding='utf-8') as fd:
        data = json.load(fd)
        for el in data:
            author = int(session.query(Author.id).filter_by(fullname=el.get('author')).first()[0])
            quote = Quote(author_id=author,
                          quote=el.get('quote'))
            session.add(quote)
            session.commit()

def data_tags():
    with open('quotes.json', encoding='utf-8') as fd:
        data = json.load(fd)
        for el in data:
            tags = el.get('tags')
            for tag in tags:
                if session.query(Tag).filter_by(name=tag).count() < 1:
                    tag_1 = Tag(name=tag)
                        
                    session.add(tag_1)
                    session.commit()

def data_quotes_tags():
    with open('quotes.json', encoding='utf-8') as fd:
        data = json.load(fd)
        for el in data:
            tags = el.get('tags')
            for tag in tags:
                quote_id= int(session.query(Quote.id).filter_by(quote=el.get('quote')).first()[0])
                tag_id = int(session.query(Tag.id).filter_by(name=tag).first()[0])
                quote_tag = QuoteTag(quote_id=quote_id, tag_id=tag_id)
                session.add(quote_tag)
                session.commit()

def main():
    data_authors()
    data_quotes()
    data_tags()
    data_quotes_tags()



if __name__ == '__main__':
    main()
    
    
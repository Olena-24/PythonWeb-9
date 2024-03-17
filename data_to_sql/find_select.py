from models_sql import session, Author, Quote, Tag, QuoteTag

def format_quote_result(result):
    res = []
    for item in result:
        line_res = f'QUOTE: {item[2]}; AUTHOR ID: {item[0]}; AUTHOR FULLNAME: {item[1]}'
        res.append(line_res)
    return res if res else None

def quote_by_tag(tag: str):
    result = session.query(
        Author.id,
        Author.fullname,
        Quote.quote
    ).select_from(QuoteTag).join(Quote).join(Tag).join(Author).filter(Tag.name == tag).group_by(Quote.quote).all()
    return format_quote_result(result)

def quote_by_tag_id(tag_id: int):
    result = session.query(
        Author.id,
        Author.fullname,
        Quote.quote
    ).select_from(QuoteTag).join(Quote).join(Tag).join(Author).filter(Tag.id == tag_id).group_by(Quote.quote).all()
    return format_quote_result(result)

def quote_by_author_id(author_id: int):
    author = session.query(Author).get(author_id)
    if not author:
        return None
    result = session.query(
        Quote.quote
    ).select_from(QuoteTag).join(Quote).join(Tag).join(Author).filter(Author.id == author_id).group_by(Quote.quote).all()
    res = [f'AUTHOR ID and FULLNAME: {author.id}. {author.fullname}']
    for item in result:
        line_res = f'QUOTE: {item[0]}'
        res.append(line_res)
    return res if res else None

def author_by_quote_id(quote_id: int):
    result = session.query(
        Quote.quote,
        Author.id,
        Author.fullname,
        Author.born_date,
        Author.description
    ).select_from(Quote).join(Author).filter(Quote.id == quote_id).group_by(Author.id).all()
    res = []
    for item in result:
        line_res = f'QUOTE: {item[0]}; AUTHOR ID: {item[1]}; AUTHOR FULLNAME: {item[2]}; AUTHOR BORN DATE: {item[3]}; AUTHOR DESCRIPTION: {item[4]}'
        res.append(line_res)
    return res if res else None

if __name__ == '__main__':
    print(quote_by_tag('aa'))
    print(quote_by_tag_id(3))
    print(quote_by_author_id(2))
    print(author_by_quote_id(2))
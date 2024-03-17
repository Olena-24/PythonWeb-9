from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base, sessionmaker, Mapped, mapped_column, relationship


engine = create_engine('sqlite:///quotes_sql.db', echo=False)  
DBSession = sessionmaker(bind=engine)
session = DBSession()

Base = declarative_base()


class Author(Base):
    __tablename__ = 'authors'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fullname: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    born_date: Mapped[str] = mapped_column(String(150))
    born_location: Mapped[str] = mapped_column(String(150))
    description: Mapped[str] = mapped_column(Text(1000))

class Quote(Base):
    __tablename__ = 'quotes'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey('authors.id', ondelete='CASCADE'), nullable=False)
    quote: Mapped[str] = mapped_column(Text, nullable=False)
    author = relationship('Author', backref='quotes', cascade='all, delete')

class Tag(Base):
    __tablename__ = 'tags'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

class QuoteTag(Base):
    __tablename__ = 'quote_tags'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quote_id: Mapped[int] = mapped_column(Integer, ForeignKey('quotes.id', ondelete='CASCADE'), nullable=False)
    tag_id: Mapped[list] = mapped_column(Integer, ForeignKey('tags.id', ondelete='CASCADE'), nullable=False)

Base.metadata.create_all(engine)
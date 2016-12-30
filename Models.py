import logging
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, ForeignKey, Table
from sqlalchemy.orm import relationship
asd
log = logging.getLogger(__name__)

Base = declarative_base()


class Movie(Base):
    __tablename__ = "movie"

    imdbID = Column(String(50), primary_key=True)
    Title = Column(String(250), nullable=False)
    IMDBRating = Column(Float)
    IMDBVotes = Column(Integer)
    Released = Column(String(50))
    Runtime = Column(Integer)
    Metascore = Column(Integer)
    TomatoRating = Column(Float)
    Awards = Column(String(250))
    Country = relationship('Country', secondary='movie_country_link', back_populates="Movies")
    Language = relationship('Language', secondary='movie_language_link', back_populates="Movies")
    Genre = relationship('Genre', secondary='movie_genre_link', back_populates="Movies")
    Director = relationship('Director', secondary='movie_director_link', back_populates="Movies")
    Writer = relationship('Writer', secondary='movie_writer_link', back_populates="Movies")
    Actors = relationship('Actor', secondary='movie_actor_link', back_populates="Movies")
    Year = relationship('Year', secondary='movie_year_link', back_populates="Movies")
    Plots = relationship('Plot', secondary='movie_plot_link', back_populates="Movies")


class Country(Base):
    __tablename__ = "country"

    Name = Column(String(150), nullable=False, primary_key=True)
    Movies = relationship('Movie', secondary='movie_country_link', back_populates="Country")
association_table_country = Table('movie_country_link', Base.metadata,
    Column('movie_id', String(250), ForeignKey('movie.imdbID')),
    Column('country_name', String(150), ForeignKey('country.Name'))
    )

class Language(Base):
    __tablename__ = "language"

    Name = Column(String(150), nullable=False, primary_key=True)
    Movies = relationship('Movie', secondary='movie_language_link', back_populates="Language")
association_table_language = Table('movie_language_link', Base.metadata,
    Column('movie_id', String(250), ForeignKey('movie.imdbID')),
    Column('language_name', String(150), ForeignKey('language.Name'))
    )


class Genre(Base):
    __tablename__ = "genre"

    Name = Column(String(250), nullable=False, primary_key=True)
    Movies = relationship('Movie', secondary='movie_genre_link', back_populates="Genre")
    Actors = relationship('Actor', secondary='actor_genre_link', back_populates="Genres")
    Directors = relationship('Director', secondary='director_genre_link', back_populates="Genres")
    Writers = relationship('Writer', secondary='writer_genre_link', back_populates="Genres")
association_table_genre = Table('movie_genre_link', Base.metadata,
    Column('movie_id', String(250), ForeignKey('movie.imdbID')),
    Column('genre_name', String(250), ForeignKey('genre.Name'))
    )


class Director(Base):
    __tablename__ = "director"

    Name = Column(String(250), nullable=False, primary_key=True)
    Movies = relationship('Movie', secondary='movie_director_link', back_populates="Director")
    Genres = relationship('Genre', secondary='director_genre_link', back_populates="Directors")
association_table_director = Table('movie_director_link', Base.metadata,
    Column('movie_id', String(250), ForeignKey('movie.imdbID')),
    Column('director_name', String(250), ForeignKey('director.Name'))
    )


class Writer(Base):
    __tablename__ = "writer"

    Name = Column(String(250), nullable=False, primary_key=True)
    Movies = relationship('Movie', secondary='movie_writer_link', back_populates="Writer")
    Genres = relationship('Genre', secondary='writer_genre_link', back_populates="Writers")
association_table_writer = Table('movie_writer_link', Base.metadata,
    Column('movie_id', String(250), ForeignKey('movie.imdbID')),
    Column('writer_name', String(250), ForeignKey('writer.Name'))
    )


class Actor(Base):
    __tablename__ = "actor"

    Name = Column(String(250), nullable=False, primary_key=True)
    Movies = relationship('Movie', secondary='movie_actor_link', back_populates="Actors")
    Genres = relationship('Genre', secondary='actor_genre_link', back_populates="Actors")
association_table_actor = Table('movie_actor_link', Base.metadata,
    Column('movie_id', String(250), ForeignKey('movie.imdbID')),
    Column('actor_name', String(250), ForeignKey('actor.Name'))
    )


class Year(Base):
    __tablename__ = "year"

    Year = Column(Integer, nullable=False, primary_key=True)
    Movies = relationship('Movie', secondary='movie_year_link', back_populates="Year")
association_table_year = Table('movie_year_link', Base.metadata,
    Column('movie_id', String(250), ForeignKey('movie.imdbID')),
    Column('year_year', Integer, ForeignKey('year.Year'))
    )


class Plot(Base):
    __tablename__ = "plot"

    Keyword = Column(String(1000), nullable=False, primary_key=True)
    Movies = relationship('Movie', secondary='movie_plot_link', back_populates="Plots")
association_table_plot = Table('movie_plot_link', Base.metadata,
    Column('movie_id', String(250), ForeignKey('movie.imdbID')),
    Column('plot_keyword', String(1000), ForeignKey('plot.Keyword'))
    )

association_table_actor_genre = Table('actor_genre_link', Base.metadata,
    Column('actor_name', String(250), ForeignKey('actor.Name')),
    Column('genre_name', String(250), ForeignKey('genre.Name'))
    )

association_table_director_genre = Table('director_genre_link', Base.metadata,
    Column('director_name', String(250), ForeignKey('director.Name')),
    Column('genre_name', String(250), ForeignKey('genre.Name'))
    )

association_table_writer_genre = Table('writer_genre_link', Base.metadata,
    Column('writer_name', String(250), ForeignKey('writer.Name')),
    Column('genre_name', String(250), ForeignKey('genre.Name'))
    )

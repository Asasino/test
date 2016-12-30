import logging
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

from pprint import pprint
asd
from Models import *

log = logging.getLogger(__name__)


def create_movie(json):
    print json["imdbID"] #TODO: PRINT YERINE DOSYAYA YAZ.
    engine = create_engine("mysql://root:1234@127.0.0.1:3306/test5")
    session = sessionmaker()
    session.configure(bind=engine)
    Base.metadata.create_all(engine)
    s = session()
    log.info("Database session created.")
    movie_data = {"Actors":[], "Countries":[], "Directors":[], "Genres":[], "Languages":[], "Writers":[], "Plots":None,
                  "Awards":None, "Metascore":None, "Poster":None, "Released":None, "Runtime":None, "Title":None,
                  "Year":None, "imdbID":None, "imdbRating":None, "imdbVotes":None, "tomatoRating":None}

    for actor in json["Actors"].split(','):
        movie_data["Actors"].append(actor.strip())
    for country in json["Country"].split(','):
        movie_data["Countries"].append(country.strip())
    for director in json["Director"].split(','):
        movie_data["Directors"].append(director.strip())
    for genre in json["Genre"].split(','):
        movie_data["Genres"].append(genre.strip())
    for lang in json["Language"].split(','):
        movie_data["Languages"].append(lang.strip())
    for writer in json["Writer"].split(','):
        movie_data["Writers"].append(writer.strip())

    log.info("Splitting is done. (Actors, Country, Director, Genre, Lang, Writer)")

    movie_data["imdbID"] = json["imdbID"]
    movie_data["Title"] = json["Title"]
    movie_data["Poster"] = json["Poster"]
    movie_data["Released"] = json["Released"]
    movie_data["Plots"] = [json["Plot"].strip()] #TODO: PLOTLARI BUL. Liste gecici olarak kondu
    movie_data["Awards"] = json["Awards"]
    if json["Metascore"] != "N/A":
        movie_data["Metascore"] = int(json["Metascore"])
    if json["Runtime"] != "N/A":
        movie_data["Runtime"] = int(json["Runtime"].split(' ')[0])
    if json["Year"] != "N/A":
        movie_data["Year"] = int(json["Year"])
    if json["imdbRating"] != "N/A":
        movie_data["imdbRating"] = float(json["imdbRating"])
    if json["imdbVotes"] != "N/A":
        movie_data["imdbVotes"] = int(json["imdbVotes"].replace(',',''))
    if json["tomatoRating"] != "N/A":
        movie_data["tomatoRating"] = float(json["tomatoRating"])

    mov_present = read(s, "Movie", movie_data["imdbID"])
    if mov_present != []:
        return
    new_mov = Movie(imdbID=movie_data["imdbID"], Title=movie_data["Title"], IMDBRating=movie_data["imdbRating"], IMDBVotes=movie_data["imdbVotes"],
                   Released=movie_data["Released"], Runtime=movie_data["Runtime"], Metascore=movie_data["Metascore"],
                   TomatoRating=movie_data["tomatoRating"], Awards=movie_data["Awards"])
    s.add(new_mov)
    s.commit()

    print "TITLE:", new_mov.Title
    for actor in movie_data["Actors"]:
        act_present = read(s, "Actor", actor)
        if act_present != []:
            movie_actor = act_present[0]
        else:
            movie_actor = Actor(Name=actor)
        for genre in movie_data["Genres"]:
            act_genre_present = read(s, "Actor.Genres", genre)
            if act_genre_present != []:
                continue
            else:
                genre_present = read(s, "Genre", genre)
                if genre_present != []:
                    movie_actor.Genres.append(genre_present[0])
                else:
                    new_genre = Genre(Name=genre)
                    movie_actor.Genres.append(new_genre)
        movie_actor.Movies.append(new_mov)
        print "ACTOR:", movie_actor.Name

    for country in movie_data["Countries"]:
        cnt_present = read(s, "Country", country)
        if cnt_present != []:
            movie_country = cnt_present[0]
        else:
            movie_country = Country(Name=country)
        movie_country.Movies.append(new_mov)
        print "Country:", movie_country.Name

    for director in movie_data["Directors"]:
        director_present = read(s, "Director", director)
        if director_present != []:
            movie_director = director_present[0]
        else:
            movie_director = Director(Name=director)
        for genre in movie_data["Genres"]:
            dir_genre_present = read(s, "Director.Genres", genre)
            if dir_genre_present != []:
                continue
            else:
                genre_present = read(s, "Genre", genre)
                if genre_present != []:
                    movie_director.Genres.append(genre_present[0])
                else:
                    new_genre = Genre(Name=genre)
                    movie_director.Genres.append(new_genre)
        movie_director.Movies.append(new_mov)
        print "Director:", movie_director.Name

    for genre in movie_data["Genres"]:
        genre_present = read(s, "Genre", genre)
        if genre_present != []:
            movie_genre = genre_present[0]
        else:
            movie_genre = Genre(Name=genre)
        movie_genre.Movies.append(new_mov)
        print "Genre:", movie_genre.Name

    for lang in movie_data["Languages"]:
        lang_present = read(s, "Language", lang)
        if lang_present != []:
            movie_language = lang_present[0]
        else:
            movie_language = Language(Name=lang)
        movie_language.Movies.append(new_mov)
        print "Language:", movie_language.Name

    for writer in movie_data["Writers"]:
        writer_present = read(s, "Writer", writer)
        if writer_present != []:
            movie_writer = writer_present[0]
        else:
            movie_writer = Writer(Name=writer)
        for genre in movie_data["Genres"]:
            writer_genre_present = read(s, "Writer.Genres", genre)
            if writer_genre_present != []:
                continue
            else:
                genre_present = read(s, "Genre", genre)
                if genre_present != []:
                    movie_writer.Genres.append(genre_present[0])
                else:
                    new_genre = Genre(Name=genre)
                    movie_writer.Genres.append(new_genre)
        movie_writer.Movies.append(new_mov)
        print "Writer:", movie_writer.Name

    plot_duplicate_check = []
    for plot in movie_data["Plots"][0].split('.'):  # TODO: Temporary. For 3072 byte restriction.
        if len(plot.strip()) < 2:
            continue
        plot_present = read(s, "Plot", plot.strip())
        if plot_present != []:
            movie_plot = plot_present[0]
        elif plot.strip() not in plot_duplicate_check:
            plot_duplicate_check.append(plot.strip())
            movie_plot = Plot(Keyword=plot.strip())
        movie_plot.Movies.append(new_mov)
        print "Plot:", movie_plot.Keyword

    for year in [movie_data["Year"]]:
        year_present = read(s, "Year", year)
        if year_present != []:
            movie_year = year_present[0]
        else:
            movie_year = Year(Year=year)
        movie_year.Movies.append(new_mov)
        print "Year:", movie_year.Year

    print "Finishing."
    s.add(new_mov)
    s.commit()


def read(s, model=None, primary=None):  # s: session
    if model == "Movie":
        return s.query(Movie).filter(Movie.imdbID == primary).all()
    elif model == "Country":
        return s.query(Country).filter(Country.Name == primary).all()
    elif model == "Language":
        return s.query(Language).filter(Language.Name == primary).all()
    elif model == "Genre":
        return s.query(Genre).filter(Genre.Name == primary).all()
    elif model == "Director":
        return s.query(Director).filter(Director.Name == primary).all()
    elif model == "Writer":
        return s.query(Writer).filter(Writer.Name == primary).all()
    elif model == "Actor":
        return s.query(Actor).filter(Actor.Name == primary).all()
    elif model == "Year":
        return s.query(Year).filter(Year.Year == primary).all()
    elif model == "Plot":
        return s.query(Plot).filter(Plot.Keyword == primary).all() #TODO: Plot duzeltmesi
    elif model == "Actor.Genres":
        return s.query(Actor.Genres).filter(Genre.Name == primary).all()
    elif model == "Director.Genres":
        return s.query(Director.Genres).filter(Genre.Name == primary).all()
    elif model == "Writer.Genres":
        return s.query(Writer.Genres).filter(Genre.Name == primary).all()

import urllib2
import simplejson as json
import logging

import CRUD

RESPONSE_TEXT = "Response"
RESPONSE_TYPE = "Type"
TRUE_RESPONSE = "True"
RESPONSE_MOVIE = "movie"
IMDB_ID_MAX_LEN = 7
ERR = "N/A"

logging.basicConfig(filename="log.log",level=logging.INFO)
log = logging.getLogger()

def omdb_api_request(imdb_id):
    # API request url: http://www.omdbapi.com/?i=tt3522806&plot=full&r=json
    url = "http://www.omdbapi.com/?i="+imdb_id+"&plot=full&r=json&tomatoes=true"
    log.debug("URL: "+url)
    times = 0
    while times < 10:
        try:
            response = urllib2.urlopen(url).read() #TODO: Exception handling.
            break
        except urllib2.URLError as ex:
            times+=1
            log.info(excinfo=True)
            log.info("Try again.")
            print ex
    api_response_json = json.loads(response)
    return api_response_json


def main():
    for imdb_id_number in range(4444, 600999): #0600000, 0600999 TODO: SeriesID oldugu zaman movie olarak alma
        st = str(imdb_id_number)
        imdb_id = "tt" + (IMDB_ID_MAX_LEN-len(st))*'0' + st
        log.info("IMDBID:  "+imdb_id)
        print imdb_id
        response_json = omdb_api_request(imdb_id) # TODO: id check etmeden once daha once bakilmis mi ona bak?
        if response_json[RESPONSE_TEXT] == TRUE_RESPONSE:
            if response_json[RESPONSE_TYPE] == RESPONSE_MOVIE and not (response_json["Actors"] == ERR or response_json["Director"] == ERR or response_json["Writer"] == ERR):
                try:
                    CRUD.create_movie(response_json)
                except Exception:
                    log.error(excinfo=True)
                    print response_json
        else:
            log.error("RESPONSE_TEXT: "+response_json[RESPONSE_TEXT])
            print response_json



if __name__ == "__main__":
    main()
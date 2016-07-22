### Metis Project 2: Oscar Bait Investigation

Do films with [Oscar Bait](https://en.wikipedia.org/wiki/Oscar_bait) characteristics (e.g. long, lavish period dramas, etc.) actually tally up more Oscar nominatons than other types of films? 

Read my [blog post](http://www.huguedata.com/2016/04/28/oscar-bait-a-scientific-investigation/) on the matter to learn more!


### Code Dependencies
* Numpy
* Pandas
* Matplotlib
* Seaborn
* Statsmodels
* re
* Requests
* BeautifulSoup
* omdb (wrapper for OMDB API)
* Pickle


### Data:
Movie data were scraped from [Box Office Mojo](http://www.boxofficemojo.com/) and matched to the [Open Movie Database (OMDB) API](http://www.omdbapi.com/) using their search query. Scraped box office mojo with matched OMDB data are pickled as lists of dictionaries here: *data/movie_data_raw_YYYY.pickle* (where YYYY represents the year of film release).

Additionally, the file **data/movie_data_clean.pickle** contains the raw movie data from all years cleaned and formatted as a pandas dataframe, and **data/genre_counts.csv and **data/genre_counts_coded.csv** contain Box Office Mojo movie categories grouped (by hand) into more general categories.


### Python Scripts, IPyhon Notebooks, and Program Flow:
1. *movie_scrape.py*: Scrape data from Box Office Mojo and match to OMDB API
2. *movie_clean.ipynb*: Clean scraped movie data and engineer features
3. *movie_describe.ipynb*: Descritive statistics for Oscar Bait movie analysis
4. *movie_model.ipynb*: Linear regression models for Oscar Bait movie analysis.

### Other Fun Stuff
1. *graphics/* : Graphics produced from descriptive analysis
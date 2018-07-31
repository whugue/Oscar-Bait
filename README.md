### Metis Project 2: Oscar Bait Investigation
Do films with [Oscar Bait](https://en.wikipedia.org/wiki/Oscar_bait) characteristics (e.g. long, lavish period dramas, etc.) actually tally up more Oscar nominatons than other types of films? 

Read my [blog post](http://www.huguedata.com/2016/04/28/oscar-bait-a-scientific-investigation/) on the matter to learn more!

### Program Flow
The table below provides high-level overviews of what each analysis script does. More information (including specific input/ouput data) can be found in each script's header.

Program 	| Description | 
----------- | ----------- |
01-Movie-Scrape.py | Scrape data from Box Office Mojo and match to OMDB API.
02-Movie-Clean.ipynb | Clean scraped movie data and engineer features.
03-Movie-Describe.ipynb | Descritive statistics for Oscar Bait movie analysis.
04-Movie-Model.ipynb | Linear regression models for Oscar Bait movie analysis.
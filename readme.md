# Apartment searcher

Everyone has different ideas about great deals, but many of the criteria people care about are not present as search filters in Finn. This leads us to cast wide nets, wasting lots of time looking at irrelevant results. With the ludicrous prices currently looking at listings is mildly put discouraging, so this tool exists to minimize the amount of time i have to spend doing so.


## Improving the finn.no search

The following limitations bother me:

* An inability to filter on availability of public transport
* All criteria are hard, making strengths unable to compensate for weaknesses
* The area limitation is a circle when more complicated shapes could be ideal
* You can't compare prices to historical levels
* I don't care about listings with no text or few pictures - unless they are extremely appealing for other reasons
* The sorting options are not multi-dimensional

These limitations however can be compensated for by intersecting multiple finn.no searches with external data sources.
The multiple searches allow you to make finn search criteria variable by certain dimensions (ex price should be lower in certain areas, points at the same distance can have drastically different travel times), while the external data sets can be used to do the same on top of more advanced analysis of apartment value and relevance.

Strictly speaking the multiple searches might not be necessary, but it limits the amount of search result pages we have to scrape. This might save us from rate limiting.

## Extensibility

By creating a data model and a framework for intersecting datasets, it is possible to easily add new ones in the future. It might also be relevant to include apartments and houses from other sources than finn (maybe some newspaper has a track record for having great deals?).

## Legality of scraping articles

This is a gray area - scraping the search results are fine, but scraping the articles themselves break the robots.txt license.
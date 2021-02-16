# Digital Humanities Project

This project is motivated by two main goals. Firstly, we would like to enrich the already existing metadata of the Cini Foundation on the Rolandi Librettos. The website already provides information about the title, the creator, and the year of representation of the libretto. This allows a user to query the libretto given a title, author, or by year and to quickly retrieve the former information. With our project, we would like to extract more entities in order to more accurately and extensively index and query the libretti. The entities we will extract are the title (a shorter version of the existing title metadatum, explained in section Title), city/place of representation, performance location (i.e. theater name, church, or other), the occasion (whether it was played at a Carnival or city fair), the genre of the opera and the composer or director of the play. Together with providing valuable indexing means, these features would allow users to carry out more extensive analyses on the corpus. For instance, it would allow to plot the distributions of the libretti in space, to extract the most flourishing theaters of the time, the most prolific composers. The creation of good, atomic, metadata would allow discerning which operas were played in more than one place, how the representation moved in space and time, which operas were put to music by the same composers, and much more.

Secondly, we would like to provide a comprehensive framework to visualize the extracted entities. This would allow the data to be easily understandable and interpretable. Specifically, the framework would allow to quickly identify time and place of representation of an opera, see what operas were played in the same period and location. It would allow zooming into the city and locating the theaters that were most prominent in the period, linking visually operas with the same title or composer, clicking on external links to Wikipedia pages and the original Cini archive.

In sum, the project is motivated by the will to extract and present information about this collection in a broad and accessible manner.


### Steps to run the visualization

1. Go to the `map_viz` folder which contains the visualization and some preprocessed data for the visualization.
2. Start the server for serving the data using this command: `python simple_cors_http_server.py 1234`
3. Open `index.html` in Google Chrome and see the visualization.

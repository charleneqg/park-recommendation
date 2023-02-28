# park-recommendation

## Project description
I love parks, so I decide to implement a ranking system which ranks the parks in the United States and recommended
the top 5 to the user. In this project, I collected information about parks. More specifically I focused on 5 different data.
Distance: the distance between a park and my current location.
Weather: the weather condition in the park, it can be sunny, windy, cloudy, rainy etc.
Temperature: the temperature in the park
Wind Speed: wind speed in the park
Rating: rating of the park by one of the Google reviews
In this project, user can input their current location and get the 5 most recommended parks to visit the next day.
I'm specifically focusing on "next day" because weather data is temporary, so we can not use that as a factor to
conclude which park is the best in a relatively long time period.

## Data
1. Park name and location data: [Scrape]
We scrape from https://www.latlong.net/ where we can find a huge list of parks in the United States and their
locations. Latitude and longitude of these parks can be obtained.
2. Weather data: [API]
We get weather data from api: https://api.weather.gov/gridpoints/lat,long, where given a latitude and longitude, we
can get the real-time data for that area.
3. Rating data: [Scrape]
We scrape rating data from google, we search the google using the parks' names as keywords, we also add a "review"
keyword so that we will find ratings for the parks.
[Note] The weather data and rating data will be collected after park location data. This is because in the program,
after we get all the park location data, we will only consider 10 nearest parks for user to visit, or otherwise the
parks could be too far from the user. Therefore, we only obtain weather data and rating data for these 10 selected
parks instead of getting these data for all parks. This can save time and scraping a small amount of data means that
we are not likely to be detected by some anti-scraping mechanics, which we also set a small time delay after each
scrape to prevent that.

Static Data:
Static data can be found in park_location.csv, weather.csv and rating.csv

Modules and Packages:

Python:
You need to run with python version > 3.0. The one I'm using is 3.8.8.

## Modules to install
requests~=2.28.1
bs4~=0.0.1
beautifulsoup4~=4.11.1

Commands to run to install:
pip3 install -r requirements.txt
pip3 install html5lib

## How to run the code

python main_app.py
It should open up a python UI where you can modify inputs easily and when you are ready just click on "Recommend
Parks" to get the recommended parks based on your preference.

In the top area:
On the left side, you can find several checkboxes, you can check the box to indicate that you want a factor to be
considered, or you can also uncheck the box to indicate that you don't want this factor.
On the right side, you can input the numbers in the text input to rank the preference. You should rank all factors
from 1 to 5, where 1 means the most important factor and 5 means the least important factor.

In the middle area:
You can enter your longitude and latitude to represent your current location. These can be either integers or float
values. If you enter nothing here, the default location will be used, which is the location of USC.

Recommend Parks:
This is a button to click when you finish editing the above input, for grading purpose or for easy testing, you can
just do nothing above and simply click this button. You can see the list of recommended parks below in the UI.

Time to run:
You can expect less than 3 minutes for this program to recommend parks. There will be no logs in the popup UI, but
you can see all the logs in the console/terminal.

There are 3 modes:
static mode, scrape mode and default mode. Each mode should take less than 3 minutes.

[static mode]

[scrape mode]
scraping data without user input: (this will use USC's location by default)

scraping data with user input: (lat, long should valid location in US, or otherwise there might be errors)

[default mode]
collect, store and display data without user input: (this will use USC's location by default)

collect, store and display data with user input: (lat, long should be valid location in US, or otherwise there might
be errors)

## Analysis
After we collect all data for the 10 nearest parks. We perform some analysis:
We assign a score to each park.
The score consists of:
Distance factor
Weather factor
Temperature factor
Wind factor
Rating factor

For distance factor, the score is based on the distance between the park to our current location. The closer the
park is, the higher the score the park gets.

For weather factor, sunny or clear days get the most score and rainy days get the least scores.

For temperature factor, the most comfortable weather gets the highest score, a too-low or too-high temperature will
get a low score.

For wind factor, smaller wind generally gets a better score than heavy wind.

For rating factor, rating is directly related to score with some mathematical conversion.

All the scores above will be assigned a weight and the final weighted score will be added to the final score of the
park. Eventually, we recommend parks from the highest scores to the lowest scores.

## Extensibility
This model is extensible in a few ways:
1. We can recommend other places to visit other than parks.
2. For now, we only recommend which park to visit the next day. We could extend the model to let user input a time
within the current week and recommend parks on that day.
3. Currently, we are assuming people want to visit parks during the day. However, some might prefer to visit at night,
so we can probably add a night choice.
4. We can collect other factors people consider when visiting a park, such as crime rate near the park.


## Maintainability
There are a few possible ways the model can break:
1. If the API stops working or any website that we scraped makes big structure changes. Our model heavily relies on
real time data rather than static data. We are getting the rating and weather data for a park. These can change
daily and they should not just be read from a static local data source. If this is a commercial product rather than
a class project, it would be better to use paid API services to obtain these data rather than scraping, because paid
APIs are usually maintained pretty well.
2. When new park data is added to https://www.latlong.net, that park might be very new that there is no google review
for it. This is okay, since we have a 4.0 rating by default to prevent this from happening. However, the newly added
data might be a malformed data. I've noticed that the park "MacArthur Park" added to the website has name "Santa
Monica" instead of "MacArthur Park" and I've manually corrected this in my code. However, if newly added parks have
this issue, there will be no catastrophic outcomes since our models will not throw an error. However, the data we
are displaying to the user might be wrong. Take the above example, they will see a park with name "Santa Monica".

## Graph
The project includes a python file "plot_geo.py", which I use it to plot the graphs in the presentation slides and
the write-up document. The .dbf, .shp and .shx files are all needed to run the files. The graph plotted are pretty
nice since they include longitude and latitude lines in the map and locations are projected onto a map.

Sadly, this python file needs "basemap" library as its dependencies. However, I think it is not maintained that well,
because when I tried to install things on another device for testing purpose using pip3 install basemap, the
installation simply fails.

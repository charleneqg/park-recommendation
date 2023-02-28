import sys

from utils import *


def execute_scrape_mode(input_lat=None, input_long=None):
    park_location_data = get_all_parks_location()
    display_objects_info(park_location_data)
    cur_lat = DEFAULT_LAT
    cur_long = DEFAULT_LONG
    if input_lat is not None and input_long is not None:
        cur_lat = float(input_lat)
        cur_long = float(input_long)
    nearest_parks = get_nearest_parks(park_location_data, cur_lat, cur_long)
    weather_data_objects = get_all_weather_info(nearest_parks)
    display_objects_info(weather_data_objects)
    rating_data_objects = get_all_rating_info(nearest_parks)
    display_objects_info(rating_data_objects)
    return


def execute_static_mode(filepath):
    object_data = read_csv_to_objects(filepath)
    display_objects_info(object_data)
    return


def execute_default_mode(input_lat=None, input_long=None):
    park_location_data = write_all_park_location_data()
    display_objects_info(park_location_data)
    cur_lat = DEFAULT_LAT
    cur_long = DEFAULT_LONG
    if input_lat is not None and input_long is not None:
        cur_lat = float(input_lat)
        cur_long = float(input_long)
    nearest_parks = get_nearest_parks(park_location_data, cur_lat, cur_long)
    weather_data = write_all_weather_data(nearest_parks)
    display_objects_info(weather_data)

    rating_data = write_all_rating_data(nearest_parks)
    display_objects_info(rating_data)
    return


def write_all_park_location_data():
    park_info_objects = get_all_parks_location()
    write_objects_to_csv(objects=park_info_objects, filename="park_location.csv")
    return park_info_objects


def read_all_park_location_data():
    location_data = read_csv_to_objects("park_location.csv")
    return location_data


def write_all_weather_data(nearest_parks):
    weather_data_objects = get_all_weather_info(nearest_parks)
    write_objects_to_csv(objects=weather_data_objects, filename="weather.csv")
    return weather_data_objects


def read_all_weather_data():
    weather_data_objects = read_csv_to_objects("weather.csv")
    return weather_data_objects


def write_all_rating_data(nearest_parks):
    rating_data_objects = get_all_rating_info(nearest_parks)
    write_objects_to_csv(objects=rating_data_objects, filename="rating.csv")
    return rating_data_objects


def read_all_rating_data():
    rating_data_objects = read_csv_to_objects("rating.csv")
    return rating_data_objects


if __name__ == '__main__':
    # execute default mode
    if len(sys.argv) == 1:
        execute_default_mode()

    elif len(sys.argv) > 1:
        # execute scrape mode
        if sys.argv[1] == "--scrape":
            # with input lat, long
            if len(sys.argv) > 3:
                lat = sys.argv[2]
                long = sys.argv[3]
                execute_scrape_mode(input_lat=lat, input_long=long)
            # without input lat, long
            else:
                execute_scrape_mode()
        # execute static mode
        elif sys.argv[1] == "--static":
            path_to_data = sys.argv[2]
            execute_static_mode(path_to_data)
        # execute default mode with input lat, long
        elif len(sys.argv) > 2:
            lat = sys.argv[1]
            long = sys.argv[2]
            execute_default_mode(input_lat=lat, input_long=long)


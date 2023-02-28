import math
import time
import requests
from bs4 import BeautifulSoup
import csv
import re


MAX_PARK_PAGE_NUM = 5
# default lat and long represents USC location
DEFAULT_LAT = 34.022415
DEFAULT_LONG = -118.285530
ALL_DAYS_IN_A_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"] 


def get_soup(url):
    print("Current url: " + url)
    r = requests.get(url)
    # consider status code starts with 2 as success code
    if r.status_code > 299:
        return None
    soup = BeautifulSoup(r.content, 'html5lib')
    return soup


# wait for some time until doing next operation to prevent potential anti-scraping checks
def wait_for_next_operation(t=0.5):
    time.sleep(t)
    return


def write_objects_to_csv(objects, filename):
    print_important("Writing file: " + filename)

    if objects is None or len(objects) == 0:
        return

    fieldnames = list(objects[0].keys())

    # write to csv without additional newline
    with open(filename, 'w', newline='') as file:
        csvwriter = csv.DictWriter(file, fieldnames=fieldnames)
        csvwriter.writeheader()
        csvwriter.writerows(objects)


def read_csv_to_objects(filename):
    print_important("Reading file: " + filename)
    objs = []

    with open(filename, 'r', newline='', encoding='cp1252') as file:
        csvreader = csv.DictReader(file)

        for row in csvreader:
            objs.append(row)
    return objs


def display_objects_info(objects, max_display_allowed=10):
    if objects is None or len(objects) == 0:
        return

    fieldnames = list(objects[0].keys())
    print("Field names: " + ", ".join(fieldnames) + "\n")
    rows_to_print = min(len(objects), max_display_allowed)
    print("Displaying " + str(rows_to_print) + " of " + str(len(objects)) + " rows of data:")
    for i in range(rows_to_print):
        s = "--------------------------------------------------------\n"
        for field in fieldnames:
            s += "[" + field + "]: " + str(objects[i][field]) + "\n"
        print(s[:-1])
    print("--------------------------------------------------------")
    return


def print_important(s):
    print("\n=========================================================")
    print(s)
    print("=========================================================\n")


def get_nearest_parks(location_data, lat, long, count=10):
    lst = []
    for i in range(len(location_data)):
        park_loc = location_data[i]
        park_lat = float(park_loc["lat"])
        park_long = float(park_loc["long"])
        lat_diff = lat - park_lat
        long_diff = long - park_long
        sqr_dist = lat_diff ** 2 + long_diff ** 2
        lst.append((sqr_dist, park_loc))
    lst.sort()
    return [i[1] for i in lst[:count]]


def get_all_parks_location():
    print_important("Scraping: Park locations")
    url_prefix = "https://www.latlong.net/category/parks-236-53"
    url_suffix = ".html"
    idx = 0
    all_soup = []
    while idx < MAX_PARK_PAGE_NUM:
        url_middle = "" if idx == 0 else "-" + str(idx+1)
        url = url_prefix + url_middle + url_suffix
        soup = get_soup(url)
        if soup is None:
            break
        all_soup.append(soup)
        wait_for_next_operation()
        idx += 1

    lst = []
    names = set([])
    for soup in all_soup:
        trs = soup.find("table").find_all("tr")[1:]
        for tr in trs:
            tds = tr.find_all("td")
            name_and_location = tds[0].find("a")["title"].strip()
            loclist = name_and_location.split(",")
            name = loclist[0]
            # correct mistake
            if name == "Santa Monica":
                name = "MacArthur Park"
            # remove duplicates
            if name in names:
                continue
            names.add(name)
            location = (",".join(loclist[1:])).strip()
            lat = tds[1].text.strip()
            long = tds[2].text.strip()
            lst.append({"name": name, "location": location, "lat": lat, "long": long})
    return lst


def get_all_weather_info(park_objs):
    print_important("API: Weather data")
    all_weather_objs = []
    for park_obj in park_objs:
        weather_obj = get_single_weather_info(park_obj)
        all_weather_objs.append(weather_obj)
        wait_for_next_operation()
    return all_weather_objs


def get_single_weather_info(park_obj):
    lat = park_obj["lat"]
    long = park_obj["long"]
    name = park_obj["name"]
    url = "https://api.weather.gov/points/" + str(lat) + "," + str(long)
    # print(url)
    res = requests.get(url=url)
    data = res.json()
    # retry if there is error
    if data.get("properties") is None:
        return get_single_weather_info(park_obj)
    forecast_url = data["properties"]["forecast"]
    print("Current url: " + forecast_url)
    res = requests.get(url=forecast_url)
    data = res.json()
    # retry if there is error
    if data.get("properties") is None:
        return get_single_weather_info(park_obj)
    all_forecasts = data["properties"]["periods"]
    closest_day_forecast = None
    for itm in all_forecasts:
        if itm["name"] in ALL_DAYS_IN_A_WEEK:
            closest_day_forecast = itm
            break
    
    obj = {"name": "", "day": "", "temperature": "", "wind": "", "forecast": ""}
    if closest_day_forecast is not None:
        obj["name"] = name
        obj["day"] = closest_day_forecast["name"]
        obj["temperature"] = closest_day_forecast["temperature"]
        obj["wind"] = closest_day_forecast["windSpeed"]
        obj["forecast"] = closest_day_forecast["shortForecast"]
    return obj


def get_all_rating_info(park_objs):
    print_important("Scrape: Rating data")
    all_rating_objs = []
    for park_obj in park_objs:
        rating_obj = get_single_rating_info(park_obj)
        all_rating_objs.append(rating_obj)
        wait_for_next_operation()
    return all_rating_objs


def get_single_rating_info(park_obj):
    name = park_obj["name"]
    suffix = "+".join(name.split())
    url = "https://www.google.com/search?q=" + suffix + "+review"
    soup = get_soup(url)
    if soup is None:
        return None
    rating_div = soup.find_all('div', {'aria-label': re.compile(r'Rated .* out of 5')})
    rating = 4.0
    if rating_div is None or rating_div == []:
        pass
    else:
        try:
            rating_str = rating_div[0]["aria-label"]
            rating = float(rating_str[6:9])
        except:
            rating = 4.0
    obj = {"name": name, "rating": rating}
    return obj


# Sample Preference:
# {
#   'distance': {'is_active': 1, 'rank': 1},
#   'temperature': {'is_active': 1, 'rank': 2},
#   'weather': {'is_active': 1, 'rank': 3},
#   'windspeed': {'is_active': 1, 'rank': 4},
#   'rating': {'is_active': 1, 'rank': 5}
# }
#
def get_rank(preference, distance_data, weather_data, rating_data):
    # get preference list
    pref_list = []
    for k, v in preference.items():
        if v["is_active"] != 0:
            pref_list.append((v["rank"], k))
    pref_list.sort()
    pref_list = [itm[1] for itm in pref_list]

    # get all names
    park_list = []
    park_result = {}
    park_data = {}
    for data in distance_data:
        name = data["name"]
        park_list.append(name)
        park_result[name] = 0
        park_data[name] = {}

    for data in weather_data:
        name = data["name"]
        park_data[name]["temperature"] = data["temperature"]
        park_data[name]["windspeed"] = data["wind"]
        park_data[name]["weather"] = data["forecast"]

    for data in rating_data:
        name = data["name"]
        park_data[name]["rating"] = data["rating"]

    cur_weight = 1.0
    for itm in pref_list:
        if itm == "distance":
            for park in park_list:
                park_result[park] += (10 - park_list.index(park)) * cur_weight
        elif itm == "weather":
            for park in park_list:
                w_data = park_data[park]["weather"]
                score = 1
                if "sunny" in w_data.lower():
                    score = 10
                elif "cloudy" in w_data.lower():
                    score = 7
                elif "rainy" in w_data.lower():
                    score = 4
                park_result[park] += score * cur_weight
        elif itm == "windspeed":
            for park in park_list:
                wind_data = park_data[park]["windspeed"]
                int_lst = map(int, re.findall(r'\d+', wind_data))
                score = 1
                int_lst = list(int_lst)
                if not int_lst:
                    score = 5
                else:
                    if max(int_lst) <= 5:
                        score = 10
                    if max(int_lst) <= 10:
                        score = 7
                    if max(int_lst) <= 15:
                        score = 4
                park_result[park] += score * cur_weight
        elif itm == "temperature":
            for park in park_list:
                temp_data = park_data[park]["temperature"]
                temp = int(temp_data)
                score = 4
                if 55 < temp < 65:
                    score = 10
                if 50 < temp < 55 and 65 < temp < 70:
                    score = 7
                if temp < 30 or temp > 90:
                    score = 1
                park_result[park] += score * cur_weight
        elif itm == "rating":
            for park in park_list:
                r_data = park_data[park]["rating"]
                rating = float(r_data)
                park_result[park] += rating * 2 * cur_weight
        cur_weight -= 0.2

    res = []
    for park in park_result.keys():
        res.append((-park_result[park], park))
    res.sort()
    res = [itm[1] for itm in res]
    res_obj = []
    for i in range(len(res)):
        for data in distance_data:
            if data["name"] == res[i]:
                res_obj.append(data)
                break
    return res_obj




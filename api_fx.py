"""Functions to use with Teleport and Sherpa APIs."""

import requests 
from pprint import pprint
from model import db, connect_to_db, User, City, UserCity
from crud import add_city_db


# ===========================================
#               TELEPORT API
# ===========================================


def search_w_scores_api(city_name, limit=1):    #paris (france, texas?)
    """Get detailed info and scores about a city from Teleport API."""
    # fetch city basics+details in one step, using embed param 

    payload = {
        "search": city_name,
        "limit": limit,
        "embed": "city:search-results/city:item/city:urban_area/{ua:scores,ua:images}",
    }

    print("*** fetching from teleport API ***")
    res = requests.get("https://api.teleport.org/api/cities/", params=payload)
    res_dict = res.json()

    return res_dict 


def clean_search_res(res_dict):
    """Clean up response from Teleport API to get city basics."""

    # ? account for multiple results?
    # * do not clean urban areas -- need to check if available separately

    pass


def clean_urban_area(city_dict):
    """Clean up dictionary for a city:item from Teleport API."""

    pass


# fetch data from teleport API
def get_city_api(city_name):
    """Get basic city info from Teleport API and save to db if necessary.
    
    Returns dict containing city details from teleport + city_id from db."""
    # return City json ??

    print("HI from get_city_api...")

    res_dict = search_w_scores_api(city_name) 
    print("HI AGAIN from get_city_api...")

    if res_dict["count"] == 0:
        return None

    emb = "_embedded"
    first_city = res_dict[emb]["city:search-results"][0] 
    city_item = first_city[emb]["city:item"]

    # 3. extract city basics from response
    # always get country and city_id from teleport
    tele_city_id = city_item["geoname_id"]
    tele_name = city_item["name"]

    city_item_links = city_item["_links"]
    tele_country = city_item_links["city:country"]["name"]
    # ------------------ ooo -------------------
    print(f"[get_city_api] result basics from teleport: ")
    print(f"[get_city_api] {tele_name} in {tele_country} with id {tele_city_id}")

    ### handle error: skip if no details/urban area available 
    # eg venice, kolkata
    try:
        city_item_links["city:urban_area"]["name"]
    except:
        print(f"[get_city_api] found a match to {tele_name} in {tele_country}")
        print("but no detailed city info available from teleport :( sorry! ")
        # add to db (without ua) anyway?? 
        return None
    else:
        # OK, get complete ua+scores data
        ua_dict = city_item[emb]["city:urban_area"]
        scores_list = ua_dict[emb]["ua:scores"]["categories"]

        scores_dict = {}
        for cat in scores_list:
            score = float(cat["score_out_of_10"])
            scores_dict[cat["name"]] = round(score, 1)

        photo_1 = ua_dict[emb]["ua:images"]["photos"][0]
        img_link = photo_1["image"]["web"]

        # compile dictionary to pass to next function
        city_dict = {
            "tele_id": tele_city_id,
            "city_name": tele_name, 
            "country_name": tele_country,
            "urban_area": city_item_links["city:urban_area"]["name"],
            "urban_id": ua_dict["ua_id"],
            "scores": scores_dict,
            "img_link": img_link
        }
        print("so far, city_dict is this:")
        pprint(city_dict)

    ### double check before adding City to db
    try:
        # look for tele_city_id in db. if one only, continue
        City.query.filter_by(teleport_id=tele_city_id).one()
    except:
        # if none, add city info to db
        # ---------------- ooo ----------------
        print('[get_city_api] city table did not have (1) record for teleport id')
        db_cities = City.query.filter_by(teleport_id=tele_city_id)
        if db_cities.count() == 0:
            print("in fact, no cities found in db.")
            print("we should add this city to db.")
            city_id = add_city_db(city_dict)
        else: 
            num_records = db_cities.count()
            print(f"[get_city_api] found {num_records} city records in db")

    # get first record only, in case of duplicates
    city = City.query.filter_by(teleport_id=tele_city_id).first()
    # ! MOCK DATA
    # print("[get_city_api] shhhh -- let's pretend we got a city from db...")
    # city = City.query.filter_by(city_name='San Francisco').first()

    print(f"[get_city_api] city from db is: {city}")
    city_id = city.city_id  # 2 (for london)
        
    city_dict["city_id"] = city_id

    return city_dict


def tele_search_cityname(city_name, limit=5):
    """Search Teleport for cityname, returns a list of results.
    
    Return [{city_name, country_name, geoid, match}, {...}]."""

    payload = {
        "search": city_name,
        "limit": limit,
        "embed": "city:search-results/city:item"
    }

    print("*** [search_cities] fetching from teleport API ***")
    res = requests.get("https://api.teleport.org/api/cities/", params=payload)
    res_dict = res.json()

    if res_dict["count"] == 0:  # no results found at all
        print("nothing found, returning {}")
        return {}

    emb = "_embedded"
    res_cities = res_dict[emb]["city:search-results"]  # list of city_items
    cities_found = []

    # make new list of results, each entry is a dict
    for city in res_cities:
        city_item = city[emb]["city:item"]
        tele_name = city_item["name"]
        match = "exact" if city_name == tele_name.lower() else "alt"

        city_dict = {
            "tele_name": tele_name,
            "tele_country": city_item["_links"]["city:country"]["name"],
            "geoid": city_item["geoname_id"],
            "match": match
        }
        cities_found.append(city_dict)
    
    # print(f"[search_cities] returning search results: {cities_found}")

    return cities_found


# ===========================================
#               SHERPA API 
# ===========================================


SHERPA_KEY = "AIzaSyBxoYsdMHOvhXJGA_oFH0jiXpaiE-uUnFw"
SHERPA_ROOT = "https://requirements-api.sandbox.joinsherpa.com/v2/"


def sherpa_all_countries():
    """Get all countries from sherpa API."""

    payload = {
        "key": SHERPA_KEY
    }

    print("*** fetching countries from sherpa API ***")
    res = requests.get(SHERPA_ROOT+"countries", params=payload)
    res_dict = res.json()

    return res_dict 


def sherpa_country_request(ccode):
    """Send request to sherpa API for country with given isocode."""

    payload = {
        "key": SHERPA_KEY,
        "filter[country]": ccode
    }

    print("*** fetching country from sherpa API ***")
    res = requests.get("https://requirements-api.sandbox.joinsherpa.com/v2/countries", params=payload)
    res_dict = res.json()

    return res_dict 

    # >>> res = sherpa_test_request()
    # >>> results_list = res["data"]
    # >>> len(results_list)
    # 1
    # >>> first_res = results_list[0]
    # >>> first_res["attributes"]["countryName"]
    # 'Japan'


def sherpa_restrictions(ccode):
    """Get entry restrictions for a particular country."""

    payload = {
        "key": SHERPA_KEY,
        "filter[country]": ccode, 
        "filter[category]": "NO_ENTRY, RESTRICTED_ENTRY"
    }

    print("*** fetching restrictions from sherpa API ***")
    res = requests.get(SHERPA_ROOT+"restrictions", params=payload)
    res_dict = res.json()

    return res_dict 

    # >>> res = sherpa_restrictions("jpn")
    # >>> res_data = res["data"]
    # >>> titles = [res["attributes"]["title"] for res in res_data]
    # * get desc, more and severity too
    # >>> titles
    # ['Entry restricted for international travelers', 'Travel is allowed with restrictions']


def sherpa_procedures(ccode):
    """Get entry procedures for a particular country."""

    payload = {
        "key": SHERPA_KEY,
        "filter[country]": ccode,
        "filter[category]": "QUARANTINE, RE_ENTRY_PERMIT, COVID_19_TEST, "\
                    "DOC_REQUIRED, HEALTH_ASSESSMENT"
    }

    print("*** fetching procedures from sherpa API ***")
    res = requests.get(SHERPA_ROOT+"procedures", params=payload)
    res_dict = res.json()

    return res_dict 

    # >>> res = sherpa_procedures("jpn")
    # >>> titles = [res["attributes"]["title"] for res in res["data"]]
    # >>> for p in res["data"]:
    # ...     procedures.append({"title": p["attributes"]["title"], 
    #                            "desc": p["attributes"]["description"], 
    #                            "cat": p["attributes"]["category"],
    #                            "subcat": p["attributes"].get("documentType")
    #         })
    # >>> len(procedures)
    # 6
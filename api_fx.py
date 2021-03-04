"""Functions to use with Teleport and Sherpa APIs."""

import requests 
from pprint import pprint
from model import db, connect_to_db, User, City, UserCity
from crud import add_city_db


# ===========================================
#               TELEPORT API
# ===========================================

TELE_ROOT = "https://api.teleport.org/api/cities/"


def make_basic_dict(res_dict):
    """Clean up response from Teleport API to get city basics."""
    # * do not clean urban areas -- need to check if available separately

    emb = "_embedded"
    print(f"[make_basic_dict] received res_dict:")
    # pprint(res_dict)

    city_basics = {
        "geoid": res_dict["geoname_id"],
        "tele_full_name": res_dict["full_name"],
        "tele_city_name": res_dict["name"],
        "tele_country_name": res_dict[emb]["city:country"]["name"],
        "country_iso": res_dict[emb]["city:country"]["iso_alpha3"],
    }

    return city_basics


def make_scores_dict(ua_dict):
    """Create a dict of all urban area scores by category."""

    scores_list = ua_dict["_embedded"]["ua:scores"]["categories"]
    scores_dict = {}
    for cat in scores_list:
        score = float(cat["score_out_of_10"])
        scores_dict[cat["name"]] = round(score, 1)

    return scores_dict


def tele_city_details(geoid):
    """Get detailed city info from Teleport, return dict. 
    
    Returns dict of {tele_id, city_name, city_id, country_iso, country_name, 
    urban_area, ~urban_id~, scores, img_link} or {basics only}"""

    # send request to teleport with geoid
    param = "embed=city:country&embed=city:urban_area/{ua:scores,ua:images}"
    res = requests.get(TELE_ROOT+f"geonameid:{geoid}/?{param}")
    res_dict = res.json()

    # make basic city dict 
    city_dict = make_basic_dict(res_dict)

    # check if city has detailed info, extract scores if avail
    try:
        res_dict["_links"]["city:urban_area"]["name"]
    except:
        print(f"[tele_city_details] found a match to {city_dict}")
        print("but no urban area info is available :( sorry! ")
    else:
        # OK, get complete ua+scores data
        ua_dict = res_dict["_embedded"]["city:urban_area"]
        city_dict["urban_area"] = ua_dict["name"]
        city_dict["urban_id"] = ua_dict["ua_id"]

        # get ua scores
        scores_dict = make_scores_dict(ua_dict)
        city_dict["scores"] = scores_dict

        # also add photo link 
        photo_1 = ua_dict["_embedded"]["ua:images"]["photos"][0]
        img_link = photo_1["image"]["web"]
        city_dict["img_link"] = img_link

    return city_dict  # could be basic or scores dict 


def search_city_country(city_name, country_iso):
    """Search Teleport for a specific city-country combo and return geoid.

    Compares cityname and countryname to each teleport result to get 
    best match."""

    prefetch_param = "city:search-results/city:item/city:country"
    payload = {
        "search": city_name,
        "limit": 5,
        "embed": prefetch_param
    }

    print("*** [search_citycountry] fetching from teleport API ***")
    res = requests.get(TELE_ROOT, params=payload)
    res_dict = res.json()

    # identify first city item with country match
    emb = "_embedded"
    res_cities = res_dict[emb]["city:search-results"]  # list of city_items

    for city in res_cities:
        city_item = city[emb]["city:item"]
        tele_iso = city_item[emb]["city:country"]["iso_alpha3"]
        if tele_iso.lower() == country_iso.lower():
            return city_item["geoname_id"]
    
    return None


def tele_search_cityname(city_name, limit=5):
    """Search Teleport for cityname, returns a list of results.
    
    Return [{city_name, country_name, geoid, match}, {...}]."""

    payload = {
        "search": city_name,
        "limit": limit,
        "embed": "city:search-results/city:item/{city:country}"
    }

    print("*** [search_cities] fetching from teleport API ***")
    res = requests.get(TELE_ROOT, params=payload)
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
        city_country = city_item[emb]["city:country"]
        match = "exact" if city_name == tele_name.lower() else "alt"

        city_dict = {
            "tele_name": tele_name,
            "tele_country": city_country["name"],
            "iso": city_country["iso_alpha3"],
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
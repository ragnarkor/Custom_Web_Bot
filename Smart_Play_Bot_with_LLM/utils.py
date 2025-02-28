import requests
from datetime import datetime

def fetch_district_info():
    """Fetches and structures district hierarchy data from the LCSD API."""
    
    # Main response structure
    api_response = {
        "fetch_date": datetime.today().strftime("%Y-%m-%d"),
        "districts": []
    }

    request_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Referer": "https://www.smartplay.lcsd.gov.hk/",
        "Accept": "application/json"
    }

    districts_endpoint = "https://www.smartplay.lcsd.gov.hk/rest/param/api/v1/publ/districts/searching-criteria?pgm=N"

    server_response = requests.get(districts_endpoint, headers=request_headers)
    response_data = server_response.json().get("data", 0)

    if response_data:

        for region_group in response_data:
            region_dict = {
                "region_id": region_group["id"],
                "region_code": region_group["code"].strip(),
                "region_name": region_group["name"].strip(),
                "sc_name": region_group["scName"].strip(),
                "tc_name": region_group["tcName"].strip(),
                "subdistricts": []
            }

            for subdistrict in region_group["children"]:
                subdistrict_dict = {
                    "subdistrict_id": subdistrict["id"],
                    "subdistrict_code": subdistrict["code"].strip(),
                    "subdistrict_name": subdistrict["name"].strip(),
                    "en_name": subdistrict["enName"].strip(),
                    "sc_name": subdistrict["scName"].strip(),
                    "tc_name": subdistrict["tcName"].strip()
                }
                region_dict["subdistricts"].append(subdistrict_dict)

            api_response["districts"].append(region_dict)

        return api_response
    
    return {"status": "error", "code": server_response.status_code}

district_info = fetch_district_info()



def fetch_available_venue_timeslot(district_codes, facility_code, play_date):
    
    base_url = "https://www.smartplay.lcsd.gov.hk/rest/facility-catalog/api/v1/publ/facilities"

    params = {
        "distCode": ",".join(district_codes),
        "faCode": facility_code,
        "playDate": play_date
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0',
        'Referer': 'https://www.smartplay.lcsd.gov.hk/facilities/search-result',
        'channel': 'INTERNET'
    }

    response = requests.get(base_url, params=params, headers=headers)
    return response.json()

district_codes=['KC', 'KT', 'SSP', 'WTS', 'YTM']
facility_code='TABT'
play_date='2025-03-05'

available_venue_timeslot = fetch_available_venue_timeslot(district_codes, facility_code, play_date)
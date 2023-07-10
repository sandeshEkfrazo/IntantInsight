import geocoder
from geopy.geocoders import Nominatim
import requests 

import pytz
from datetime import datetime

def getUserCountry():
    g = geocoder.ip('me')
    print("g==>>", g)
    if g.latlng:
        latitude, longitude = g.latlng
        geolocator = Nominatim(user_agent="myapp")
        location = geolocator.reverse(f"{latitude}, {longitude}")

        print("location==>", location)

        address = location.raw['address']
        
        print("address==>>>>", getUserCountry)
        country = address.get('country', '')

        print("country==>", country)

        return country


def getCountryDetails(ip_address):
    print("ip_address==??", ip_address)
    g = geocoder.ip(ip_address)
    print("gvalue==>", g)
    if g.ok:
        country_name = g.country
        print("coutry name ==>", country_name)
        return country_name
    else:
        return "Unknown"

    print("ipaddress==>", ip_address)

def getCountry(ipAdress):
    url = f"http://ipinfo.io/{ipAdress}/json"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print("data==> in getCountry fun",data)
        country = data.get('country')
        if country:
            country_timezone = pytz.country_timezones.get(country)

            if country_timezone:
                user_time = datetime.now(pytz.timezone(country_timezone[0]))

                return country, user_time, country_timezone[0]

            return country
    return "Unknown"


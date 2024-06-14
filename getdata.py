import requests
def getdata(name):
    url = f'https://www.ndbc.noaa.gov/data/realtime2/{name}.txt'
    res = requests.get(url)
    if res.status_code == 200:
        return res.text
    elif res.status_code == 404:
        print("No data available")
        return None
    else:
        print("Unknown error")
        return None

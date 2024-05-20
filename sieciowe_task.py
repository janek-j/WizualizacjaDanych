import requests
import json
import sys
import time

API_URL = 'https://api.discogs.com'
TOKEN = 'SSKawwVZmfShSEXsPMAGjDApvBKZOkUPkHkhaoOA'

headers = {
    'User-Agent': 'Mozilla/5.0',
    'Authorization': f'Discogs token={TOKEN}'
}

def get_musician_data(musician_id):
    url = f"{API_URL}/artists/{musician_id}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print(response.json)
        return response.json()
    else:
        return response.status_code
        sys.exit(1)

def get_bands(musicians):
    musician_bands = {}
    for musician_id in musicians:
        data = get_musician_data(musician_id)
        musician_name = data['name']
        bands = {group['name']: group['id'] for group in data['groups']}
        musician_bands[musician_name] = bands
    common_bands = None
    for bands in musician_bands.values():
        if common_bands is None:
            common_bands = set(bands.keys())
        else:
            common_bands.intersection_update(bands.keys())
    return common_bands, musician_bands

def main() -> None:
    if len(sys.argv) < 2:
        print(f"Uzycie: python3 sieciowe_task.py <musician_id1> <musician_id2> ... <musician_idN> ")
        sys.exit(1)
    musician_ids = sys.argv[1:]
    try:
        common_bands, musician_bands = get_bands(musician_ids)
        if not common_bands:
            print("Nie znaleziono zespolow. Program konczy swoje dzialanie.\n")
            sys.exit(1)
        sorted_bands = sorted(common_bands)
        for band in sorted_bands:
            print(f"Zespol: {band}")
            print("Muzycy: ")
            for musician, bands in musician_bands.items():
                print(f"{musician}, ktory gral/grala w zespolach: ")
                print(bands)
                print()
    except Exception as e:
        print(f"Wyjatek: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
    sys.exit(0)
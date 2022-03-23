#!/usr/bin/env python3


import csv
import urllib.parse
import webbrowser
from matplotlib import pyplot as plt


def tell_me_your_coordinates(filename):
    lat = []
    lon = []
    with open(filename) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        print(f'Hey there... \n'
              f'these are the locations of friends who want to hang:')
        for row in csv_reader:
            lat.append(row["latitude"])
            lon.append(row["longitude"])
            print(f'{row["latitude"]} {row["longitude"]}')
    print()
    return lat, lon


# Naive estimate...
def find_center(latitude, longitude, plot=False):
    plt.rcParams["figure.figsize"] = [10.0, 10.0]
    plt.rcParams["figure.autolayout"] = True
    x = [float(la) for la in latitude]
    y = [float(lo) for lo in longitude]
    center = sum(x) / len(x), sum(y) / len(y)
    # Fancy geometry if you would like
    if plot:
        plt.scatter(x, y)
        plt.plot(center[0], center[1], marker='*')
        plt.annotate(
            "MEET HERE",
            xy=center, xytext=(-20, 20),
            textcoords='offset points', ha='right', va='bottom',
            bbox=dict(boxstyle='round,pad=0.8', fc='yellow', alpha=0.5),
            arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
        plt.show()
    return center


def main():
    lat, lon = tell_me_your_coordinates("example.csv")
    meet_lat, meet_lon = find_center(lat, lon)
    print(f'With my superpowers, I have calculated a center-point')
    print(f'Result: {meet_lat} , {meet_lon}\n')

    radius = 666
    print(f'According to nothing, we should meet within a {radius}m radius')

    # Start here to get the hang of it :)
    # osm_script = requests.get(
    #    "http://overpass-api.de/api/interpreter?data="
    #    "<query type='node'><around lat='" + str(meet_lat) +
    #    "' lon='" + str(meet_lon) + "' radius='" + str(300) +
    #    "'/><has-kv k='amenity' v='restaurant'/></query><print/>")
    query = f"<osm-script> " \
            f"<query type='node'> " \
            f"<around lat='{meet_lat}' lon='{meet_lon}' " \
            f"radius='{radius}'/>" \
            f"<has-kv k='amenity' v='restaurant'/> </query> <print/> " \
            f"</osm-script>"

    q = urllib.parse.quote(query)
    url = "https://overpass-turbo.eu/map.html?Q=" + q

    webbrowser.open(url)

    print(f'Now if everything worked AMAZINGLY\n'
          f'you should see this link in your browser\n'
          f'{url}')


if __name__ == '__main__':
    main()

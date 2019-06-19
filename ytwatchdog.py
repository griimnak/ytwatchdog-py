import sys
import time
try:
    from bs4 import BeautifulSoup
    import requests
except ImportError:
    print("bs4 and requests are not installed!")
    exit("Install: pip install bs4 requests")

"""
Seconds to minutes cheat sheet
120   -> 2m
600   -> 10m
3600  -> 1hr
43200 -> 12hr
86400 -> 24hr
"""
URL = sys.argv[1] if len(sys.argv) > 1 else "https://youtube.com/user/PewDiePie"  #  URL = ""

watch_subs = True  # or False

sleep_time = 600  # seconds


# Script start
data = {}


def soup_strip(html):
    """ Strip response html and discover youtube data
        :param html: passed by scrape() function
        :returns: data
    """
    soup = BeautifulSoup(html, 'html.parser')

    # scraped data
    data["channel_name"] = soup.title.text.replace("\n", "").replace("- YouTube", "").lstrip()
    data["sub_count"] = soup.find(
        "span", class_="yt-subscription-button-subscriber-count-branded-horizontal subscribed yt-uix-tooltip").text
    try:
        # see if related channels are listed
        data["related_channels"] = soup.find("div", class_="branded-page-v2-secondary-col")
        data["related_channels_title"] = data["related_channels"].find(
            "h2", class_="branded-page-module-title").text.replace("\n", "").lstrip()
    except:
        data["related_channels"], data["related_channels_title"] = "none", "none"


def print_yt_data():
    """ Print function
        :returns: data
    """
    print("Channel: " + data["channel_name"])
    print("Subscribers: " + data["sub_count"])
    print()
    # Related channels section
    print(data["related_channels_title"] + " (related channels)")
    # if url has related channels
    if(data["related_channels"] != "none"):
        # find ul tag
        for ultag in data["related_channels"].find_all("ul", class_="branded-page-related-channels-list"):
            # find all li tags
            for litag in ultag.find_all("li", class_="branded-page-related-channels-item spf-link clearfix"):
                # print channel name and real url
                print(litag.span.find("div", class_="yt-lockup-content").h3.text.replace(" - Channel", "") +
                      " >> https://youtube.com/channel/" + litag["data-external-id"])


def compare_sub_count():
    """ Compares sub count of subs and subs_new
    """
    subs = int(data["sub_count"].replace(",", ""))  # current data

    scrape(URL)  # renew data
    subs_new = int(data["sub_count"].replace(",", ""))  # renewed sub count

    # Subs lost
    if(subs > subs_new):
        print(data["channel_name"] + " lost", subs - subs_new, "subscribers :(")
        print(subs_new, "-", subs,)

    # Subs gained
    if(subs < subs_new):
        print(data["channel_name"] + " gained", subs_new - subs, "subscribers :D")

    # No change
    if(subs == subs_new):
        print("No change in subscription count.")
    print(data["sub_count"])
    print("\n[" + time.ctime() +"] Subscriber watchdog renewing..")


def scrape(url):
    """ Make request and return response html for work
        :param url: url to scrape defined as URL
    """
    response = requests.get(url)
    print("url: " + url)
    if response.status_code == 404:
        # invalid url
        exit("Not found.")
    elif response.status_code == 200:
        soup_strip(response.text)  # Strip & append to data{}
    else:
        exit("Failure")


def write_html(html):
    """ Debugging function
    :param html: writes to local file source.html
    """
    with open("source.html", "w", encoding="UTF-8") as f:
        f.write(html)
    f.close()


# Entry point
scrape(URL)
print_yt_data()

# Subscriber watchdog
if watch_subs == True:
    if __name__ == '__main__':
        try:
            print("\n[" + time.ctime() + "] Watching subscriber count every", sleep_time/60, "minutes..")
            while True:
                time.sleep(sleep_time)
                compare_sub_count()
        except KeyboardInterrupt:
            exit("\nGoodbye")

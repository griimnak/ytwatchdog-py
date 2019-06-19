# ytwatchdog-py

![Alt Text](https://i.imgur.com/XIzLbfH.png)

Simple watchdog script that monitors youtube subscription count by scraping channel html with bs4.


Usage:
```sh
$ python ytwatchdog.py https://youtube.com/user/PewDiePie
```

Config:
```python
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
```
<b>Note: Don't set the sleep time to less than 2 minutes or youtube could block your requests.</b>

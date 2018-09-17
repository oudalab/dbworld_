# dbworld_
A script for running the dbworld_ announcement feed

To run,

```bash
watch -n 600 python3 checkandupdate.py | tee dbworld.log
```

Need to install

bs4 BeautifulSoup
requests

sudo apt install python3-pip3
pip3 install bs4
pip3 install requests
pip3 install lxml

## Print all entries

python3 -c "import shelve,json; print(json.dumps(shelve.open('dbworld.shelve')['rows']))"

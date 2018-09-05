#! /bin/bash

watch -n 600 python3 checkandupdate.py | tee dbworld.log

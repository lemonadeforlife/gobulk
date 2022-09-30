#!/bin/bash
cd ~/.local/share/applications/
git clone https://github.com/lemonadeforlife/gobulk.git
cd gobulk
python3 -m pip install -r requirements.txt
ln -s ~/.local/share/applications/gobulk/downime.py ~/.local/bin/gobulk
echo Installation complete!
echo
echo run gobulk login
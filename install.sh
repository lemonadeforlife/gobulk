#!/bin/bash
cd ~/.local/share/applications/
mkdir gobulk && cd gobulk
wget --content-disposition https://github.com/lemonadeforlife/gobulk/releases/download/latest/gobulk.tar.gz
tar -zxf gobulk.tar.gz
rm -rf gobulk.tar.gz
python3 -m pip install -r requirements.txt
ln -s ~/.local/share/applications/gobulk/downime.py ~/.local/bin/gobulk
echo Installation complete!
echo
echo run gobulk login
#!/bin/bash
cd ~/.local/share/applications/
wget -c "https://github.com/lemonadeforlife/gobulk/releases/download/latest/gobulk.tar.gz" | tar -xz
python3 -m pip install -r requirements.txt
cd gobulk && ln -s downime.py gobulk
mv gobulk ~/.local/bin
clear
echo Installation complete!
gobulk login
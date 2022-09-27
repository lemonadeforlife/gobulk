#!/bin/bash
cd ~/.local/share/applications/
wget -c "https://github.com/lemonadeforlife/gobulk/releases/download/latest/gobulk.tar.gz" | tar -xz
cd gobulk && ln -s downime.py gobulk
mv gobulk ~/.local/bin
echo Installation complete!
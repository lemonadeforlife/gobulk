# gobulk ⏬
Gets your favorite anime all episode download link from [gogoanime](https://gogoanime.tel)
You can batch download from your favorite download manager like aria2c or uGet.
It exports download link txt format in documents folder for other download manager. So that you can import and bulk download your favorite anime.

* [Setup](https://github.com/lemonadeforlife/gobulk#setup)
  * [Install](https://github.com/lemonadeforlife/gobulk#install)
	
  * [Login](https://github.com/lemonadeforlife/gobulk#login)
* [Usage](https://github.com/lemonadeforlife/gobulk#usage)
  * [resolution](https://github.com/lemonadeforlife/gobulk#resolution)
  * [Custom episode](https://github.com/lemonadeforlife/gobulk#Custom-episode)
  * [Exclude episode](https://github.com/lemonadeforlife/gobulk#Exclude-episode)
  * [Command Formats](https://github.com/lemonadeforlife/gobulk#command-formats)
  * [Search & Download](https://github.com/lemonadeforlife/gobulk#search--download)

<br>

#### Supported Platform:
* Linux <br> Tested on Linux Mint 21 vanessa & Ubuntu 22.04 jammy

<br>
<br>

## Setup
#### Install:
create `install.sh` file and copy paste this [lines](https://github.com/lemonadeforlife/gobulk/releases/tag/Linux) and run:
```bash
chmod +x install.sh && ./install.sh
```
Don't worry I didn't use any selenium. Only requests and Beautifulsoup <br/>Tested on python3.8 & python3.10<br/>
#### Login
If you don't have gogoanime account then [create](https://gogoanime.tel/login.html) one. Because now gogoanime gives download access only if we log in.<br>
![](https://github.com/lemonadeforlife/gobulk/blob/52b859b31e34ab2354b8569c7d337c02d637bce1/img/gogoanime_list_download.png "gogoanime download options at login") <br/><br/>

Get your user-agent from [here](https://www.whatismybrowser.com/detect/what-is-my-user-agent/)<br>
Because even though you have entered the correct email and password<br>The server will reject and return **403**.<br>Because gogoanime doesn't accept bot requests so we are using custom headers and pretending like a browser.

**Finally**:
```
gobulk login
```
<br>

## Usage:
```
gobulk URL QUALITY OPTIONS
```
<br>


### resolution
By default resolutions is 720 and it will automatically get whole episode download link.<br>
Example:
```bash
# To download 480
$ gobulk URL 480

# OR
$ gobulk URL 720x480
```
*[Note: It doesn't convert any video. It's just a video link grabber. If the spicified resolution found it will return the link]*

**To get specific episode download with default resolution**:
```
gobulk URL episode_no
```
Example: (To get episode no. 20 from an anime with default resolution)
```
gobulk https://gogoanime.tel/category/3-gatsu-no-lion 20
```
<b>To get specific episode download with custom resolution</b>:
```
gobulk URL quality episode_no
```
Example: (To get episode no. 20 from an anime with custom resolution)
```
gobulk https://gogoanime.tel/category/3-gatsu-no-lion 1080 20
```
<br>

### Custom episode
To download a single episode
```bash
$ gobulk URL ep

# Example(To get episode no. 20 from an anime):

$ gobulk https://gogoanime.tel/category/3-gatsu-no-lion 20
```
<br>

To specify range you need to use `colon(:)`.Its work just like Python slice.
```
gobulk URL episode_no:episode_no
```
Example:(To get episode no. 7-13 download link from an anime with custom resolution)
```bash
$ gobulk URL 1920x1080 7:13
# OR
$ gobulk URL 1080 7:13

# it will start download from ep 5 to the very end of the anime
$ gobulk URL 480 5:

# it will start download from ep 1 to 20 episode
$ gobulk URL :20
```

<br>

### Exclude episode

Many times we want to exclude fillers or episodes that we already downloaded or by the time some download links might expire while downloading. In that situation excluding options come handy.
```
gobulk URL QUALITY|default EPISODE|CUSTOM_EP|default EXCLUDE
```
For single exclude you have to use `comma(,)` at the end. If you want to exclude only episode 5 then you have to use `5,` same goes for single range if you want to exclude from range 40 to 47 it will be `40-47,` **use `-` for range in exclude**.
Example:
```bash

# This command will get download link of ONE PIECE in 480p all episode except 5
$ gobulk https://gogoanime.tel/category/one-piece 480 5,

# This command will get download link of ONE PIECE in 720 18 to 25 except 23
$ gobulk https://gogoanime.tel/category/one-piece 720 18:25 23,

# This command will get download link of One Piece in 1080 25 to 80 except 40 to 47
$ gobulk https://gogoanime.tel/category/one-piece 720 25:80 40-47,
```
now there are some cases where you want to get rid of multiple episodes. In that case you don't need to use `comma(,)` at the end.
```bash
# This command will get download link of ONE PIECE in 1080p 100 episodes except it will ignore 40 to 50,63,75,84 to 87,90
$ gobulk https://gogoanime.tel/category/one-piece 1080 :100 40-50,63,75,84-87,90
```

<br>

### Command Formats:
```bash
# To get all episode download link with default resolutions or 720p
$ gobulk https://gogoanime.tel/category/one-piece

# To get download link from 20 to the end with 360p except 36 to 39
$ gobulk https://gogoanime.tel/category/great-teacher-onizuka 360 20: 36-39,

# To get all episode download link with default resolution except episode 1 to 10
$ gobulk https://gogoanime.tel/category/great-teacher-onizuka 1-10,
```

<br>

### Search & Download
Don't worry its very interactive. Just type:
````
gobulk search
````

* To specify range use `:` (colon) example --> 1:5</li>

* To exclude single episode or episode range use `,` (comma) example: 1-5, OR 2,</li>

* To exclude multiple episode or multiple range or both use coma as well but this time it doesn't need add at end.<br>
	example: `2,3,5` or `1-5,10-15` or `1-5,9,11,20-13`

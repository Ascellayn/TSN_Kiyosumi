<p align="center">
	<img src="https://sirio-network.com/Root/Banner/Unknown.png" alt="Kiyosumi Banner">
	<h2 align="center">A silly Pixiv-Based Artwork Stash Browser</h2>
</p>
<p align="center">
	modern problems require modern solutions.
</p>

<br> <br> <br> <br> <br>

# How to use
##### 1: Download Repository
##### 2: Install dependencies
- [TSN Abstracter v6.1+](https://github.com/Ascellayn/TSN_Abstracter)
- `python3-httpx`
- `python3-dotenv`
##### 3: Configure .env
Create a `.env` file that should look something like this:
```.env
pixivCookie="PHPSESSID=...;" # You can get this via your Cookies
pixivUA="..." # THIS MUST BE THE SAME USER AGENT YOU USE WITH PIXIV
discordWebhook="https://canary.discord.com/api/webhooks/.../..." # OPTIONAL

Input="myStash"
Output="Output"
```
##### 4: Configure Exclusions (Optional)
Create a `Exclusions.json` file that should look something like this:
```json
{
	"Tag": [],
	"Character": [],
	"Source": []
}
```
Note: This file is automatically created when Kiyosumi is launched.
##### 5: is cooking time
Run inside a terminal `python3 TSN_Kiyosumi.py` in the same directory as where you downloaded the Kiyosumi Repository.


<br>


## Artwork Stash Schema:
Following how I stash things is relatively simple, at the root of your stash, divide each and every single one of your artwork **per source material**.  
Then divide everything **per character and "tag"**. This must be in the format `Character Name (Tag)`.  
Finally each file MUST BE SAVED WHILE **KEEPING THE ORIGINAL PIXIV FILE NAME** INTACT (ie: `111758984_p1.jpg`)  

If this is too complicated for you to understand this way then here's how it basically should look like:
```
/
	- Blue Archive/
		- Mika Misono (Silly)
			- 111758984_p1.jpg
			- ...
		- Mika Misono (Cute)
			- 113297402_p0.jpg
			- ...
		- ...
	- ...
```


<br>


## ok but why lol
You'd be surprised, but actually a lot of people crawl into my hands to get artworks I've picked *(after I've made them addicted accidentally)*.  
I wish I was joking. This tool was created solely so that people would stop asking me directly and go to the deployed version of Kiyosumi.  
People have been converted into loving Blue Archive because of apparently how good the artworks I pick are.  
To be fair this isn't a healthy obsession, I do pour literal hours browsing through Pixiv looking for something to explode my heart in cuteness. I guess as a result of me being ungodly picky about what I choose to save, that this is why the quality is out there.  

Art is to be shared and tasted with your eyes as if it were fine wine.  
Please do recognize these artists pouring their time, effort, money and soul to create such beautiful eye candy that would send one straight into heaven.  


<br>


### Additional Random Notices
- **Kiyosumi's Templates are by default using [The Sirio Network Design Language (TSNDL)](https://sirio-network.com/project/tsndl), however usage of TSNDL outside of The Sirio Network is STRICTLY FORBIDDEN**
If you are going to deploy a version of Kiyosumi publicly, make sure to replace TSNDL with your own CSS.
- At the time of writing Kiyosumi does not serve any of the images you have save and thus piggy backs off of Phixiv's proxy service.  
I haven't tested but beware depending on the size of the stash you may get rate limited.  
- AI generated or assisted filth are unsupported by Kiyosumi and are automatically ignored and will not show up.  
- Do avoid as much as possible deleting the `Kiyosumi.cache` file, it takes forever to regenerate depending on the stash's size.
- This project is obviously not serious and barely fits The Sirio Network's professional impressions.
*i mean what did you expect this project literally outs me as a gooner*

<br>


#### Special "I fucked up" Notice
This project single-handled caused the closure of the Phixiv API.  
No seriously. It happened during late refactoring of a major portion of the code where I had to constantly send requests.  

Apologies, I genuinely sharted that one up. I probably should've asked how the black magic worked instead of being lazy and calling Phixiv to get their proxied urls instead of figuring out myself how the url format worked.  
This project still heavily pegs Phixiv however when a client goes to one of the "browse" pages, as each individual Artwork goes back to Phixiv for the URLs.  
Fun fact actually, if this project was so delayed to become public this is the exact reason why. I was a bit very concerned if a lot of people were to use this tool (I doubt it but you never know) that it'd cause absolute hell.

I do intend someday to manually myself host the images to not piss off the Phixiv servers but that's something planned for later.  


<br>
<br>
<br>


###### The Sirio Network Design Language © 2022-2026 | All Rights Reserved
###### [Kiyosumi © Ascellayn (2025-2026) - TSN License 2.2 Universal](./LICENSE.md)
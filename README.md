# TSN Project Codename "Misono"
TSN "Misono" is a currently extremely simple [TSNA-Based](https://github.com/Ascellayn/TSN_Abstracter) Python Script that automatically creates TSNWE-Compliant Webpages containing a repository of every single artwork "stashed" according to the APSF (Ascellayn's Pixiv Stash Format).  

> *As an enjoyer and consumer of artworks, I find myself often sharing many artworks, and turns out people really enjoy my tastes.*  
> *Since I'm pretty good with scripting I just decided why not make this tool even if it's just for myself.*  
> - Ascellayn


> [!WARNING]
> TSN Misono does a RIDICULOUS amounts of API Requests to Phixiv and Pixiv in order to get Source/Character Descriptions and Proxied URLs to properly show previews on the resulting pages.
> So... Please be kind and don't run this script an obscenely huge stash. TSN Misono does automatically cache requests inside `Misono.cache` in a futile attempt to avoid further API Spam, so do not delete that file it's very important.

We recommend providing Misono with a `.env` containing your Pixiv cookie, not having your token for Pixiv will result in far worse descriptions! (Seems like Pixiv silently locks down those...)  

## Dependencies
- [TSN_Abstracter v5.4.0 (or above)](https://github.com/Ascellayn/TSN_Abstracter)
- python3-httpx
- python3-re
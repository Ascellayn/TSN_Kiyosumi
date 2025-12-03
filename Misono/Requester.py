from Misono.Globals import *;

def Fetch_Artwork(Pixiv_ID: str) -> dict[str | int, Any] | None:
	global Cache_JSON;
	Headers: dict[str, str] = {
		"User-Agent": f"TSN_Misono/{Misono_Version} Ascellayn/TSN_Misono",
		"Contact-Information": "contact+tsn_misono@sirio-network.com"
	}; URL: str = f"https://www.phixiv.net/api/info?id={Pixiv_ID}&language=en";

	if (Pixiv_ID in Cache_JSON.keys()):
		Log.Debug(f"CACHED | {Pixiv_ID}"); return Cache_JSON[Pixiv_ID];

	Log.Warning(f"GET | {URL} ...");
	Response: httpx.Response = httpx.get(URL, headers=Headers);
	if (Response.status_code != 200): Log.Awaited().ERROR(f"Unexpected Status Code: {Response.status_code}"); return None;
	Log.Awaited().OK();

	JSON: dict[str | int, Any] = {
		"Title": Response.json()["title"],
		"Description": Response.json()["description"],
		"Author_Name": Response.json()["author_name"],
		"Author_ID": Response.json()["author_id"],
		"Date": Time.Convert_Datetime(Time.Convert_ISO8601(Response.json()["create_date"])),
		"NSFW": True if (Response.json()["x_restrict"] == 1) else False,
		"AI": True if (Response.json()["ai_generated"]) else any(AI_Tag in Response.json()["tags"] for AI_Tag in ["AI-assisted", "aI-generated illustration"]),
		"Tags": [Tag[1:] for Tag in Response.json()["tags"]], # Remove extra "#" at the beginning
		"Images": Response.json()["image_proxy_urls"],
	};

	Log.Debug(f"CACHING | {Pixiv_ID} ...");
	Cache_JSON[Pixiv_ID] = JSON;
	File.JSON_Write("Misono.cache", Cache_JSON, True);
	Log.Awaited().OK();

	return JSON;
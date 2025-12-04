from Misono.Globals import *;

def Fetch_Artwork(Pixiv_ID: str, Attempt: int = 1) -> dict[str | int, Any] | None:
	Headers: dict[str, str] = {
		"User-Agent": f"TSN_Misono/{Misono_Version} Ascellayn/TSN_Misono",
		"Contact-Information": "contact+tsn_misono@sirio-network.com"
	}; URL: str = f"https://www.phixiv.net/api/info?id={Pixiv_ID}&language=en";

	if (Pixiv_ID in Cache_JSON["Artworks"].keys()): Log.Debug(f"CACHED | {Pixiv_ID}"); return Cache_JSON["Artworks"][Pixiv_ID];
	else: Cache_JSON["Artworks"][Pixiv_ID] = {};

	if (Attempt == 1):
		if (not Fetch_Valid(Pixiv_ID)):
			Log.Warning(f"Pixiv Artwork of ID {Pixiv_ID} no longer exists!");
			Cache_JSON["Artworks"][Pixiv_ID]["Fetched"] = None;

			Log.Debug(f"CACHING | {Pixiv_ID} ...");
			File.JSON_Write("Misono.cache", Cache_JSON, True);
			Log.Awaited().OK();

			return None;

	Log.Warning(f"GET | {URL} ...");
	Response: httpx.Response = httpx.get(URL, headers=Headers);
	if (Response.status_code != 200):
		if (Attempt > 5): Log.Error(f"failed to communicate for over 10 times with the Phixiv API!"); return None;
		Log.Warning(f"Attempt N°{Attempt}: Rate Limited by Phixiv or API Down! Retrying in {Attempt * Attempt} seconds.\nStatus Code: {Response.status_code} | Content:\n{Response.content}");
		Time.time.sleep(Attempt * Attempt);
		return Fetch_Artwork(Pixiv_ID, Attempt + 1);

	Log.Awaited().OK();


	JSON: dict[str | int, Any] = {
		"Fetched": Time.Get_Unix(),
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
	Cache_JSON["Artworks"][Pixiv_ID] = JSON;
	File.JSON_Write("Misono.cache", Cache_JSON, True);
	Log.Awaited().OK();

	return JSON;



def Fetch_Abstract(Tag: str, Attempt: int = 1) -> str:
	if (Tag not in Cache_JSON["Abstracts"].keys()): Cache_JSON["Abstracts"][Tag] = {};
	
	if ("Description" in Cache_JSON["Abstracts"][Tag].keys()):
		Log.Debug(f"CACHED | {Tag}"); return Cache_JSON["Abstracts"][Tag]["Description"];

	Headers: dict[str, str] = {
		"User-Agent": f"TSN_Misono/{Misono_Version} Ascellayn/TSN_Misono",
		"Contact-Information": "contact+tsn_misono@sirio-network.com",
		"Cookie": Cookie if (Cookie) else "null"
	}; URL: str = f"https://www.pixiv.net/ajax/search/tags/{Tag}?lang=en";
	print(URL);

	Log.Debug(f"GET {URL} ...");
	Response: httpx.Response = httpx.get(URL, headers=Headers);
	if (Response.status_code != 200):
		if (Attempt > 5): Log.Error(f"failed to communicate for over 10 times with the Pixiv API!"); return "<i>An error occurred while attempting to fetch the Pixpedia Abstract!</i>";
		Log.Warning(f"Attempt N°{Attempt}: Rate Limited by Pixiv or API Down! Retrying in {Attempt * Attempt} seconds.\nStatus Code: {Response.status_code} | Content:\n{Response.content}");
		Time.time.sleep(Attempt * Attempt);
		return Fetch_Abstract(Tag, Attempt + 1);
	Log.Awaited().OK();

	Log.Debug(f"CACHING | {Tag}");
	print(Response.json());
	print(Response.json()["body"]["pixpedia"]);
	Cache_JSON["Abstracts"][Tag] = {
		"Description": Response.json()["body"]["pixpedia"].get("abstract", "<i>No Pixpedia Abstract was found!</i>"),
		"Fetched": Time.Get_Unix()
	};
	File.JSON_Write("Misono.cache", Cache_JSON, True);
	Log.Awaited().OK();

	return Cache_JSON["Abstracts"][Tag]["Description"];



def Fetch_Valid(Pixiv_ID: str, Attempt: int = 1) -> bool:
	Headers: dict[str, str] = {
		"User-Agent": f"TSN_Misono/{Misono_Version} Ascellayn/TSN_Misono",
		"Contact-Information": "contact+tsn_misono@sirio-network.com"
	}; URL: str = f"https://www.pixiv.net/ajax/illust/{Pixiv_ID}?lang=en";

	Log.Debug(f"GET | {URL} ...");
	try: Response: httpx.Response = httpx.get(URL, headers=Headers);
	except Exception as Except:
		if (Attempt > 5): Log.Error(f"Failed to communicate for over 10 times with the Pixiv API!"); return False;
		Log.Warning(f"Attempt N°{Attempt}: Rate Limited by Pixiv or API Down! Retrying in {Attempt * Attempt} seconds.\nException:\n{Except}");
		Time.time.sleep(Attempt * Attempt);
		return Fetch_Valid(Pixiv_ID, Attempt + 1);

	Log.Awaited().OK();

	return (not Response.json()["error"]);

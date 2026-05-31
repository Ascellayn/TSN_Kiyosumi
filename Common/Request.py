from .Globals import *;
import time;





class Ratelimited(Exception): ...;
def Fetcher(URL: str, Attempt: int | None = None, maxAttempts: int = 3) -> dict[str, Any] | None:
	if (not Attempt): Attempt = 0;
	Attempt += 1;


	Log.Stateless(f"[GET ({Attempt}/{maxAttempts})] {URL}...");
	try:
		R: httpx.Response = httpx.get(URL, headers=HEADERS_AUTH);
		if (R.status_code not in [200, 404]):
			error: dict[str, Any] | None = None;
			try: error = R.json();
			except: pass;
			if (R.status_code == 429): raise Ratelimited("429 - Too Many Requests");
			raise Exception(f"Unhandled HTTP Code: {R.status_code}{f'\n{error}' if (error) else ''}");
		JSON: dict[str, Any] = R.json();
		Log.Awaited().OK();
		return JSON;
	except Ratelimited as E:
		if (Attempt > maxAttempts):
			Log.Awaited().EXCEPTION(E, Traceback=False);
			Log.Critical(f"Could not communicate with the Pixiv API after {Attempt} attempts! Giving up.");
			return None;
		Log.Awaited().EXCEPTION(E, Traceback=False);
		Log.Stateless(f"Retrying after {Attempt * 65} seconds.");
		time.sleep(Attempt * 65);
		return Fetcher(URL, Attempt, maxAttempts);
	except Exception as E:
		Log.Awaited().EXCEPTION(E, Traceback=False);
		return None;





def FUCK_CLANKERS(DETAILS: Type.pxDetails) -> bool:
	# isnt this a bit ironic since tsn_kiyosumi is... well a clanker? it's an automated script so it's a bot.
	# eh whatever fuck ai slop imagery
	if (DETAILS["body"]["aiType"] == 2): return True;

	AllTags: set[str] = set();
	for TAG in DETAILS["body"]["tags"]["tags"]:
		AllTags.add(TAG["tag"]);
		if ("romaji" in TAG.keys() and TAG["romaji"]): AllTags.add(TAG["romaji"]);
		if ("translation" in TAG.keys()):
			if (TAG["translation"] and LANGUAGE in TAG["translation"].keys()): AllTags.add(TAG["translation"][LANGUAGE]);

	for TAG in AllTags:
		if (TAG.lower() in AI_TAGS): return True;
	return False;





def Artwork(Pixiv_ID: str) -> Type.KiyoArtwork | Type.KiyoDummy | None:
	if (Pixiv_ID in KiyoCache["Artworks"].keys()):
		Log.Debug(f"CACHED ARTWORK: {Pixiv_ID}");
		return KiyoCache["Artworks"][Pixiv_ID];



	try:
		PAGES: Type.pxPages | None = cast(Type.pxPages, Fetcher(Strings.API.Pages(Pixiv_ID)));
		if (not PAGES): raise Exception("Empty API Response.");
	except: return None;
	
	if (PAGES["error"]):
		Log.Warning(f"Pixiv Artwork \"{Pixiv_ID}\" no longer exists!");
		KiyoCache["Artworks"][Pixiv_ID] = {
			"Error": True,
			"Stashed": Time.Get_Unix()
		};
		return KiyoCache["Artworks"][Pixiv_ID];

	try:
		DETAILS: Type.pxDetails | None = cast(Type.pxDetails, Fetcher(Strings.API.Details(Pixiv_ID)));
		if (not DETAILS): raise Exception("Empty API Response.");
	except: return;

	Images: list[Type.KiyoImage] = [];
	for IMG in PAGES["body"]:
		Images.append({
			"URL": f"https://phixiv.net/i/{IMG['urls']['regular'].replace('https://i.pximg.net/', '')}",
			"Width": IMG["width"],
			"Height": IMG["height"]
		});
	
	Tags: list[Type.KiyoTag] = [];
	for TAG in DETAILS["body"]["tags"]["tags"]:
		Tags.append({
			"Name": TAG["tag"],
			"Romanji": TAG.get("romaji", None),
			"Translation": TAG.get("translation", cast(dict[str, str], None)),
		});



	KiyoCache["Artworks"][Pixiv_ID] = {
		"Error": False,
		"Stashed": Time.Get_Unix(),
		"ID": DETAILS["body"]["illustId"],
		"Title": DETAILS["body"]["illustTitle"],
		"Description": DETAILS["body"]["illustComment"],
		"Artist_Name": DETAILS["body"]["userName"],
		"Artist_ID": DETAILS["body"]["userId"],
		"Date": Time.Convert_Datetime(Time.Convert_ISO8601(DETAILS["body"]["uploadDate"])),
		"NSFW": DETAILS["body"]["xRestrict"] == 1,
		"AI": FUCK_CLANKERS(DETAILS),
		"Tags": Tags,
		"Images": Images
	};

	return KiyoCache["Artworks"][Pixiv_ID];





def Abstract(Abstract: str) -> str:
	if (Abstract in KiyoCache["Abstracts"].keys()):
		Log.Debug(f"CACHED ABSTRACT: {Abstract}");
		return KiyoCache["Abstracts"][Abstract]["Description"];

	RAW: dict[str, Any] | bool | None = Fetcher(Strings.API.Abstract(Abstract));
	if (not RAW): Log.Warning(f"Ignoring {Abstract} for this run of {App.Name}."); return f"<code>Unable to obtain Abstract \"{Abstract}\" for this session of {App.Name}.</code>";
	KiyoCache["Abstracts"][Abstract] = {
		"Error": RAW["error"],
		"Fetched": Time.Get_Unix(),
		"Description": f"<code>An error occurred while attempting to get the Abstract \"{Abstract}\"</code>" if (RAW["error"]) else RAW["body"]["pixpedia"].get("abstract", f"<code>No Pixpedia Abstract was found associated with \"{Abstract}\"</code>")
	};
	
	return KiyoCache["Abstracts"][Abstract]["Description"];
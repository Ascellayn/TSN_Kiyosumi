from TSN_Abstracter import TSN_Abstracter, Config, File, Log, Time;
from typing import Any;
import httpx, re;

Misono_Version: str = "v0.1";


Cache_JSON: dict[str | int, Any] = File.JSON_Read("Misono.cache", True);

def Fetch_Artwork(Pixiv_ID: str) -> dict[str, str] | None:
	global Cache_JSON;
	Headers: dict[str, str] = {
		"User-Agent": f"TSN_Misono/{Misono_Version}",
		"Contact-Information": "contact+tsn_misono@sirio-network.com"
	}; URL: str = f"https://www.phixiv.net/api/info?id={Pixiv_ID}&language=en";

	if (Pixiv_ID in Cache_JSON.keys()):
		Log.Info(f"CACHED | {Pixiv_ID}"); return Cache_JSON[Pixiv_ID];

	Log.Warning(f"GET | {URL} ...");
	Response: httpx.Response = httpx.get(URL, headers=Headers);
	if (Response.status_code != 200): Log.Awaited().ERROR(f"Unexpected Status Code: {Response.status_code}"); return None;
	Log.Awaited().OK();

	JSON: dict[str, Any] = {
		"Title": Response.json()["title"],
		"Description": Response.json()["description"],
		"Author_Name": Response.json()["author_name"],
		"Author_ID": Response.json()["author_id"],
		"Date": Time.Convert_Datetime(Time.Convert_ISO8601(Response.json()["create_date"])),
		"NSFW": True if (Response.json()["x_restrict"] == 1) else False,
		"AI": Response.json()["ai_generated"],
		"Tags": [Tag[1:] for Tag in Response.json()["tags"]], # Remove extra "#" at the beginning
		"Images": Response.json()["image_proxy_urls"],
	};

	Log.Info(f"CACHING | {Pixiv_ID} ...");
	Cache_JSON[Pixiv_ID] = JSON;
	File.JSON_Write("Misono.cache", Cache_JSON, True);
	Log.Awaited().OK();

	return JSON;

if (__name__ == "__main__"):
	Log.Clear(); TSN_Abstracter.Require_Version((5,3,1));
	Config.Logger.File = False;
	Log.Stateless(f"TSN Misono - {Misono_Version}");

	# Config Validation
	Log.Info("Loading Configuration...");
	Root_CFG: dict[str | int, Any] = File.JSON_Read("Root_CFG.json");

	HTML_Folder: str | None = Root_CFG.get("HTML_Folder");
	if (not HTML_Folder): Log.Awaited().ERROR("Root_CFG → HTML_Folder is null."); exit();

	HTML_Template: str | None = Root_CFG.get("HTML_Template");
	if (not HTML_Template): Log.Awaited().ERROR("Root_CFG → HTML_Template is null."); exit();
	if (not File.Exists(HTML_Template)): Log.Awaited().ERROR("HTML_Template → File Not Found"); exit();

	Stash_Folder: str | None = Root_CFG.get("Stash_Folder");
	if (not Stash_Folder): Log.Awaited().ERROR("Root_CFG → Stash_Folder is null."); exit();
	if (not File.Exists(Stash_Folder)): Log.Awaited().ERROR("Stash_Folder → Folder Not Found"); exit();

	Log.Awaited().OK();

	# PoC Stash Seeker
	Log.Info("Analyzing Stash...");
	Stash_Tree: tuple[tuple[File.Folder_Matrix, ...], File.Folder_Contents] = File.Tree(Stash_Folder);
	Log.Awaited().OK();
	Stash_JSON: dict[str | int, Any] = {};
	
	for Source in Stash_Tree[0]:
		#Log.Info(f"Processing: {Source[0]}");
		for Character_Matrix in Source[1][0]:
			Character_Folder: str = Character_Matrix[0];

			Character_Match: re.Match[str] | None = re.search(pattern=r"(?<= \().+(?=\))", string=Character_Folder);
			Character_Tag: str | None = Character_Match[0] if (Character_Match) else None;
			if (not Character_Tag): Log.Error(f"{Source[0]}/{Character_Folder} → Tag not in Folder Name");
			del Character_Match;

			Character_Name: str = Character_Folder.replace(f" ({Character_Tag})","");

			for Artworks in Character_Matrix[1]:
				for Artwork in Artworks:
					Artwork_File: str = str(Artwork); # Shush big typing.

					Pixiv_IDm: re.Match[str] | None = re.search(pattern=r"\d+(?=_p)", string=Artwork_File);
					Pixiv_ID: str | None = Pixiv_IDm[0] if (Pixiv_IDm) else None;
					if (not Pixiv_ID): Log.Error(f"{Source[0]}/{Character_Name}/{Character_Tag}/{Artwork_File} → IGNORED | Invalid PixivID"); continue;
					del Pixiv_IDm;

					Pixiv_sIDm: re.Match[str] | None = re.search(pattern=r"(?<=_p)\d+", string=Artwork_File);
					Pixiv_sID: str | None = Pixiv_sIDm[0] if (Pixiv_sIDm) else None;
					if (not Pixiv_sID): Log.Error(f"{Source[0]}/{Character_Name}/{Character_Tag}/{Artwork_File} → IGNORED | Invalid Pixiv Sub ID"); continue;
					del Pixiv_sIDm;

					Log.Info(f"{Source[0]}/{Character_Name}/{Character_Tag}/{Pixiv_ID}/{Pixiv_sID} ...");
					Artwork_Details: dict[str, str] | None = Fetch_Artwork(Pixiv_ID);
					if (not Artwork_Details): Log.Error(f"{Source[0]}/{Character_Name}/{Character_Tag}/{Artwork_File} → IGNORED | Could not fetch Artwork Details"); continue;

					print(Artwork_Details);
					Log.Awaited().OK();

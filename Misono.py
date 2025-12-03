from TSN_Abstracter import TSN_Abstracter, Config, File, Log, Time;
from typing import Any;
import httpx, random, re;





Misono_Version: str = "v0.3";
Cache_JSON: dict[str | int, Any] = File.JSON_Read("Misono.cache", True);



def Pixiv_Artist(Artist_ID: str) -> str: return f"https://www.pixiv.net/en/users/{Artist_ID}";
def Pixiv_Artwork(Artwork_ID: str) -> str: return f"https://www.pixiv.net/en/artworks/{Artwork_ID}";
def Stash_File(Source: str, Character_Name: str, Character_Tag: str) -> str: return f"{HTML_Folder}/{Source.replace(" ", "_")}/{Character_Name.replace(" ", "_")}-{Character_Tag}.html";



def HTML_Compiler(
		HTML: str,
		Artwork: dict[str | int, Any] | None,
		Source: str, Character_Name: str, Character_Tag: str,
		Pixiv_ID: str | None, Pixiv_sID: int | None,
		Tags_All: set[str] = set(), Artwork_Embeds: list[str] = [],
		Artworks: list[str] = [], Sources: list[str] = []
	) -> str:
	return HTML\
.replace("{Artwork_Image}", Artwork["Images"][Pixiv_sID].replace(".mp4", ".gif") if (Artwork) else "")\
.replace("{Artwork_Title}", Artwork["Title"] if (Artwork) else "")\
.replace("{Artwork_Description}", Artwork["Description"] if (Artwork) else "")\
.replace("{Artwork_URL}", Pixiv_Artwork(Pixiv_ID) if (Pixiv_ID) else "")\
.replace("{Artwork_Tags}", ", ".join(f"#{Tag}" for Tag in [Artwork["Tags"]]) if (Artwork) else "")\
.replace("{Artwork_Date}", " ".join(Time.Get_DateStrings(Artwork["Date"]) if (Artwork) else ""))\
.replace("{Artwork_Random}", Artworks[random.randint(0, len(Artworks) - 1)] if (Artworks) else "")\
\
.replace("{Artist_Name}", Artwork["Author_Name"] if (Artwork) else "")\
.replace("{Artist_URL}", Pixiv_Artist(Artwork["Author_ID"]) if (Artwork) else "")\
\
.replace("{Source_Name}", Source)\
.replace("{Source_Character}", Character_Name)\
.replace("{Source_Tag}", Character_Tag)\
.replace("{Source_Keywords}", ", ".join(Tags_All))\
.replace("{Source_Sources}", ", ".join(Sources))\
\
.replace("{TSN_Misono}", "\n<br>\n".join(Artwork_Embeds))\
.replace("{TSN_Misono-Version}", Misono_Version)\
.replace("{TSN_Misono-Legal}", f"TSN Misono © 2025 Ascellayn | TSN License 2.1 - Strict")\





def Fetch_Artwork(Pixiv_ID: str) -> dict[str | int, Any] | None:
	global Cache_JSON;
	Headers: dict[str, str] = {
		"User-Agent": f"TSN_Misono/{Misono_Version} Ascellayn/TSN_Misono",
		"Contact-Information": "contact+tsn_misono@sirio-network.com"
	}; URL: str = f"https://www.phixiv.net/api/info?id={Pixiv_ID}&language=en";

	if (Pixiv_ID in Cache_JSON.keys()):
		Log.Info(f"CACHED | {Pixiv_ID}"); return Cache_JSON[Pixiv_ID];

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

	Stash_Folder: str | None = Root_CFG.get("Stash_Folder");
	if (not Stash_Folder): Log.Awaited().ERROR("Root_CFG → Stash_Folder is null."); exit();
	if (not File.Exists(Stash_Folder)): Log.Awaited().ERROR("Stash_Folder → Folder Not Found"); exit();


	Templates: dict[str, int | Any] | None = Root_CFG.get("Templates");
	if (not Templates): Log.Awaited().ERROR("Root_CFG → Templates is null."); exit();

	Template_Page: str | int | None = Templates.get("Page"); # pyright: ignore[reportRedeclaration]
	if (not Template_Page): Log.Awaited().ERROR("Templates → Page is null."); exit();
	if (type(Template_Page) != str): Log.Awaited().ERROR("Templates → Page is not a string."); exit();
	if (not File.Exists(Template_Page)): Log.Awaited().ERROR("Page → File Not Found"); exit();

	tHTML_Page: str | None = File.Read(Template_Page);
	if (not tHTML_Page): Log.Awaited().ERROR("Page → File could not be read."); exit();


	Template_Artwork: str | int | None = Templates.get("Embed_Artwork");
	if (not Template_Artwork): Log.Awaited().ERROR("Templates → Artwork is null."); exit();
	if (type(Template_Artwork) != str): Log.Awaited().ERROR("Templates → Page is not a string."); exit();
	if (not File.Exists(Template_Artwork)): Log.Awaited().ERROR("Artwork → File Not Found"); exit();

	tHTML_Artwork: str | None = File.Read(Template_Artwork);
	if (not tHTML_Artwork): Log.Awaited().ERROR("Artwork → File could not be read."); exit();


	Template_Character: str | int | None = Templates.get("Embed_Character");
	if (not Template_Character): Log.Awaited().ERROR("Templates → Character is null."); exit();
	if (type(Template_Character) != str): Log.Awaited().ERROR("Templates → Character is not a string."); exit();
	if (not File.Exists(Template_Character)): Log.Awaited().ERROR("Character → File Not Found"); exit();

	tHTML_Character: str | None = File.Read(Template_Character);
	if (not tHTML_Character): Log.Awaited().ERROR("Character → File could not be read."); exit();


	Template_Source: str | int | None = Templates.get("Embed_Source");
	if (not Template_Source): Log.Awaited().ERROR("Templates → Source is null."); exit();
	if (type(Template_Source) != str): Log.Awaited().ERROR("Templates → Source is not a string."); exit();
	if (not File.Exists(Template_Source)): Log.Awaited().ERROR("Source → File Not Found"); exit();

	tHTML_Source: str | None = File.Read(Template_Source);
	if (not tHTML_Source): Log.Awaited().ERROR("Artwork → File could not be read."); exit();


	Template_Browser_Character: str | int | None = Templates.get("Browser_Character");
	if (not Template_Browser_Character): Log.Awaited().ERROR("Templates → Browser_Character is null."); exit();
	if (type(Template_Browser_Character) != str): Log.Awaited().ERROR("Templates → Browser_Character is not a string."); exit();
	if (not File.Exists(Template_Browser_Character)): Log.Awaited().ERROR("Browser_Character → File Not Found"); exit();

	tHTML_Browser_Character: str | None = File.Read(Template_Browser_Character);
	if (not tHTML_Browser_Character): Log.Awaited().ERROR("Browser_Character → File could not be read."); exit();


	Template_Browser_Source: str | int | None = Templates.get("Browser_Source");
	if (not Template_Browser_Source): Log.Awaited().ERROR("Templates → Browser_Source is null."); exit();
	if (type(Template_Browser_Source) != str): Log.Awaited().ERROR("Templates → Browser_Source is not a string."); exit();
	if (not File.Exists(Template_Browser_Source)): Log.Awaited().ERROR("Browser_Source → File Not Found"); exit();

	tHTML_Browser_Source: str | None = File.Read(Template_Browser_Source);
	if (not tHTML_Browser_Source): Log.Awaited().ERROR("Browser_Source → File could not be read."); exit();


	del Templates; del Template_Page;
	del Template_Artwork; del Template_Character; del Template_Source;
	del Template_Browser_Source; del Template_Browser_Character;

	Log.Awaited().OK();



	# PoC Stash Seeker
	Log.Info("Analyzing Stash...");
	Stash_Tree: tuple[tuple[File.Folder_Matrix, ...], File.Folder_Contents] = File.Tree(Stash_Folder);
	Log.Awaited().OK();
	Stash_JSON: dict[str | int, Any] = {};
	
	# Source Folder
	Browser_Data: dict[str | int, Any] = {};
	for Source in Stash_Tree[0]:
		# Character Folder
		Characters: list[str] = [];
		Character_Artworks: list[str] = [];
		for Character_Matrix in Source[1][0]:
			Character_Folder: str = Character_Matrix[0];

			Character_Match: re.Match[str] | None = re.search(pattern=r"(?<= \().+(?=\))", string=Character_Folder);
			Character_Tag: str | None = Character_Match[0] if (Character_Match) else None;
			if (not Character_Tag): Log.Error(f"{Source[0]}/{Character_Folder} → Tag not in Folder Name");
			Character_Tag = str(Character_Tag); # Shush big typing
			del Character_Match;

			Character_Name: str = Character_Folder.replace(f" ({Character_Tag})","");
			Characters.append(Character_Name);



			# Artwork File
			Artworks_HTML: list[str] = [];
			Tags_All: set[str] = set();
			for Artworks in Character_Matrix[1]:
				for Artwork_Raw in Artworks:
					Artwork_File: str = str(Artwork_Raw); # Shush big typing.

					Pixiv_IDm: re.Match[str] | None = re.search(pattern=r"\d+(?=_p)", string=Artwork_File);
					Pixiv_ID: str | None = Pixiv_IDm[0] if (Pixiv_IDm) else None;
					if (not Pixiv_ID): Log.Error(f"{Source[0]}/{Character_Name}/{Character_Tag}/{Artwork_File} → IGNORED | Invalid PixivID"); continue;
					del Pixiv_IDm;

					Pixiv_sIDm: re.Match[str] | None = re.search(pattern=r"(?<=_p)\d+", string=Artwork_File);
					Pixiv_sIDs: str | None = Pixiv_sIDm[0] if (Pixiv_sIDm) else None;
					if (not Pixiv_sIDs): Log.Error(f"{Source[0]}/{Character_Name}/{Character_Tag}/{Artwork_File} → IGNORED | Invalid Pixiv Sub ID"); continue;
					Pixiv_sID = int(Pixiv_sIDs);
					del Pixiv_sIDm; del Pixiv_sIDs;

					Log.Info(f"{Source[0]}/{Character_Name}/{Character_Tag}/{Pixiv_ID}/{Pixiv_sID} ...");
					Artwork: dict[str | int, Any] | None = Fetch_Artwork(Pixiv_ID);
					if (not Artwork): Log.Error(f"{Source[0]}/{Character_Name}/{Character_Tag}/{Artwork_File} → IGNORED | Could not fetch Artwork Details"); continue;
					if (Pixiv_sID > (len(Artwork["Images"]) - 1)):  Log.Error(f"{Source[0]}/{Character_Name}/{Character_Tag}/{Artwork_File} → IGNORED | Pixiv_sID is larger than proxied images: {Pixiv_sID}"); continue;

					# Embed Compilation
					Artworks_HTML.append(
						HTML_Compiler(
							tHTML_Artwork,
							Artwork,
							Source[0], Character_Name, Character_Tag,
							Pixiv_ID, Pixiv_sID
						)
					);

					Character_Artworks.append(Artwork["Images"][Pixiv_sID]);
					for Tag in Artwork["Tags"]: Tags_All.add(Tag);

					Log.Awaited().OK();

			# Page Compilation
			HTML_File_Name: str = Stash_File(Source[0], Character_Name, Character_Tag);
			Log.Info(f"Building {HTML_File_Name}...");
			try:
				File.Path_Require(HTML_File_Name);
				File.Write(HTML_File_Name, HTML_Compiler(tHTML_Page, None, Source[0], Character_Name, Character_Tag, None, None, Tags_All, Artworks_HTML, Character_Artworks));
				Log.Awaited().OK();
			except Exception as Except: Log.Awaited().EXCEPTION(Except);

			if (Source[0] not in Browser_Data.keys()): Browser_Data[Source[0]] = {};
			if (Character_Name not in Browser_Data[Source[0]].keys()): Browser_Data[Source[0]][Character_Name] = {};
			Browser_Data[Source[0]][Character_Name][Character_Tag] = Character_Artworks[random.randint(0, len(Character_Artworks) -1)];

	# Browser Compilation: TBD
	#HTML_Links: list[str] = [];

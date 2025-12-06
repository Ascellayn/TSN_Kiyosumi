from TSN_Abstracter import TSN_Abstracter, Config, File, Log, String, Time; # pyright: ignore[reportMissingTypeStubs, reportUnusedImport]
from typing import Any;
import dotenv, httpx, os, random, re; # pyright: ignore[reportUnusedImport]
dotenv.load_dotenv();



Misono_Version: str = "v0.9";
Cache_JSON: dict[str | int, Any] = File.JSON_Read("Misono.cache", True);
if (Cache_JSON == {}):
	Cache_JSON = {
		"Misono": {
			"Version": "v0.6",
			"Updated": Time.Get_Unix()
		},
		"Abstracts": {},
		"Artworks": {}
	}

Cookie: str | None = os.getenv("Cookie");
Browser_Data: dict[str, Any] = {};



# TSNA & Config Validation
Log.Clear(); TSN_Abstracter.Require_Version((5,4,0));
Config.Logger.File = False; #Config.Logger.Print_Level = 15;
Log.Stateless(f"TSN Misono - {Misono_Version}");


Log.Info("Loading and Validating Configuration...");
Root_CFG: dict[str | int, Any] = File.JSON_Read("Root_CFG.json");



def Validate_Folder(Folder: str) -> str:
	Content: str | None = Root_CFG.get(Folder);
	if not (Content): Log.Awaited("Validate_RCFG").ERROR(f"Root_CFG: {Folder} is null."); exit();
	return Content;

def Validate_Template(D: dict[str, Any], Template: str) -> str:
	Key: str | None = D.get(Template);
	if not (Key): Log.Awaited("Validate_RCFG").ERROR(f"Templates: {Template} is null."); exit();
	if (type(Key) != str): Log.Awaited().ERROR(f"Templates: {Template} is not a string."); exit();
	if (not File.Exists(Key)): Log.Awaited().ERROR(f"Templates: {Template} file not found."); exit();

	Content: str | None = File.Read(Key);
	if (not Content): Log.Awaited().ERROR(f"{Key}: File could not be read."); exit();
	return Content;

def Validate_Exclude(D: dict[str, Any], Exclusion: str) -> list[str]:
	Content: list[str] | None = D.get(Exclusion);
	if not (Content): return [];
	if (type(Content) != list): Log.Awaited().ERROR(f"Exclude: {Exclusion} is not a list."); exit();
	return Content;


Folder_Output: str = Validate_Folder("Folder_Output");
Folder_Stash: str = Validate_Folder("Folder_Stash");



Templates: dict[str, str] | None = Root_CFG.get("Templates");
if (not Templates): Log.Awaited().ERROR("Root_CFG → Templates is null."); exit();
if (type(Templates) != dict): Log.Awaited().ERROR("Root_CFG → Templates is not a dictionary."); exit();


Template_bArtwork: str = Validate_Template(Templates, "Browser_Artwork");
Template_bCharacter: str = Validate_Template(Templates, "Browser_Character");
Template_bSource: str = Validate_Template(Templates, "Browser_Source");

Template_eArtwork: str = Validate_Template(Templates, "Embed_Artwork");
Template_eCharacter: str = Validate_Template(Templates, "Embed_Character");
Template_eSource: str = Validate_Template(Templates, "Embed_Source");


Exclude: dict[str, str] | None = Root_CFG.get("Exclude");
if (not Exclude): Log.Awaited().ERROR("Root_CFG → Exclude is null."); exit();
if (type(Exclude) != dict): Log.Awaited().ERROR("Root_CFG → Exclude is not a dictionary."); exit();

Exclude_Tag: list[str] = Validate_Exclude(Exclude, "Tag");
Exclude_Character: list[str] = Validate_Exclude(Exclude, "Character");
Exclude_Source: list[str] = Validate_Exclude(Exclude, "Source");


del Root_CFG; del Templates; del Exclude;
# ↑ Baby's manual memory management



Log.Awaited().OK();



if (not Cookie):
	Log.Critical("A Pixiv Cookie was not defined in your .env! Abstracts may not get properly fetched.\n\
TSN Misono will keep executing after 30 seconds. We however still heavily recommend to stop Misono to configure your Cookie.");
	Time.time.sleep(30);

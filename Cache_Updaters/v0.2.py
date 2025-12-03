from TSN_Abstracter import TSN_Abstracter, Config, File, Log, Time;
from typing import Any;

def Update_Cache() -> None:
	Cache_JSON: dict[str | int, Any] = File.JSON_Read("Misono.cache", True);
	File.JSON_Write(f"Misono_v0.1-{Time.Get_Unix()}.cache_backup", Cache_JSON, True);

	Log.Stateless(f"TSN Misono - v0.1 Cache to v0.2 Cache Updater");

	Log.Info(f"Updating a Cache of {len(Cache_JSON.keys())} entries...")
	for Pixiv_ID in Cache_JSON:
		if (not Cache_JSON[Pixiv_ID]["AI"]):
			if (any(AI_Tag in Cache_JSON[Pixiv_ID]["Tags"] for AI_Tag in ["AI-assisted", "aI-generated illustration"])):
				Log.Warning(f"Correcting Maliciously Missing AI Definition for Artwork {Pixiv_ID}");
				Cache_JSON[Pixiv_ID]["AI"] = True;

	File.JSON_Write("Misono.cache", Cache_JSON, True);
	Log.Awaited().OK();


if (__name__ == "__main__"):
	Log.Clear(); TSN_Abstracter.Require_Version((5,3,1));
	Config.Logger.File = False;
	Update_Cache();
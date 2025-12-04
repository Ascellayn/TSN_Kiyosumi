from TSN_Abstracter import TSN_Abstracter, Config, File, Log, Time;
from typing import Any;

def Update_Cache() -> None:
	Cache_JSON: dict[str | int, Any] = File.JSON_Read("Misono.cache", True);
	File.JSON_Write(f"Cache_Updaters/Backups/Misono_v0.2-{Time.Get_Unix()}.cache_backup", Cache_JSON, True);

	Log.Stateless(f"TSN Misono - v0.2 Cache to v0.5 Cache Updater");

	Log.Info(f"Updating a Cache of {len(Cache_JSON.keys())} entries...")
	for Pixiv_ID in Cache_JSON.keys():
		Cache_JSON[Pixiv_ID]["Fetched"] = Time.Get_Unix();

	File.JSON_Write(
		"Misono.cache",
		{
			"Misono": {
				"Version": "v0.5",
				"Updated": Time.Get_Unix(),
			},
			"Abstracts": {},
			"Artworks": Cache_JSON
		},
		True
	);
	Log.Awaited().OK();


if (__name__ == "__main__"):
	Log.Clear(); TSN_Abstracter.Require_Version((5,4,0));
	Config.Logger.File = False;
	Update_Cache();
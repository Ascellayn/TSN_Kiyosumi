from TSN_Abstracter import TSN_Abstracter, Config, File, Log;

def Uncacher() -> None:
	Log.Stateless(f"TSN Yae - Uncacher");
	File.JSON_Write("Yae.uncached", File.JSON_Read("Yae.cache", True));


if (__name__ == "__main__"):
	Log.Clear(); TSN_Abstracter.Require_Version((5,4,0));
	Config.Logger.File = False;
	Uncacher();
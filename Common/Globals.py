from TSN_Abstracter import *;
import httpx;
import dotenv;
import os;

from . import Type;





# Environment
dotenv.load_dotenv();
def requireEnv(envVar: str, Default: str | None = None) -> str:
	var: str | None = os.getenv(envVar);
	if (not var and not Default): Log.Critical(f"Environment variable \"{envVar}\" is undefined. Exiting."); exit(1);
	if (not var and Default):
		Log.Warning(f"Environment variable \"{envVar}\" is undefined. Defaulting to \"{Default}\".");
		return Default;
	return cast(str, var);

INPUT: str = requireEnv("Input");

OUTPUT: str = requireEnv("Output", "Output");
LANGUAGE: str = requireEnv("Language", "en");

DISCORD_WEBHOOK: str | None = os.getenv("discordWebhook");





# Constants
HEADERS: dict[str, Any] = { "User-Agent": f"TSN_Kiyosumi/{TSN_Abstracter.App_Version()} (+https://github.com/Ascellayn/TSN_Kiyosumi) Python" };
HEADERS_AUTH: dict[str, Any] = { "User-Agent": requireEnv("pixivUA"), "Cookie": requireEnv("pixivCookie"), "Script-Agent": f"TSN_Kiyosumi/{TSN_Abstracter.App_Version()} (+https://github.com/Ascellayn/TSN_Kiyosumi) Python"};
if (not File.Exists("Exclusions.json")): File.JSON_Write("Exclusions.json", {"Source": [], "Tag": [], "Character": []});
EXCLUSIONS: Type.Exclusions = cast(Type.Exclusions, File.JSON_Read("Exclusions.json"));
AI_TAGS: list[str] = [
	"ai-assisted",
	"al-assisted",
	"ai_assisted",
	"al_assisted",
	"ai-generated",
	"al-generated",
	"ai_generated",
	"al_generated",
	"ai-generated illustration",
	"al-generated illustration",
	"ai_generated illustration",
	"al_generated illustration"
]; # Special message to those who set the "I" to a lower case "L" to escape the AI blacklist set in Pixiv Settings:
# Go fuck yourself you talentless piece of shit. Pick up a pen you absolute waste of dioxygen.
# Sincerely,
# - Ascellayn.





# File Constants
LASTLAUNCH: str | None = File.Read("lastlaunch.unix");
File.Write("lastlaunch.unix", str(Time.Get_Unix()));





# Global Variables
if (not File.Exists("Kiyosumi.cache")): File.JSON_Write("Kiyosumi.cache", { "_VERSION": App.Version, "Abstracts": {}, "Artworks": {}}, True);
KiyoCache: Type.KiyoCache = cast(Type.KiyoCache, File.JSON_Read("Kiyosumi.cache", True));










from . import Strings;
from . import Request;
from Misono.Globals import *;
from Misono.Requester import *;
from Misono.Strings import *;





def HTML_Compiler(
		HTML: str, Embeds: list[str],
		Artwork: dict[str | int, Any] | None,
		Source_Name: str | None = None, Character_Name: str | None = None, Character_Tag: str | None = None,
		Pixiv_ID: str | None = None, Pixiv_sID: int | None = None,
	) -> str:
	Full: bool = True if (Source_Name and Character_Name and Character_Tag) else False;

	Artwork_Total: int = 0;
	Source_Total: int = 0; Character_All: list[str] = [];
	if (Source_Name):
		Artwork_Total = len(Browser_Data[Source_Name][Character_Name][Character_Tag]["Artworks"]) if (Full) else 0;
		for Character in Browser_Data[Source_Name]:
			Character_All.append(Character);
			for Tag in Browser_Data[Source_Name][Character]:
				Source_Total += len(Browser_Data[Source_Name][Character][Tag]["Artworks"]);

	return HTML\
.replace("{Artwork_Image}", Artwork["Images"][Pixiv_sID].replace(".mp4", ".gif") if (Artwork) else "")\
.replace("{Artwork_Title}", Artwork["Title"] if (Artwork) else "")\
.replace("{Artwork_Description}", Artwork["Description"] if (Artwork) else "")\
.replace("{Artwork_URL}", Pixiv_Artwork(Pixiv_ID) if (Pixiv_ID) else "")\
.replace("{Artwork_Tags}", ", ".join(["#" + Tag for Tag in Artwork["Tags"]]) if (Artwork) else "")\
.replace("{Artwork_Date}", " ".join(Time.Get_DateStrings(Artwork["Date"]) if (Artwork) else ""))\
.replace("{Artwork_Random}", Browser_Data[Source_Name][Character_Name][Character_Tag]["Artworks"][random.randint(0, len(Browser_Data[Source_Name][Character_Name][Character_Tag]["Artworks"]) - 1)].replace(".mp4", ".gif") if (Full and Source_Name) else "")\
.replace("{Artwork_Total}", str(Artwork_Total))\
\
.replace("{Artist_Name}", Artwork["Author_Name"] if (Artwork) else "")\
.replace("{Artist_URL}", Pixiv_Artist(Artwork["Author_ID"]) if (Artwork) else "")\
\
.replace("{Character_Name}", Character_Name if (Character_Name) else "")\
.replace("{Character_Description}", Fetch_Abstract(Character_Name) if (Character_Name) else "")\
.replace("{Character_Tag}", Character_Tag if (Character_Tag) else "")\
.replace("{Character_Tags}", ", ".join(Browser_Data[Source_Name][Character_Name][Character_Tag]["Tags"]) if (Source_Name and Character_Name and Character_Tag) else "")\
.replace("{Character_Total}", str(len(Browser_Data[Source_Name].keys())) if (Source_Name) else "")\
.replace("{Character_All}", ", ".join(Character_All))\
.replace("{Character_Browser}", f"{Character_Name.replace(" ", "_")}-{Character_Tag}.html" if (Character_Name and Character_Tag) else "")\
\
.replace("{Source_Name}", Source_Name if (Source_Name) else "")\
.replace("{Source_Description}", Fetch_Abstract(Source_Name) if (Source_Name) else "")\
.replace("{Source_Total}", str(Source_Total))\
.replace("{Source_Character}", ", ".join(Browser_Data[Source_Name].keys()) if (Source_Name) else "")\
.replace("{Source_All}", ", ".join(Browser_Data.keys()))\
.replace("{Source_Browser}", f"{Source_Name.replace(" ", "_")}/Browser.html" if (Source_Name) else "")\
.replace("{Source_NameHTML}", f"{Source_Name.replace(" ", "_")}" if (Source_Name) else "")\
\
.replace("{TSN_Misono}", "\n<br>\n".join(Embeds))\
.replace("{Misono_Version}", Misono_Version)\
.replace("{Misono_Legal}", f"TSN Misono © 2025 Ascellayn | TSN License 2.1 - Strict")\
\
\
\
.replace("{Pixiv_ID}", Pixiv_ID if (Pixiv_ID) else "")\
.replace("{Pixiv_sID}", str(Pixiv_sID) if (Pixiv_sID) else "")
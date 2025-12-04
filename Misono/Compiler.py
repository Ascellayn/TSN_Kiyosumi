from Misono.Globals import *;
from Misono.Requester import *;
from Misono.Strings import *;





def HTML_Compiler(
		HTML: str, Embeds: list[str],
		Artwork: dict[str | int, Any] | None,
		Source_Name: str, Character_Name: str, Character_Tag: str,
		Pixiv_ID: str | None, Pixiv_sID: int | None,
	) -> str:
	Full: bool = True if (Source_Name and Character_Name and Character_Tag) else False;

	Artwork_Total: int = len(Browser_Data[Source_Name][Character_Name][Character_Tag]["Artworks"]) if (Full) else 0;
	Source_Total: int = 0; Character_All: list[str] = [];
	if (Source_Name):
		for Character in Browser_Data[Source_Name]:
			Character_All.append(Character);
			for Tag in Character:
				Source_Total += len(Tag);

	return HTML\
.replace("{Artwork_Image}", Artwork["Images"][Pixiv_sID].replace(".mp4", ".gif") if (Artwork) else "")\
.replace("{Artwork_Title}", Artwork["Title"] if (Artwork) else "")\
.replace("{Artwork_Description}", Artwork["Description"] if (Artwork) else "")\
.replace("{Artwork_URL}", Pixiv_Artwork(Pixiv_ID) if (Pixiv_ID) else "")\
.replace("{Artwork_Tags}", ", ".join(["#" + Tag for Tag in Artwork["Tags"]]) if (Artwork) else "")\
.replace("{Artwork_Date}", " ".join(Time.Get_DateStrings(Artwork["Date"]) if (Artwork) else ""))\
.replace("{Artwork_Random}", Browser_Data[Source_Name][Character_Name][Character_Tag]["Artworks"][random.randint(0, len(Browser_Data[Source_Name][Character_Name][Character_Tag]["Artworks"]) - 1)] if (Full) else "")\
.replace("{Artwork_Total}", str(Artwork_Total))\
\
.replace("{Artist_Name}", Artwork["Author_Name"] if (Artwork) else "")\
.replace("{Artist_URL}", Pixiv_Artist(Artwork["Author_ID"]) if (Artwork) else "")\
\
.replace("{Character_Name}", Character_Name)\
.replace("{Character_Description}", Fetch_Abstract(Character_Name))\
.replace("{Character_Tag}", Character_Tag)\
.replace("{Character_Tags}", ", ".join(Browser_Data[Source_Name][Character_Name][Character_Tag]["Tags"]) if (Source_Name and Character_Name and Character_Tag) else "")\
.replace("{Character_Total}", str(len(Browser_Data[Source_Name].keys())))\
.replace("{Character_All}", ", ".join(Character_All))\
\
.replace("{Source_Name}", Source_Name)\
.replace("{Source_Description}", Fetch_Abstract(Source_Name))\
.replace("{Source_Total}", str(Source_Total))\
.replace("{Source_Character}", ", ".join(Browser_Data[Source_Name].keys()))\
.replace("{Source_All}", ", ".join(Browser_Data.keys()))\
\
.replace("{TSN_Misono}", "\n<br>\n".join(Embeds))\
.replace("{Misono_Version}", Misono_Version)\
.replace("{Misono_Legal}", f"TSN Misono © 2025 Ascellayn | TSN License 2.1 - Strict")\
\
\
\
.replace("{Pixiv_ID}", Pixiv_ID if (Pixiv_ID) else "")\
.replace("{Pixiv_sID}", str(Pixiv_sID) if (Pixiv_sID) else "")
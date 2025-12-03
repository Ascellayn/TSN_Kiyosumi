from Misono.Globals import *;
from Misono.Strings import *;

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
.replace("{TSN_Misono-Legal}", f"TSN Misono © 2025 Ascellayn | TSN License 2.1 - Strict")
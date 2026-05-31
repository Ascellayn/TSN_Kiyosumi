from .Globals import *;
from typing import Iterable;
import random;





class TEMPLATE:
	class EMBED:
		ARTWORK: str = cast(str, File.Read("Template/Embed/Artwork.html"));
		CHARACTER: str = cast(str, File.Read("Template/Embed/Character.html"));
		SOURCE: str = cast(str, File.Read("Template/Embed/Source.html"));
	class BROWSER:
		ARTWORK: str = cast(str, File.Read("Template/Browser/Artwork.html"));
		CHARACTER: str = cast(str, File.Read("Template/Browser/Character.html"));
		SOURCE: str = cast(str, File.Read("Template/Browser/Source.html"));





def Base_Compiler(Template: str) -> str:
	return String.Bulk_Replace(
		[
			["{App.Name}", App.Name],
			["{App.Description}", App.Description],
			["{App.Author}", ", ".join(App.Author)],
			["{App.Contributors}", ", ".join(App.Contributors)],
			["{App.License}", App.License],
			["{App.License}", App.License_Year],
			["{App.Codename}", App.Codename],
			["{App.Branch}", App.Branch],
			["{App.Version}", TSN_Abstracter.App_Version()],
			["{App.TSNA}", TSN_Abstracter.Version(App.TSNA)],
			["{TSNA}", TSN_Abstracter.Version()],
			["{Kiyosumi.LastLaunch}", " ".join(reversed(Time.Get_DateStrings(int(LASTLAUNCH)))) if (LASTLAUNCH) else 'N/A'],
			["{Kiyosumi.LastLaunch_Elapsed}", Time.Elapsed_String(Time.Get_Unix() - int(LASTLAUNCH)) if (LASTLAUNCH) else 'N/A'],
			["{Excluded.Count_Tag}", str(len(EXCLUSIONS["Tag"]))],
			["{Excluded.Count_Character}", str(len(EXCLUSIONS["Character"]))],
			["{Excluded.Count_Source}", str(len(EXCLUSIONS["Source"]))]
		],
		Template
	);

type Tag_Tuple = tuple[list[str], list[str | None], list[str | None]];
def Tag_Tuples(TAGS_Artwork: Iterable[Type.KiyoTag]) -> Tag_Tuple:
	Tags_OG: list[str] = [];
	Tags_Romanji: list[str | None] = [];
	Tags_Translated: list[str | None] = [];
	for tag in TAGS_Artwork:
		Tags_OG.append(tag["Name"]);
		Tags_Romanji.append(tag["Romanji"]);
		Tags_Translated.append(tag["Translation"].get(LANGUAGE, None) if (tag["Translation"]) else None);
	return Tags_OG, Tags_Romanji, Tags_Translated;









class Embed:
	@staticmethod
	def Artwork(KiyoArtwork: Type.KiyoArtwork, PIX_ID: str, SUB_ID: int, EXT: str) -> str:
		T: Tag_Tuple = Tag_Tuples(KiyoArtwork["Tags"]);

		return String.Bulk_Replace(
			[
				["{Artwork.URL}", Strings.URL.Artwork(PIX_ID)],
				["{Artwork.Stashed}", " ".join(Time.Get_DateStrings(KiyoArtwork["Stashed"]))],
				["{Artwork.Stashed_Unix}", str(KiyoArtwork["Stashed"])],
				["{Artwork.Title}", KiyoArtwork["Title"]],
				["{Artwork.Description}", KiyoArtwork["Description"]],
				["{Artwork.Artist_Name}", KiyoArtwork["Artist_Name"]],
				["{Artwork.Artist_ID}", KiyoArtwork["Artist_ID"]],
				["{Artwork.Artist_URL}", Strings.URL.Artist(KiyoArtwork["Artist_ID"])],
				["{Artwork.Date}", " ".join(Time.Get_DateStrings(KiyoArtwork["Date"]))],
				["{Artwork.Date_Unix}", str(KiyoArtwork["Date"])],
				["{Artwork.NSFW}", "NSFW" if (KiyoArtwork["NSFW"]) else ""],
				[
					"{Artwork.Tags_URL}", " ".join(
						[
							f'<a href="{Strings.URL.Tag(T[0][x])}" target="_blank">#{T[2][x] if (T[2][x]) else T[0][x]}</a>' for x in range(len(T[0]) - 1)
						]
					)
					if (len(T[0]) != 0) else "<i>This artwork has no tags!</i>"
				],
				["{Artwork.Image}", KiyoArtwork["Images"][SUB_ID]["URL"]],
				["{Artwork.Width}", str(KiyoArtwork["Images"][SUB_ID]["Width"])],
				["{Artwork.Height}", str(KiyoArtwork["Images"][SUB_ID]["Height"])],
				["{Artwork.Total}", str(len(KiyoArtwork["Images"]))],
				["{Artwork.Nth}", str(SUB_ID + 1)],
				["{Artwork.SubID}", str(SUB_ID)],
				["{Artwork.PixID}", PIX_ID],
				["{Artwork.Ext}", EXT],
				["{Artwork.Type}", "video" if (EXT.lower() in ["mp4", "gif", "webm"]) else "img"]
			],
			Base_Compiler(TEMPLATE.EMBED.ARTWORK)
		);



	@staticmethod
	def Character(CHARACTER: str, TAG: str, FRONT_Artwork: list[str]) -> str:
		ABSTRACT: str = Request.Abstract(CHARACTER);

		return String.Bulk_Replace(
			[
				["{Character.Name}", CHARACTER],
				["{Character.Tag}", TAG],
				["{Character.Abstract}", ABSTRACT],
				["{Character.Total}", str(len(FRONT_Artwork))],
				["{Character.Total_Padded}", str(String.Trailing_Zero(len(FRONT_Artwork), 5))],
				["{Character.Image}", FRONT_Artwork[random.randint(0, len(FRONT_Artwork) - 1) if (len(FRONT_Artwork) != 0) else 0]],
			],
			Base_Compiler(TEMPLATE.EMBED.CHARACTER)
		);



	@staticmethod
	def Source(SOURCE: str, TAGS_Characters: set[str], TAGS_exCharacters: set[str], TOTAL_Artworks: int, TOTAL_exArtworks: int) -> str:
		ABSTRACT: str = Request.Abstract(SOURCE);

		return String.Bulk_Replace(
			[
				["{Source.Name}", SOURCE],
				["{Source.Abstract}", ABSTRACT],
				["{Artwork.Total}", str(TOTAL_Artworks)],
				["{Artwork.Total_Excluded}", str(TOTAL_exArtworks)],
				["{Artwork.Total_Diff}", str(TOTAL_Artworks - TOTAL_exArtworks)],
				["{Character.Total}", str(len(TAGS_Characters))],
				["{Character.Total_Excluded}", str(len(TAGS_Characters))],
				["{Character.Total_Diff}", str(len(TAGS_Characters) - len(TAGS_exCharacters))],
				["{Character.Total_Padded}", str(String.Trailing_Zero(len(TAGS_Characters), 5))],
				["{Character.Total_exPadded}", str(String.Trailing_Zero(len(TAGS_exCharacters), 5))],
				["{Character.Tags}", ", ".join(TAGS_Characters)],
				["{Character.Tags_Excluded}", ", ".join(TAGS_exCharacters)],
				["{Character.Tags_Diff}", ", ".join(TAGS_Characters.difference(TAGS_exCharacters))]
			],
			Base_Compiler(TEMPLATE.EMBED.SOURCE)
		);










class Browser:
	@staticmethod
	def Artwork(EMBEDS_Artwork: list[str], CHARACTER: str, TAG: str, TAGS_Artwork: Iterable[Type.KiyoTag], FRONT_Artwork: list[str], SOURCE: str) -> str:
		T: Tag_Tuple = Tag_Tuples(TAGS_Artwork);
		ABSTRACT: str = Request.Abstract(CHARACTER);

		return String.Bulk_Replace(
			[
				["{Character.Name}", CHARACTER],
				["{Character.Abstract}", ABSTRACT],
				["{Character.URL}", Strings.URL.Tag(CHARACTER)],
				["{Character.Tag}", TAG],
				["{Character.Tags}", ", ".join(T[0])],
				[
					"{Character.Tags_URL}", " ".join(
						[
							f'<a href="{Strings.URL.Tag(T[0][x])}" target="_blank">#{T[2][x] if (T[2][x]) else T[0][x]}</a>' for x in range(len(T[0]) - 1)
						]
					)
					if (len(T[0]) != 0) else "<i>This artwork has no tags!</i>"
				],
				["{Character.Image}", FRONT_Artwork[random.randint(0, len(FRONT_Artwork) - 1) if (len(FRONT_Artwork) != 0) else 0]],
				["{Character.Total}", str(len(FRONT_Artwork))],
				["{Character.Source}", SOURCE],
				["{Character.Source_URL}", Strings.URL.Tag(SOURCE)],
				["{Artwork.Embeds}", "".join(reversed(sorted(EMBEDS_Artwork)))]
			],
			Base_Compiler(TEMPLATE.BROWSER.ARTWORK)
		);



	@staticmethod
	def Character(EMBEDS_Character: list[str], SOURCE: str, TAGS_Characters: set[str], TAGS_exCharacters: set[str], TOTAL_Artworks: int, TOTAL_exArtworks: int) -> str:
		ABSTRACT: str = Request.Abstract(SOURCE);

		return String.Bulk_Replace(
			[
				["{Source.Name}", SOURCE],
				["{Source.Abstract}", ABSTRACT],
				["{Artwork.Total}", str(TOTAL_Artworks)],
				["{Artwork.Total_Excluded}", str(TOTAL_exArtworks)],
				["{Artwork.Total_Diff}", str(TOTAL_Artworks - TOTAL_exArtworks)],
				["{Character.Total}", str(len(TAGS_Characters))],
				["{Character.Total_Excluded}", str(len(TAGS_Characters))],
				["{Character.Total_Diff}", str(len(TAGS_Characters) - len(TAGS_exCharacters))],
				["{Character.Tags}", ", ".join(TAGS_Characters)],
				["{Character.Tags_Excluded}", ", ".join(TAGS_exCharacters)],
				["{Character.Tags_Diff}", ", ".join(TAGS_Characters.difference(TAGS_exCharacters))],
				["{Character.Embeds}", "".join(reversed(sorted(EMBEDS_Character)))]
			],
			Base_Compiler(TEMPLATE.BROWSER.CHARACTER)
		);



	@staticmethod
	def Source(EMBEDS_Source: list[str], TAGS_allCharacters: set[str], TAGS_allexCharacters: set[str], TOTAL_allArtworks: int, TOTAL_allexArtworks: int, TAGS_Sources: list[str], TAGS_exSources: list[str]) -> str:
		return String.Bulk_Replace(
			[
				["{Artwork.Total}", str(TOTAL_allArtworks)],
				["{Artwork.Total_Excluded}", str(TOTAL_allexArtworks)],
				["{Artwork.Total_Diff}", str(TOTAL_allArtworks - TOTAL_allexArtworks)],
				["{Character.Total}", str(len(TAGS_allCharacters))],
				["{Character.Total_Excluded}", str(len(TAGS_allCharacters))],
				["{Character.Total_Diff}", str(len(TAGS_allCharacters) - len(TAGS_allexCharacters))],
				["{Character.Tags}", ", ".join(TAGS_allCharacters)],
				["{Character.Tags_Excluded}", ", ".join(TAGS_allexCharacters)],
				["{Character.Tags_Diff}", ", ".join(TAGS_allCharacters.difference(TAGS_allexCharacters))],
				["{Source.Total}", str(len(TAGS_Sources))],
				["{Source.Total_Excluded}", str(len(TAGS_exSources))],
				["{Source.Total_Diff}", str(len(TAGS_Sources) - len(TAGS_exSources))],
				["{Source.Tags}", ", ".join(TAGS_Sources)],
				["{Source.Tags_Excluded}", ", ".join(TAGS_exSources)],
				["{Source.Tags_Diff}", ", ".join(TAGS_Sources + TAGS_exSources)],
				["{Source.Embeds}", "".join(reversed(sorted(EMBEDS_Source)))]
			],
			Base_Compiler(TEMPLATE.BROWSER.SOURCE)
		);
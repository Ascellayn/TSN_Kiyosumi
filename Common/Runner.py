from .Globals import *;
from . import HTML;
import random;
import re;



def Stash() -> tuple[int, int]:
	t_init: int = Time.Get_Unix();
	Log.Info(f"Sprouting a tree from the stash...");
	TREE: File.Folder_Tree = File.Tree(INPUT);
	Log.Awaited().OK(Time.Elapsed_String(Time.Get_Unix() - t_init, ":"));
	del t_init;

	Invalids: Type.Invalids = {
		"Missing_Tag": [],
		"Invalid_Filename": [],
		"SubID_Overflow": [],
		"AI": [],
		"Ignored": [],
		"Error": []
	};


	EMBEDS_Sources: list[str] = [];
	TAGS_Sources: list[str] = [];
	TAGS_exSources: list[str] = [];
	TAGS_allCharacters: set[str] = set(); TAGS_allexCharacters: set[str] = set();
	TOTAL_allArtworks: int = 0; TOTAL_allexArtworks: int = 0;
	for MATRIX_SOURCE in TREE[0]:
		SOURCE: str = MATRIX_SOURCE[0];


		EMBEDS_Characters: list[str] = [];
		TAGS_Characters: set[str] = set(); TAGS_exCharacters: set[str] = set();
		TOTAL_Artworks: int = 0; TOTAL_exArtworks: int = 0;
		Log.Stateless(f"Processing all {SOURCE} Characters...");
		for MATRIX_CHARACTER in MATRIX_SOURCE[1][0]:
			folder: str = MATRIX_CHARACTER[0];
			m: re.Match[str] | None = re.match(r"(.+) \((.+)\)", folder);
			if (not m):
				Log.Error(f"{SOURCE}/{folder}: Tag not found.");
				Invalids["Missing_Tag"].append(f"{SOURCE}/{folder}"); continue;



			CHARACTER: str = m.group(1);
			TAG: str = m.group(2);
			del m;



			EMBEDS_Artwork: list[str] = [];
			TAGS_Artwork: list[Type.KiyoTag] = [];
			FRONT_Artwork: list[str] = [];
			Log.Stateless(f"Processing all {SOURCE}/{CHARACTER}/{TAG} Artworks...");
			for ARTWORKS in MATRIX_CHARACTER[1]:
				for ARTWORK in ARTWORKS:
					p: str = f"{SOURCE}/{CHARACTER}/{TAG}/{ARTWORK}";
					m: re.Match[str] | None = re.match(r"(\d+)_p(\d+)\.(\w+)", cast(str, str(ARTWORK)));
					if (not m):
						Log.Error(f"{p}: Invalid Filename.");
						Invalids["Invalid_Filename"].append(p); continue;
					PIX_ID: str = m.group(1);
					SUB_ID: int = int(m.group(2));
					EXT: str = m.group(3);

					Proxy: Type.KiyoArtwork | Type.KiyoDummy | None = Request.Artwork(PIX_ID);
					if (not Proxy): Log.Error(f"{p}: Got nothing! Ignored."); Invalids["Ignored"].append(p); continue;
					if (Proxy["Error"]): Log.Error(f"{p}: Artwork likely deleted! Ignored."); Invalids["Error"].append(p); continue;
					Proxy = cast(Type.KiyoArtwork, Proxy);

					if (Proxy["AI"]): Log.Error(f"{p}: AI Artwork! Ignored."); Invalids["AI"].append(p); continue;
					if (SUB_ID > (len(Proxy["Images"]) - 1)): Log.Error(f"{p}: SubID Overflow! Ignored."); Invalids["SubID_Overflow"].append(p); continue;

					for x in Proxy["Tags"]:
						if (x not in TAGS_Artwork): TAGS_Artwork.append(x);
					FRONT_Artwork.append(Proxy["Images"][SUB_ID]["URL"]);
					Log.Stateless(f"Compiling Artwork Embed for {SOURCE}/{CHARACTER}...");
					EMBEDS_Artwork.append(HTML.Embed.Artwork(Proxy, PIX_ID, SUB_ID, EXT));
					Log.Awaited().OK();
					TOTAL_Artworks += 1; TAGS_Characters.add(CHARACTER);



			Log.Awaited().OK(f"{len(FRONT_Artwork)} Artworks");
			if (len(FRONT_Artwork) == 0): continue;
			if (CHARACTER in EXCLUSIONS["Character"]): Log.Warning(f"{SOURCE}/{CHARACTER}: CHARACTER EXCLUDED"); continue;
			if (TAG in EXCLUSIONS["Tag"]): Log.Warning(f"{SOURCE}/{CHARACTER}/{TAG}: TAG EXCLUDED"); continue;
			TOTAL_exArtworks += len(FRONT_Artwork); TAGS_exCharacters.add(CHARACTER);



			Log.Stateless(f"Compiling Artwork Browser for {SOURCE}/{CHARACTER}...");
			p: str = f"{OUTPUT}/{SOURCE}/{CHARACTER}/{TAG}.html";
			File.Path_Require(p);
			File.Write(p, HTML.Browser.Artwork(EMBEDS_Artwork, CHARACTER, TAG, TAGS_Artwork, FRONT_Artwork, SOURCE));
			Log.Awaited().OK();
			del EMBEDS_Artwork;

			Log.Stateless(f"Compiling Character Embed for {SOURCE}/{CHARACTER}...");
			EMBEDS_Characters.append(HTML.Embed.Character(CHARACTER, TAG, FRONT_Artwork));
			Log.Awaited().OK();
			del FRONT_Artwork;



		Log.Stateless(f"Compiling Source Browser for {SOURCE}...");
		p: str = f"{OUTPUT}/{SOURCE}/browse.html";
		File.Path_Require(p);
		File.Write(p, HTML.Browser.Character(EMBEDS_Characters, SOURCE, TAGS_Characters, TAGS_exCharacters, TOTAL_Artworks, TOTAL_exArtworks));
		Log.Awaited().OK();
		del EMBEDS_Characters;


		Log.Awaited().OK();
		TAGS_Sources.append(SOURCE);
		if (SOURCE in EXCLUSIONS["Source"]): Log.Warning(f"{SOURCE}: SOURCE EXCLUDED"); continue;
		TAGS_exSources.append(SOURCE);

		Log.Stateless(f"Compiling Source Embed for {SOURCE}...");
		EMBEDS_Sources.append(HTML.Embed.Source(SOURCE, TAGS_Characters, TAGS_exCharacters, TOTAL_Artworks, TOTAL_exArtworks));
		Log.Awaited().OK();
		TOTAL_allArtworks += TOTAL_Artworks; TOTAL_allexArtworks += TOTAL_exArtworks;
		TAGS_allCharacters.update(TAGS_exCharacters); TAGS_allexCharacters.update(TAGS_exCharacters);
		del TOTAL_Artworks; del TOTAL_exArtworks; del TAGS_Characters; del TAGS_exCharacters;



	Log.Stateless(f"Compiling Source Browser...");
	p: str = f"{OUTPUT}/browse.html";
	File.Path_Require(p);
	File.Write(p, HTML.Browser.Source(EMBEDS_Sources, TAGS_allCharacters, TAGS_allexCharacters, TOTAL_allArtworks, TOTAL_allexArtworks, TAGS_Sources, TAGS_exSources));
	Log.Awaited().OK();
	del EMBEDS_Sources;



	Log.Info(f"Writing to disk Invalids...");
	File.JSON_Write("Invalids.json", Invalids);
	Log.Awaited().OK();

	Log.Info(f"Writing to disk Kiyosumi Cache...");
	File.JSON_Write("Kiyosumi.cache", KiyoCache, True);
	Log.Awaited().OK();

	return TOTAL_allArtworks, TOTAL_allexArtworks;
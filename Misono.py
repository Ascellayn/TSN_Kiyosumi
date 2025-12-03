from Misono import *;

if (__name__ == "__main__"):
	# PoC Stash Seeker
	T_Init: int = Time.Get_Unix();
	Log.Info("Analyzing Stash...");
	Stash_Tree: File.Folder_Tree = File.Tree(Folder_Stash);
	Log.Awaited().OK(f"took {Time.Elapsed_String(Time.Get_Unix() - T_Init, ":")}");



	# Source Folder
	Browser_Data: dict[str | int, Any] = {};
	for Source in Stash_Tree[0]:
		# Character Folder
		Character_Artworks: list[str] = [];
		for Character_Matrix in Source[1][0]:
			Character_Folder: str = Character_Matrix[0];

			character_match: re.Match[str] | None = re.search(pattern=r"(?<= \().+(?=\))", string=Character_Folder);
			Character_Tag: str | None = character_match[0] if (character_match) else None;
			if (not Character_Tag): Log.Error(f"{Source[0]}/{Character_Folder} → IGNORED: Tag not in Folder Name"); continue;
			del character_match;

			Character_Name: str = Character_Folder.replace(f" ({Character_Tag})","");



			# Artwork File
			Artworks_HTML: list[str] = [];
			Tags_All: set[str] = set();
			for Artworks in Character_Matrix[1]:
				for Artwork_Raw in Artworks:
					Artwork_File: str = str(Artwork_Raw); # Shush big typing.

					Pixiv_IDm: re.Match[str] | None = re.search(pattern=r"\d+(?=_p)", string=Artwork_File);
					Pixiv_ID: str | None = Pixiv_IDm[0] if (Pixiv_IDm) else None;
					if (not Pixiv_ID): Log.Error(f"{Source[0]}/{Character_Name}/{Character_Tag}/{Artwork_File} → IGNORED | Invalid PixivID"); continue;
					del Pixiv_IDm;

					Pixiv_sIDm: re.Match[str] | None = re.search(pattern=r"(?<=_p)\d+", string=Artwork_File);
					Pixiv_sIDs: str | None = Pixiv_sIDm[0] if (Pixiv_sIDm) else None;
					if (not Pixiv_sIDs): Log.Error(f"{Source[0]}/{Character_Name}/{Character_Tag}/{Artwork_File} → IGNORED | Invalid Pixiv Sub ID"); continue;
					Pixiv_sID = int(Pixiv_sIDs);
					del Pixiv_sIDm; del Pixiv_sIDs;

					Log.Debug(f"{Source[0]}/{Character_Name}/{Character_Tag}/{Pixiv_ID}/{Pixiv_sID} ...");
					Artwork: dict[str | int, Any] | None = Fetch_Artwork(Pixiv_ID);
					if (not Artwork): Log.Error(f"{Source[0]}/{Character_Name}/{Character_Tag}/{Artwork_File} → IGNORED | Could not fetch Artwork Details"); continue;
					if (Pixiv_sID > (len(Artwork["Images"]) - 1)):  Log.Error(f"{Source[0]}/{Character_Name}/{Character_Tag}/{Artwork_File} → IGNORED | Pixiv_sID is larger than proxied images: {Pixiv_sID}"); continue;

					# Embed Compilation
					Artworks_HTML.append(
						HTML_Compiler(
							Template_eArtwork,
							Artwork,
							Source[0], Character_Name, Character_Tag,
							Pixiv_ID, Pixiv_sID
						)
					);

					Character_Artworks.append(Artwork["Images"][Pixiv_sID]);
					for Tag in Artwork["Tags"]: Tags_All.add(Tag);

					Log.Awaited().OK();

			# Page Compilation
			HTML_File_Name: str = Stash_File(Source[0], Character_Name, Character_Tag);
			Log.Info(f"Building Artwork Browser: {HTML_File_Name}...");
			try:
				File.Path_Require(HTML_File_Name);
				File.Write(HTML_File_Name, HTML_Compiler(Template_bArtwork, None, Source[0], Character_Name, Character_Tag, None, None, Tags_All, sorted(Artworks_HTML), Character_Artworks));
				Log.Awaited().OK();
			except Exception as Except: Log.Awaited().EXCEPTION(Except);

			if (Source[0] not in Browser_Data.keys()): Browser_Data[Source[0]] = {};
			if (Character_Name not in Browser_Data[Source[0]].keys()): Browser_Data[Source[0]][Character_Name] = {};
			Browser_Data[Source[0]][Character_Name][Character_Tag] = Character_Artworks[random.randint(0, len(Character_Artworks) -1)];

	# Browser Compilation: TBD
	#HTML_Links: list[str] = [];

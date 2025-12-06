from Misono import *;





def Misono() -> None:
	# PoC Stash Seeker
	T_Init: int = Time.Get_Unix();
	Log.Info("Analyzing Stash...");
	Stash_Tree: File.Folder_Tree = File.Tree(Folder_Stash);
	Log.Awaited().OK(f"took {Time.Elapsed_String(Time.Get_Unix() - T_Init, ":")}");



	# Source Folder
	HTML_eSource: list[str] = [];
	for Source in Stash_Tree[0]:
		if (Source[0] in Exclude_Source): Log.Error(f"{Source[0]} → EXCLUDED"); continue;
		# Character Folder
		HTML_eCharacter: list[str] = [];
		for Character_Matrix in Source[1][0]:
			Character_Folder: str = Character_Matrix[0];

			character_match: re.Match[str] | None = re.search(pattern=r"(?<= \().+(?=\))", string=Character_Folder);
			Character_Tag: str | None = character_match[0] if (character_match) else None;
			if (not Character_Tag): Log.Error(f"{Source[0]}/{Character_Folder} → IGNORED: Tag not in Folder Name."); continue;
			del character_match;

			Character_Name: str = Character_Folder.replace(f" ({Character_Tag})","");
			if (Character_Name in Exclude_Character): Log.Error(f"{Source[0]}/{Character_Name} → EXCLUDED"); continue;
			if (Character_Tag in Exclude_Tag): Log.Error(f"{Source[0]}/{Character_Name}/{Character_Tag} → EXCLUDED"); continue;

			# Artwork File
			HTML_eArtwork: list[str] = [];

			if (Source[0] not in Browser_Data.keys()): Browser_Data[Source[0]] = {};
			if (Character_Name not in Browser_Data[Source[0]].keys()): Browser_Data[Source[0]][Character_Name] = {};
			Browser_Data[Source[0]][Character_Name][Character_Tag] = {
				"Artworks": [],
				"Tags": set()
			};

			for Artworks in Character_Matrix[1]:
				for Artwork_Raw in Artworks:
					Artwork_File: str = str(Artwork_Raw); # Shush big typing.

					pixiv_id: re.Match[str] | None = re.search(pattern=r"\d+(?=_p)", string=Artwork_File);
					Pixiv_ID: str | None = pixiv_id[0] if (pixiv_id) else None;
					if (not Pixiv_ID): Log.Error(f"{Source[0]}/{Character_Name}/{Character_Tag}/{Artwork_File} → IGNORED | Invalid PixivID."); continue;
					del pixiv_id;

					pixiv_sid: re.Match[str] | None = re.search(pattern=r"(?<=_p)\d+", string=Artwork_File);
					pixiv_sids: str | None = pixiv_sid[0] if (pixiv_sid) else None;
					if (not pixiv_sids): Log.Error(f"{Source[0]}/{Character_Name}/{Character_Tag}/{Artwork_File} → IGNORED | Invalid Pixiv Sub ID."); continue;
					Pixiv_sID = int(pixiv_sids);
					del pixiv_sid; del pixiv_sids;

					Log.Debug(f"{Source[0]}/{Character_Name}/{Character_Tag}/{Pixiv_ID}/{Pixiv_sID} ...");
					Artwork: dict[str | int, Any] | None = Fetch_Artwork(Pixiv_ID);
					if (not Artwork): Log.Error(f"{Source[0]}/{Character_Name}/{Character_Tag}/{Artwork_File} → IGNORED | Could not fetch Artwork Details."); continue;
					if (not Artwork["Fetched"]): Log.Error(f"{Source[0]}/{Character_Name}/{Character_Tag}/{Artwork_File} → IGNORED | Artwork no longer exists."); continue;
					if (Pixiv_sID > (len(Artwork["Images"]) - 1)):  Log.Error(f"{Source[0]}/{Character_Name}/{Character_Tag}/{Artwork_File} → IGNORED | Pixiv_sID is larger than proxied images: {Pixiv_sID}"); continue;


					Browser_Data[Source[0]][Character_Name][Character_Tag]["Artworks"].append(Artwork["Images"][Pixiv_sID]);
					for Tag in Artwork["Tags"]: Browser_Data[Source[0]][Character_Name][Character_Tag]["Tags"].add(Tag);


					# Artwork Embed Compilation
					HTML_eArtwork.append(
						HTML_Compiler(
							Template_eArtwork,
							[], Artwork,
							Source[0], Character_Name, Character_Tag,
							Pixiv_ID, Pixiv_sID
						)
					);

					Log.Awaited().OK();

			# Browser Artwork Compilation
			Browser_Artwork: str = Stash_File(Source[0], Character_Name, Character_Tag);
			if (len(HTML_eArtwork) < 1): continue;
			Log.Info(f"Building Artwork Browser: {Browser_Artwork}...");
			try:
				File.Path_Require(Browser_Artwork);
				File.Write(
					Browser_Artwork,
					HTML_Compiler(
						Template_bArtwork,
						sorted(HTML_eArtwork, reverse=True), None,
						Source[0], Character_Name, Character_Tag
					)
				);
				Log.Awaited().OK();
			except Exception as Except: Log.Awaited().EXCEPTION(Except); raise Except;

			# Character Embed Compilation
			HTML_eCharacter.append(
				HTML_Compiler(
					Template_eCharacter,
					[], None,
					Source[0], Character_Name, Character_Tag
				)
			);

			Log.Awaited().OK();


		# Browser Character Compilation
		Browser_Character: str = f"{Folder_Output}/{Source[0].replace(" ", "_")}/Browser.html";
		if (len(HTML_eCharacter) < 1): continue;
		Log.Info(f"Building Character Browser: {Browser_Character}...");
		try:
			File.Path_Require(Browser_Character);
			File.Write(
				Browser_Character,
				HTML_Compiler(
					Template_bCharacter,
					sorted(HTML_eCharacter), None,
					Source[0]
				)
			);
			Log.Awaited().OK();
		except Exception as Except: Log.Awaited().EXCEPTION(Except); raise Except;



		# Source Embed Compilation
		HTML_eSource.append(
			HTML_Compiler(
				Template_eSource,
				[], None,
				Source[0],
			)
		);

	# Browser Source Compilation
	Browser_Source: str = f"{Folder_Output}/Browser.html";
	if (len(HTML_eSource) < 1): Log.Critical(f"Found NOTHING to showcase!"); exit();
	Log.Info(f"Building Source Browser: {Browser_Source}...");
	try:
		File.Path_Require(Browser_Source);
		File.Write(
			Browser_Source,
			HTML_Compiler(
				Template_bSource,
				sorted(HTML_eSource, reverse=True), None
			)
		);
		Log.Awaited().OK();
	except Exception as Except: Log.Awaited().EXCEPTION(Except); raise Except;

if (__name__ == "__main__"): Misono();
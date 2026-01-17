import Yae.Globals as Globals;

def Pixiv_Artist(Artist_ID: str) -> str: return f"https://www.pixiv.net/en/users/{Artist_ID}";
def Pixiv_Artwork(Artwork_ID: str) -> str: return f"https://www.pixiv.net/en/artworks/{Artwork_ID}";
def Stash_File(Source: str, Character_Name: str, Character_Tag: str) -> str: return f"{Globals.Folder_Output}/{Source.replace(" ", "_")}/{Character_Name.replace(" ", "_")}-{Character_Tag}.html";
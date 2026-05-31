from .Globals import *;





class Pixiv:
	@staticmethod
	def Artist(Artist_ID: str) -> str:
		return f"https://www.pixiv.net/en/users/{Artist_ID}";
	
	@staticmethod
	def Artwork(Artwork_ID: str) -> str:
		return f"https://www.pixiv.net/en/artworks/{Artwork_ID}";





class Output:
	@staticmethod
	def Character_Browser(Source: str, Character_Name: str, Character_Tag: str) -> str:
		return f"{OUTPUT}/{Source.replace(" ", "_")}/{Character_Name.replace(" ", "_")}-{Character_Tag}.html";





class API:
	@staticmethod
	def Pages(Pixiv_ID: str) -> str:
		return f"https://www.pixiv.net/ajax/illust/{Pixiv_ID}/pages";



	@staticmethod
	def Details(Pixiv_ID: str) -> str:
		return f"https://www.pixiv.net/ajax/illust/{Pixiv_ID}?lang={LANGUAGE}";



	@staticmethod
	def Abstract(Tag: str) -> str:
		return f"https://www.pixiv.net/ajax/search/tags/{Tag}?lang={LANGUAGE}";





class URL:
	@staticmethod
	def Tag(Tag: str) -> str:
		return f"https://www.pixiv.net/en/tags/{Tag}";



	@staticmethod
	def Artist(Artist_ID: str) -> str:
		return f"https://www.pixiv.net/en/users/{Artist_ID}";



	@staticmethod
	def Artwork(ID: str) -> str:
		return f"https://www.pixiv.net/en/artworks/{ID}";



	@staticmethod
	def Embed(PIX_ID: str, SUB_ID: str) -> str:
		return f"https://www.phixiv.net/en/artworks/{PIX_ID}/{SUB_ID}";
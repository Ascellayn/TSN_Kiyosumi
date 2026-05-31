from typing import Any, TypedDict, Optional;
type Unix = int | float; # To be added in TSNA v6.2.X



# Pixiv API (HEAVILY Shortened)
class pxBase(TypedDict):
	error: bool;
	message: str;



class pxURLs(TypedDict):
	thumb_mini: str;
	small: str;
	regular: str;
	original: str;



class pxPage(TypedDict):
	urls: pxURLs;
	width: int;
	height: int;



class pxPages(pxBase):
	body: list[pxPage];





class pxTag(TypedDict):
	tag: str;
	romaji: Optional[str];
	translation: Optional[dict[str, str]];



class pxTags(TypedDict):
	tags: list[pxTag];



class pxDetail(TypedDict):
	""" This only contains what interests me, there's a lot more data otherwise... """
	illustId: str;
	illustTitle: str;
	illustComment: str;
	uploadDate: str;
	xRestrict: int;
	tags: pxTags;
	userId: str;
	userName: str;
	bookmarkCount: int;
	likeCount: int;
	commentCount: int;
	responseCount: int;
	viewCount: int;
	aiType: int;



class pxDetails(pxBase):
	body: pxDetail;





class KiyoTag(TypedDict):
	Name: str;
	Romanji: Optional[str];
	Translation: Optional[dict[str, str]];



class KiyoImage(TypedDict):
	URL: str;
	Width: int;
	Height: int;





class KiyoDummy(TypedDict):
	Error: bool;
	Stashed: Unix;



class KiyoArtwork(KiyoDummy):
	ID: str; # illustId
	Title: str; # illustTitle
	Description: str; # illustComment
	Artist_Name: str; # userName
	Artist_ID: str; # userId
	Date: Unix; # uploadDate (ISO)
	NSFW: bool; # xRestrict = 1
	AI: bool; # aiType = 2 or Tag Matches
	Tags: list[KiyoTag]; # Less stupid version of Artwork_Tag
	Images: list[KiyoImage]; # From PAGES with extra processing, Phixiv Proxy URLs



class KiyoAbstract(TypedDict):
	Error: bool;
	Fetched: Unix;
	Description: str;





class KiyoCache(TypedDict):
	_VERSION: tuple[int, ...];
	Artworks: dict[str, KiyoArtwork | KiyoDummy];
	Abstracts: dict[str, KiyoAbstract];





class Invalids(TypedDict):
	Missing_Tag: list[str];
	Invalid_Filename: list[str];
	SubID_Overflow: list[str];
	AI: list[str];
	Ignored: list[str];
	Error: list[str];



class Exclusions(TypedDict):
	Source: list[str];
	Tag: list[str];
	Character: list[str];
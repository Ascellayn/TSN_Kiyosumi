from .Globals import *;





def Send(Title: str, Description: str | None = None, File: bytes | None = None) -> None:
	if (DISCORD_WEBHOOK):
		Log.Info("Sending Webhook...");
		try:
			R: httpx.Response = httpx.post(
				DISCORD_WEBHOOK,
				headers={
					"User-Agent": f"TSN_Kiyosumi/{TSN_Abstracter.App_Version()} (+https://github.com/Ascellayn/TSN_Kiyosumi)"
				},
				json={
					"username": "Kiyosumi",
					"avatar_url": "https://sirio-network.com/Root/Project/Kiyosumi/Profile.png",
					"embeds": [
						{
							"title": Title,
							"description": Description,
							"color": 16115445
						}
					]
				} # pyright: ignore[reportUnknownArgumentType]
			);
			if (R.status_code == 204): Log.Awaited().OK();
			error: dict[str, Any] | None = None;
			try: error = R.json();
			except: pass;
			raise Exception(f"Non-OK HTTP Code: {R.status_code}{f'\n{error}' if (error) else ''}");
		except Exception as E: Log.Awaited().EXCEPTION(E, Traceback=False);



def Link(PIX_ID: str, SUB_ID: str) -> None:
	if (DISCORD_WEBHOOK):
		Log.Info("Sending Webhook...");
		try:
			R: httpx.Response = httpx.post(
				DISCORD_WEBHOOK,
				headers={
					"User-Agent": f"TSN_Kiyosumi/{TSN_Abstracter.App_Version()} (+https://github.com/Ascellayn/TSN_Kiyosumi)"
				},
				json={
					"content": Strings.URL.Embed(PIX_ID, SUB_ID)
				}
			);
			if (R.status_code == 204): Log.Awaited().OK();
			error: dict[str, Any] | None = None;
			try: error = R.json();
			except: pass;
			raise Exception(f"Non-OK HTTP Code: {R.status_code}{f'\n{error}' if (error) else ''}");
		except Exception as E: Log.Awaited().EXCEPTION(E, Traceback=False);
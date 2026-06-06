from .Globals import *;





def Send(Title: str, Description: str | None = None, Await = False) -> str | None:
	if (DISCORD_WEBHOOK):
		Log.Info("Sending Webhook...");
		try:
			R: httpx.Response = httpx.post(
				f"{DISCORD_WEBHOOK}{'?wait=true' if (Await) else ''}",
				headers={
					"User-Agent": f"TSN_Kiyosumi/{TSN_Abstracter.App_Version()} (+https://github.com/Ascellayn/TSN_Kiyosumi)"
				},
				json={
					"embeds": [
						{
							"title": Title,
							"description": Description,
							"color": 16115445
						}
					]
				} # pyright: ignore[reportUnknownArgumentType]
			);
			if (R.status_code in [204, 200]):
				Log.Awaited().OK();
				return R.json()["id"] if (R.status_code == 200) else None;

			error: dict[str, Any] | None = None;
			try: error = R.json();
			except: pass;
			raise Exception(f"Non-OK HTTP Code: {R.status_code}{f'\n{error}' if (error) else ''}");
		except Exception as E: Log.Awaited().EXCEPTION(E, Traceback=False);



def Edit(ID: str, Title: str, Description: str | None = None, Content: str | None = None) -> None:
	if (DISCORD_WEBHOOK):
		Log.Info("Editing Webhook...");
		try:
			R: httpx.Response = httpx.patch(
				f"{DISCORD_WEBHOOK}/messages/{ID}",
				headers={
					"User-Agent": f"TSN_Kiyosumi/{TSN_Abstracter.App_Version()} (+https://github.com/Ascellayn/TSN_Kiyosumi)"
				},
				json={
					"embeds": [
						{
							"title": Title,
							"description": Description,
							"color": 16115445
						}
					],
					"content": Content
				} # pyright: ignore[reportUnknownArgumentType]
			);
			if (R.status_code in [204, 200]):
				Log.Awaited().OK();
				return;
			error: dict[str, Any] | None = None;
			try: error = R.json();
			except: pass;
			raise Exception(f"Non-OK HTTP Code: {R.status_code}{f'\n{error}' if (error) else ''}");
		except Exception as E: Log.Awaited().EXCEPTION(E, Traceback=False);



def Content(Content: str) -> None:
	if (DISCORD_WEBHOOK):
		Log.Info("Sending Webhook...");
		try:
			R: httpx.Response = httpx.post(
				DISCORD_WEBHOOK,
				headers={
					"User-Agent": f"TSN_Kiyosumi/{TSN_Abstracter.App_Version()} (+https://github.com/Ascellayn/TSN_Kiyosumi)"
				},
				json={
					"content": Content
				}
			);
			if (R.status_code == 204): Log.Awaited().OK();
			error: dict[str, Any] | None = None;
			try: error = R.json();
			except: pass;
			raise Exception(f"Non-OK HTTP Code: {R.status_code}{f'\n{error}' if (error) else ''}");
		except Exception as E: Log.Awaited().EXCEPTION(E, Traceback=False);
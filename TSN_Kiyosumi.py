from Common import *;
from watchdog.observers import Observer;
from watchdog.observers.api import BaseObserver;
from watchdog.events import FileSystemEventHandler, DirCreatedEvent, FileCreatedEvent, DirDeletedEvent, FileDeletedEvent, DirMovedEvent, FileMovedEvent, FileSystemEvent;
import re;





def FoF(event: FileSystemEvent) -> str:
	""" File or Folder """
	return "Folder" if (event.is_directory) else "File";



class Stash_Handler(FileSystemEventHandler):
	def on_any_event(self, event: FileSystemEvent) -> None:
		if (event.event_type not in ["created", "moved", "deleted"]): return;
		if (event.event_type == "created" and event.is_directory): return; # Likely empty, ignore.

		src: str = getattr(event, "dest_path" if (event.event_type == "moved") else "src_path")[len(INPUT) + 1:];
		Log.Info(f"{event.event_type.capitalize()}: {src}");
		try:
			source, character_folder, artwork = str(src).split("/", 3);
			m: re.Match[str] | None = re.match(r"(.+) \((.+)\)", character_folder);
			if (not m):
				Log.Error(f"Tag not found: {source}/{character_folder} -- Ignoring");
				return;
			character: str = m.group(1);
			tag: str = m.group(2);
		except: Log.Error(f"Invalid: {src} -- Ignoring."); return;

		m: re.Match[str] | None = re.match(r"(\d+)_p(\d+)\.(\w+)", artwork);
		if (not m):
			Log.Error(f"Invalid Filename: {artwork} -- Ignoring");
			return;

		PIX_ID: str = m.group(1);
		SUB_ID: int = int(m.group(2));
		del m;

		Log.Stateless(f"Got: {source} → {character} → {tag} → {artwork}");



		def Webhook_Event(Source_Text: str) -> None:
			Webhook.Send(f"🗂️ {App.Name} - File System Event", f"**{event.event_type.capitalize()}:** `{Source_Text}` -- Updating Stash Browser...");

		isExcluded: bool = True;
		if (source not in EXCLUSIONS["Source"]):
			if (character not in EXCLUSIONS["Character"]):
				if (tag not in EXCLUSIONS["Tag"]):
					isExcluded = False;
					Webhook_Event(f"{source}/{character}/{tag}/{artwork}");
				else: Webhook_Event(f"{source}/{character}/[EXCLUDED TAG]");
			else: Webhook_Event(f"{source}/[EXCLUDED CHARACTER]");
		else: Webhook_Event(f"[EXCLUDED SOURCE]");

		c_int: int = Time.Get_Unix();
		artworks, exartworks = Runner.Stash();
		Webhook.Send(f"✅ {App.Name} - File System Event", f"Took {Time.Elapsed_String(Time.Get_Unix() - c_int)} to refresh the browsers.\n{App.Name} is now aware of a total of {artworks} artworks, of which only {exartworks} are displayed as {artworks - exartworks} ({round(((artworks - exartworks) / artworks) * 100, 2)}%) have been excluded.");
		if (isExcluded): return;
		Webhook.Link(PIX_ID, str(SUB_ID));





if (__name__ == "__main__"):
	TSN_Abstracter.App_Init();
	Webhook.Send(f"⏳ {App.Name} Backend Launched", f"Build {TSN_Abstracter.App_Version()} | {Time.Elapsed_String(Time.Get_Unix() - int(LASTLAUNCH)) if (LASTLAUNCH) else 'N/A'} since last startup. -- Running on-launch stash...");
	c_int: int = Time.Get_Unix();
	try: Runner.Stash();
	except Exception as E:
		Log.Info(f"CRASH: Writing to disk Kiyosumi Cache...");
		File.JSON_Write("Kiyosumi.cache", KiyoCache, True);
		Log.Awaited().OK();
		raise E;
	Webhook.Send(f"⌛ {App.Name} - Launch Routine", f"Took {Time.Elapsed_String(Time.Get_Unix() - c_int)} to refresh the browsers. -- Now launching Watchdog.");
	del c_int;



	O: BaseObserver = Observer();
	O.schedule(Stash_Handler(), INPUT, recursive=True);
	O.start();
	try:
		while O.is_alive(): O.join(1);
	except KeyboardInterrupt: Webhook.Send(f"🛑 {App.Name} Backend - Shutting down...");
	except Exception as E: Webhook.Send(f"🛑 {App.Name} Backend - CRASHED!", str(E));
	finally:
		O.stop();
		O.join();
		Log.Info(f"CRASH: Writing to disk Kiyosumi Cache...");
		File.JSON_Write("Kiyosumi.cache", KiyoCache, True);
		Log.Awaited().OK();
		exit(1);

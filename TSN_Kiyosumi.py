from Common import *;
from watchdog.observers import Observer;
from watchdog.observers.api import BaseObserver;
from watchdog.events import FileSystemEventHandler, DirCreatedEvent, FileCreatedEvent, DirDeletedEvent, FileDeletedEvent, DirMovedEvent, FileMovedEvent, FileSystemEvent;
from typing import Literal;
import threading;
import time;
import re;





class Buffered_Artwork(TypedDict):
	Event: Literal["created", "moved", "deleted"];
	Logged: str;
	Excluded: bool;
	Source: str;
	Character: str;
	Tag: str;
	Artwork: str;
	Pix_ID: str;
	Sub_ID: str;





def FoF(event: FileSystemEvent) -> str:
	""" File or Folder """
	return "Folder" if (event.is_directory) else "File";



class Stash_Handler(FileSystemEventHandler):
	def Routine(self) -> None:
		Log.Info(f"Kiyosumi Buffer System initialized.");
		Timer: int = -1;
		lastBuffer_Size = 0;
		while True:
			time.sleep(1);
			if (Timer == -1 and len(self.Buffer) != 0):
				Log.Info(f"Buffer triggered.");
				Timer = BUFFER_SIZE;
				lastBuffer_Size = len(self.Buffer);
				self.Buffer_ID = cast(str, Webhook.Send(f"🚥 {App.Name} - Buffer Triggered", f"Flushing {len(self.Buffer)} items inside the buffer <t:{Time.Get_Unix() + Timer}:R>.", True));
			elif (len(self.Buffer) == 0): continue;

			if (lastBuffer_Size != len(self.Buffer)):
				lastBuffer_Size = len(self.Buffer);
				Timer = BUFFER_SIZE;
				Webhook.Edit(self.Buffer_ID, f"🚥 {App.Name} - Buffer Triggered", f"Flushing {len(self.Buffer)} items inside the buffer <t:{Time.Get_Unix() + Timer}:R>.");



			Timer -= 1;
			if (Timer == 0):
				Webhook.Edit(self.Buffer_ID, f"🚥 {App.Name} - Buffer Triggered", f"Flushing {len(self.Buffer)} items inside the buffer `NOW`.");
				self.Flush(self.Buffer_ID);
				Timer = -1; lastBuffer_Size = 0;
				continue;
			Log.Stateless(f"Flushing {len(self.Buffer)} items inside the buffer after {Timer} seconds.");



	def __init__(self) -> None:
		super().__init__();
		self.Buffer: list[Buffered_Artwork] = [];
		Misc.Thread_Start(self.Routine);



	def Flush(self, ID: str) -> None:
		TITLE: str = f"🗂️ {App.Name} - Stash Update";
		BUFFERED: list[Buffered_Artwork] = self.Buffer;
		self.Buffer = []; # Avoids clearing too late if something else gets added right as the buffer is flushed
		self.Buffer_ID: str = "";

		base_text: str = f"**Handling `{len(BUFFERED)}` Buffered Events**\n";
		for artwork in BUFFERED:
			base_text += f"- **{artwork['Event'].upper()}** - `{artwork['Logged']}`\n";

		Webhook.Edit(ID, TITLE, f"{base_text}\n### ⏳ Refreshing browsers...");

		c_int: int = Time.Get_Unix();
		artworks, exartworks = Runner.Stash();
		base_text = f"{base_text}\n### ⏳ Refreshing browsers [OK: {Time.Elapsed_String(Time.Get_Unix() - c_int)}]\n{App.Name} is now aware of a total of {artworks} artworks, of which only {exartworks} are displayed as {artworks - exartworks} ({round(((artworks - exartworks) / artworks) * 100, 2)}%) have been excluded.";
		Webhook.Edit(ID, f"🗂️ {App.Name} - Stash Update", base_text);

		links: str = "";
		for artwork in BUFFERED:
			if (artwork["Excluded"]): continue;
			links += Strings.URL.Embed(artwork["Pix_ID"], artwork["Sub_ID"]) + f"\n";
		Webhook.Content(links);



	def on_any_event(self, event: FileSystemEvent) -> None:
		# Buffers events after they're validated
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



		isExcluded: bool = True;
		logged: str = "";
		if (source not in EXCLUSIONS["Source"]):
			if (character not in EXCLUSIONS["Character"]):
				if (tag not in EXCLUSIONS["Tag"]):
					isExcluded = False;
					logged = f"{source}/{character}/{tag}/{artwork}";
				else: logged = f"{source}/{character}/[EXCLUDED TAG]";
			else: logged = f"{source}/[EXCLUDED CHARACTER]";
		else: logged = f"[EXCLUDED SOURCE]";



		if (event.event_type == "deleted"): isExcluded = True;
		self.Buffer.append(cast(Buffered_Artwork, {
			"Event": event.event_type,
			"Logged": logged,
			"Excluded": isExcluded,
			"Source": source,
			"Character": character,
			"Tag": tag,
			"Artwork": artwork,
			"Pix_ID": PIX_ID,
			"Sub_ID": str(SUB_ID)
		}));





if (__name__ == "__main__"):
	TSN_Abstracter.App_Init();
	base_text: str = f"Build {TSN_Abstracter.App_Version()} | {Time.Elapsed_String(Time.Get_Unix() - int(LASTLAUNCH)) if (LASTLAUNCH) else 'N/A'} since last startup.\n";
	id: str = cast(str, Webhook.Send(f"💎 {App.Name} Backend - Launch", f"{base_text}  ⏳ On-launch Stash refresh...\n  ⏳ Launch Watchdog", True));
	c_int: int = Time.Get_Unix();
	try: ... #Runner.Stash();
	except Exception as E:
		Log.Info(f"CRASH: Writing to disk Kiyosumi Cache...");
		File.JSON_Write("Kiyosumi.cache", KiyoCache, True);
		Log.Awaited().OK();
		raise E;



	O: BaseObserver = Observer();
	O.schedule(Stash_Handler(), INPUT, recursive=True);
	O.start();
	Webhook.Edit(id, f"💎 {App.Name} Backend - Launch", f"{base_text}    ✅ On-launch Stash refresh [OK: {Time.Elapsed_String(Time.Get_Unix() - c_int)}]\n    ✅ Launch Watchdog [OK]\n\nNow watching for any stash updates...")
	del c_int;
	try:
		while O.is_alive(): O.join(1);
	except KeyboardInterrupt: Webhook.Send(f"🛑 {App.Name} Backend - Shutting down...");
	except Exception as E: Webhook.Send(f"🛑 {App.Name} Backend - CRASHED!", str(E));
	finally:
		O.stop();
		O.join();
		Log.Info(f"EXIT: Writing to disk Kiyosumi Cache...");
		File.JSON_Write("Kiyosumi.cache", KiyoCache, True);
		Log.Awaited().OK();
		exit(1);
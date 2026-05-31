from Common import *;
import watchdog;







if (__name__ == "__main__"):
	TSN_Abstracter.App_Init();
	Webhook.Send("🔋 Backend Launched", f"Build {TSN_Abstracter.Version()} - [{Time.Elapsed_String(Time.Get_Unix() - int(LASTLAUNCH)) if (LASTLAUNCH) else 'N/A'}] since last startup.");
	try: Runner.Stash();
	except Exception as E:
		Log.Info(f"CRASH: Writing to disk Kiyosumi Cache...");
		File.JSON_Write("Kiyosumi.cache", KiyoCache, True);
		Log.Awaited().OK();
		raise E;
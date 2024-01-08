Warning! This will overwrite your current resolution, fov, window mode and vsync settings for Star Citizen (the attributes.xml file)

1) Place both SCVR.exe and SCVR.json next to your attributes file

	Default location is C:\Program Files\Roberts Space Industries\StarCitizen\LIVE\user\client\0\Profiles\default\

2) Run SCVR.exe
	Select your headset (and lens configuration if applicable)
	Select your resolution
	
3)	DONE!


2.0.3:
Added:
-Forces MotionBlur Disabled
-Forces GForceZoomScale Static
-Forces AutoZoomOnSelectedTargetStrength Static
-Forces ShakeScale to 0 (off)
-Forces Sharpening 100%
-Forces ChromaticAberration 0%
-Forces FilmGrain Disabled

Fixed:
-Fixed bug where Height and Width were still setting to 0 if you chose from the additional resolutions list.

2.0.2:
-Fixed bug where Height and Width were set to 0 in the attributes.xml file.
-Fixed bug where VSync off and windowed borderless was appended rather than replaced.
-Fixed deprecated code causing warning to be printed to console.
-Fixed resolution confirmation prints to correctly display to the user.

This is laying the foundation for a new C-based program coming soon.

Feel free to create a desktop shortcut so that you can switch between resolutions easily.

Version 2.0.3


Special thanks to Cachi, Kaglaaz and blu! <3
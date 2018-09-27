# VSE Crossfades 1.1
A Blender Addon that allows the user to select a directory, and it will create crossfades between all the files.
It is located on the Properties Panel of the Video Sequence Editor.

This version fixes a number of issues with the original:
* Inserting multiple sequences caused the script to crash
* Removed 'start_frame' setting and always insert at current cursor position
* Fixed an 'off-by-one' error on length of clips inserted
* Refactored to preserve original clip names (e.g. file names)

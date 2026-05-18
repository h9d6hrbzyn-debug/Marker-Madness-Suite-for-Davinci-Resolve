<img width="1767" height="2357" alt="splash" src="https://github.com/user-attachments/assets/218e3bc3-e706-4e97-87ed-2b5466b4c455" />
[README.md](https://github.com/user-attachments/files/27972742/README.md)
# 🎯 Marker Madness
### *Because your markers deserve better than chaos.*

You dropped a hundred markers across a timeline. Some are on clips, some are on the ruler, some are named, some aren't. You need to find the red ones, rename them all, nudge them two frames earlier, export a CSV with thumbnail frames, and do it before lunch.

**Marker Madness** is a DaVinci Resolve utility that puts every marker in your timeline — clip markers and timeline markers alike — into a single, searchable, sortable table you can actually work with.

---

## What It Does

### See Everything
Every marker in your timeline in one place. Timeline markers and clip markers, listed side by side with their timecode, color, name, note, and the clip they live on. Filter by color, filter by type, or search by name, note, or clip name. The list updates live as you type.

### Add Markers
Add a marker right from the tool — no clicking around in Resolve's UI. Place it on the timeline ruler, drop it automatically on the clip under your playhead (Clip Auto), or pick an exact track from a list. The Add Marker window stays visible above Resolve so you can move the playhead and refresh position without losing your place.

### Edit Markers
Double-click any marker to open a full editor: name, note, color, duration — all in one window. Or right-click the Name or Note column to edit inline without opening a dialog at all.

### Batch Rename
The Batch Renamer is its own mini-tool. Add a prefix, add a suffix, find and replace text across all selected markers, copy the clip name into the marker name, or copy the name into the note. Preview every change before committing. Undo it all with one click if you change your mind.

### Change Colors
Select any number of markers and right-click the Color column to change them all at once. Or use the color picker from the toolbar.

### Move Markers Around

**Nudge** — shift selected markers forward or backward by any number of frames. Handles timeline markers and clip markers. Undoable.

**Promote** — copy or move clip markers up to the timeline ruler. Pick a frame offset and optionally change the color on the way up.

**Demote** — copy or move timeline markers down onto a clip. Choose which track, set a frame offset, and change color if needed.

### Delete With Confidence
Delete selected markers, or delete all markers matching the current filter. Every delete asks for confirmation. If you live dangerously, there's a *Delete without prompt* checkbox.

### Undo
Most operations — edits, color changes, nudges, adds, promotes, demotes — push onto an undo stack. One button rolls back the last action.

### Jump to Any Marker
Select a marker and hit Jump to Marker to move Resolve's playhead directly to it. Toggle auto-jump to have the playhead follow your selection automatically.

### Grab Frames
Select a marker, click Grab Frame, and see a live preview thumbnail in the panel. Export it as a PNG with a name derived from the marker's timecode and label.

### Batch Export Frames
Export a still frame for every marker — or just the selected ones — in one shot. Files are named with index, type, timecode, and marker name. Clean, organized, ready to hand off.

### Export to CSV
Export your marker list as a CSV. Include thumbnails and an auto-generated HTML report — open it in any browser to see your markers as a visual table with images. Import a CSV back in to recreate markers from a spreadsheet. The export follows your current column order — rearrange columns first and the CSV matches.

### Reorder Columns
Drag any column heading left or right to rearrange the table to your preference. The new order sticks between sessions and carries through to CSV exports.

### Copy and Paste Markers Across Timelines
Select any markers, hit **Copy Markers**, then switch to a different timeline, position your playhead, and hit **Paste Markers**. The markers land relative to the playhead — the earliest copied marker aligns to the playhead position and all others follow at the same offsets. Useful for transferring marker sets between timelines or recreating work after a mistake.

---

## Floating Above Resolve

Marker Madness knows you need to keep clicking in Resolve while it's open. The *Float above Resolve* option keeps the window on top when Resolve is your frontmost app, and steps aside politely when you switch to other applications. The Add Marker window stays visible independently so you can move the playhead without losing the dialog.

---

## Installation

1. Download `Marker Madness 1.1.py`
2. Place it in your DaVinci Resolve scripts folder:
   - **Mac:** `~/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Utility/`
   - **Windows:** `%APPDATA%\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Utility\`
3. In DaVinci Resolve, open a project and timeline
4. Go to **Workspace → Scripts → Utility → Marker Madness 1.1**

Requires DaVinci Resolve 18+ with scripting enabled. No external Python packages needed.

---

## Notes

- Works with both timeline markers and clip markers
- Clip markers on text layers and Fusion compositions may not support all operations
- Grab Frame and Batch Export require the Edit or Color page to be active in Resolve
- The Undo stack clears when you Refresh
- Preferences (column order, sort, window size, toggle states) are saved automatically to `prefs.json` in the same folder as the script

---

## License

Free. Do whatever you want with it.

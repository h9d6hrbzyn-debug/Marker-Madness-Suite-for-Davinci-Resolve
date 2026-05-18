[README.md](https://github.com/user-attachments/files/27974788/README.md)
![Marker Madness Suite](banner.svg)

---

Three free scripting tools for DaVinci Resolve. No subscriptions, no nonsense, no install wizard. Drop them in your scripts folder and get to work.

---

## The Tools

---

### 🎯 Marker Madness
*Because your markers deserve better than chaos.*

You dropped a hundred markers across a timeline. Some are on clips, some are on the ruler, some are named, some aren't. You need to find the red ones, rename them all, nudge them two frames earlier, export a CSV with thumbnail frames, and do it before lunch.

Marker Madness puts every marker in your timeline — clip markers and timeline markers alike — into a single, searchable, sortable table you can actually work with.

**See Everything** — Timeline markers and clip markers side by side, with timecode, color, name, note, and the clip they live on. Filter by color, filter by type, or search by name, note, or clip name. The list updates live as you type.

**Add Markers** — Place a marker on the timeline ruler, drop it automatically on the clip under your playhead (Clip Auto), or pick an exact track from a list. The Add Marker window stays visible so you can move the playhead and refresh position without losing your place.

**Edit Markers** — Double-click any marker to open a full editor: name, note, color, duration. Or right-click the Name or Note column to edit inline without opening a dialog at all.

**Batch Rename** — Add a prefix, add a suffix, find and replace text across all selected markers, copy the clip name into the marker name, or copy the name into the note. Preview every change before committing. Undo with one click if you change your mind.

**Change Colors** — Select any number of markers and right-click the Color column to recolor them all at once.

**Nudge** — Shift selected markers forward or backward by any number of frames. Handles timeline markers and clip markers. Undoable.

**Promote & Demote** — Copy or move clip markers up to the timeline ruler. Copy or move timeline markers down onto a clip. Pick a frame offset and optionally change the color on the way.

**Copy and Paste Across Timelines** — Select any markers, hit Copy Markers, switch to a different timeline, position your playhead, and hit Paste Markers. The earliest copied marker aligns to the playhead, all others follow at the same offsets.

**Jump to Any Marker** — Select a marker and move Resolve's playhead directly to it. Toggle auto-jump to have the playhead follow your selection automatically.

**Grab Frames** — See a live preview thumbnail for any marker and export it as a PNG named with the marker's timecode and label.

**Batch Export Frames** — Export a still frame for every marker — or just the selected ones — in one shot. Files are named with index, type, timecode, and marker name. Clean and organized.

**Export to CSV** — Export your marker list as a CSV, with optional thumbnails and an auto-generated HTML report you can open in any browser. Import a CSV back to recreate markers from a spreadsheet. The export follows your current column order — rearrange first and the CSV matches.

**Drag to Reorder Columns** — Drag any column heading left or right. The new order sticks between sessions and carries through to CSV exports.

**Undo** — Most operations push onto an undo stack. One button rolls back the last action.

**Floating Above Resolve** — The *Float above Resolve* option keeps the window on top when Resolve is your frontmost app and steps aside when you switch to something else.

---

### ✏️ Clip Renamer Pro
*Batch rename without the batch headache.*

You've got 200 clips in a bin that all came off camera named something like `A001C002_240318_R3D2`. You need them to say something a human can read. Or you've got a mix of cases and want everything sentence-case. Or you're adding a project code prefix to every clip before you hand off the drive.

Clip Renamer Pro handles all of it — with a live before/after preview so you can see every change before it happens.

**Find & Replace** — Simple text replacement across every selected clip name at once.

**Prefix & Suffix** — Add text to the beginning or end of every name in one pass.

**Counter** — Insert an auto-incrementing number anywhere in the name: before, after, or embedded in a find/replace pattern.

**Case Conversion** — Uppercase, lowercase, title case, or sentence case. Fix whatever the camera operator did.

**Trim** — Strip leading and trailing whitespace, or remove a set number of characters from either end.

**Live Preview** — The before column shows what you've got. The after column shows exactly what you'll get. Nothing changes until you hit Apply.

Works on Media Pool clips, timelines, or both. Select what you want to rename, configure the transform, preview, apply.

---

### 🎚️ Track Command
*Your timeline's track names, finally under control.*

A 65-track timeline where half the audio tracks are still named "Audio 1" through "Audio 65" is nobody's friend — not in exports, not in delivery, not when a client asks where the music stem is.

Track Command puts every audio and video track from your current timeline into an editable list. Rename one, rename all, do it fast.

**Batch Rename** — The same rename engine from Clip Renamer Pro: prefix, suffix, find and replace, counter, case conversion. Select any tracks and rename them in one pass with a live preview.

**Add Tracks** — Add audio tracks (mono, stereo, adaptive, etc.) or video tracks without leaving the tool. Specify how many and what type.

**Delete Tracks** — Select tracks and delete them directly from the list.

**Search** — Filter the track list by name to find what you're looking for in a dense timeline.

**Save & Load Templates** — Save your current track name set as a reusable template. Load it later to recreate your standard track layout on any timeline.

---

## Installation

1. Download the three `.py` files from this repo
2. Copy them to your DaVinci Resolve scripts folder:
   - **macOS:** `/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Utility/`
   - **Windows:** `C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Scripts\Utility\`
3. Launch DaVinci Resolve
4. Run any tool from **Workspace → Scripts → Utility**

Requires DaVinci Resolve 18+. No external Python packages needed.

---

## Notes

- Marker Madness works with both timeline markers and clip markers
- Grab Frame and Batch Export require the Edit or Color page to be active in Resolve
- The Undo stack clears when you Refresh
- Preferences (column order, sort, window size, toggle states) are saved automatically to `prefs.json` alongside the script
- Clip markers on text layers and Fusion compositions may not support all operations

---

*Free to use and share. Built with love for editors.*

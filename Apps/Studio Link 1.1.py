#!/usr/bin/env python3
"""
Studio Link 1.1 — Modify Studio → DaVinci Resolve live bridge

1.1: QNAP-aware — polls the NAS container (192.168.1.45:8790) as well as
localhost, and translates container paths (/data/...) to the SMB mount
(/Volumes/ModifyStudio/...) so imports resolve on this machine.

Watches Modify Studio's generation jobs (localhost API) and imports each
completed image / video / audio file straight into a "MODIFY STUDIO" bin
in the current Resolve project. Generate on one monitor, cut on the other.
Part of the Marker Madness suite.

Behavior:
  • Auto-Import ON: generations finishing while the link is open appear in
    the media pool within seconds, sorted into Images / Video / Audio bins.
  • Generations that finished BEFORE the link opened are not auto-imported —
    use "Import All Now" to pull everything Studio currently knows about.
  • Never touches a timeline. Bins only. The editor places clips.
  • Duplicate-safe: remembers what it imported (per Resolve project) in
    ~/.modify_studio_link_state.json and skips repeats across sessions.

Installation:
  Copy to your DaVinci Resolve scripts folder and run from
  Workspace > Scripts > Utility inside DaVinci Resolve.

  macOS:   /Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Utility/
  Windows: C:\\ProgramData\\Blackmagic Design\\DaVinci Resolve\\Fusion\\Scripts\\Utility\\
  Linux:   /opt/resolve/Developer/Scripting/Modules/

Requires Modify Studio running locally (default port 8766; the porter
proxy on 8765 is tried as a fallback).
"""

import sys
import os
import json
import time
import threading
import urllib.request
import urllib.error
import tkinter as tk

# ---------------------------------------------------------------------------
# Modify Studio connection
# ---------------------------------------------------------------------------

STUDIO_URLS = [
    "http://127.0.0.1:8766",     # studio engine on this machine (run.sh default)
    "http://127.0.0.1:8765",     # porter proxy fallback
    "http://192.168.1.45:8790",  # QNAP container (CPW-NAS) over the LAN
]
POLL_SECONDS = 4
STATE_FILE = os.path.expanduser("~/.modify_studio_link_state.json")

# Server-side path -> this-machine path. When Studio runs on the QNAP its
# jobs report container paths (/data/...); this machine sees those files
# through the SMB mount. First matching prefix wins; localhost jobs whose
# paths already exist locally are imported as-is.
PATH_MAP = {
    "/data/": "/Volumes/ModifyStudio/",
}


def localize(path):
    """Translate a server-reported file path into one this machine can read."""
    for remote, local in PATH_MAP.items():
        if path.startswith(remote):
            return local + path[len(remote):]
    return path

# job kind -> sub-bin name
KIND_BINS = {
    "image":   "Images",
    "video":   "Video",
    "refvideo": "Video",
    "upscale": "Video",
    "audio":   "Audio",
    "speech":  "Audio",
    "sfx":     "Audio",
    "music":   "Audio",
}
ROOT_BIN = "MODIFY STUDIO"


def _api_get(base, path, timeout=3):
    req = urllib.request.Request(base + path, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def find_studio():
    """Return the first reachable Studio base URL, else None."""
    for base in STUDIO_URLS:
        try:
            _api_get(base, "/api/status", timeout=2)
            return base
        except Exception:
            continue
    return None


def job_files(job):
    """Extract absolute media file paths from a completed job's result dict.
    Engine results use keys like image_path / image_paths / video_path /
    audio_path — collect every *_path / *_paths value generically."""
    result = job.get("result") or {}
    paths = []
    for key, val in result.items():
        if key.endswith("_paths") and isinstance(val, list):
            paths.extend(str(v) for v in val)
        elif key.endswith("_path") and isinstance(val, str):
            paths.append(val)
    # de-dup while preserving order (image_path duplicates image_paths[-1])
    seen, out = set(), []
    for p in paths:
        if p not in seen:
            seen.add(p)
            out.append(p)
    return out


# ---------------------------------------------------------------------------
# DaVinci Resolve API connection
# ---------------------------------------------------------------------------

RESOLVE_SCRIPT_PATHS = {
    "darwin": "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules",
    "win32":  os.path.join(
        os.environ.get("PROGRAMDATA", "C:\\ProgramData"),
        "Blackmagic Design", "DaVinci Resolve", "Support", "Developer",
        "Scripting", "Modules",
    ),
    "linux": "/opt/resolve/Developer/Scripting/Modules",
}


def _add_resolve_path():
    p   = sys.platform
    key = "darwin" if p == "darwin" else "win32" if p.startswith("win") else "linux"
    path = RESOLVE_SCRIPT_PATHS.get(key, "")
    if path and path not in sys.path:
        sys.path.append(path)


def get_resolve():
    _add_resolve_path()
    try:
        import DaVinciResolveScript as dvr
        return dvr.scriptapp("Resolve")
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Theme  (identical across the Marker Madness suite)
# ---------------------------------------------------------------------------

BG       = "#2d2d2d"
PANEL    = "#333333"
TEXT     = "#E2E2E2"
ACCENT   = "#ffa500"
BTN      = "#505050"
BTN_HOV  = "#626262"
ENTRY_BG = "#1e1e1e"
TITLE_BG = "#1a1a1a"
DIM      = "#909090"
GREEN    = "#388E3C"
RED      = "#C62828"
BTN_TEXT = "#111111"

F_MAIN   = ("Avenir Next", 12)
F_BOLD   = ("Avenir Next", 13, "bold")
F_SMALL  = ("Avenir Next", 10)
F_MONO   = ("Courier", 11)
F_STATUS = ("Avenir Next", 10, "italic")


def _hover_color(hex_color, factor=0.18):
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)
    r = min(255, int(r + (255 - r) * factor))
    g = min(255, int(g + (255 - g) * factor))
    b = min(255, int(b + (255 - b) * factor))
    return f"#{r:02x}{g:02x}{b:02x}"


class TBtn(tk.Button):
    def __init__(self, parent, bg=BTN, fg=BTN_TEXT, padx=12, pady=6,
                 font=F_MAIN, **kw):
        _hov = _hover_color(bg)
        super().__init__(parent, bg=bg, fg=fg, relief="flat", bd=0,
                         activebackground=_hov, activeforeground=fg,
                         highlightthickness=0,
                         padx=padx, pady=pady, cursor="hand2",
                         font=font, **kw)
        self.bind("<Enter>", lambda _: self.config(bg=_hov))
        self.bind("<Leave>", lambda _: self.config(bg=bg))


# ---------------------------------------------------------------------------
# Import state (per Resolve project, survives restarts)
# ---------------------------------------------------------------------------

def load_state():
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_state(state):
    try:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=1)
    except Exception:
        pass


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

class StudioLink:
    def __init__(self):
        self.resolve = get_resolve()
        self.studio_base = None
        self.state = load_state()          # {project_name: [imported paths]}
        self.seen_jobs = set()             # job ids observed this session
        self.baselined = False             # first poll marks pre-existing jobs
        self.pending = []                  # (job, paths) awaiting main-thread import
        self.pending_lock = threading.Lock()
        self.stop_flag = threading.Event()

        self.root = tk.Tk()
        self.root.title("Studio Link 1.1")
        self.root.configure(bg=BG)
        self.root.geometry("420x430")
        self.root.attributes("-topmost", True)

        self._build_ui()
        self._log("Studio Link ready.")
        if not self.resolve:
            self._log("⚠ Resolve API not found — running detached (no imports).")

        threading.Thread(target=self._poll_loop, daemon=True,
                         name="studio-link-poll").start()
        self.root.after(500, self._drain_pending)
        self.root.protocol("WM_DELETE_WINDOW", self._quit)

    # ---------------- UI ----------------

    def _build_ui(self):
        title = tk.Frame(self.root, bg=TITLE_BG)
        title.pack(fill="x")
        tk.Label(title, text="STUDIO LINK 1.1", bg=TITLE_BG, fg=ACCENT,
                 font=F_BOLD, pady=6).pack(side="left", padx=10)
        self.lbl_studio = tk.Label(title, text="● Studio", bg=TITLE_BG,
                                   fg=DIM, font=F_SMALL)
        self.lbl_studio.pack(side="right", padx=(0, 10))
        self.lbl_resolve = tk.Label(title, text="● Resolve", bg=TITLE_BG,
                                    fg=GREEN if self.resolve else RED,
                                    font=F_SMALL)
        self.lbl_resolve.pack(side="right", padx=6)

        opts = tk.Frame(self.root, bg=PANEL)
        opts.pack(fill="x", padx=10, pady=(10, 6))

        self.var_auto = tk.BooleanVar(value=True)
        tk.Checkbutton(opts, text="Auto-Import new generations",
                       variable=self.var_auto, bg=PANEL, fg=TEXT,
                       selectcolor=ENTRY_BG, activebackground=PANEL,
                       activeforeground=TEXT, font=F_MAIN,
                       highlightthickness=0).pack(anchor="w", padx=8, pady=(6, 2))

        kinds = tk.Frame(opts, bg=PANEL)
        kinds.pack(fill="x", padx=20, pady=(0, 6))
        self.var_img = tk.BooleanVar(value=True)
        self.var_vid = tk.BooleanVar(value=True)
        self.var_aud = tk.BooleanVar(value=True)
        for text, var in (("Images", self.var_img), ("Video", self.var_vid),
                          ("Audio", self.var_aud)):
            tk.Checkbutton(kinds, text=text, variable=var, bg=PANEL, fg=TEXT,
                           selectcolor=ENTRY_BG, activebackground=PANEL,
                           activeforeground=TEXT, font=F_SMALL,
                           highlightthickness=0).pack(side="left", padx=(0, 12))

        btns = tk.Frame(self.root, bg=BG)
        btns.pack(fill="x", padx=10, pady=(0, 6))
        TBtn(btns, text="Import All Now", bg=ACCENT,
             command=self._import_all).pack(side="left")
        TBtn(btns, text="Clear Log",
             command=lambda: self.txt.delete("1.0", "end")).pack(side="right")

        logf = tk.Frame(self.root, bg=BG)
        logf.pack(fill="both", expand=True, padx=10, pady=(0, 4))
        self.txt = tk.Text(logf, bg=ENTRY_BG, fg=TEXT, font=F_MONO,
                           relief="flat", wrap="word", height=12,
                           insertbackground=TEXT)
        self.txt.pack(side="left", fill="both", expand=True)
        sb = tk.Scrollbar(logf, command=self.txt.yview, bg=BG)
        sb.pack(side="right", fill="y")
        self.txt.config(yscrollcommand=sb.set)

        self.lbl_status = tk.Label(self.root, text="", bg=BG, fg=DIM,
                                   font=F_STATUS, anchor="w")
        self.lbl_status.pack(fill="x", padx=12, pady=(0, 8))

    def _log(self, msg):
        stamp = time.strftime("%H:%M:%S")
        self.txt.insert("end", f"[{stamp}] {msg}\n")
        self.txt.see("end")

    def _status(self, msg):
        self.lbl_status.config(text=msg)

    # ---------------- polling (background thread) ----------------

    def _poll_loop(self):
        while not self.stop_flag.is_set():
            base = self.studio_base or find_studio()
            if base != self.studio_base:
                self.studio_base = base
            ok = False
            if base:
                try:
                    jobs = _api_get(base, "/api/jobs")
                    ok = True
                    self._scan_jobs(jobs)
                except Exception:
                    self.studio_base = None
            color = GREEN if ok else RED
            try:
                self.lbl_studio.config(fg=color)
            except tk.TclError:
                return  # window closed
            self.stop_flag.wait(POLL_SECONDS)

    def _scan_jobs(self, jobs, force_all=False):
        """Queue completed jobs for import. On the first pass, pre-existing
        completed jobs are baselined (marked seen, not imported) so opening
        the link doesn't dump the whole day's history into the bin."""
        first_pass = not self.baselined
        for job in jobs:
            jid = job.get("id")
            if not jid or job.get("status") != "done":
                continue
            if jid in self.seen_jobs and not force_all:
                continue
            self.seen_jobs.add(jid)
            if first_pass and not force_all:
                continue  # baseline: known, but not auto-imported
            paths = job_files(job)
            if paths:
                with self.pending_lock:
                    self.pending.append((job, paths))
        if first_pass:
            self.baselined = True

    # ---------------- importing (main thread only) ----------------

    def _drain_pending(self):
        if self.stop_flag.is_set():
            return
        batch = []
        with self.pending_lock:
            if self.pending:
                batch, self.pending = self.pending, []
        for job, paths in batch:
            if self.var_auto.get() or getattr(job, "_forced", False) or job.get("_forced"):
                self._import_job(job, paths)
        self.root.after(500, self._drain_pending)

    def _import_all(self):
        """Import every completed job Studio currently knows about."""
        if not self.studio_base:
            self._log("⚠ Studio not reachable.")
            return
        try:
            jobs = _api_get(self.studio_base, "/api/jobs")
        except Exception as e:
            self._log(f"⚠ jobs fetch failed: {e}")
            return
        n = 0
        for job in jobs:
            if job.get("status") != "done":
                continue
            paths = job_files(job)
            if paths:
                self.seen_jobs.add(job.get("id"))
                self._import_job(job, paths)
                n += 1
        self.baselined = True
        if n == 0:
            self._log("Nothing to import.")

    def _kind_allowed(self, kind):
        bin_name = KIND_BINS.get(kind, "Other")
        return {"Images": self.var_img.get(),
                "Video":  self.var_vid.get(),
                "Audio":  self.var_aud.get()}.get(bin_name, True)

    def _import_job(self, job, paths):
        if not self.resolve:
            return
        kind = job.get("kind", "")
        if not self._kind_allowed(kind):
            return

        pm = self.resolve.GetProjectManager()
        project = pm.GetCurrentProject() if pm else None
        if not project:
            self._log("⚠ No open Resolve project.")
            return
        pname = project.GetName() or "Untitled"
        done = set(self.state.get(pname, []))

        fresh = []
        for p in paths:
            p = localize(p)   # QNAP container paths -> local SMB mount
            if p in done:
                continue
            # iCloud/SMB safety: only import fully-materialized files
            if not (os.path.isfile(p) and os.path.getsize(p) > 0):
                self._log(f"… waiting on file: {os.path.basename(p)}")
                continue
            fresh.append(p)
        if not fresh:
            return

        mp = project.GetMediaPool()
        target = self._ensure_bin(mp, KIND_BINS.get(kind, "Other"))
        if target:
            mp.SetCurrentFolder(target)
        items = mp.ImportMedia(fresh)
        if items:
            done.update(fresh)
            self.state[pname] = sorted(done)
            save_state(self.state)
            label = job.get("label", "")
            for p in fresh:
                self._log(f"✓ {os.path.basename(p)} → {KIND_BINS.get(kind, 'Other')}")
            self._status(f"Imported {len(fresh)} from “{label}” into {pname}")
        else:
            self._log(f"⚠ ImportMedia failed for {len(fresh)} file(s).")

    def _ensure_bin(self, mp, sub_name):
        """Find or create MODIFY STUDIO/<sub_name> and return the sub-bin."""
        try:
            root = mp.GetRootFolder()
            studio = None
            for f in (root.GetSubFolderList() or []):
                if f.GetName() == ROOT_BIN:
                    studio = f
                    break
            if studio is None:
                studio = mp.AddSubFolder(root, ROOT_BIN)
            if not studio:
                return None
            for f in (studio.GetSubFolderList() or []):
                if f.GetName() == sub_name:
                    return f
            return mp.AddSubFolder(studio, sub_name)
        except Exception as e:
            self._log(f"⚠ bin error: {e}")
            return None

    # ---------------- lifecycle ----------------

    def _quit(self):
        self.stop_flag.set()
        save_state(self.state)
        self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    StudioLink().run()

#!/usr/bin/env python3
"""
Clip Renamer Pro 2.0 — DaVinci Resolve Clip & Timeline Renamer

Renames clips and/or timelines selected in the Resolve Media Pool bin.
Part of the Marker Madness suite.

Installation:
  Copy to your DaVinci Resolve scripts folder and run from
  Workspace > Scripts > Utility inside DaVinci Resolve.

  macOS:   /Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Utility/
  Windows: C:\\ProgramData\\Blackmagic Design\\DaVinci Resolve\\Fusion\\Scripts\\Utility\\
  Linux:   /opt/resolve/Developer/Scripting/Modules/
"""

import sys
import os
import threading
import subprocess
import tkinter as tk
from tkinter import ttk
import webbrowser

# ---------------------------------------------------------------------------
# App icon (embedded Base64 PNG — no external file required)
# ---------------------------------------------------------------------------

APP_ICON_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAABAAAAAQACAYAAAB/HSuDAAAnY0lEQVR4nO3dva5l2VWG4WqLiLCc"
    "V0RkyYkDSBCSCU3CFRByBR0hkRL1FTjkCogc2hIigcCJJYuAiNhcQ6Fy9XKdrrH3OftnrTXHnN/z"
    "JC3LVtXWsZPvHfNsf/P+/YeP7wAAAICl/Wj0BwAAAACOJwAAAABAAAEAAAAAAggAAAAAEEAAAAAA"
    "gAACAAAAAAQQAAAAACCAAAAAAAABBAAAAAAIIAAAAABAAAEAAAAAAggAAAAAEEAAAAAAgAACAAAA"
    "AAQQAAAAACCAAAAAAAABBAAAAAAIIAAAAABAAAEAAAAAAggAAAAAEEAAAAAAgAACAAAAAAQQAAAA"
    "ACCAAAAAAAABBAAAAAAIIAAAAABAAAEAAAAAAggAAAAAEEAAAAAAgAACAAAAAAQQAAAAACCAAAAA"
    "AAABBAAAAAAIIAAAAABAAAEAAAAAAggAAAAAEEAAAAAAgAACAAAAAAQQAAAAACCAAAAAAAABBAAA"
    "AAAIIAAAAABAAAEAAAAAAggAAAAAEEAAAAAAgAACAAAAAAQQAAAAACCAAAAAAAABBAAAAAAIIAAA"
    "AABAAAEAAAAAAggAAAAAEEAAAAAAgAACAAAAAAQQAAAAACCAAAAAAAABBAAAAAAIIAAAAABAAAEA"
    "AAAAAggAAAAAEEAAAAAAgAACAAAAAAQQAAAAACCAAAAAAAABBAAAAAAIIAAAAABAAAEAAAAAAggA"
    "AAAAEEAAAAAAgAACAAAAAAQQAAAAACCAAAAAAAABBAAAAAAIIAAAAABAAAEAAAAAAggAAAAAEEAA"
    "AAAAgAACAAAAAAQQAAAAACCAAAAAAAABBAAAAAAIIAAAAABAAAEAAAAAAggAAAAAEEAAAAAAgAAC"
    "AAAAAAQQAAAAACCAAAAAAAABBAAAAAAIIAAAAABAAAEAAAAAAggAAAAAEEAAAAAAgAACAAAAAAQQ"
    "AAAAACCAAAAAAAABBAAAAAAIIAAAAABAAAEAAAAAAggAAAAAEEAAAAAAgAACAAAAAAQQAAAAACCA"
    "AAAAAAABBAAAAAAIIAAAAABAAAEAAAAAAggAAAAAEEAAAAAAgAACAAAAAAQQAAAAACCAAAAAAAAB"
    "BAAAAAAIIAAAAABAAAEAAAAAAggAAAAAEEAAAAAAgAACAAAAAAQQAAAAACCAAAAAAAABBAAAAAAI"
    "IAAAAABAAAEAAAAAAggAAAAAEEAAAAAAgAACAAAAAAQQAAAAACCAAAAAAAABBAAAAAAIIAAAAABA"
    "AAEAAAAAAggAAAAAEEAAAAAAgAACAAAAAAQQAAAAACCAAAAAAAABBAAAAAAIIAAAAABAAAEAAAAA"
    "AggAAAAAEEAAAAAAgAACAAAAAAQQAAAAACCAAAAAAAABBAAAAAAIIAAAAABAAAEAAAAAAggAAAAA"
    "EEAAAAAAgAACAAAAAAQQAAAAACCAAAAAAAABBAAAAAAIIAAAAABAAAEAAAAAAggAAAAAEEAAAAAA"
    "gAACAAAAAAQQAAAAACCAAAAAAAABBAAAAAAIIAAAAABAAAEAAAAAAggAAAAAEEAAAAAAgAACAAAA"
    "AAQQAAAAACCAAAAAAAABBAAAAAAIIAAAAABAAAEAAAAAAggAAAAAEEAAAAAAgAACAAAAAAQQAAAA"
    "ACCAAAAAAAABBAAAAAAIIAAAAABAAAEAAAAAAggAAAAAEEAAAAAAgAACAAAAAAQQAAAAACCAAAAA"
    "AAABBAAAAAAIIAAAAABAAAEAAAAAAggAAAAAEEAAAAAAgAACAAAAAAQQAAAAACCAAAAAAAABBAAA"
    "AAAIIAAAAABAAAEAAAAAAggAAAAAEEAAAAAAgAACAAAAAAQQAAAAACCAAAAAAAABBAAAAAAIIAAA"
    "AABAAAEAAAAAAggAAAAAEEAAAAAAgAACAAAAAAQQAAAAACCAAAAAAAABBAAAAAAIIAAAAABAAAEA"
    "AAAAAggAAAAAEEAAAAAAgAACAAAAAAQQAAAAACCAAAAAAAABBAAAAAAIIAAAAABAAAEAAAAAAggA"
    "AAAAEEAAAAAAgAACAAAAAAQQAAAAACCAAAAAAAABBAAAAAAIIAAAAABAAAEAAAAAAggAAAAAEEAA"
    "AAAAgAACAAAAAAQQAAAAACCAAAAAAAABBAAAAAAIIAAAAABAAAEAAAAAAggAAAAAEEAAAAAAgAAC"
    "AAAAAAQQAAAAACCAAAAAAAABBAAAAAAIIAAAAABAAAEAAAAAAggAAAAAEEAAAAAAgAACAAAAAAQQ"
    "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"
    "OOH5/5HXf8MfAAC4hQAAkzL8AQCAewgAMOH1/+vx7/f7AQCAtwgAMBHDHwAAeJQAABNc/w1/AADg"
    "WQIANGb4AwAAexEAoOH1/+Xw9/v9AADAHgQAaMTwBwAAjvLN+/cfPh72p0Oon/zkZ3f95w1/AADg"
    "aF4AwMDn/4Y/AABwFi8AYMD1fxv+fr8fAAA4ixcAcOL13/AHAABG8QIATrr+fxr/Lv4AAMAoPxr2"
    "N8OC1/9rw//3v/+t8Q8AAAzlBQAcdP3/NPoBAAC68AIAdr7+fxr+xj8AANCNFwCw0/Xf6AcAADoT"
    "AAAAACCAXwEAAACAAAIAAAAABBAAAAAAIIAAAAAAAAEEAAAAAAggAAAAAEAAAQAAAAACCAAAAAAQ"
    "QAAAAACAAAIAAAAABBAAAAAAIIAAAAAAAAEEAAAAAAggAAAAAEAAAQAAAAACCAAAAAAQQAAAAACA"
    "AAIAAAAABBAAAAAAIIAAAAAAAAEEAAAAAAggAAAAAEAAAQAAAAACCAAAAAAQQAAAAACAAAIAAAAA"
    "BBAAAAAAIIAAAAAAAAEEAAAAAAggAAAAAEAAAQAAAAACCAAAAAAQQAAAAACAAAIAAAAABBAAAAAA"
    "IIAAAAAAAAEEAAAAAAggAAAAAEAAAQAAAAACCAAAAAAQQAAAAACAAAIAAAAABBAAAAAAIIAAAAAA"
    "AAEEAAAAAAggAAAAAEAAAQAAAAACCAAAAAAQQAAAAACAAAIAAAAABBAAAAAAIIAAAAAAAAEEAAAA"
    "AAggAAAAAEAAAQAAAAACCAAAAAAQQAAAAACAAAIAAAAABBAAAAAAIIAAAAAAAAEEAAAAAAggAAAA"
    "AEAAAQAAAAACCAAAAAAQQAAAAACAAAIAAAAABBAAAAAAIIAAAAAAAAEEAAAAAAggAAAAAEAAAQAA"
    "AAACCAAAAAAQQAAAAACAAAIAAAAABBAAAAAAIIAAAAAAAAEEAAAAAAggAAAAAEAAAQAAAAACCAAA"
    "AAAQQAAAAACAAAIAAAAABBAAAAAAIIAAAAAAAAEEAAAAAAggAAAAAEAAAQAAAAACCAAAAAAQQAAA"
    "AACAAAIAAAAABBAAAAAAIIAAAAAAAAEEAAAAAAggAAAAAEAAAQAAAAACCAAAAAAQQAAAAACAAAIA"
    "AAAABBAAAAAAIIAAAAAAAAEEAAAAAAggAAAAAEAAAQAAAAACCAAAAAAQQAAAAACAAAIAAAAABBAA"
    "AAAAIIAAAAAAAAEEAAAAAAggAAAAAEAAAQAAAAACCAAAAAAQQAAAAACAAAIAAAAABBAAAAAAIIAA"
    "AAAAAAEEAAAAAAggAAAAAEAAAQAAAAACCAAAAAAQQAAAAACAAAIAAAAABBAAAAAAIIAAAAAAAAEE"
    "AAAAAAggAAAAAEAAAQAAAAACCAAAAAAQQAAAAACAAAIAAAAABBAAAAAAIIAAAAAAAAEEAAAAAAgg"
    "AAAAAEAAAQAAAAACCAAAAAAQQAAAAACAAAIAAAAABBAAAAAAIIAAAAAAAAEEAAAAAAggAAAAAEAA"
    "AQAAAAACCAAAAAAQQAAAAACAAAIAAAAABBAAAAAAIIAAAAAAAAEEAAAAAAggAAAAAEAAAQAAAAAC"
    "CAAAAAAQQAAAAACAAAIAAAAABBAAAAAAIIAAAAAAAAEEAAAAAAggAAAAAEAAAQAAAAACCAAAAAAQ"
    "QAAAAACAAAIAAAAABBAAAAAAIIAAAAAAAAEEAAAAAAggAAAAAEAAAQAAAAACCAAAAAAQQAAAAACA"
    "AAIAAAAABBAAAAAAIIAAAAAAAAEEAAAAAAggAAAAAEAAAQAAAAACCAAAAAAQQAAAAACAAAIAAAAA"
    "BBAAAAAAIIAAAAAAAAEEAAAAAAggAAAAAEAAAQAAAAACCAAAAAAQQAAAAACAAAIAAAAABBAAAAAA"
    "IIAAAAAAAAEEAAAAAAggAAAAAEAAAQAAAAACCAAAAAAQQAAAAACAAAIAAAAABBAAAAAAIIAAAAAA"
    "AAEEAAAAAAggAAAAAEAAAQAAAAACCAAAAAAQQAAAAACAAAIAAAAABBAAAAAAIIAAAAAAAAEEAAAA"
    "AAggAAAAAEAAAQAAAAACCAAAAAAQQAAAAACAd+v7fwTdsAeDrkkYAAAAAElFTkSuQmCC"
)

# ---------------------------------------------------------------------------
# DaVinci Resolve API connection
# ---------------------------------------------------------------------------

RESOLVE_SCRIPT_PATHS = {
    "darwin": "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules",
    "win32":  os.path.join(
        os.environ.get("PROGRAMDATA", "C:\\ProgramData"),
        "Blackmagic Design", "DaVinci Resolve", "Support", "Developer", "Scripting", "Modules",
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
# Theme  (matches Marker Madness exactly)
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
BLUE     = "#1976D2"
PURPLE   = "#7B1FA2"
RED      = "#E53935"

F_MAIN   = ("Avenir Next", 12)
F_SMALL  = ("Avenir Next", 10)
F_MONO   = ("Courier", 12)
F_STATUS = ("Avenir Next", 10, "italic")
F_HDR    = ("Avenir Next", 10, "bold")

# ---------------------------------------------------------------------------
# TBtn  (matches Marker Madness)
# ---------------------------------------------------------------------------

def _hover_color(hex_color, factor=0.18):
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)
    r = min(255, int(r + (255 - r) * factor))
    g = min(255, int(g + (255 - g) * factor))
    b = min(255, int(b + (255 - b) * factor))
    return f"#{r:02x}{g:02x}{b:02x}"

BTN_TEXT = "#111111"

class TBtn(tk.Button):
    def __init__(self, parent, bg=BTN, fg=BTN_TEXT, padx=12, pady=6, font=F_MAIN, **kw):
        _hov = _hover_color(bg)
        super().__init__(parent, bg=bg, fg=fg, relief="flat",
                         activebackground=_hov, activeforeground=fg,
                         padx=padx, pady=pady, cursor="hand2", font=font, **kw)
        self.bind("<Enter>", lambda _: self.config(bg=_hov))
        self.bind("<Leave>", lambda _: self.config(bg=bg))

# ---------------------------------------------------------------------------
# Transformation engine  (stepped counter from Marker Madness)
# ---------------------------------------------------------------------------

def apply_transform(text, *, find="", replace="", add="", add_pos="After",
                    replace_all=False, trim=False, trim_begin=0, trim_end=0,
                    counter=0, counter_enabled=False, counter_digits=2,
                    counter_pos="After", upper=False, lower=False,
                    title_case=False, remove_digits=False):
    n = text
    if trim and (trim_begin > 0 or trim_end > 0):
        end_idx = len(n) - trim_end if trim_end > 0 else len(n)
        n = n[trim_begin:end_idx] if trim_begin < end_idx else ""
    if replace_all:
        n = add
    else:
        if find:
            n = n.replace(find, replace)
        if add and add_pos != "After counter":
            n = (add + n) if add_pos == "Before" else (n + add)
    if upper:
        n = n.upper()
    elif lower:
        n = n.lower()
    elif title_case:
        n = n.title()
    if remove_digits:
        n = "".join(c for c in n if not c.isdigit())
    if counter_enabled and counter_digits > 0:
        cs = str(counter).zfill(counter_digits)
        if counter_pos == "Before":
            n = cs + n
        else:
            n = n + cs
            if add_pos == "After counter" and add:
                n = n + add
    return n.strip()

# ---------------------------------------------------------------------------
# Main app
# ---------------------------------------------------------------------------

class ClipRenamerPro:
    def __init__(self, root):
        self.root = root
        self.root.withdraw()
        self.root.title("Clip Renamer Pro")
        self.root.configure(bg=BG)
        self.root.createcommand('::tk::mac::ShowHelp',
            lambda: webbrowser.open("https://resolve-tools.com/clip-renamer-pro-guide"))
        self.root.resizable(False, True)
        self.root.minsize(720, 567)
        _w, _h = 720, 697
        _cx = self.root.winfo_pointerx()
        _cy = self.root.winfo_pointery()
        self.root.geometry(f"{_w}x{_h}+{_cx - _w // 2}+{_cy - _h // 2}")

        self._resolve     = get_resolve()
        self._project     = None
        self._media_pool  = None
        self._undo_stack        = []   # list of batches; each batch = [(obj, old_name), ...]
        self._session_originals = {}   # id(obj): (obj, name) before any session rename
        self._preview_job       = None

        if self._resolve:
            pm = self._resolve.GetProjectManager()
            self._project    = pm.GetCurrentProject() if pm else None
            self._media_pool = self._project.GetMediaPool() if self._project else None

        self._stay_on_top_var   = tk.BooleanVar(value=True)
        self._topmost_check_job = None
        self._hdr_proj_var      = tk.StringVar(value="—")

        self._style_comboboxes()
        self._build()
        self.root.bind("<Command-z>", lambda e: self._undo())
        self.root.bind("<Control-z>", lambda e: self._undo())
        if self._project:
            try:
                self._hdr_proj_var.set(self._project.GetName())
            except Exception:
                pass
        self._update_preview()
        self._on_stay_on_top_changed()
        self.root.after(150, self._initial_lift)

    # ── Combobox dark style ────────────────────────────────────────────────

    def _style_comboboxes(self):
        try:
            s = ttk.Style()
            s.theme_use("default")
            s.configure("Dark.TCombobox",
                        fieldbackground=ENTRY_BG,
                        background=BTN,
                        foreground=TEXT,
                        arrowcolor=TEXT,
                        selectbackground=BTN_HOV,
                        selectforeground=TEXT)
            s.map("Dark.TCombobox",
                  fieldbackground=[("readonly", ENTRY_BG)],
                  foreground=[("readonly", TEXT)],
                  background=[("readonly", BTN)])
        except Exception:
            pass

    # ── Build UI ───────────────────────────────────────────────────────────

    def _build(self):
        _tb = tk.Frame(self.root, bg=TITLE_BG, pady=8)
        _tb.pack(fill="x")
        tk.Label(_tb, text="  Clip Renamer Pro", fg=ACCENT, bg=TITLE_BG,
                 font=("Avenir Next", 18)).pack(side="left")
        tk.Label(_tb, text="v2.0", fg=DIM, bg=TITLE_BG,
                 font=("Avenir Next", 10)).pack(side="left", pady=(6, 0))
        _info = tk.Frame(_tb, bg=TITLE_BG)
        _info.pack(side="right", padx=12)
        tk.Label(_info, text="Project", fg=DIM, bg=TITLE_BG, font=F_STATUS).pack(side="left")
        tk.Label(_info, textvariable=self._hdr_proj_var,
                 fg=TEXT, bg=TITLE_BG, font=F_MAIN).pack(side="left", padx=(5, 0))

        # Top button bar
        top = tk.Frame(self.root, bg=BG)
        top.pack(fill="x", padx=8, pady=6)

        TBtn(top, text="Clear",            command=self._clear,
             bg=BTN,    padx=10, pady=4).pack(side="left", padx=(0, 4))
        TBtn(top, text="Refresh",          command=self._refresh,
             bg=PURPLE, padx=10, pady=4).pack(side="left", padx=4)
        self._undo_btn = TBtn(top, text="Undo", command=self._undo,
                              bg=BLUE, padx=10, pady=4)
        self._undo_btn.pack(side="left", padx=4)
        self._undo_btn.config(state="disabled")
        TBtn(top, text="Restore Original", command=self._restore,
             bg=RED, padx=10, pady=4).pack(side="left", padx=4)
        tk.Checkbutton(top, text="Float on Top", variable=self._stay_on_top_var,
                       command=self._on_stay_on_top_changed,
                       fg=TEXT, bg=BG, selectcolor=ENTRY_BG,
                       activebackground=BG, activeforeground=TEXT,
                       font=F_SMALL).pack(side="right", padx=8)

        # Main panel
        main = tk.Frame(self.root, bg=PANEL)
        main.pack(fill="both", expand=True, padx=8, pady=(0, 4))

        # ── Rename Operations header ──────────────────────────────────────
        tk.Label(main, text="RENAME OPERATIONS", fg=ACCENT, bg=PANEL,
                 font=F_HDR).pack(fill="x", padx=12, pady=(10, 2))

        ops = tk.Frame(main, bg=PANEL)
        ops.pack(fill="x", padx=12, pady=4)

        def entry_var(trace=True):
            v = tk.StringVar()
            if trace:
                v.trace_add("write", lambda *_: self._schedule_preview())
            return v

        def spin_var(val, trace=True):
            v = tk.IntVar(value=val)
            if trace:
                v.trace_add("write", lambda *_: self._schedule_preview())
            return v

        def check(parent, text, var, cmd=None):
            return tk.Checkbutton(parent, text=text, variable=var,
                                  fg=TEXT, bg=PANEL, selectcolor=ENTRY_BG,
                                  activebackground=PANEL, activeforeground=TEXT,
                                  font=F_MAIN, command=cmd or self._schedule_preview)

        def entry(parent, var, width=None):
            kw = {"width": width} if width else {}
            e = tk.Entry(parent, textvariable=var, bg=ENTRY_BG, fg=TEXT,
                         insertbackground=TEXT, relief="flat", font=F_MAIN,
                         highlightthickness=1, highlightbackground="#444444",
                         highlightcolor="#666666", **kw)
            e.bind("<Up>",       lambda ev: e.icursor(0)              or "break")
            e.bind("<Down>",     lambda ev: e.icursor("end")          or "break")
            e.bind("<KP_Enter>", lambda ev: self._schedule_preview()  or "break")
            return e

        def spin(parent, var, lo, hi, width=4):
            sb = tk.Spinbox(parent, from_=lo, to=hi, textvariable=var, width=width,
                            bg=ENTRY_BG, fg=TEXT, insertbackground=TEXT,
                            buttonbackground=BTN, relief="flat", font=F_MAIN,
                            highlightthickness=1, highlightbackground="#444444",
                            highlightcolor="#666666",
                            command=self._schedule_preview)
            sb.bind("<KP_Enter>", lambda ev: self._schedule_preview() or "break")
            return sb

        def combo(parent, var, values, width=13):
            cb = ttk.Combobox(parent, textvariable=var, values=values,
                              state="readonly", width=width, style="Dark.TCombobox",
                              font=F_MAIN)
            cb.bind("<<ComboboxSelected>>", lambda *_: self._schedule_preview())
            return cb

        def lbl(parent, text, w=None):
            kw = {"width": w} if w else {}
            return tk.Label(parent, text=text, fg=DIM, bg=PANEL, font=F_MAIN, **kw)

        def row(parent):
            f = tk.Frame(parent, bg=PANEL)
            f.pack(fill="x", pady=3)
            return f

        # Find / Replace
        r = row(ops)
        self._find_var    = entry_var()
        self._replace_var = entry_var()
        lbl(r, "Find:", 7).pack(side="left")
        entry(r, self._find_var).pack(side="left", fill="x", expand=True, padx=(0, 8))
        lbl(r, "Replace with:").pack(side="left", padx=(0, 4))
        entry(r, self._replace_var).pack(side="left", fill="x", expand=True)

        # Add / Replace entire / Position
        r = row(ops)
        self._add_var         = entry_var()
        self._replace_all_var   = tk.BooleanVar()
        self._after_counter_var = tk.BooleanVar()
        self._add_pos_var       = tk.StringVar(value="After name")
        lbl(r, "Add:", 7).pack(side="left")
        entry(r, self._add_var).pack(side="left", fill="x", expand=True, padx=(0, 8))
        check(r, "Replace entire name", self._replace_all_var).pack(side="left", padx=(0, 8))
        check(r, "After counter", self._after_counter_var).pack(side="left", padx=(0, 8))
        combo(r, self._add_pos_var, ["After name", "Before name"]).pack(side="left")

        # Trim + Counter in a shared grid so spinboxes align in columns
        tc_grid = tk.Frame(ops, bg=PANEL)
        tc_grid.pack(fill="x", pady=3)
        tc_grid.columnconfigure(7, weight=1)

        PAD_LBL  = (12, 4)
        PAD_SPIN = (0, 0)

        self._trim_var       = tk.BooleanVar()
        self._trim_begin_var = spin_var(0)
        self._trim_end_var   = spin_var(0)
        check(tc_grid, "Trim",    self._trim_var   ).grid(row=0, column=0, sticky="w", padx=(0, 4), pady=3)
        lbl(tc_grid, "Begin:").grid(row=0, column=1, sticky="e", padx=PAD_LBL)
        spin(tc_grid, self._trim_begin_var, 0, 100, width=4).grid(row=0, column=2, sticky="w", padx=PAD_SPIN)
        lbl(tc_grid, "End:").grid(row=0, column=3, sticky="e", padx=PAD_LBL)
        spin(tc_grid, self._trim_end_var,   0, 100, width=4).grid(row=0, column=4, sticky="w", padx=PAD_SPIN)

        self._counter_var    = tk.BooleanVar()
        self._ctr_digits_var = spin_var(2)
        self._ctr_start_var  = spin_var(1)
        self._ctr_step_var   = spin_var(1)
        self._ctr_pos_var    = tk.StringVar(value="After name")
        check(tc_grid, "Counter", self._counter_var).grid(row=1, column=0, sticky="w", padx=(0, 4), pady=3)
        lbl(tc_grid, "Digits:").grid(row=1, column=1, sticky="e", padx=PAD_LBL)
        spin(tc_grid, self._ctr_digits_var, 1, 5,    width=4).grid(row=1, column=2, sticky="w", padx=PAD_SPIN)
        lbl(tc_grid, "Start:").grid(row=1, column=3, sticky="e", padx=PAD_LBL)
        spin(tc_grid, self._ctr_start_var,  0, 9999, width=4).grid(row=1, column=4, sticky="w", padx=PAD_SPIN)
        combo(tc_grid, self._ctr_pos_var, ["After name", "Before name"], width=12).grid(row=1, column=7, sticky="w", padx=(12, 0))
        lbl(tc_grid, "Step:").grid(row=2, column=1, sticky="e", padx=PAD_LBL, pady=(0, 3))
        spin(tc_grid, self._ctr_step_var, 1, 9999, width=4).grid(row=2, column=2, sticky="w", padx=PAD_SPIN)

        # Case / Remove digits
        r = row(ops)
        self._upper_var = tk.BooleanVar()
        self._lower_var = tk.BooleanVar()
        self._title_var = tk.BooleanVar()
        self._nodig_var = tk.BooleanVar()

        def upper_cmd():
            if self._upper_var.get():
                self._lower_var.set(False); self._title_var.set(False)
            self._schedule_preview()

        def lower_cmd():
            if self._lower_var.get():
                self._upper_var.set(False); self._title_var.set(False)
            self._schedule_preview()

        def title_cmd():
            if self._title_var.get():
                self._upper_var.set(False); self._lower_var.set(False)
            self._schedule_preview()

        check(r, "UPPERCASE",     self._upper_var, upper_cmd).pack(side="left", padx=(0, 8))
        check(r, "lowercase",     self._lower_var, lower_cmd).pack(side="left", padx=(0, 8))
        check(r, "Title Case",    self._title_var, title_cmd).pack(side="left", padx=(0, 8))
        check(r, "Remove digits", self._nodig_var).pack(side="left")

        # Divider
        tk.Frame(main, bg=BTN_HOV, height=1).pack(fill="x", padx=12, pady=8)

        # Preview panels
        pf = tk.Frame(main, bg=PANEL)
        pf.pack(fill="both", expand=True, padx=12, pady=(0, 4))
        pf.columnconfigure(0, weight=1)
        pf.columnconfigure(1, weight=1)
        pf.rowconfigure(0, weight=1)

        left_col = tk.Frame(pf, bg=PANEL)
        left_col.grid(row=0, column=0, sticky="nsew", padx=(0, 4))
        tk.Label(left_col, text="SELECTED IN BIN", fg=DIM, bg=PANEL,
                 font=F_HDR).pack(anchor="w", pady=(0, 2))
        self._selected_text = tk.Text(left_col, bg=ENTRY_BG, fg=TEXT, relief="flat",
                                      font=F_MONO, state="disabled", wrap="none", height=16,
                                      highlightthickness=1, highlightbackground="#444444",
                                      highlightcolor="#666666")
        self._selected_text.pack(fill="both", expand=True)

        right_col = tk.Frame(pf, bg=PANEL)
        right_col.grid(row=0, column=1, sticky="nsew", padx=(4, 0))
        tk.Label(right_col, text="RENAME PREVIEW", fg=ACCENT, bg=PANEL,
                 font=F_HDR).pack(anchor="w", pady=(0, 2))
        self._preview_text = tk.Text(right_col, bg=ENTRY_BG, fg=ACCENT, relief="flat",
                                     font=F_MONO, state="disabled", wrap="none", height=16,
                                     highlightthickness=1, highlightbackground="#444444",
                                     highlightcolor="#666666")
        self._preview_text.pack(fill="both", expand=True)

        # Status bar
        self._status_var = tk.StringVar(
            value="Select items in the bin, then choose an action below.")
        tk.Label(main, textvariable=self._status_var, fg=DIM, bg=PANEL,
                 font=F_STATUS, anchor="w").pack(fill="x", padx=12, pady=(6, 10))

        # Action buttons
        btn_row = tk.Frame(self.root, bg=BG)
        btn_row.pack(fill="x", padx=8, pady=(0, 8))
        TBtn(btn_row, text="Rename Clips",
             command=lambda: self._do_rename("clips"),
             bg=BLUE, padx=14, pady=8,
             font=F_MAIN).pack(side="left", fill="x", expand=True, padx=(0, 4))
        TBtn(btn_row, text="Rename Timelines",
             command=lambda: self._do_rename("timelines"),
             bg=PURPLE, padx=14, pady=8,
             font=F_MAIN).pack(side="left", fill="x", expand=True, padx=4)
        TBtn(btn_row, text="Rename All",
             command=lambda: self._do_rename("all"),
             bg=GREEN, padx=14, pady=8,
             font=F_MAIN).pack(side="left", fill="x", expand=True, padx=(4, 0))

    # ── Helpers ───────────────────────────────────────────────────────────

    def _get_params(self, counter=0):
        add_pos = "After counter" if self._after_counter_var.get() else ("Before" if "Before" in self._add_pos_var.get() else "After")
        ctr_pos = "Before" if "Before" in self._ctr_pos_var.get() else "After"
        return dict(
            find            = self._find_var.get(),
            replace         = self._replace_var.get(),
            add             = self._add_var.get(),
            add_pos         = add_pos,
            replace_all     = self._replace_all_var.get(),
            trim            = self._trim_var.get(),
            trim_begin      = self._trim_begin_var.get(),
            trim_end        = self._trim_end_var.get(),
            counter         = counter,
            counter_enabled = self._counter_var.get(),
            counter_digits  = self._ctr_digits_var.get(),
            counter_pos     = ctr_pos,
            upper           = self._upper_var.get(),
            lower           = self._lower_var.get(),
            title_case      = self._title_var.get(),
            remove_digits   = self._nodig_var.get(),
        )

    def _get_selected(self):
        result = {"clips": [], "timelines": []}
        if not self._media_pool or not self._project:
            return result
        selected = self._media_pool.GetSelectedClips()
        if not selected:
            return result

        tl_by_name = {}
        tl_count = self._project.GetTimelineCount()
        for i in range(1, tl_count + 1):
            tl = self._project.GetTimelineByIndex(i)
            if tl:
                tl_by_name[tl.GetName()] = tl

        for item in selected:
            props = item.GetClipProperty() or {}
            nm    = props.get("Clip Name", "") or item.GetName() or ""
            itype = props.get("Type", "")
            if itype == "Timeline" or nm in tl_by_name:
                result["timelines"].append({
                    "name": nm, "obj": tl_by_name.get(nm), "clip_obj": item})
            else:
                result["clips"].append({"name": nm, "obj": item})
        return result


    def _set_text(self, widget, text):
        widget.config(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", text)
        widget.config(state="disabled")

    def _schedule_preview(self, *_):
        if self._preview_job:
            self.root.after_cancel(self._preview_job)
        self._preview_job = self.root.after(80, self._update_preview)

    def _update_preview(self):
        self._preview_job = None
        sel   = self._get_selected()
        total = len(sel["clips"]) + len(sel["timelines"])

        if total == 0:
            self._set_text(self._selected_text, "(nothing selected in bin)")
            self._set_text(self._preview_text,  "")
            self._status_var.set(
                "Select items in the bin, then choose an action below.")
            return

        step      = self._ctr_step_var.get()
        counter   = self._ctr_start_var.get() * step
        sel_lines = []
        prv_lines = []

        for it in sel["clips"]:
            new = apply_transform(it["name"], **self._get_params(counter))
            if self._counter_var.get():
                counter += step
            sel_lines.append(f"[clip]      {it['name']}")
            prv_lines.append(f"[clip]      {new}")

        for it in sel["timelines"]:
            new = apply_transform(it["name"], **self._get_params(counter))
            if self._counter_var.get():
                counter += step
            sel_lines.append(f"[timeline]  {it['name']}")
            prv_lines.append(f"[timeline]  {new}")

        self._set_text(self._selected_text, "\n".join(sel_lines))
        self._set_text(self._preview_text,  "\n".join(prv_lines))
        self._status_var.set(
            f"{len(sel['clips'])} clip(s), {len(sel['timelines'])} timeline(s) selected")

    def _initial_lift(self):
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
        if self._stay_on_top_var.get():
            self.root.attributes("-topmost", True)

    def _on_stay_on_top_changed(self, *_):
        if self._stay_on_top_var.get():
            self.root.attributes("-topmost", True)
            self.root.bind("<FocusIn>",  self._on_focus_in)
            self.root.bind("<FocusOut>", self._on_focus_out)
        else:
            self.root.attributes("-topmost", False)
            try:
                self.root.unbind("<FocusIn>")
                self.root.unbind("<FocusOut>")
            except Exception:
                pass

    def _on_focus_in(self, event):
        if event.widget is not self.root:
            return
        if self._stay_on_top_var.get():
            self.root.attributes("-topmost", True)
        self._schedule_preview()

    def _on_focus_out(self, event):
        if event.widget != self.root or not self._stay_on_top_var.get():
            return
        if sys.platform != "darwin":
            return
        if self._topmost_check_job:
            self.root.after_cancel(self._topmost_check_job)
        self._topmost_check_job = self.root.after(120, self._check_frontmost_app)

    def _check_frontmost_app(self):
        self._topmost_check_job = None
        if not self._stay_on_top_var.get():
            return
        try:
            if self.root.focus_displayof() is not None:
                return
        except Exception:
            pass
        def _query():
            try:
                result = subprocess.run(
                    ["osascript", "-e",
                     "tell application \"System Events\" to name of "
                     "first application process whose frontmost is true"],
                    capture_output=True, text=True, timeout=1.0)
                keep = "Resolve" in result.stdout.strip()
            except Exception:
                keep = True
            self.root.after(0, lambda: self.root.attributes("-topmost", keep))
        threading.Thread(target=_query, daemon=True).start()

    # ── Actions ───────────────────────────────────────────────────────────

    def _do_rename(self, filter_type):
        sel     = self._get_selected()
        step    = self._ctr_step_var.get()
        counter = self._ctr_start_var.get() * step
        changed = 0
        batch   = []   # collects (obj, old_name) for this operation only

        if filter_type in ("clips", "all"):
            for it in sel["clips"]:
                new = apply_transform(it["name"], **self._get_params(counter))
                if self._counter_var.get():
                    counter += step
                if new != it["name"]:
                    oid = id(it["obj"])
                    if oid not in self._session_originals:
                        self._session_originals[oid] = (it["obj"], it["name"])
                    it["obj"].SetName(new)
                    batch.append((it["obj"], it["name"]))
                    changed += 1

        if filter_type in ("timelines", "all"):
            for it in sel["timelines"]:
                if it["obj"]:
                    new = apply_transform(it["name"], **self._get_params(counter))
                    if self._counter_var.get():
                        counter += step
                    if new != it["name"]:
                        oid = id(it["obj"])
                        if oid not in self._session_originals:
                            self._session_originals[oid] = (it["obj"], it["name"])
                        it["obj"].SetName(new)
                        batch.append((it["obj"], it["name"]))
                        changed += 1

        if batch:
            self._undo_stack.append(batch)
            if len(self._undo_stack) > 10:   # cap at 10 levels
                self._undo_stack.pop(0)
        self._update_undo_btn()
        self._status_var.set(f"[OK] Renamed {changed} item(s).")
        self._update_preview()

    def _update_undo_btn(self):
        """Keep Undo button label and state in sync with the undo stack."""
        n = len(self._undo_stack)
        if n == 0:
            self._undo_btn.config(state="disabled", text="Undo")
        elif n == 1:
            self._undo_btn.config(state="normal",   text="Undo")
        else:
            self._undo_btn.config(state="normal",   text=f"Undo ({n})")

    def _undo(self):
        if not self._undo_stack:
            return
        batch = self._undo_stack.pop()
        for obj, old_name in reversed(batch):
            obj.SetName(old_name)
        self._update_undo_btn()
        self._status_var.set(f"[OK] Undone {len(batch)} rename(s).")
        self._update_preview()

    def _restore(self):
        if not self._session_originals:
            self._status_var.set("[!] Nothing to restore.")
            return
        count = 0
        for obj, orig in self._session_originals.values():
            try:
                obj.SetName(orig)
                count += 1
            except Exception:
                pass
        self._session_originals.clear()
        self._undo_stack = []
        self._update_undo_btn()
        self._status_var.set(f"[OK] Restored {count} item(s).")
        self._update_preview()

    def _refresh(self):
        self._undo_stack = []
        self._session_originals = {}
        self._update_undo_btn()
        self._update_preview()

    def _clear(self):
        self._find_var.set("")
        self._replace_var.set("")
        self._add_var.set("")
        self._replace_all_var.set(False)
        self._after_counter_var.set(False)
        self._trim_var.set(False)
        self._trim_begin_var.set(0)
        self._trim_end_var.set(0)
        self._counter_var.set(False)
        self._ctr_digits_var.set(2)
        self._ctr_start_var.set(1)
        self._ctr_step_var.set(1)
        self._upper_var.set(False)
        self._lower_var.set(False)
        self._title_var.set(False)
        self._nodig_var.set(False)
        self._add_pos_var.set("After name")
        self._ctr_pos_var.set("After name")
        self._schedule_preview()


if __name__ == "__main__":
    try:
        root = tk.Tk()
        if sys.platform == "darwin":
            import tempfile as _tempfile, base64 as _b64
            _icon_path = None
            try:
                _tf = _tempfile.NamedTemporaryFile(suffix='.png', delete=False)
                _tf.write(_b64.b64decode(APP_ICON_B64))
                _tf.close()
                _icon_path = _tf.name
            except Exception:
                pass
            if _icon_path:
                # Tkinter window icon (Mission Control, Exposé) — own try so
                # ctypes dock-icon code still runs even if PhotoImage fails
                try:
                    root._icon_photo = tk.PhotoImage(data=APP_ICON_B64)
                    root.iconphoto(True, root._icon_photo)
                except Exception:
                    pass
                # NSApplication dock icon + Cmd+Tab identity
                try:
                    import ctypes, ctypes.util
                    _objc = ctypes.cdll.LoadLibrary(ctypes.util.find_library('objc'))
                    _objc.objc_getClass.restype = _objc.sel_registerName.restype = ctypes.c_void_p
                    _msg = _objc.objc_msgSend; _msg.restype = ctypes.c_void_p
                    _msg.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_char_p]
                    _ns_path = _msg(_objc.objc_getClass(b'NSString'), _objc.sel_registerName(b'stringWithUTF8String:'), _icon_path.encode())
                    _msg.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                    _img = _msg(_objc.objc_getClass(b'NSImage'), _objc.sel_registerName(b'alloc'))
                    _msg.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p]
                    _img = _msg(_img, _objc.sel_registerName(b'initWithContentsOfFile:'), _ns_path)
                    if _img:  # nil means file not found — skip rather than clear the icon
                        _msg.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                        _app = _msg(_objc.objc_getClass(b'NSApplication'), _objc.sel_registerName(b'sharedApplication'))
                        _msg.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p]
                        _msg(_app, _objc.sel_registerName(b'setApplicationIconImage:'), _img)
                        _msg.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_long]
                        _msg(_app, _objc.sel_registerName(b'setActivationPolicy:'), 0)
                        _msg.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_char_p]
                        _app_name = _msg(_objc.objc_getClass(b'NSString'), _objc.sel_registerName(b'stringWithUTF8String:'), b'Clip Renamer Pro')
                        _msg.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                        _pi = _msg(_objc.objc_getClass(b'NSProcessInfo'), _objc.sel_registerName(b'processInfo'))
                        _msg.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p]
                        _msg(_pi, _objc.sel_registerName(b'setProcessName:'), _app_name)
                except Exception:
                    pass
                try:
                    import os as _os; _os.unlink(_icon_path)
                except Exception:
                    pass
        ClipRenamerPro(root)
        root.mainloop()
    except Exception as e:
        import traceback
        print("[Clip Renamer Pro] Fatal error:")
        traceback.print_exc()

# Seedance 2.0 / 2.5 — Prompting & API Reference

Distilled working reference compiled from ByteDance's official BytePlus/ModelArk documentation,
official sample prompts, and our own field experience. Boilerplate SDK code is deliberately
omitted — this doc keeps the rules, specs, and gotchas.

**Provenance labels used throughout:**

- **[OFFICIAL]** — stated in ByteDance's own docs (BytePlus ModelArk).
- **[FIELD]** — verified in our own runs (Fal.ai route, Kling work, etc.). Where FIELD and
  OFFICIAL disagree, FIELD wins for *our* pipeline; OFFICIAL describes ByteDance's platform.
- **[SITE]** — from third-party write-ups; useful, but the official docs are the tiebreaker.

---

## 1. Model lineup

| Model | Model ID (ModelArk) | Best for |
|---|---|---|
| Seedance 2.5 | `dreamina-seedance-2-5-260628` | Length + control: 30s videos, 50 reference assets, timestamp editing |
| Seedance 2.0 | `dreamina-seedance-2-0-260128` | **Resolution**: only model with 1080p / 4K (10-bit HEVC) |
| Seedance 2.0 fast | `dreamina-seedance-2-0-fast-260128` | Cheaper/faster iteration drafts |
| Seedance 2.0 mini | `dreamina-seedance-2-0-mini-260615` | Best cost-performance |

**The core fork [OFFICIAL]:** 2.5 caps at **720p** (no 1080p/4K). 2.0 caps at **15 seconds**
(no 30s, fewer assets, no timestamps). So:

> **2.5 for length and control → upscale afterward. 2.0 for native resolution.**

Our pipeline already has Topaz video upscale wired up (media-gen skill), so "master in 2.5 at
720p, upscale to HD/4K" is the practical default. **[FIELD]**

### Spec comparison

| | Seedance 2.5 | Seedance 2.0 series |
|---|---|---|
| Max duration | 4–30 s (or `-1` = model picks) | 4–15 s (or `-1`) |
| Max reference assets | 50 (30 img + 10 vid + 10 aud) | 15 (9 img + 3 vid + 3 aud) |
| Ref video/audio total length | ≤ 30 s each type | ≤ 15 s |
| Resolution | 480p, 720p | 480p–4K (4K = 2.0 full only) |
| Aspect ratio | 6 fixed + `adaptive` (adaptive range 0.4–2.5) | 6 fixed + `adaptive` |
| Output format | mp4, **mov** (yuv444p + PCM) | mp4 only |
| Pure-audio reference | ✓ | ✗ (audio needs image/video alongside) |
| Timestamps in prompts | ✓ (integer seconds) | ✗ — **2.0 ignores timestamps; use Shot N** |
| Multi-view subject images | ✓ | not recommended |
| Languages | 11 native (incl. EN, JA, KO, ES, AR…) | — |

---

## 2. Prompt structure — the sandwich

Both generations respond to the same overall shape; 2.5 formalizes it. **[OFFICIAL]**

```
┌─ 1. GLOBAL DECLARATION (once, up top)
│    One-sentence summary: subject + action/event + scene + style + camera + sound.
│    Style block: visual style, lens/camera hardware, lighting, grade, mood.
│    Asset bindings (if any references — see §3).
│
├─ 2. EVENT SCRIPT (the middle)
│    Timeline beats (2.5: "0-3s: … 3-8s: …") or numbered shots ("Shot 1: […] …").
│    Each beat: action + camera + audio + an explicit END STATE
│    ("the door has swung shut behind her") so the world can't drift between beats.
│
└─ 3. INVARIANTS (restated at the bottom)
     What must stay constant: identity, wardrobe, layout, camera behavior,
     depth of field, audio policy, overall mood. "Overall requirements: …"
```

- Bracketed section labels seen in the wild (`[Generation Goal]`, `[Event Script]`,
  `[Maintain Consistency]`) are **house style, not syntax** — official examples use free-form
  headers (`[Subject settings]`, `[Overall style]`, `[Shot list]`). The *shape* is the contract. **[OFFICIAL]**
- Per-shot camera grammar goes in brackets at the head of each shot:
  `[Wide shot, locked-off camera, eye-level, rule-of-thirds composition]`. **[OFFICIAL]**
- Naming real production hardware ("shot on Arri Alexa Mini LF, 35 mm cinema lens") plus
  anti-beautification language ("no excessive skin smoothing, real facial bone structure")
  pulls output toward drama/documentary realism. **[OFFICIAL example]**

### Basic formula [OFFICIAL]

> Subject + action/event + scene & environment + visual style + camera movement/shot cuts + sound.
> Omit what you don't need. Prefer positive descriptions.

---

## 3. Asset referencing (@ tags)

- Number assets **by upload order, per type, starting at 1**: `@Image 1`, `@Video 2`, `@Audio 1`.
  "Image n" = the nth `image_url` item in the request's `content` array. **[OFFICIAL]**
- **Declare each asset's role in the prompt text** — and, critically, its **exclusions**:
  - `"@Image 1 defines Mara's face and coat. Do not use its background."`
  - `"Refer to @Video 1 only for camera movement and motion — not the visual content."`
  - `"Refer to Image 1 for lighting and filters."`
- Don't label inside the image (writing "John" on the photo) — causes character confusion.
  Mapping lives in the prompt text. **[OFFICIAL]**
- Asset IDs (`asset://…`) are request-body plumbing only; the prose still says "Image 1",
  never the asset ID. **[OFFICIAL]**
- If the reference is already accurate, don't re-describe it — just bind it:
  `"Strictly refer to the actions and camera movements in Video 1."` **[OFFICIAL]**
- Sweet spots for stability **[OFFICIAL]**: 1–5 subjects (image refs up to 8), subject clips
  5–10 s, storyboards ≤ 15 panels (line art, no text burned in), edit-input videos ≤ 20 s,
  1–5 reference images for guided edits.

**2.0 vs 2.5 tag behavior [SITE, consistent with OFFICIAL]:** in 2.0 tags are loose pointers —
the model decides what to take from each reference. In 2.5 tags are assignments with declared
roles and exclusions. If you don't scope a reference, the model's own judgment fills the gap.

---

## 4. Audio notation

**Four bracket types [OFFICIAL — 2.5 API tutorial]:**

| Bracket | Meaning |
|---|---|
| `{ … }` | dialogue / spoken lines |
| `( … )` | music |
| `< … >` | sound effects |
| `【 … 】` | burned-in subtitles |

- For non-Chinese dialogue, state the language before the line. **[OFFICIAL]**
- Plain prose audio direction also works ("Sound effects: a 'ding' discovery sound";
  "Natural environmental audio only: wind, rustling grass") — official examples use both.
  Brackets = precision tool; prose = looser direction. **[OFFICIAL examples]**
- Dialogue can also be written `Dialogue (character): "line"` per shot. **[OFFICIAL example]**
- ⚠ **Migration trap:** in 2.0-era style, `【Style】` marked a header block. In 2.5, `【】`
  means *subtitles* — a pasted 2.0 header can render as on-screen text. **[SITE + OFFICIAL bracket table]**

### Negative controls [OFFICIAL]

Officially guaranteed only for **subtitles and audio**: "No subtitles." / "No BGM; only
environmental and action sounds." / "No audio." Visual negatives (`[Strictly exclude] …`)
appear in official examples but aren't a promised capability — prefer positive description.

---

## 5. Time control (2.5 only)

2.0 **does not respond to timestamps** — it only respects Shot numbers. 2.5 honors: **[OFFICIAL]**

- **Intervals** at 1-second granularity, gapless: `0-3s … 3-8s … 8-15s` (no holes).
- **Time points**: "At the 5-second mark, a burst of golden lightning…"
- **Relative time**: "After 3 seconds, everyone shakes their head."
- Don't use timestamps for high-frequency actions ("shake head 3×/second").
- Under-specified ranges → model improvises; over-packed ranges → dropped beats or extra cuts.

Shot lists without durations are also valid in 2.5 — the model paces the cut itself.

---

## 6. Task types & locked parameters (2.5)

Seedance 2.5 classifies every request from **assets + prompt intent**. Some types lock output
parameters. Violations → errors (`InvalidParameter.TaskTypeConstraint` async, or
`InvalidParameter.TaskTypeMismatch` if your declared type disagrees with the model's reading). **[OFFICIAL]**

| Task | Trigger | Locks |
|---|---|---|
| Text-to-video | text only | none |
| First/last frame | `role: first_frame` / `last_frame` | `ratio` must be `adaptive` (AR follows first frame); duration free |
| Reference-to-video | any `reference_*` role | none |
| **Video editing** | ref video + editing intent words | `ratio: adaptive`, `duration: -1` (output ≈ input, −0.4 s max); input must be 4–30 s |
| **Video extension** | ref video + extension intent words | `ratio: adaptive`; duration free |

- **Trigger keywords are mandatory** for edit/extend: *edit video, add, remove, delete,
  modify, replace, change to* / *extend forward, extend backward, continue, continue the story*.
- `omni_reference_task_type` (`auto` | `edit` | `extend`) moves validation to submission time.
  The model still re-classifies from the prompt at runtime — parameter and prompt must agree.
- Editing: describe changes **A → B**, scope with timestamps
  ("from 4–6 s change the man's action from drinking coffee to mopping; leave the rest unchanged").
- Extension: output normally contains **only the new footage** — say "…and then end with
  Video 1" to include the original. 2–3 clips can be bridged seamlessly in one request.
- Recommend `output_format: mov` for edit/extend (color/brightness/audio continuity).

---

## 7. Special reference modes (2.5)

- **Storyboard (multi-panel, one image):** high-level *plot* guidance only — output won't
  match panel-for-panel. Use simple line art, ≤ 15 panels, no text on the image; fill gaps
  (actions, camera, style) in the prompt.
- **Keyframes (separate images):** strict visual alignment. Lead with:
  `"Use Images 1 to 7 in order as keyframes."` Duration user-defined.
- **First/last frame via `role` param** = strict + locks AR. Via `reference_image` + prose
  ("Image 3 is the first frame") = looser, AR stays free.
- **3D clay-model previz → render:** feed a crude blockout video (simple geometric primitives,
  no trajectory lines/camera cones) as the *only* reference for camera, blocking, rhythm;
  bind cast/scene stills for appearance; state exactly which channels to take
  ("camera movement and motion only — not the visual content"; add "lighting changes" only if
  wanted). Fine-grained clay models suit re-rendering ("coloring").
- **Pure audio reference** (2.5 only): song/voice as the sole non-text input.
- **Motion / style / voice reference formulas [OFFICIAL, 2.0-era, still valid]:**
  - Image ref: *Reference/extract/combine "X" from Image n to generate "plot", keeping X consistent.*
  - Video ref: *Reference "action/camera/effect" from Video n… keeping it consistent.*
  - Voice timbre: *"Character" says: "line", voice timbre references Audio n.*

---

## 8. API mechanics (ModelArk)

- Async: `tasks.create` → poll `tasks.get` (~10–30 s) → video URL. Base URL
  `https://ark.ap-southeast.bytepluses.com/api/v3`, auth via `ARK_API_KEY`.
- `content` array = one text item + asset items, each with `type` (`image_url` / `video_url` /
  `audio_url`) and `role` (`reference_image` / `reference_video` / `reference_audio` /
  `first_frame` / `last_frame`). Asset URLs must be publicly reachable (they recommend TOS).
- Key params: `generate_audio`, `resolution`, `ratio`, `duration`, `output_format`,
  `watermark` (default **false**), `omni_reference_task_type`, `return_last_frame`,
  `service_tier` (offline/flex — currently unsupported on these models).
- **mov** = H.264 + **yuv444p** + PCM — the "don't destroy my chroma before grading" option.
  Plays in VLC / mpv / IINA / ffplay; not guaranteed elsewhere. 4K (2.0) is H.265 10-bit —
  safe players: VLC, mpv, Safari (macOS), QuickTime.
- Input limits (2.5): images 300–6000 px/side, AR 0.4–2.5, ≤ 30 MB each; videos 2–30 s each,
  ≤ 200 MB, 24–60 fps, mp4/mov (H.264/H.265 + AAC/MP3); audio wav/mp3, 2–30 s, ≤ 15 MB;
  request body ≤ 64 MB; **no base64 for video**.
- Frame-jump/stretch bug on first-frame tasks = input/output AR mismatch → use
  `ratio: adaptive` or pre-crop to a supported pixel size.

### Operational gotchas

- **Output URLs expire in 24 h, max 100 downloads. Task records last 7 days.**
  Archive outputs immediately (they push TOS data-subscription for auto-transfer).
- Rate limits (per account, per model): individual 180 RPM / **3 concurrent**;
  enterprise 600 RPM / 10 concurrent (2.0 4K: 15 RPM / 1 concurrent). Excess queues.
- Activation requires >$30 balance or a resource pack.

---

## 9. Faces & portrait compliance

- **[OFFICIAL]** Seedance 2.0 **and** 2.5 on ModelArk reject reference images/videos
  containing real human faces at input moderation. Sanctioned paths:
  1. **Trusted model outputs** — face-containing outputs generated under *your own account on
     ModelArk* in the last 30 days can be re-input (videos since 2026-03-11; last-frames and
     Seedream 5.0 lite images since 2026-04-16). Same account + same platform only; originals
     only — any re-edit, compression, or re-encode breaks trust verification. Trust covers
     input only; output moderation still applies.
  2. **Preset digital characters** — platform library, passed as `asset://<ID>`.
  3. **Authorized real-person assets** — formal verification + onboarding, then `asset://<ID>`.
- **[FIELD]** This fence is **ModelArk's**, not a property of AI video generally. Our Kling
  work (HTB) used real actors and real footage with no rejections, and our route to Seedance
  is **Fal.ai**, whose moderation behavior is not ModelArk's. Field results on our actual
  route outrank this section for our pipeline — this section documents ByteDance's front door.

---

## 10. Discrepancy ledger (resolved)

| Claim | Verdict |
|---|---|
| Four audio brackets `{}` `()` `<>` `【】` | **Canonical for 2.5** (API tutorial, Prompt Rules). Prose audio also accepted. |
| `[Generation Goal]`-style section labels | House style, not syntax. Sandwich shape is what matters. |
| 2.0 responds to timestamps | **No.** 2.0 = Shot numbers only; timestamps are 2.5+. |
| Real faces always rejected | ModelArk-only fence; our Fal/Kling route differs **[FIELD]**. |
| Prompt-enhancement flags on API platforms | Can *hurt* structured prompts — the structure carries the information. Keep optimizers off for template prompts. |

## 11. Official prompt-optimization skills

The official **2.5 skill (`sd25-pe`, v0.1.1)** is captured in this folder as
`sd25-pe SKILL.md` — reviewed and clean (pure prompt-engineering instructions; no file,
network, or tool access needed). Install locally with:

```bash
npx --yes skills@latest add \
  "https://arkdocs-en.tos-ap-southeast-1.volces.com/skills/" \
  --skill sd25-pe --yes     # usage: /sd25-pe + prompt
```

Standout rules the skill adds beyond the docs **[OFFICIAL]**:

- **`【Unused Assets】` closure** — every attached-but-unused asset is listed and explicitly
  deactivated, so downstream prompt enhancers can't reactivate them.
- **Parameter separation** — ratio/duration/resolution/fps/audio-toggle are API parameters,
  never prose in the prompt.
- **Routing gate** — if the requested output ratio/duration conflicts with a reference video,
  the task is *not* editing; it becomes generation with the sentence
  `Please note that this is not video editing.` placed after the goal.
- **Editing scope closure** — every edit prompt ends with "everything not explicitly modified
  remains unchanged" (or the retain-only variant).
- **Keyframe role sentences are verbatim**: `Use @ImageN as the first frame.` — never weakened
  to "as a composition reference."
- **Mapping priority chain**: user's explicit spec > prompt text > asset content > filename >
  upload order (order = tie-breaker only, never evidence of identity).
- **Motion-slot replacement** for swapping moving subjects: remove original, inherit exact
  timing/path/speed/occlusions, declare the original gone.
- ⚠ One behavior to know: the skill self-updates (`npx skills update sd25-pe`) on first
  trigger per session — its instructions can change between versions; re-review after updates.

The 2.0 skill (`/sd2-pe`) is distributed as a SKILL.md from their docs page — not yet captured.

---

*Compiled 2026-08-15 from BytePlus ModelArk docs (Seedance 2.5 prompt guide & API tutorial,
Seedance 2.0 series doc, portrait-videos doc) plus field notes. Official docs describe
ByteDance's platform; our pipeline runs via Fal.ai — where behavior differs, trust the runs.*

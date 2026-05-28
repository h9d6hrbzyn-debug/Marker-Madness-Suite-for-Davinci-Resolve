#!/usr/bin/env python3
"""
Reel Time Plus 1.2 — Running Time Calculator

Plan and track running times across multiple shows or projects.
Add acts or reels, set a goal time, configure commercial breaks or
film leader, and instantly see how far over or under you are.

Part of the Marker Madness suite. Standalone — no DaVinci Resolve
connection required.

Installation:
  Copy to your DaVinci Resolve scripts folder and run from
  Workspace > Scripts > Utility inside DaVinci Resolve, or
  run directly with:  python3 "Reel Time Plus 1.2.py"

  macOS:   /Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Utility/
  Windows: C:\\ProgramData\\Blackmagic Design\\DaVinci Resolve\\Fusion\\Scripts\\Utility\\
  Linux:   /opt/resolve/Developer/Scripting/Modules/
"""

import sys
import os
import json
import uuid
import platform
import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser

_IS_WINDOWS = platform.system() == "Windows"

# ---------------------------------------------------------------------------
# App icon (embedded Base64 PNG — no external file required)
# ---------------------------------------------------------------------------

APP_ICON_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAABAAAAAQACAYAAAB/HSuDAABIHElEQVR4nO3dP3JcV5YnYFKhFYAm"
    "g1iBmmWP2Z4WMCbdVmiW0CvoJYyC49KcBdBrc+xmcwViwNQaOJGlyhIIIoHMl+/ee/58X0QZJVHE"
    "QwL57jm/e+7Llzc3t19fAAAAAKX9sPoCAAAAgPEEAAAAANCAAAAAAAAaEAAAAABAAwIAAAAAaEAA"
    "AAAAAA0IAAAAAKABAQAAAAA0IAAAAACABgQAAAAA0IAAAAAAABoQAAAAAEADAgAAAABoQAAAAAAA"
    "DQgAAAAAoAEBAAAAADQgAAAAAIAGBAAAAADQgAAAAAAAGhAAAAAAQAMCAAAAAGhAAAAAAAANCAAA"
    "AACgAQEAAAAANCAAAAAAgAYEAAAAANCAAAAAAAAaEAAAAABAAwIAAAAAaEAAAAAAAA0IAAAAAKAB"
    "AQAAAAA0IAAAAACABgQAAAAA0IAAAAAAABoQAAAAAEADAgAAAABoQAAAAAAADQgAAAAAoAEBAAAA"
    "ADQgAAAAAIAGBAAAAADQgAAAAAAAGhAAAAAAQAMCAAAAAGhAAAAAAAANCAAAAACgAQEAAAAANCAA"
    "AAAAgAYEAAAAANCAAAAAAAAaEAAAAABAAwIAAAAAaEAAAAAAAA0IAAAAAKABAQAAAAA0IAAAAACA"
    "BgQAAAAA0IAAAAAAABoQAAAAAEADAgAAAABoQAAAAAAADQgAAAAAoAEBAAAAADQgAAAAAIAGBAAA"
    "AADQgAAAAAAAGhAAAAAAQAMCAAAAAGhAAAAAAAANCAAAAACgAQEAAAAANCAAAAAAgAYEAAAAANCA"
    "AAAAAAAaEAAAAABAAwIAAAAAaEAAAAAAAA0IAAAAAKABAQAAAAA0IAAAAACABgQAAAAA0IAAAAAA"
    "ABoQAAAAAEADAgAAAABoQAAAAAAADQgAAAAAoAEBAAAAADQgAAAAAIAGBAAAAADQgAAAAAAAGvhx"
    "9QUAAH/5v//j93Ivx//8f7erLwEAePHixcubm9uvXgkAWKdi03+KMAAA1nEEAAAW6tT8d/x+ASAS"
    "AQAALNK1Ge76fQPAagIAAFigexPc/fsHgBUEAAAwmebX6wAAKwgAAGAizb/XAwBWEQAAwCSaf68L"
    "AKwkAAAAAIAGBAAAAADQgAAAACYw/u/1AYDVBAAAAADQgAAAAAAAGhAAAAAAQAMCAAAAAGhAAAAA"
    "AAANCAAAAACgAQEAAAAANCAAAAAAgAYEAAAAANCAAAAAAAAaEAAAAABAAwIAAAAAaEAAAAAAAA0I"
    "AAAAAKABAQAAAAA0IAAAAACABgQAAAAA0IAAAAAAABoQAAAAAEADAgAAAABoQAAAAAAADQgAAAAA"
    "oAEBAAAAADQgAAAAAIAGBAAAAADQgAAAAAAAGhAAAAAAQAMCAAAAAGhAAAAAAAAN/Lj6AgCA8/zr"
    "v8R9pf7zv1dfAQDwHAEAAEwWuZGf/T0JDgBgnpc3N7dfJ349ACjrj19+X30JZb16f7v6EgAgPQEA"
    "AJxJgx+XgAAAnicAAIB7NPn1CAcA4E8CAABa0ugjGACgGwEAAOVp9jmXUACAygQAAJSh0WcUwQAA"
    "FQgAAEhLw88qAgEAMhIAAJCCZp/ohAIARCcAACAkDT/ZCQQAiEYAAEAIGn6qEwgAsJoAAIAlNPx0"
    "JxAAYDYBAABTaPjhaQIBAEYTAAAwjKYfthEGADCCAACA3Wj4YQyBAAB7EAAAcBVNP8wlDABgKwEA"
    "ABfT9Ofz5sPbZ//Ml3efplwL+xEGAHAJAQAAz9Lw1236TxEG5CQQAOApAgAAHqXp79n4PyQIyEsY"
    "AMBDAgAA/knTn9+ezf+RECA/YQAABwIAgOY0/TWMaPwfEgTUIAwA6EsAANCUxr+OGc3/kRCgDkEA"
    "QD8CAIBGNP31zGz+j4QA9QgDAHoQAAAUp+mva0XzfyQEqEsYAFDXj6svAIAxNP7ANfcOQQBAPSYA"
    "AArR9Pexcvf/yBRAH8IAgBoEAAAFaPx7idD8HwkBehEEAOTmCABAUpp+YOV9RxgAkI8JAIBkNP69"
    "Rdr9PzIF0JsgACAPEwAACWj6gahMBQDkIQAACEzjD2TiEwQAYnMEACAgjT9Zxv+PHAPgMY4HAMRi"
    "AgAgCE0/UI3jAQCxCAAAFtP4Ax04HgCwngAAYBGNP9CRIABgHQEAwGQafwBBAMAKAgCASTT+AKfv"
    "jR4YCDCeAABgMI0/wPn3SkEAwDgCAIBBNP4A2++dggCA/QkAAHam8QfY714qCADYz8ubm9uvO/59"
    "AG1p/JnhzYe34V7oL+8+rb4EGhAEAFzPBADAlTT+AOOZCAC4ngAAYCONP8B8ggCA7RwBALiQxp/V"
    "Ih0DMP7Pao4GAJzPBADAmTT+APGYCAA4nwkAgGdo/IkowhSA3X8iMhEAcNoPT/w7gPY0/0S1uvle"
    "/fXhFPdtgNMcAQB4hAISIC/HAgAe5wgAwD0af7JZcRTA7j/ZOBYA8CcBAIDGn+RmhgCafzITBADd"
    "CQCA1uz4U8WMEEDzTxWCAKArAQDQluafikYEARp/KhICAB0JAIB2NP5Ut2cIoPmnOkEA0IkAAGhD"
    "40831wQBGn+6EQQAHQgAgBY0/3R3Thig6ac7IQBQnQAAKE3jD8ClBAFAVT+svgCAUTT/AFg/AP5i"
    "AgAoR+MPwF5MAwCVCACAMjT+AIwiCAAqcAQAKEHzD4B1BuBpJgCA1DT+AMxmGgDIygQAkJbmHwDr"
    "D8D5TAAA6Wj8AYjCNACQiQkAIBXNPwCRWJeATEwAACkosACIzjQAEJ0JACA8zT8AGVivgOhMAABh"
    "KaQAyMo0ABCRCQAgJM0/AJlZx4CITAAAoSiYAKjGNAAQhQkAIAzNPwAVWd+AKAQAQAiKIwAqs84B"
    "ETgCACylIILLvfnwNszL9uXdp9WXAOk4EgCsIgAAltH8Q6xmfhahAQgBgDUEAMASmn866Njc70VI"
    "QAcmAYDZBADAVBp/qtHkzyccoBpBADCLAACYRvNPZhr9+AQDZCYEAGYQAABTaP7JRLNfh1CATIQA"
    "wGgCAGAojT/Rafb7EQoQnSAAGEUAAAyj+ScazT6nCAWIRggAjCAAAIbQ/BOBhp+tBAJEIAQA9iYA"
    "AHal8WclDT+jCARYSRAA7EUAAOxG889sGv7n/fzzrxe/rh8//rbp59GJQIDZhADAHn7c5W8B2tP8"
    "M0P2hv/1658e/ed3d59fVFfte3/4uygQYMY6KwQAriUAAK6m+Wek7E0//X5PhQGMIgQAriUAADbT"
    "+DOChp/sTAcwY+01DQBsIQAANtH8sydNP5WZDmAE0wDAFgIA4GKafyo2/Ycz6qPPox/+/sfOws/4"
    "2itVO/9/DWEAexICAJcSAAAX0fxToek/1ZBST+RwRRjAHoQAwCUEAMDZNP9kbvrp67HAJ1ooIAzg"
    "GkIA4FwCAOBZGn+6NP2Rd4vpQxjAFh4OCJzjh7P+FNCW5p9LG5cMzb8mv4cKRz2yvKeIw7oNPMUE"
    "AHCSIoJzaE7IJmMAZCqASzgSAJwiAAAepfnnKZp+WEcYwDmEAMBjBADAdzT/nKLxh5jvyS/vPq2+"
    "FAISAgAPeQYA8A3NPyvPIUc4sz36Gk6Nn0f43kc49X1lHMO/1MyfqWcFcIp1HbjPBADwdwoEVu72"
    "r2h+Dw1o1aabOIHK8TpmBR6OB/AYnxAAHAkAAM0/Sxr/Uw2aj+JjpFmN+MPf7/v/f3YY4HgAR44E"
    "AAIAaM7OP0fO90NNggDuEwJAbwIAaEzzz8qmv/MIfofz7x2/1+ivh+MBHAkBoC8PAYSmNP+9RX9g"
    "2OpgYPXXJ7cMvz/R7wGMpw6AngQA0JBFvy9F/7fsTteUoQGPwj2hN/UA9CMAgGYs9j1FLfI14HT6"
    "fVv99TPeIxhPXQC9eAYANGKR7ydzQT/z0wAiN2bkkn36wAMDe/JMAOhDAABNaP57ydT4r34YoOa/"
    "nsd+pqsb82y/Z4KAfoQA0IMjANCA5r+PamO8q5s26pjRgFf8fa12T+Fp6gWoTwAAxVnMexhRpFds"
    "ZqC6Ue9bQUAf6gaozREAKMwiXt+InbkVjf/qYwBQafz/+F4a8XUdDejBcQCoSwAARWn+a5u12z/z"
    "QXynRLgGeE6EAOvhNdz//3u/hwQB9QkBoCYBABSk+a/LWVwgEkFAbUIAqOflzc3t19UXAexH81/T"
    "jMb/qR3MWTvwI3csu/r5518v/m8+fvxtyLV0seL3OML79+DLu0/TvhbzvHp/6+WGIjwEEArR/NfU"
    "bdf/0Kxo/sms8+9wt/tVF+oLqEMAAEVYnOuZ/dTtpxqWWeebuzZN1NRt9//IJwbUpM6AGjwDAAqw"
    "KNdiBw2owPMB6vFMAMjPBAAkp/mvI8KumR14qCPK+znCvY39qDsgNwEAJGYRriNDcRzhY86AvO/L"
    "DPc5zqP+gLwcAYCkLL41KIiBThwLqMNxAMhJAAAJzWr+z2lOfeTTuNd25djwqV3Fwz+PMlYM3UV7"
    "+N8lBAHXv3YR1mYhAOQjAIBkRjf/lzam9/+8MGDMa3zqs919Vjuwyl73oMP90Npx3ut06et6NPr1"
    "FQJALi9vbm6/rr4IYH3zv+eOtGJu3Gt8KLrvGxkCZN5d5PTvzDmES/GtfH+Oug9ZO3Kvza/e3w79"
    "+4F9eAggJJGl+R/x91UwovkHiGCve5O1Y+zrMfr19WwiyMEEACQwalGdUWx139GZ0fjPmgKw65+T"
    "CYD6Zr5PZ92POq8d2ddmkwAQmwkACC5z8z/z60R07fd+KLQj7PofGgrNP8QV6T26132r69pRYW02"
    "CQCxmQCAwLI3/113c1aM+zuzDYy26r7UZf2otjabBICYTABAUJWa/5Vfd7Yqu/4A1zIN0HttNgkA"
    "MQkAICCLZj6HImqPQmrrjpnQABhp6z1mrymAve6xzKWegXgEABBMpqf9Z/v61b8vIQBQ/d4S5X5b"
    "6Xvy6QDQiwAAAqnc/Ee7jsg7Us7zAxWMupdVmgaI8n0IAaAPAQBA4qIt8k4dkF/ke0rU+zBAZAIA"
    "CKLD7n/U64m482QKAMhs1j0s8zRAtOs2BQA9CAAgAA/JySFasZZxxw7II9O9JMv9uTv1DqwnAIDF"
    "LIY5rCguTQEAGa26dwkBclD3wFovb25uvy6+BmhrxiIYuSD68u7Ti+givH6rP34L6Cf7fSf6+hJh"
    "bVn92r16fzvl6wDfMgEAi0jA44tcoFUb3wXiqHDvyH7/7kAdBGsIAGABi158kYrHKDtqAJnuVZHu"
    "4zxOPQTzCQAAijxRuupOHjBPtXtGtXs6wLUEADCZtDuurUXi69c/vei2swaQ6R4lBIhLXQRzCQBg"
    "Iotc3eZ/RgiwVbUdPaDnveLa+6wQIC71EcwjAIBJLG61xkMPhejspj/6DhvQ04x7015hqyMBcamT"
    "YA4BAExgUesx8h/5KED0nT1grUwf+7dHAGsaICb1EownAIDBLGYxXVP83d19PvnvHAUAsokeEI4K"
    "XYUAMambYCwBABT35d2nFxGtvK7sRZ+jAEC30f9Lw9jo64G1GVhFAAADSbFj2fPspykAoILou/8z"
    "eC5APOonGEcAAINYvGIZscuzMgQwBQCsVGH3v9p0WDXqKBhDAAANFq1oo4azr2dVURf1eQB2/IDo"
    "94LZzf+K9aL72pyxnoIKBACwM4tVLKOLuZGF6HNMAQAV7z2rw1OTALGoq2BfAgBoIkqyP/M6ZhVx"
    "GY8CRN75A8bL9LF/K0LXWetHx7UZWEsAAI1S6tUL/Kyvv+KBThkfCigEgJ4iv/dXjf6vXEu6rM2V"
    "6yvIRAAAO7E4xdBxdHP1jhzQw8rR/5XHrTquKxGps2AfAgBotiitSvpnfN3VRZopACC6yLv/kY1e"
    "XyqvzV3rLYhKAAANzV7wOzT/z4UAo3evTAEAme8xUXf/K4cA2Zp/YB8CAGiaRs9a+Ds1/6cK1yjF"
    "6yl2BKGHyO/1VeFp1xAgc/Ofte6CKF7e3Nx+XX0RkFWVRWhEQTPzgX8RHXazVhSuWZ/sDYyX5f5w"
    "fxogWgCQPdzO3Pg/9Or97epLgJQEANC8+R9RaHRv/lfLUuQD82S7L6wKUSuHAJWa/yMhAFzuxw3/"
    "DVDQsTC4ptiYWVxo/vej8Yc+7/PIxwDui978H9eh0etetrUZiM8EAGxQbff/lHMKjhWFheb/eecW"
    "+Zp/6Mf9YV+z18Goa/MqpgDgMgIAuFCX5j+qS5v/DGOkKwp8jT/gPrGfTg13REIAOJ8AAC6g+c/X"
    "/B8JAf6k8QfOCQI63iuuDYyFAGsJAeA8PgYQSNH4X9P8P/b/O+pY0APPc2/4a424Zq3YslYBzGYC"
    "AM5k93+NLcXUUwVct0mAw86e4h5wz7hszbh2rTANsIYpAHieAADOoPlf45qdFCEAACvXCiHAGkIA"
    "eJojAPAMzf8a145RPlW4OQ4AwOig2HGANdRt8DQBABDOXkVTt3F/AGJNiQkBgGgEAPAEKfJ8exdL"
    "pwo5UwAAnLtmXEMIMJ/6DU4TAMAJFo/5RhVJQgAAnguAR06NCQHmU8fB4wQAQAiriiOTAAB9rGj+"
    "j4QAQAQCAHiE1HiuGUWRhwIC9BYh8BUCzKWeg+8JAOABi0VdQgCAnnw0bF/qOviWAABotRtyKgTw"
    "iQEANUVr/k0BACsJAOAeKXGPIuhhwaf5B6grYvArBJhLfQd/EQDAP1gcehU/x8JP8w9QX8Tgd/U6"
    "2I06D/4kAADaFj0RCkAA+ga/UdZDoI+XNze3X1dfBKwmFZ5HsQMA3/ry7pOXZJJX72+91rRmAoD2"
    "NP/zaP4BwPq4krqP7gQAwBSafwCwTgJrCQBoTQo8h+YfAKyXUaj/6EwAQFtu/nNo/gHAuhmNOpCu"
    "BADAMJp/ALB+AnEIAGhJ6huv+X/9+qdh1wIA2QjRx1MP0pEAAFju2PwLAQCoxtoGRCIAoB1pb6xd"
    "i4eFkUIJgCquDbhNAYynLqQbAQCtuMnHbv6f++cAkMVeAbcQYDz1IZ0IAIDdXFqk3N19PvnvhAAA"
    "ZLV3wC0EAPYiAKAN6e5YW4sTIQAAlTzV5D+15j1HCDCWOpEuXt7c3H5dfREwmpv6WHsUJc/tilxT"
    "NAFA5ub/vi/vPu3y9/C4V+9vvTSUZgIACOG5wsiRAACiOqxRM5p/gGuZAKA8u/9jjRhJVEQBkMWK"
    "CTZTAGOZAqAyEwBAuPOIngsAQAbPBdajdv49DwDYSgBAaXb/xxldfAgBAIhs9bSaEGAc9SOVCQAo"
    "y807f9FxqoBylhKAzs3/kRBgHHUkVQkAgNAeFlKafwBWE1ADWQkAKElqW2u34Vhoaf4BiCJKQG0K"
    "YBz1JBUJAIAURYbmH4BoogTUQgDgXD4GkHKktWMoLgAgNh8POIaPBaQSEwAAAADQgACAUuz+j2H3"
    "HwDis16Pob6kEgEA8CTFBADkYd0GniIAoAzp7P4UEQCQj/V7f+pMqhAAUIKbMgAA6k14mgAAeJTd"
    "AwDIyzoOPEYAQHp2//enaACA/Kzn+1N3kp0AAPiGYgEA6rCuA/cJAEhNCrvO69c/LfzqANCT9Xc9"
    "9SeZCQCAi3cJjsWHIgQA5tm6/poCAI4EAKQlfd3X1uLgUIQIAgBgnD3WWiHAvtShZCUAAC5yqgAR"
    "AgDA/qy7wJ5e3tzcft31b4QJpK5rR/+fc3f3+corAoDeRq25X9592nhFPObV+1svDKmYAIDmLhkJ"
    "PLfIMA0AANuNDNwdBYDeflx9AXApu/9rHYuN54qT4783DQAA5zFpl7MuNQVAJiYAoLFrdgFMAwBA"
    "zubfFAD05RkApGL3fz97Lv52LAAg3xrqeQD7MQVAFiYAgKuZBgCAywnQgdlMAJCG3f/9jBz9e6qY"
    "8TwAAIi1bpoC2I8pADIwAQDNjD73d6pY0fwDQLx10/MAoBcBACnY/c/lULRo+AHAGtqJepUMBADQ"
    "yOyU/xgCCAMAIO56aQoA+vAMAMKTpu7D4g4APMXzAPbhWQBEZgIAAAAAGhAAEJrd/33Y/QcA1Atz"
    "qF+JTAAAxWn+AQB1A3AgACAs6SkAABmpY4lKAACF2f0HANQPwJEAgJCkpgAAZKaeJSIBABRl9x8A"
    "UEcA9wkACEdaej3NPwCgnlhPXUs0AgAAAABoQAAAjXf/f/7516HXAgDEcunab6oQanl5c3P7dfVF"
    "wJExqeudu1A/LAA+fvzNLyIAFHXNuv/l3acBV9TLq/e3qy8B/s4EABRyTUpvGgAAarp2jTcFAHWY"
    "ACAMu//rdv8fMg0AAPntud6bArieKQAi+HH1BQD72DOdPxYMggAAyGfEVN+hzhACQH4mAAjB7n/s"
    "B/8JAgAgvhlrvBDgOqYAWM0zAKCRrTsCng8AALFZ44FzOAIAyc16MI9jAQAQz+yQ3lEAyM0RAJYz"
    "/h/jwX+XciwAANZZua47BnAdxwBYyQQAJLbyY3lMBADAuvV3JVMAkJdnALCU3f/8xUKEQgQAOrCe"
    "16D+ZSVHAFjKDXDu7v/oZt2xAADYX9T121GA7RwDYBVHAKCR4wI/qpBwLAAA9l9XRxHcQz8mAFjG"
    "7v/as/8zRvcVFgBQe402BbCdKQBW8AwAaOqw8I9u0D0fAABirZ0z1n8gLhMALGH3P96T/40ZAsA6"
    "mddhUwDbmQJgNs8AAP7O8wEAYL7MjT+QjwkAljABEGv3P/PZQwDIqNpaawpgGxMAzCYAYDrNf/wA"
    "4MiuBABYX88hANhOCMBMAgCmEwDkaP7vEwQAwPm+fPmv7/7Zmzd/K7+eCgG2EQAwkwCAqTT/OQOA"
    "o+qFCwDs3fg/9G//9r/Lrp8CgO2EAMwiAGAqAUDe5n90CBCleAGAEY3/qCAg2vopBNhGAMAsP0z7"
    "SkAJPj8YAK5r/g/+z//5X9ZjYDoTAExj9z//7v+oiYBouxcAMDoA2DoFkGHNNAWwjSkAZvhxylcB"
    "yjoWIjM+zggAKjT+96cAzg0BMjT+QHyOAEBg0Xf/9yhMFDQAZGv892j+K6+VmeoX6MYRAKYw/t9r"
    "AT13GiBbQQNAXyOb/lNTAJnXSccAtnEMgNEcAYCgsjb/B44FAFCJHf9tdYwQAOIRADCc3f++ngoC"
    "Mu9qANCDxp8VdbMpAEbyDABI7PXrn15koNkHIBPn/IGqPAOA4UwAjBv/vx8A3N19fpHBYRpAIABA"
    "RLN3/I/evPnbiywOtcclNYdjAJczAcBIjgAwlOZ/3u5/ljBA8w9ARJr/GlOHFTgGwEgCACj48L/j"
    "Ih05CACAzo1/5qb/kikADwOEWAQAkNC5KbwgAADiNv5RR//t9kNdngHAMMb/55z9v5SpAAA6i9D4"
    "Rw0ALq0vPAtgLM8CYAQTAJDQccHdEgSYCgCgK83/9+z2Qy8CAEjsfvJuAQeAx2n8v2eaEHpyBIAh"
    "jP+vefjfuQu6YwAAdKDxXzPuf/Ln8e7T1X9HN44BsDcTAFDMNccDAKCCKI1/tDP+D+sFmwbQjwAA"
    "Cu3+n3M8wO4/AJVFaP4jN/7nGlEv+EhAWE8AAA2YCgCgOo3/9VMANgmgPs8AYHfO/6/f/QeALiI0"
    "/pl3/Q8BwOzG37MALuM5AOzJBAAAAOlo/Pdh1x96EQAAAJBKhOY/644/0JsjAOzK+P9ljP8DwPk0"
    "/nU4BnAZxwDYiwkAAABCi9D4H9j1B7ITAAAUKoQVp0A1EZp/91agCkcA2I3x/8sY/2dkEaxYBbLT"
    "+NfnGMBlHANgDyYAAAoWwoc/LwQAMtL4A4wjAIAF7P4zoxA+/reCACCDCI3/gXvmxNf6w1tTADDZ"
    "D7O/IAA9i2qAyPepQ+Ov+QeqEwCwC+f/IXZBHKG4Bnjs3rT6/qTxJwv1NntwBAAmM/7POUYUxI4E"
    "AFGsbvoP7PbH4BgAzGUCAKCZCIU30FOEHf8DzT/QlQCAqxlHgn3NKI6jFOFAHxHuOcb9yU7dzbUE"
    "ADCR8X+iiVCQA7VFCBw1/rGpj2AezwAAaM6zAYCR95aVjPoDfMsEAABhinUgvwg7/geaf4DvCQC4"
    "inNI+4+3vX790+afB1Qp3IGcItw/jPvn5BjA+dTfXMMRAAjofghwd/d56bXQt4i3ewZccs9YzT0r"
    "Zj2jjoFYBAAQyGO7/8IAVvFsAODc+8Rqmv84TDJCbC9vbm6/rr4I8jKCtGb8X5peX5Si+khxDUS8"
    "R7k3xfBc/XJJ3fLl3acdrqi+V+9vV18CSZkAYDPN/7rE3FQAs5kGAB7eD1bS+Mdgt39tHS4EYAsB"
    "ACQnDKjpUNxGKLIf8mwA6CvCPUnjn7Pp9ywAiEMAAEHG/++Px0nUiR4CHCjEoYco9yH3nHVm1iWH"
    "uskxABhHAAABbQkDPBeA2UwDQH0Rmn+Nf15qE4jHQwDZxPn/+Z9ru+cDdsgnQhH+FAU61BLhnuO+"
    "EsvMDQkTAOfzHAAuZQIACkwFaP7ri3oc4Mg0ANQQ4T6j8c9JLQI5mABgExMAc3f/n+LBOv1EKNCf"
    "oniHfKLcV9w/Ypu5AWEK4DwmALiUCQBITuLej2kAoFrzr/HPQ90BuZkA4GJ2/2NNANBbhML9KYp6"
    "iCvC/cM9glNMAJzPFACX+OGiPw2cTfPPDNGL5wgNBvD9+3L1e/Nw74p+/2ItdRSM4QgAQHLHInp1"
    "QX/K8boU+7BWlHuEewHAOiYAAIqIXlRHaT6gowjvP7v+AOuZAAAoJMM0QPSgAiqJcC/wngeIw0MA"
    "uYgHAJ7HuTUiiFD4P0VTALXf/97j7MHDAM/jQYCcyxEAgKKij9tGaFCgmggP+DuIfO8B6EwAAFBc"
    "5EI8SrMCFUR4L0UPHgG68wwAgAY8GwDqitL4AxCfZwBwNuf/z+P8P9FFaBaeopGAXO9l71lG8xyA"
    "83gOAOcwAQDQjGkAyE3jD8BWngEA0FTkXTvPBoDT743VnPMHyMsEAEBjpgEghyiNPwC5mQCAHTn/"
    "T1aRC3vTAHQW5fc/8j2C+tRXsB8TAAD8nWkAiCNC03+g8QeoxQQAZ/EJANBH5II/ym4ojBThd9w5"
    "f8hHvc45TAAA8B3TANC38QegLhMAsBPn06gocjNgGoAqovwuR36/gzoL9iEAACD1KHCExgky//5G"
    "f48DsB9HAGCi169/enF399lrTkqHBiFCs/KY43VpYsgiwnvJ+wWgHwEAz/JAkf1DgIeEAmTh2QBw"
    "HY0//MXGyJi6/dX7W79mnCQAgACEAmRjGgDyNf4Hdv2JVOsA8728ubn9uuDrkogJgH0eTLPHwmdS"
    "gGiiNDWnaHaIIML7xHuBmS6peS6tbb68+7ThinoxAcBTTAAAUPpIwIHmh5W/fyv53We0azc4HAOA"
    "uXwKAADlm4wIjRh9RPhYP0/2B+AxJgBgksdG3EaOyMFspgHobnXTnyWQA2AdzwDgSc7/7/cMgHOd"
    "CgUEAGQSpRE6RYNExd95v9esMnNDwzMAzuM5AJxiAgACNf97TApABKYB6ELjD6eN2Lw41F1CANhO"
    "AAAJ2P0nq8gfF3hwuDa7pmz93VnN7y6RqFUgBw8BBKD1w8giNHLkEeEBfweR31P0o/mHPAQAALzo"
    "3rBEaeqILcLvSPRADYDYHAEAYJoMzwbQXPHY78Vqfi8B2IMJAAj0AEDoInIzYxqAaL8Lkd8vsIL6"
    "C7YTAHCSjwAEOo8yR2j8WCNS4x/5PQLEpY7nFAEAAEtFbnCiNILME+HnrfEHYBTPAABgOc8GYLUo"
    "jT8AjGQCAIAwIjdApgFqivJzjfy7D0AdJgAACMU0ADNEaPoPNP4AzGQCADbyBFro2xhF2TVmmwg/"
    "O+f84cr3kE9igk1MAAAQlmkAKjb+ALCKCQAAwovcNJkGiC/Kzyjy7zEAPQgAeJTPDgWiiT4yHaHB"
    "JObPJfrvLlCTep7HOAIAQCqHRipCU/eY43Vp9taL8Dvi9wCAaAQAAKTj2QCcovEHgNMcAQAgrcg7"
    "rFHOnXcR5fWO/DsJAAIA2MBHz0Ac0c9XR2hKq4vwGkf/PYSK1GNwOUcAACjBswH6idL4A0AWJgAA"
    "KCN6MxahYa0gwri/HX8AMjIBAEApGR4QmCGsiCjKz9TPDoCsTADAIK9f/+S1hYWiN2lRmtksIrxe"
    "dv0ByM4EACwKAe7uPnvtYTDTAPlFafyBufWTOgnGEADwnT9++d2rEmBCwMIHPR4QeHC4Nk3m96/J"
    "an4mMI5JyXl1/av3t5O+GhkIAABowTRADhEa/wPNP1xHgw8xeQYAAK1Eb+yiNMBdv3fn/AGozAQA"
    "XOjNh7deM0jONEAsURp/IGdd9uXdp9WXAWkIAGCQ587wG42D9TwbYK0Ijf+B5h+ALgQAEDAgEA7A"
    "PBmmAao1qFFe62qvK2TiYcewhgAAArIownyRpwGO11WhYY3wGld4HSED9QzEIwAAgH8wDTCOxh96"
    "0fxDTD4FAAAS7RAfGukIzXS26438MwWAWUwAAMAjTANcJ0LTf6DxB4C/mAAAgKQNZJTd9YciXNPh"
    "5xb5ZwcAK5gAAIAG0wDnfE724fO0r72O1TT9AHCaAAAAin5SwDlN/zd/x70/f0kYEOU10fwDwNME"
    "AABQaRrgwqb/2jAgwuug8QeA87y8ubn9euafpYE/fvl96dc/Z8dpr+J2q2tHZIE6IjS/3/j3l9Pu"
    "fRG+d40/kKU2XH2Nr97fLv36xGECgOUubajv//nVN1OgtzDTAAMb/+/ut/+xft9A4w+spn4lKxMA"
    "LJsA2HMnfVYQYPcfOHkfWhUCTGj+v7MwBND8A1VqwZkbWSYAOPIxgCyxdyOtMQdafuzciuZ/0df1"
    "sX7AaupXKnAEgKlGNurHv9uxAKDFJwWsav7vf/0JkwB2/IHV1K9UYgKAaWbt0psGAFYbvlu9uvmf"
    "8dDBFRMVAA+oX6lGAEDJplwIAEQwpIGN0vwPvB6NPxCB+pWKBACUbcaFAEAEdrK9VkA+6leqEgAA"
    "wAS77GpH2/3f6bqEJAAwh4cAUnoX/vD1PRQQKPGAwB2a///879P/7l//Zf5DAY36AxGpX6nMBABl"
    "b57RrgNg1W73ofF/qvk/98/sSfMPRBSlboxyHdQjAACABWY1wJc29aNDAOP+ALCOAIAWqWW06wG4"
    "qBneOP6/tZnfHAI8cZ0afyC6aPVitOuhBs8AgAF+/vnX8K/rx4+/rb4EYI9nAwzayT/891c/F+Af"
    "jPtDTOoV6McEAAAEsOcO+V5j/Nf+PXb9ASAWAQBtxpWiXhfAfd+FAFE/+u+Uf3+p8QfSiVonRr0u"
    "8hIAAEAw1+yc7/0Qv5mfDAAAjCUAAICgnJ0HAPYkAAAAAIAGBAAAAADQgAAAAAAAGhAAAAC7+vLl"
    "v7yiABCQAAAA2J0QAADiEQAAQNAGeksT/a//su91XPP3bf0eAIAxBADs7su7TyFf1ajXBfBk0/wf"
    "X3O9QI9crxAAiC5qnRj1ushLAAAAAey5W77XFMCe0wSmAQBgvR9XXwBU9PHjb6svAUhkxA75oXn/"
    "z/++7r8f9b2+efO3MX85cBH1CvRjAoAW40rRrgfgol3xjccAtjbxm5v/M6/TNAAQUbR6Mdr1UIMA"
    "AAAmm9kAX9rMj9r5f4xnAwDAXAIAyqeWUa4DYNXO96Gpf66xP+fPjGAaAIgkSt0Y5TqoxzMAGH7z"
    "evPh7bJX2c0TiOLqxv8wXv/vL6/6K4Y2+Fd+WoFnAwBRqF+pzAQAAGTZ4Y76kYA7XZdpAAAYSwBA"
    "2V14u//ASprZ6147gJXUr1QlAKDkTVTzD5Rt/KNNAQy6HgEKsJr6lYoEAJS7iWr+gfI711FCgAnX"
    "YRoAWEn9SjUeAsiSm+iIBwNq/IFVljSpOzwU8OqvP/n1ffPmb9O+JsA/70HqVwoxAcASezfrmn9g"
    "heVj6qsmARZ9XdMAwErqVyp4eXNzG2SOkAj++OX36V/zmmmAFY3/yo81BGKI0oged8Sn3guDHD8w"
    "DQBkrQdXXO+r97fTvyYxOQLAcvdvgufcTO32A92b/4fN7/HeOfT+GKTxv/9zEAIAy+5B6leSMgFA"
    "iCmATEwAQE8RG//HDAkBgjX/DwkCoDebQ0+z+899JgAA4Mwmc2UIcG6Tez+kvKYo/ibs/LD2e3+O"
    "aQAAOI8AAACK7m5fGgY8NeH0z+cNBAwCTAAAwHkEAAAQcApg76Z2r+NLqychAIDtBAAAEEiG3exI"
    "0wAZXi8AiOKH1RcAAJmMbDizNbOrr3f11weAbEwAQECvX//04u7u8+rLACbJ3MhGmgYAAJ4mAICF"
    "TT6Q017n4DM3/qufDVDptYOKbGZATAIAGESDD7Vd0/BWbV5nTQNUff2gUy1k0hHWEAAAwEQdmlef"
    "FABcu1EiIIAxPAQQACY084c/26H5H/39dnoNAWBvAgC40Jd3n7xmwNm6Nf4P7fm9d34dgcepy+Ay"
    "jgDAIkbboPa4u2b1+9fCJwUAwFoCABhIkw89af5Pvy4enAg9PFcDeVgyrPHy5ub266KvTWB//PL7"
    "6ksI7c2Ht6svAQjm0Nhq/C97vc7ldYVeLvkIQUcAnvbq/e0uPxPq8AwAANiBJtXrBezDBCWMIwAA"
    "AMI+IFGwAgD7EQAAAEudavI1/wCwLwEAALBc949LBIAZBAAAQBjHEEAYAAD7EwDABp44CzCO5h84"
    "h3oMLicAAAAAgAYEAAAAANCAAAAAAAAaEADwqFfvb70yAACQlHqexwgAAAAAoAEBAAAAADQgAICN"
    "fPQMAMAa6jDYRgAAAAAADQgAAAAAoAEBAAAAADQgAAAAAIAGBACc5LNDAQAgH3U8pwgA4AqeQAsA"
    "MJf6C7YTAAAAAEADAgBI4vXrn1ZfAgAAkNiPqy8A+J5mHwDIVrvc3X1efRnAMwQAsJhmHwCoWtMI"
    "BSAWAQDs8CCaNx/eTmn2pesAQOdQwAMA4ToCAJ79CJE/fvndqwQAwC4bHCYFxvIRgDzFQwABAACg"
    "ARMAMNFh5O2SlNy5OQAAYC8CAAhCsw8AVKlhbHhATAIAmPwgwAPNPgBQ2bWhwGM8ABCuJwCAyTT/"
    "AEBHI0IB4DIeAsizPEkUAIARbIzsS93OcwQAAAAA0IAAAAAAABoQAMBOPJgGAGAMdRbsQwAAAAAA"
    "DQgAOIsHigAAQFzqdc4hAAAAAIAGBACwI+fTAAD2pb6C/QgAAAAAoAEBAAAAADQgAAAAAIAGBACc"
    "zZNFz+OcGgDAPtRV51Gncy4BAAAAADQgAAAAAIAGBAAAAADQgACAizhfdB7n1QAArqOeOo/6nEsI"
    "AAAAAKABAQAAAAA0IAAAAACABgQAkPzc2uvXP035OgAAszj/D2MIALiYB42sd2j6j/8DAJhVfxCL"
    "upxL/XjxfwGEW3QP/+7u7vPU6wEAetcjag/IRwAAg8fX3nx4e9XfIW0HAFZ7rB4ZFQYY/4dxBAAQ"
    "0Jam3xQAALC6djEVALEJANh83uiPX3736u3ITj8AkL1GcURgHuf/2UIAAMlJ2gGAiIQBEI8AAII8"
    "B+DQyJ+bsGv6AYBZ7tcdoycWnf+HsQQAkIjGHwDIFgaoXyCOH1ZfAHk5d7S/xxbIwz87/g8AIAr1"
    "yTrqcLYyAQABPw5Qsw8AVJgKuKSmMf4P4wkAIBjNPwCQ1cznBQCXcwQAAADYnU0NiEcAwFWcPzqf"
    "sTYAAHXStdTfXEMAAAAAAA0IAAAAAKABAQBM5BgAAID6CFYRAHA155AAAGA8dTfXEgAAAABAAwIA"
    "mMwxAAAAdRGsIABgF8aRAABgHPU2exAAAAAAQAMCAFjAMQAAoDv1EMwnAAAAAIAGBADsxrmky0i9"
    "AYCu1EGXUWezFwEAAAAANCAAAAAAgAYEAOzKeNJljL8BAN2ofy6jvmZPAgBo5PXrn1ZfAgAAsIgA"
    "AJo0/pp/AOCxGgHo4+XNze3X1RdBPX/88vvqS0jlzYe3Uxf0u7vPu389ACCf+/XCjPrA+P9ljP+z"
    "tx93/xuBpST5AMCWmmF2GADM5wgABLBHGn7JmL+QAADYq644l91/WM8EACSmkQcARtYQxz9nIgBq"
    "8AwAhvEcgHHPArim8beAAwCzawm7/5dz/p8RTABAA5p+AOCx2mBLEGAqAPISAEDSRfucBVvjDwCc"
    "Wys4Wgj1OQLAUI4BrDkGoPEHALbae5PB+P/ljP8zigkAKDIFoOkHAPaqMQ5MBEA9AgAI5pCSnzsF"
    "cKDxBwBmHg+w+w95/bD6AqjN+NJYGZv/n3/+dfUlAEAImdbEQ82Rse7ISP3MSJ4BwHCeA7DNJVMA"
    "GYucjx9/W3YtALBah3XR2f9tBACMZAIAGC7TDgcArGCtBGYwAcAUpgB6TgA8V8xU3O0AgOd0WR9N"
    "AFzO7j+jeQggFHkYYCR2MQDg+nU0cxCg+YeYTAAwjSmAy2ULALY0/pmLGwC4VJe1UgBwObv/zOAZ"
    "ABBYpsVz666/aQEAuuiyVmaqX6AbRwCAq2QrSgAgowrHAoD1HAFgKscA6hwF2LvxV9AAUFmXddPu"
    "/zbG/5nFBABwETv+ALCeiQBgC88AgASipOkjm3/BAgBVdVk/o9QrwGmOADCdYwD5jgGMLi6ijjEC"
    "wJ6qr6cCgG2M/zOTAIDpBAB5QoDqhQoArFBxfdX8bycAYCYBAEsIAWIHADPGCTX/AHRWba0VAGyj"
    "+Wc2AQBLCADihgAVdyUAIKoK667mfzsBALP5FACgTAECANkc18dR67BPCwDuMwHAMqYAYkwBaPwB"
    "II5s67Ld/+3s/rOCjwGExgVGtiIDAKobvXbOWP+BuEwAsJQpgDVTABp/AIgv+npt9387u/+s4hkA"
    "0Ej0QgIA+H5d9XwAYC8mAFjKBMCcKQCNPwDkF2k9t/t/HRMArOIZACzl5jfHyJ15u/4AMIf1vAb1"
    "Lys5AgCJHdL3PT8R4BIafwBYt/6ufJCf3X/IyxEAQnAUYLtLAoA9igWNPwDEsWJtFwBsZ/ef1UwA"
    "QHKzpgA0/gAQz+yJAM0/5OYZANDI1iZe8w8AsVnjgXM4AkAYjgHEOwqg8QeAfEat83b/r2P8nwgc"
    "AYAi9jwKoPEHgLxGHAvQ/EMNJgAIxRTA2ikAjT8A1LPHmi8AuI7df6LwDAAo5JrFWfMPADVdu8Zr"
    "/qEOEwCEYwpg7hSAxh8A+tiy9gsArmP3n0gEAIQjALjejI8FBADq0/xfTwBAJI4AAAAAQAMCAMKR"
    "kl5PWg8AqCfWU9cSjQAAihICAADqCOA+AQAhSUsBAMhMPUtEAgAozBQAAKB+AI4EAIQlNQUAICN1"
    "LFEJAKA4UwAAgLoBOBAAEJr0dB9CAABAvTCH+pXIBADAcK9f/+RVBgDrJbCYAIDwpKi5pwCOzb8Q"
    "AADirpemBfehbiU6AQA0MnNxPxQwmn4AiL+Gav6hDwEAKUhTczlVtAgEAMC6WZV6lQwEANDMyJT/"
    "nB0LIQAAnL8ujp4GsPsPvQgASEOqGnuxP7c4ubv7vPvXBoCszl0XR4QAmv/9qFPJ4sfVFwDkpvEH"
    "gH1CgHOn6ITpwFYmAEhFuhor9df8A0DOaQC7//tRn5KJCQBo7LD4v/nw9uL/TuMPAHmnATT/0JcJ"
    "ANKRsq6l+QeA2s8G4HzqUrIRAEBzl+4CPFeQHP69s4kAcL1z1tRL11y7/9CbAICUpK0xQwCNPwDs"
    "b691V/O/L/UoGXkGAHA1jT8AxHg2AMBTTACQltQ1xhSA5h8A5tm6/tr935c6lKwEAMCw5wEAAPvT"
    "/ANbCQBITfoKAID6E84jAAC+YUQQAOqwrgP3CQBIzxTA/hQLAJCf9Xx/6k6yEwAAj1I0AEBe1nHg"
    "MQIASpDGAgCg3oSnCQAoQwiwP7sHAJCP9Xt/6kyqEAAAT1JEAEAe1m3gKQIASpHOjqGYAID4rNdj"
    "qC+pRAAApPH69U+rLwEAANISAFCOlLbmrsKx+RcCABBNhLVp9TpdlbqSagQAQPji4mFhFaHQAoAo"
    "AbXmHziXAICSpLV1ioxTBZUQAIDVIgTUmv9x1JNUJAAAwnqqkLq7+zz1WgDgPgE1kJEAgLKktrl3"
    "GzT/AET2VBA9axLA7v846kiqenlzc/t19UXASH/88rsXeJA3H97u/nc+VzTZ+QcgklWBteZ/HM0/"
    "lZkAAMIUH5p/AKpNAoyYBtD8A1uZAKAFUwDxJwGM/AOQ2awQW/M/lt1/qjMBACyn+Qcgu0ODH+G5"
    "AABPEQDQgjR3rGt2IzT/AFQyMgSw+z+WepEOBAC04aY+1tai5FSh5GF/AGQ1IgTQ/I+lTqQLAQAQ"
    "LgTQ/AOQ3Z4Bt+Yf2IsAgFaku/FDAM0/AFXsEXBr/sdTH9KJTwGgJZ8KkOOTAQCggsPYv+Y/Js0/"
    "3ZgAAACAgUy3AVEIAGhJ2juekUUAsI5Gph6kIwEAMIwQAACsn0AcAgDakvrOIQQAAOtmNOpAuhIA"
    "0Jqb/xxCAACwXkah/qMzAQAwhRAAAKyTwFoCANqTAvcOAQ4fzQQAK0VcH6tS99GdAAAsBm2LnGPz"
    "LwQA6CPaPT/Sulid5h8EAEDTYudhARitIASgfvAbYT0EejEBAP8gFe5T9Jwq/KIUhADUD341/3Op"
    "8+BPAgC4x+JQv/h5quC7u/s89VoA6Bn8av7nUt/BXwQAwFIziyDNP0BPTwW8s0MAzT+wkgAAHpAS"
    "92PnH6C+SCEA86jr4FsCAHiExeJFud2QU8Wd5h+gj9X3fLv/c6nn4HsCACCEkUWR5h+A50KA0VMA"
    "mn8gAgEAnCA1nm9EcWSsE4DVIYDmfz51HDxOAABPsHjMt2eR5KF/AOy5dmyh+Z9P/QanCQCAcPYo"
    "ljT/AKx+KKDmH4hGAADPkCKvcW3RdKqwW/0AqBV+/vnX1ZcAJNHtfjEyBND8r6Fug6e9vLm5/frM"
    "nwFevHjxxy+/ex0WePPh7VX//f0CTvP/4sXHj7/t8FMBqjf+3e4VjzX716wZmv81NP/wPBMAcCaL"
    "Su5JgI7N/2O67e4Bz3Nf+H6N0Pzno06D85gAgAuYAsg9DdDNc0V9tx0+4FvuEY9PAmxt/u36ryUA"
    "gPMIAOBCnUKAcxru2QWPEGD/XT1BAPTi3rC/mWthxLV5Nc0/nE8AABtUDgGuabBnFRxCgP1HeoUA"
    "0IN7w/5mrH0Z1uZVNP9wGQEAbFQtBNizqY5eDEUfI115plcQADW5J4wxer3LtjbPpvmHy3kIILB7"
    "Mz2jOY9cyByfJr3X50hfSqEP7BXurXpA4Kr7Z9Xmf8TfB+RkAgAaTwFUaNQjFjR7f5zUrGLd7j/U"
    "luX+kOHjW0eubRXW5hns/sM2JgCg6eIzq3Ee/XWiFTGndq2i72Zp/qG+6O/zw30y+r2yQvM/8+uM"
    "krn+gtUEANBwEZq98HcJAZ4qXGfsYvksbyDr/SVLeFqh+V/19TrXXRCJAACaWbXgdwkBMoq+KwjU"
    "f78/FZJGCQEqNf+rvy6wjgAAdiCNjmFlCGD3H6iu85SRkDkG9RZcTwAAjRal1Ul/1QcbrW7+K+4G"
    "Av3e91GnAKo/zHb1169UZ0EGPgUAmnwyQKQFflaTPuN7fq4ojXz2P2oTAMwR9d4RJVSdsVZ1XJu3"
    "0PzDfkwAAGWtLmYiN/8AGe87syYBVq8fAKMIAKBBSh1ph2H29Yws4qLsUm1h9x+Ieh9Yff+sNKWW"
    "+Xoi11WQmQAABrBYxTKimIvQ/Nv9B1YZff9Z9TwAO/+xqKdgfwIAGMSiFYuiLv6uHzBf5PvB7BDA"
    "OhGLOgrGEABA8cUr6kjfius6FHd7FHh2/wHqTCHttTZcwtocv36CqgQAQDvXFnqndqVWn1vNvtsH"
    "rNF5CsCuP9CNAAAGk2LXDQFWNfxRP7oLyGvr/WHGFMCo0FXzH5O6CcYSAMAEFrOY9ij+jgWoB/8B"
    "Xc0+CrBHAKv5j0m9BOMJAGASi1rds59G/4EKIk8J7RW2rjjvz3nUSTCHAAAmsrjFlaEgrPLALaCe"
    "lUcBKt3nu1IfwTwCAJjMIhdX1eIw8q4eEEvV+0XV+3sF6iKYSwAAkGA81O4/EF3E+1TUezrAKgIA"
    "WEDaHV+VgrHqbh4wTpX7RpX7eGXqIZhPAADFF72oBVDU64p4jT72D5gt8scCZrp/Z7u+mdel+Yc1"
    "BACwkMUvvtXjo1GKaYAM963V92zOo/6BdQQAsJhFMIdsBWWVEV5gnWz3kWz36a7UPbCWAAAaLIbR"
    "iqJo1xP1uu3+A1nNvn9lXFeiXfOM69H8w3oCAAjCophDhvHSbLt2QFzR7ycZ7sn8SZ0DMQgAoIko"
    "BVKU64j+fdj9B7IbfR+rsJ5E+R6iXAcwngAAAql+FGD11++w8xR9tw7IJ9p9JeK99xqrvxej/9CL"
    "AACCMSKXz97Fk4/9A6KJ8rGAq5tlLqeugVhe3tzcfl19EcD3/vjl92Evy5sPb6e/5F2Ktj1f20sL"
    "52i7dEAtK+9JHdaQimuz5h/iMQEAQY1cNGcXUh0KtxHf6yXF88jm//Xrn4b93UCe9+uqe1KXNaTa"
    "2qz5h5hMAEBw2ScBuhRuq6cBZgUAd3efh30dxtgygm2aJJ9Z79OZ96Ku60eFtVnzD3EJAKB5CDCq"
    "2OhauI1+bR8rvlft/gsDchAA1LXq/TnjPmQNybs2a/4hNkcAIIFsnw6gcPv2tVh1LABghr13/a0h"
    "f70We9L8AwcmACCR0ZMA1+44KNrGvbanduHs/nPO78mlBE15rJwCsOs/T4a12c4/5CAAgGRmhACX"
    "FBya/jGvawTG/2sQANRW4X1qHcm/Nmv+IQ8BACQ0MwSgZwhQoangTwKA+jK/XzX/+Wn+IZcfV18A"
    "sG2xFQLkdix6owcBACNo/GvQ/EM+HgIISVl0a8j2wKvou4nQUab3ZbZ7HqepQyAnAQAkZvGtI1JB"
    "/NQ4MZBLpPdzpPsc11F/QF6OAEByjgPU4VgAUJHGvxbNP+RmAgAKsBjXsnJENsLDxCLtWEKW3+en"
    "3p+r3lPG/etRb0B+JgCgCJMA9XSeCDg2LJnONsN9nYMsO/41af6hBhMAUIjFuaZZxXTE3f/D/z/+"
    "D6I79fvaaQpA81+T+gLqMAEAxZgEqKnzNAAQn8a/Ls0/1CIAgIKEAHWNDALu7x7e3y2MMIYf4Rrg"
    "nN/T1dMqD69h9HtH41+b5h/qEQBAUUKA2kZPBBybhpnNzOrGCUb/fs8MsjT+XEvzDzUJAKAwIUB9"
    "s4IAII+R71s7/j1o/qEuDwGE4iziPVT+uK0ZIYTpA/ZSNTSrfI/hW+oGqM0EADRgEqCPrA8LjNCA"
    "P3YNVZu5rmaP4Uf7+lto+nvR/EN9AgBoQgjQS9Yg4KFszRJxrAyVIjwM8Foa/340/9CDIwDQiMW9"
    "nwxju6sbpdVfn16i/75luGewP/UB9CEAgGYs8j0p6i9n+qCm6A34Ku4RfakLoBcBADRkse8rU5Gv"
    "ASfz78/qr1/xnsD+1APQj2cAQFOeCdBblGcEdN6NPfW9Z2kcL9Hpe83yMEBNP5p/6EkAAI0JAbjf"
    "BKwOA4CxNP0caf6hLwEANCcEYOVUwP1d0Pu7xLN2RztPIDD/0wBW7fpr/LlP8w+9CQAAIQAhjgcc"
    "m6MITfnq8WxqjeBr/IlC8w8IAIBvioI/fvndK8LS4wEdmu9uZ+If7oTPasRPfd2ZZv9M7fbzGI0/"
    "cCQAAL7hSACRHxoIPE7jzymaf+A+AQDwHSEApwgCIBaNP0/R/AMPCQCARwkBqP7pAatHw2ErTT/n"
    "0PwDjxEAACcJAegSBnQ4h8/aBwFeS9PPJTT/wCk/nPw3AIoINjQpGhUiydTkP8Z7iktp/oGnmAAA"
    "nuUTAqg4FfBYY+hYABEI0dhC4w+cQwAAnM2RAKqGAVV2i8n7s9X0cw3NP3Culzc3t1/P/tMAL168"
    "+OOX370OXC16GDDKqSmDUQ3qzz//evF/8/HjbyW+9+g0/exB8w9cwgQAcDGTAHSbDIC9aPrZk+Yf"
    "uJQAANhECMCehAFUpulnBM0/sIUAANjMwwGZ0SyZDiAbDT8jafyBawgAgKuZBmCkatMBXc+7V//e"
    "Nf3MoPkHriUAAHYhBGAG0wFEoeFnNs0/sAefAgDsyicEsFKFCQFi0vCzkuYf2IsAABhCEEAEAgG2"
    "0vATgcYf2JsAABhGCEA0AgFO0fATjeYfGEEAAAwlBCA6oUA/mn2i0/wDowgAgCkEAWQiFKhDs08m"
    "Gn9gNAEAMI0QgMyEAvFp9slM8w/MIAAAphICUI1gYD6NPtVo/oFZBADAEoIAOhAObKfJpwONPzCb"
    "AABYRggAPUMCzT1o/oE1BADAUkIAyB0aaObhcnb+gVUEAEAIggAAqtP4A6v9sPoCAA4URQBUZp0D"
    "IhAAAGEojgCoyPoGROEIABCSIwEAZKfxB6IxAQCEpGgCIDPrGBCRCQAgPNMAAGSh8QciMwEAhKeY"
    "AiAD6xUQnQkAIBXTAABEo/EHsjABAKSiyAIgEusSkIkJACAt0wAArKLxBzIyAQCkpfgCwPoDcD4T"
    "AEAJpgEAGE3wDGRnAgAoQVEGgHUG4GkmAIByTAMAsBcBM1CJAAAoSxAAwFYaf6AiRwCAshRvAFg/"
    "AP5iAgBowTQA3b358PbZP/Pl3acp1wJRCY6B6gQAQBtCALo5p+k/RRhAN5p/oAMBANCOIIDqrmn8"
    "HxIEUJ3GH+hEAAC0JQigoj2b/yMhABVp/IGOBABAa0IAqhjR+D8kCKAKzT/QlQAAQBBAcjOa/yMh"
    "AJlp/IHuBAAA95gIIJuZzf+REIBsNP4AfxIAADxCEEAGK5r/IyEAGWj8Ab7144P/D8C9olEQAJCP"
    "xh/gcT+c+OcAKCIJbOXuf4SvD6do/gFOcwQA4EymAYgiUvPtKABRaPwBnucIAMCZHAsAiEfjD3A+"
    "EwAAG5kIoPvu/5EpAFbQ+ANczgQAwEYmAgDm0/gDbCcAALiSIABgPI0/wPUcAQDYmaMBdBr/P3IM"
    "gFE0/gD7MQEAsDMTAQD73UsB2I8AAGAQQQDA9nsnAPsTAAAMJggAOP9eCcA4AgCASQQBAKfvjQCM"
    "JwAAmEwQAKDxB1hBAACwiCAA6MiOP8A6AgCAxQQBQAcaf4D1BAAAAYvjP375fem1AOxB0w8Qy8ub"
    "m9uvqy8CgMcJAnjozYe34V6UL+8+rb4EgtH4A8RkAgAgMMcDgEw0/gCxCQAAEnA8AIhK0w+QhyMA"
    "AEk5HtBXpGMAxv/70vgD5GMCACApUwHAyvsOAPmYAAAoxFRAHxGmAOz+96HxB6hBAABQlDCgvpUh"
    "gOa/Pk0/QD2OAAAU5RMEgGvuHQDUYwIAoBFTAfWsmAKw+1+Pph+gBwEAQFPCgDpmhgCa/zo0/QD9"
    "CAAAmhME1DAjBND816DxB+hLAADAPwkD8hsRBGj889P0A3AgAADgUcKAvPYMATT/eWn6AXhIAADA"
    "s4QB/YIAjX9Omn4AniIAAOBiAoGaYYCmPx8NPwCXEAAAcBVhAMyl6QdgKwEAALsRBsAYmn4A9iAA"
    "AGAYgQBso+EHYAQBAABTCAPgaZp+AEYTAACwhECA7jT8AMwmAAAgBIEA1Wn4AVhNAABASAIBstPw"
    "AxCNAACAFAQCRKfhByA6AQAAaQkFWEWzD0BGAgAAyhAIMIqGH4AKBAAAlCcY4FwafQAqEwAA0JJQ"
    "AM0+AN0IAADgHsFAPRp9APiTAAAAziQciEuTDwDPEwAAwE4EBONo8AHgegIAAJhMUPAXjT0AzCMA"
    "AIAkIgcHGnkAiE8AAAAAAA38sPoCAAAAgPEEAAAAANCAAAAAAAAaEAAAAABAAwIAAAAAaEAAAAAA"
    "AA0IAAAAAKABAQAAAAA0IAAAAACABgQAAAAA0IAAAAAAABoQAAAAAEADAgAAAABoQAAAAAAADQgA"
    "AAAAoAEBAAAAADQgAAAAAIAGBAAAAADQgAAAAAAAGhAAAAAAQAMCAAAAAGhAAAAAAAANCAAAAACg"
    "AQEAAAAANCAAAAAAgAYEAAAAANCAAAAAAAAaEAAAAABAAwIAAAAAaEAAAAAAAA0IAAAAAKABAQAA"
    "AAA0IAAAAACABgQAAAAA0IAAAAAAABoQAAAAAEADAgAAAABoQAAAAAAADQgAAAAAoAEBAAAAADQg"
    "AAAAAIAGBAAAAADQgAAAAAAAGhAAAAAAQAMCAAAAAGhAAAAAAAANCAAAAACgAQEAAAAANCAAAAAA"
    "gAYEAAAAANCAAAAAAAAaEAAAAABAAwIAAAAAaEAAAAAAAA0IAAAAAKABAQAAAAA0IAAAAACABgQA"
    "AAAA0IAAAAAAABoQAAAAAEADAgAAAABoQAAAAAAADQgAAAAAoAEBAAAAADQgAAAAAIAGBAAAAADQ"
    "gAAAAAAAGhAAAAAAQAMCAAAAAGhAAAAAAAANCAAAAACgAQEAAAAANCAAAAAAgAYEAAAAANCAAAAA"
    "AAAaEAAAAABAAwIAAAAAaEAAAAAAAA0IAAAAAKABAQAAAAA0IAAAAACABgQAAAAA0IAAAAAAABoQ"
    "AAAAAEADAgAAAABoQAAAAAAADQgAAAAAoAEBAAAAADQgAAAAAIAGBAAAAADQgAAAAAAAGhAAAAAA"
    "QAMCAAAAAGhAAAAAAAANCAAAAACgAQEAAAAANCAAAAAAgAYEAAAAANCAAAAAAAAaEAAAAABAAwIA"
    "AAAAaEAAAAAAAA0IAAAAAKABAQAAAAA0IAAAAACABgQAAAAA0IAAAAAAABoQAAAAAEADAgAAAABo"
    "QAAAAAAADQgAAAAAoAEBAAAAADQgAAAAAIAGBAAAAADQgAAAAAAAGhAAAAAAQAMCAAAAAGhAAAAA"
    "AAANCAAAAACgAQEAAAAANCAAAAAAgAYEAAAAANCAAAAAAAAaEAAAAABAAwIAAAAAaEAAAAAAAA0I"
    "AAAAAKABAQAAAAA0IAAAAACABgQAAAAA8KK+/w/UZfH9Qwr1mAAAAABJRU5ErkJggg=="
)

# ---------------------------------------------------------------------------
# Theme  (matches Marker Madness suite exactly)
# ---------------------------------------------------------------------------

BG       = "#2d2d2d"
PANEL    = "#333333"
PANEL2   = "#2e2e2e"
TEXT     = "#E2E2E2"
ACCENT   = "#ffa500"
BTN      = "#404040"
BTN_HOV  = "#505050"
ENTRY_BG = "#1e1e1e"
TITLE_BG = "#1a1a1a"
DIM      = "#909090"
GREEN    = "#6DBF87"
RED      = "#E05C5C"
SEP      = "#3a3a3a"

F_MAIN   = ("Avenir Next", 12)
F_BOLD   = ("Avenir Next", 13, "bold")
F_SMALL  = ("Avenir Next", 10)
F_TITLE  = ("Avenir Next", 18, "bold")
F_STATUS = ("Avenir Next", 10, "italic")
F_HDR    = ("Avenir Next", 10, "bold")
F_HUGE   = ("Avenir Next", 38, "bold")
F_MED    = ("Avenir Next", 26, "bold")

# Segment bar colours — varied palette for easy differentiation
SEG_COLORS = [
    "#3A6BC0",  # blue
    "#2E9E7A",  # teal
    "#B87020",  # amber
    "#7A3AB0",  # purple
    "#B84040",  # muted red
    "#2A8E50",  # green
    "#C05A28",  # burnt orange
    "#3A8EC0",  # sky blue
    "#8050C0",  # lavender
    "#5A9E30",  # lime
]

# Extended palette shown in the right-click colour picker (4 cols × 5 rows)
ALL_SEG_COLORS = SEG_COLORS + [
    "#C03878",  # raspberry
    "#20A0B0",  # cyan
    "#906838",  # warm brown
    "#607898",  # slate
    "#788820",  # olive
    "#C06880",  # rose
    "#909090",  # silver / gray
    "#505060",  # dark slate
    "#C8A030",  # gold
    "#486080",  # steel blue
]

# ---------------------------------------------------------------------------
# FPS definitions
# ---------------------------------------------------------------------------

FPS_KEYS = [
    "23.98 ndf", "24 fps", "25 fps",
    "29.97 df",  "29.97 ndf", "30 fps",
    "48 fps",    "50 fps",
    "59.94 df",  "59.94 ndf", "60 fps",
]

# key → (numerator, denominator, is_drop_frame)
_FPS_TABLE = {
    "23.98 ndf": (24000, 1001, False),
    "24 fps":    (24,    1,    False),
    "25 fps":    (25,    1,    False),
    "29.97 df":  (30000, 1001, True),
    "29.97 ndf": (30000, 1001, False),
    "30 fps":    (30,    1,    False),
    "48 fps":    (48,    1,    False),
    "50 fps":    (50,    1,    False),
    "59.94 df":  (60000, 1001, True),
    "59.94 ndf": (60000, 1001, False),
    "60 fps":    (60,    1,    False),
}

def fps_info(key):
    """Return (numerator, denominator, is_drop, nominal_int_fps)."""
    num, den, drop = _FPS_TABLE.get(key, (24, 1, False))
    return num, den, drop, round(num / den)

# ---------------------------------------------------------------------------
# Timecode helpers
# ---------------------------------------------------------------------------

def _to_hmsf_ndf(frames, nom):
    fr = frames % nom
    ts = frames // nom
    s  = ts % 60
    tm = ts // 60
    return tm // 60, tm % 60, s, fr


def _to_hmsf_df(frames, nom):
    drop  = 2 if nom == 30 else 4
    fp10m = nom * 600 - drop * 9   # frames per 10 minutes
    fpm   = nom * 60  - drop        # frames per non-drop minute

    d   = frames // fp10m
    rem = frames % fp10m

    if rem < nom * 60:
        m_extra = 0
    else:
        rem    -= nom * 60
        m_extra = rem // fpm + 1
        rem    %= fpm

    total_m = d * 10 + m_extra
    h = total_m // 60
    m = total_m % 60
    s = rem // nom
    fr = rem % nom
    return h, m, s, fr


def _from_hmsf_ndf(h, m, s, fr, nom):
    return (h * 3600 + m * 60 + s) * nom + fr


def _from_hmsf_df(h, m, s, fr, nom):
    drop = 2 if nom == 30 else 4
    tm   = 60 * h + m
    return nom * 3600 * h + nom * 60 * m + nom * s + fr - drop * (tm - tm // 10)


def frames_to_tc(frames, fps_key):
    """Return display string like  1:23:55:00  or  9:02:00  (colons throughout)."""
    _, _, drop, nom = fps_info(fps_key)
    neg = frames < 0
    if neg:
        frames = -frames
    if drop:
        h, m, s, fr = _to_hmsf_df(frames, nom)
    else:
        h, m, s, fr = _to_hmsf_ndf(frames, nom)
    if h > 0:
        tc = f"{h}:{m:02d}:{s:02d}:{fr:02d}"
    else:
        tc = f"{m}:{s:02d}:{fr:02d}"
    return f"-{tc}" if neg else tc


def parse_tc(s, fps_key, compact=True):
    """Parse TC string (H:MM:SS.FF, H:MM:SS:FF, MM:SS.FF …) or raw integer frames.
    Returns frame count (int) or None on failure.
    When compact=True (default), pure digit strings of 3+ digits are treated as
    compact timecode padded to 8 digits: HHMMSSFF (e.g. '215518' → 21:55:18).
    Pass compact=False in frames-entry mode to treat digits as raw frame counts."""
    s = s.strip()
    if not s:
        return None
    if s.lstrip("-").isdigit():
        v = int(s)
        if v < 0:
            return None
        if compact and len(s) >= 3:
            # Compact TC: pad to 8 digits left, parse as HHMMSSFF
            padded = s.zfill(8)
            h  = int(padded[0:2])
            m  = int(padded[2:4])
            sc = int(padded[4:6])
            fr = int(padded[6:8])
            _, _, drop, nom = fps_info(fps_key)
            if drop:
                return _from_hmsf_df(h, m, sc, fr, nom)
            return _from_hmsf_ndf(h, m, sc, fr, nom)
        return v
    _, _, drop, nom = fps_info(fps_key)
    # Normalise separators to colon
    norm = s.replace(";", ":").replace(".", ":")
    parts = norm.split(":")
    try:
        parts = [int(p) for p in parts]
    except ValueError:
        return None
    if len(parts) == 4:
        h, m, sc, fr = parts
    elif len(parts) == 3:
        h, m, sc, fr = 0, parts[0], parts[1], parts[2]
    elif len(parts) == 2:
        h, m, sc, fr = 0, 0, parts[0], parts[1]
    elif len(parts) == 1:
        return parts[0]
    else:
        return None
    if drop:
        return _from_hmsf_df(h, m, sc, fr, nom)
    return _from_hmsf_ndf(h, m, sc, fr, nom)

def frames_to_ff(frames, film_format="35mm"):
    """Convert frames to feet+frames.
    35mm 4-perf: 16 frames/foot  ·  16mm: 40 frames/foot.
    Display format: 1978+14"""
    fpf  = 40 if film_format == "16mm" else 16
    feet = frames // fpf
    fr   = frames % fpf
    return f"{feet}+{fr:02d}"


def parse_ff(s, film_format="35mm"):
    """Parse a feet+frames string like '1234+08' → frame count.
    Falls back to raw integer if no '+' present. Returns None on failure."""
    s   = s.strip()
    fpf = 40 if film_format == "16mm" else 16
    if "+" in s:
        parts = s.split("+", 1)
        try:
            feet = int(parts[0].strip())
            fr   = int(parts[1].strip())
            if feet >= 0 and 0 <= fr < fpf:
                return feet * fpf + fr
        except ValueError:
            pass
        return None
    try:
        v = int(s)
        return v if v >= 0 else None
    except ValueError:
        return None

# ---------------------------------------------------------------------------
# Project data
# ---------------------------------------------------------------------------

def _data_path():
    if getattr(sys, "frozen", False):
        # Running inside a PyInstaller bundle — write data to user's App Support
        base = os.path.join(
            os.path.expanduser("~"), "Library", "Application Support", "Reel Time Plus"
        )
        os.makedirs(base, exist_ok=True)
    else:
        try:
            base = os.path.dirname(os.path.abspath(__file__))
        except NameError:
            base = os.path.expanduser("~")
    return os.path.join(base, "reel_time_plus_projects.json")


def load_data():
    path = _data_path()
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"projects": []}


def save_data(data):
    with open(_data_path(), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def new_project(name, fps_key, goal_frames, seg_label,
                break_type, break_frames,
                leader_mode, leader_head, leader_tail,
                film_format="digital"):
    return {
        "id":                str(uuid.uuid4()),
        "name":              name,
        "fps_key":           fps_key,
        "goal_frames":       goal_frames,
        "segment_label":     seg_label,        # "Act" or "Reel"
        "film_format":       film_format,      # "digital" | "35mm" | "16mm"
        "break_type":        break_type,       # "tv_breaks" | "film_leader" | "no_breaks"
        "break_frames":      break_frames,
        "leader_mode":       leader_mode,      # "whole_show" | "per_segment"
        "leader_head_frames": leader_head,
        "leader_tail_frames": leader_tail,
        "segments":          [],
    }


def calc_totals(proj):
    """Return (content_frames, total_frames_with_breaks)."""
    segs          = proj.get("segments", [])
    content       = sum(s.get("frames", 0) for s in segs)
    n             = len(segs)
    bt            = proj.get("break_type", "no_breaks")

    if bt == "tv_breaks" and n > 1:
        total = content + (n - 1) * proj.get("break_frames", 0)
    elif bt == "film_leader":
        h = proj.get("leader_head_frames", 0)
        t = proj.get("leader_tail_frames", 0)
        if proj.get("leader_mode", "whole_show") == "per_segment":
            total = content + n * (h + t)
        else:
            total = content + h + t
    else:
        total = content
    return content, total

# ---------------------------------------------------------------------------
# UI helpers
# ---------------------------------------------------------------------------

def _hover_color(hex_color, factor=0.18):
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)
    r = min(255, int(r + (255 - r) * factor))
    g = min(255, int(g + (255 - g) * factor))
    b = min(255, int(b + (255 - b) * factor))
    return f"#{r:02x}{g:02x}{b:02x}"


class TBtn(tk.Label):
    """Button built on tk.Label so Windows never applies its native press styling."""
    def __init__(self, parent, bg=BTN, fg=TEXT, padx=12, pady=6, font=F_MAIN,
                 command=None, **kw):
        # Strip Button-only kwargs that Label doesn't accept
        for _k in ("activebackground", "activeforeground", "overrelief",
                   "relief", "bd", "state"):
            kw.pop(_k, None)
        hov = _hover_color(bg)
        super().__init__(parent, bg=bg, fg=fg,
                         padx=padx, pady=pady, cursor="hand2", font=font, **kw)
        self._bg  = bg
        self._hov = hov
        self._cmd = command
        self.bind("<Enter>",          lambda _e: self.config(bg=hov))
        self.bind("<Leave>",          lambda _e: self.config(bg=bg))
        self.bind("<ButtonPress-1>",  lambda _e: self.config(bg=hov))
        self.bind("<ButtonRelease-1>", self._on_release)

    def _on_release(self, event):
        self.config(bg=self._hov)
        # Only fire if pointer is still inside the widget
        if (0 <= event.x <= self.winfo_width() and
                0 <= event.y <= self.winfo_height()):
            if self._cmd:
                self._cmd()
        self.after(80, lambda: self.config(bg=self._bg))


class ScrollFrame(tk.Frame):
    """Vertically-scrollable container. Use .inner for child widgets."""
    def __init__(self, parent, bg=BG, **kw):
        super().__init__(parent, bg=bg, **kw)
        self._canvas = tk.Canvas(self, bg=bg, highlightthickness=0, bd=0)
        vsb = tk.Scrollbar(self, orient="vertical", command=self._canvas.yview)
        self._canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self._canvas.pack(side="left", fill="both", expand=True)
        self.inner = tk.Frame(self._canvas, bg=bg)
        self._win  = self._canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.inner.bind("<Configure>", self._on_inner)
        self._canvas.bind("<Configure>", self._on_canvas)
        for seq in ("<MouseWheel>", "<Button-4>", "<Button-5>"):
            self._canvas.bind_all(seq, self._scroll)

    def _on_inner(self, _):
        self._canvas.configure(scrollregion=self._canvas.bbox("all"))

    def _on_canvas(self, e):
        self._canvas.itemconfig(self._win, width=e.width)

    def _scroll(self, e):
        if e.num == 4:
            self._canvas.yview_scroll(-3, "units")
        elif e.num == 5:
            self._canvas.yview_scroll(3, "units")
        else:
            d = e.delta
            if abs(d) >= 120:
                # Windows / some setups: ±120 per notch
                amt = int(-d / 120) * 3
            else:
                # macOS trackpad / mouse: small raw delta
                amt = -d * 3
            if amt == 0:
                amt = -1 if d > 0 else 1
            self._canvas.yview_scroll(amt, "units")


def _sep(parent, bg=SEP, height=1, padx=0):
    tk.Frame(parent, bg=bg, height=height).pack(fill="x", padx=padx)


def _section_label(parent, text):
    _sep(parent)
    tk.Label(parent, text=text, fg=DIM, bg=BG,
             font=F_HDR).pack(fill="x", padx=16, pady=(14, 4))
    _sep(parent)


def _dark_entry(parent, var, width=24, state="normal", large=False):
    font = ("Avenir Next", 16, "bold") if large else F_MAIN
    e = tk.Entry(parent, textvariable=var, bg=ENTRY_BG, fg=TEXT,
                 insertbackground=TEXT, relief="flat", font=font,
                 highlightthickness=1, highlightbackground="#444444",
                 highlightcolor=ACCENT, width=width, state=state)
    e.pack(side="left")
    return e


def _toggle_lbl(parent, text, active, command, font=F_MAIN, padx=14, pady=5):
    """Toggle button using tk.Label — respects custom colours reliably on macOS."""
    bg  = ACCENT if active else BTN
    fg  = "#111111" if active else TEXT
    hov = _hover_color(bg)
    lbl = tk.Label(parent, text=text, font=font, bg=bg, fg=fg,
                   padx=padx, pady=pady, cursor="hand2")
    lbl.pack(side="left", padx=(0, 4))
    lbl.bind("<Button-1>", lambda _: command())
    lbl.bind("<Enter>",    lambda _: lbl.config(bg=hov))
    lbl.bind("<Leave>",    lambda _: lbl.config(bg=bg))
    return lbl


def _retoggle(widget_dict, active_key):
    """Update a dict of {key: label_widget} to reflect the new active key."""
    for k, lbl in widget_dict.items():
        bg = ACCENT if k == active_key else BTN
        fg = "#111111" if k == active_key else TEXT
        lbl.config(bg=bg, fg=fg)
        lbl.bind("<Enter>", lambda e, b=bg, l=lbl: l.config(bg=_hover_color(b)))
        lbl.bind("<Leave>", lambda e, b=bg, l=lbl: l.config(bg=b))


def _field_row(parent, label_text):
    """Return (row_frame, inner_frame) for a labelled settings row."""
    row   = tk.Frame(parent, bg=PANEL)
    row.pack(fill="x")
    _sep(row)
    inner = tk.Frame(row, bg=PANEL)
    inner.pack(fill="x", padx=16, pady=10)
    tk.Label(inner, text=label_text, fg=DIM, bg=PANEL,
             font=F_SMALL, width=14, anchor="w").pack(side="left")
    return row, inner

# ---------------------------------------------------------------------------
# Main application
# ---------------------------------------------------------------------------

class ReelTimePlus:

    def __init__(self, root):
        self.root = root
        self.root.withdraw()
        self.root.title("Reel Time Plus")
        self.root.configure(bg=BG)
        self.root.createcommand('::tk::mac::ShowHelp',
            lambda: webbrowser.open("https://resolve-tools.com/reel-time-plus-guide"))
        self.root.resizable(True, True)
        self.root.minsize(480, 520)
        w, h = 560, 740

        self._data             = load_data()

        # Always open centred on the display containing the cursor.
        # Restore saved window SIZE if available; ignore saved position so the
        # window always follows the cursor across displays.
        _cx = self.root.winfo_pointerx()
        _cy = self.root.winfo_pointery()
        saved_geom = self._data.get("window_geom")
        if saved_geom:
            try:
                self.root.geometry(saved_geom)
                self.root.update_idletasks()
                _sw = self.root.winfo_width()
                _sh = self.root.winfo_height()
                if _sw > 0 and _sh > 0:
                    w, h = _sw, _sh
            except Exception:
                pass
        self.root.geometry(f"{w}x{h}+{_cx - w // 2}+{_cy - h // 2}")

        # Save geometry after user resizes (debounced 600ms)
        self._geom_save_id = None
        def _on_configure(e):
            if e.widget is not self.root:
                return
            if self._geom_save_id:
                self.root.after_cancel(self._geom_save_id)
            self._geom_save_id = self.root.after(600, self._save_window_geom)
        self.root.bind("<Configure>", _on_configure)
        self._stay_on_top          = tk.BooleanVar(value=True)
        self._open_to_projects     = tk.BooleanVar(
            value=self._data.get("open_to_projects", False))
        self._quick_entry_to_name  = tk.BooleanVar(value=False)
        self._last_sized    = {}   # project_id → n segments when window was last auto-sized
        self._view_mode     = {}   # project_id → "tc" | "ff" | "frames"
        self._ff_overrides  = set()  # {(project_id, idx)} right-click spot-check overrides
        self._runtime_mode  = {}   # project_id → "total" | "content"
        self._last_tc_click    = None # (project_id, idx) of most recent TC click
        self._auto_open_edit   = None # key to auto-open after a page rebuild
        self._seg_sf           = None  # current segment ScrollFrame
        self._style_comboboxes()
        self._build_title_bar()

        self._content = tk.Frame(self.root, bg=BG)
        self._content.pack(fill="both", expand=True)

        last_id = self._data.get("last_project_id")
        if (not self._open_to_projects.get()
                and last_id
                and any(p["id"] == last_id for p in self._data.get("projects", []))):
            self._show_project_detail(last_id)
        else:
            self._show_projects_view()
        self._apply_topmost()
        self.root.after(120, lambda: (self.root.deiconify(), self.root.lift()))

    # ── combobox dark style ────────────────────────────────────────────────

    def _style_comboboxes(self):
        try:
            s = ttk.Style()
            s.theme_use("default")
            s.configure("Dark.TCombobox",
                        fieldbackground=ENTRY_BG, background=BTN,
                        foreground=TEXT, arrowcolor=TEXT,
                        selectbackground=BTN_HOV, selectforeground=TEXT)
            s.map("Dark.TCombobox",
                  fieldbackground=[("readonly", ENTRY_BG)],
                  foreground=[("readonly", TEXT)],
                  background=[("readonly", BTN)])
        except Exception:
            pass

    def _save_window_geom(self):
        try:
            self._data["window_geom"] = self.root.wm_geometry()
            save_data(self._data)
        except Exception:
            pass

    def _ensure_row_visible(self, widget):
        """Scroll _seg_sf so widget (a segment outer frame) is fully visible."""
        sf = self._seg_sf
        if sf is None:
            return
        try:
            if not widget.winfo_exists():
                return
            canvas   = sf._canvas
            inner_h  = sf.inner.winfo_height()
            canvas_h = canvas.winfo_height()
            if inner_h <= canvas_h or inner_h <= 0 or canvas_h <= 0:
                return   # everything fits — no scroll needed
            wy = widget.winfo_y()
            wh = widget.winfo_height()
            top_frac, _ = canvas.yview()
            view_top = top_frac * inner_h
            view_bot = view_top + canvas_h
            if wy < view_top:
                canvas.yview_moveto(wy / inner_h)
            elif (wy + wh) > view_bot:
                new_top = (wy + wh - canvas_h) / inner_h
                canvas.yview_moveto(max(0.0, min(1.0, new_top)))
        except Exception:
            pass

    # ── title bar ─────────────────────────────────────────────────────────

    def _build_title_bar(self):
        tb = tk.Frame(self.root, bg=TITLE_BG, pady=8)
        tb.pack(fill="x")
        tk.Label(tb, text="  Reel Time Plus", fg=ACCENT, bg=TITLE_BG,
                 font=("Avenir Next", 18)).pack(side="left")
        tk.Label(tb, text="v1.2", fg=DIM, bg=TITLE_BG,
                 font=("Avenir Next", 10)).pack(side="left", pady=(6, 0))
        tk.Checkbutton(tb, text="Float on Top", variable=self._stay_on_top,
                       command=self._apply_topmost,
                       fg=DIM, bg=TITLE_BG, selectcolor=TITLE_BG,
                       activebackground=TITLE_BG, activeforeground=TEXT,
                       font=F_SMALL).pack(side="right", padx=12)

        def _save_open_to_projects():
            self._data["open_to_projects"] = self._open_to_projects.get()
            save_data(self._data)

        tk.Checkbutton(tb, text="Open to Projects", variable=self._open_to_projects,
                       command=_save_open_to_projects,
                       fg=DIM, bg=TITLE_BG, selectcolor=TITLE_BG,
                       activebackground=TITLE_BG, activeforeground=TEXT,
                       font=F_SMALL).pack(side="right", padx=(0, 0))

    def _apply_topmost(self):
        self.root.attributes("-topmost", self._stay_on_top.get())

    # ── content helpers ────────────────────────────────────────────────────

    def _clear(self):
        for w in self._content.winfo_children():
            w.destroy()

    # =========================================================================
    # PROJECTS VIEW
    # =========================================================================

    def _show_projects_view(self):
        self._clear()
        if self._data.get("last_project_id") is not None:
            self._data["last_project_id"] = None
            save_data(self._data)
        c = self._content

        hdr = tk.Frame(c, bg=PANEL, pady=4)
        hdr.pack(fill="x")
        tk.Label(hdr, text="PROJECTS", fg=ACCENT, bg=PANEL,
                 font=F_HDR).pack(side="left", padx=16, pady=8)
        TBtn(hdr, text="＋  New Project", command=self._open_project_editor,
             bg=ACCENT, fg="#111111", padx=12, pady=4,
             font=("Avenir Next", 11, "bold")).pack(side="right", padx=10, pady=6)
        _sep(c)

        projects = self._data.get("projects", [])
        if not projects:
            tk.Label(c, text="No projects yet.",
                     fg=DIM, bg=BG, font=F_MAIN).pack(pady=60)
            tk.Label(c, text='Click "＋  New Project" to get started.',
                     fg=DIM, bg=BG, font=F_SMALL).pack()
            return

        sf = ScrollFrame(c, bg=BG)
        sf.pack(fill="both", expand=True)
        for i, proj in enumerate(projects):
            self._build_project_row(sf.inner, proj, i)

    def _build_project_row(self, parent, proj, idx):
        row_bg = PANEL if idx % 2 == 0 else PANEL2
        outer  = tk.Frame(parent, bg=row_bg, cursor="hand2")
        outer.pack(fill="x")
        _sep(outer, height=1)

        inner = tk.Frame(outer, bg=row_bg)
        inner.pack(fill="x", padx=16, pady=12)

        fps_key = proj.get("fps_key", "23.98 ndf")
        _, total = calc_totals(proj)
        n        = len(proj.get("segments", []))
        lbl      = proj.get("segment_label", "Act")
        lbl_pl   = lbl.lower() + ("s" if n != 1 else "")
        sub_text = f"{frames_to_tc(total, fps_key)}  ·  {n} {lbl_pl}  ·  {fps_key}"

        lbl_name = tk.Label(inner, text=proj.get("name", "Untitled"),
                            fg=TEXT, bg=row_bg, font=F_BOLD, anchor="w")
        lbl_name.pack(side="left", fill="x", expand=True)
        lbl_arr  = tk.Label(inner, text="›", fg=DIM, bg=row_bg,
                            font=("Avenir Next", 22))
        lbl_arr.pack(side="right")

        # Delete button — sits left of the arrow, only lights up on row hover
        lbl_del = tk.Label(inner, text="Delete", fg=row_bg, bg=row_bg,
                           font=("Avenir Next", 10), cursor="hand2", padx=8)
        lbl_del.pack(side="right")

        lbl_sub  = tk.Label(outer, text=sub_text, fg=DIM, bg=row_bg,
                            font=F_SMALL, anchor="w", padx=16)
        lbl_sub.pack(fill="x", pady=(0, 10))

        pid = proj["id"]
        all_w = [outer, inner, lbl_name, lbl_arr, lbl_sub]

        def _enter(_):
            for w in all_w:
                w.config(bg=BTN_HOV)
            lbl_del.config(bg=BTN_HOV, fg=RED)   # reveal in red on hover
        def _leave(_):
            for w in all_w:
                w.config(bg=row_bg)
            lbl_del.config(bg=row_bg, fg=row_bg)  # hide when not hovered
        def _click(_):
            self._show_project_detail(pid)

        for w in all_w:
            w.bind("<Enter>",    _enter)
            w.bind("<Leave>",    _leave)
            w.bind("<Button-1>", _click)

        # Delete button hover + click (NOT in all_w so its click stays isolated).
        # Re-use _enter/_leave so the whole row stays highlighted when hovering
        # the delete label, and the row dims correctly when the mouse leaves.
        lbl_del.bind("<Enter>", _enter)
        lbl_del.bind("<Leave>", _leave)

        def _del_click(e):
            if messagebox.askyesno(
                    "Delete Project",
                    f'Delete "{proj["name"]}"?\n\nThis cannot be undone.',
                    parent=self.root):
                self._data["projects"] = [
                    p for p in self._data["projects"] if p["id"] != pid]
                if self._data.get("last_project_id") == pid:
                    self._data["last_project_id"] = None
                save_data(self._data)
                self._show_projects_view()
            return "break"   # don't let the click bubble to the row handler
        lbl_del.bind("<Button-1>", _del_click)

    # =========================================================================
    # NEW / EDIT PROJECT EDITOR  (modal Toplevel)
    # =========================================================================

    def _open_project_editor(self, project_id=None):
        proj   = None
        is_new = project_id is None
        if not is_new:
            proj = next((p for p in self._data["projects"]
                         if p["id"] == project_id), None)
            if proj is None:
                return

        dlg = tk.Toplevel(self.root)
        dlg.title("New Project" if is_new else "Edit Project")
        dlg.configure(bg=BG)
        dlg.resizable(False, True)
        dw, dh = 480, 660
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        dlg.geometry(f"{dw}x{dh}+{(sw - dw) // 2}+{(sh - dh) // 2}")
        dlg.transient(self.root)
        dlg.update_idletasks()
        dlg.grab_set()
        # Lower main window's topmost so the dialog wins
        self.root.attributes("-topmost", False)
        dlg.attributes("-topmost", True)
        dlg.lift()
        dlg.focus_force()

        def _keep_top_proj():
            if dlg.winfo_exists():
                try:
                    dlg.attributes("-topmost", True)
                    dlg.lift()
                    # Re-grab if something silently released it
                    if dlg.grab_current() is not dlg:
                        dlg.grab_set()
                except Exception:
                    pass
                dlg.after(120, _keep_top_proj)
        _keep_top_proj()

        def _on_root_focus_proj(e):
            if dlg.winfo_exists():
                dlg.lift()
                dlg.focus_force()
        _proj_bind = self.root.bind("<FocusIn>", _on_root_focus_proj, add=True)

        def _proj_cleanup(e):
            # <Destroy> propagates from child widgets — only act when the
            # dialog itself is being destroyed, not one of its children.
            if e.widget is not dlg:
                return
            try:
                self.root.unbind("<FocusIn>", _proj_bind)
            except Exception:
                pass
            self.root.attributes("-topmost", self._stay_on_top.get())
        dlg.bind("<Destroy>", _proj_cleanup)

        # ── header ────────────────────────────────────────────────────────
        hdr = tk.Frame(dlg, bg=TITLE_BG, pady=8)
        hdr.pack(fill="x")
        tk.Label(hdr, text=f"  {'New' if is_new else 'Edit'} Project",
                 fg=ACCENT, bg=TITLE_BG,
                 font=("Avenir Next", 15, "bold")).pack(side="left")
        TBtn(hdr, text="✕", command=dlg.destroy,
             bg=TITLE_BG, fg=DIM, padx=8, pady=4,
             font=F_MAIN).pack(side="right", padx=8)

        sf   = ScrollFrame(dlg, bg=BG)
        sf.pack(fill="both", expand=True)
        body = sf.inner

        # ── BASIC INFO ─────────────────────────────────────────────────────
        _section_label(body, "BASIC INFO")

        v_name = tk.StringVar(value=proj.get("name", "") if proj else "")
        _, i = _field_row(body, "name")
        _dark_entry(i, v_name)

        v_goal = tk.StringVar(
            value=frames_to_tc(proj.get("goal_frames", 0),
                               proj.get("fps_key", "23.98 ndf")) if proj else "")
        _, i = _field_row(body, "goal time")
        e_goal = _dark_entry(i, v_goal)
        tk.Label(i, text="  e.g. 1:30:00.00", fg=DIM, bg=PANEL,
                 font=F_SMALL).pack(side="left")

        # Segment count + label toggle (same row)
        init_count = len(proj.get("segments", [])) if proj else 1
        v_count = tk.IntVar(value=max(1, init_count))
        v_seg   = tk.StringVar(value=proj.get("segment_label", "Act") if proj else "Act")
        _, i    = _field_row(body, "segments")

        tk.Label(i, text="count", fg=DIM, bg=PANEL, font=F_SMALL).pack(side="left")
        tk.Spinbox(i, from_=1, to=99, textvariable=v_count, width=4,
                   bg=ENTRY_BG, fg=TEXT, insertbackground=TEXT, relief="flat",
                   buttonbackground=BTN, font=F_MAIN,
                   highlightthickness=1, highlightbackground="#444444",
                   highlightcolor=ACCENT).pack(side="left", padx=(4, 18))

        seg_lbls = {}

        def _pick_seg(lbl):
            v_seg.set(lbl)
            _retoggle(seg_lbls, lbl)

        for lbl_text in ("Act", "Reel"):
            seg_lbls[lbl_text] = _toggle_lbl(
                i, lbl_text,
                active=(lbl_text == v_seg.get()),
                command=lambda l=lbl_text: _pick_seg(l),
                padx=12, pady=4)

        # FPS
        v_fps = tk.StringVar(value=proj.get("fps_key", "23.98 ndf") if proj else "23.98 ndf")
        _, i  = _field_row(body, "fps")
        fps_state = "disabled" if (proj and not is_new) else "readonly"
        cb = ttk.Combobox(i, textvariable=v_fps, values=FPS_KEYS,
                          state=fps_state, width=16,
                          style="Dark.TCombobox", font=F_MAIN)
        cb.pack(side="left")
        def _fmt_goal(*_):
            s = v_goal.get().strip()
            if s:
                f = parse_tc(s, v_fps.get())
                if f is not None:
                    v_goal.set(frames_to_tc(f, v_fps.get()))
        e_goal.bind("<FocusOut>", _fmt_goal)
        e_goal.bind("<Return>",   _fmt_goal)

        if proj and not is_new:
            tk.Label(i, text="  🔒 locked", fg=DIM, bg=PANEL,
                     font=F_SMALL).pack(side="left")
            tk.Label(body,
                     text="❄️  FPS is locked to protect your timecode data. "
                          "If you selected the wrong rate, create a new project "
                          "— it only takes a moment.",
                     fg=DIM, bg=BG, font=F_SMALL,
                     wraplength=400, justify="left").pack(
                         fill="x", padx=16, pady=(4, 0))

        # Film Format — controls feet+frames display; can be changed any time
        v_film = tk.StringVar(
            value=proj.get("film_format", "digital") if proj else "digital")
        _, i = _field_row(body, "film format")
        film_btns = {}

        def _pick_film(fmt):
            v_film.set(fmt)
            _retoggle(film_btns, fmt)

        for _fmt_key, _fmt_lbl in [("digital", "Digital"),
                                    ("35mm",    "35mm"),
                                    ("16mm",    "16mm")]:
            film_btns[_fmt_key] = _toggle_lbl(
                i, _fmt_lbl,
                active=(_fmt_key == v_film.get()),
                command=lambda f=_fmt_key: _pick_film(f),
                padx=12, pady=4)

        # ── BREAKS (OPTIONAL) ─────────────────────────────────────────────
        _section_label(body, "BREAKS  (OPTIONAL)")

        v_btype       = tk.StringVar(value=proj.get("break_type", "no_breaks") if proj else "no_breaks")
        v_break_dur   = tk.StringVar(value=str(proj.get("break_frames", 0)) if proj else "0")
        v_lmode       = tk.StringVar(value=proj.get("leader_mode", "whole_show") if proj else "whole_show")
        # Default Film Leader times: 12 seconds head, 6 seconds tail.
        # For existing projects, show the saved value as a TC string.
        _fps_init = proj.get("fps_key", "23.98 ndf") if proj else "23.98 ndf"
        _lhf      = proj.get("leader_head_frames", 0) if proj else 0
        _ltf      = proj.get("leader_tail_frames",  0) if proj else 0
        v_lhead   = tk.StringVar(value=frames_to_tc(_lhf, _fps_init) if _lhf > 0 else "12:00")
        v_ltail   = tk.StringVar(value=frames_to_tc(_ltf, _fps_init) if _ltf > 0 else "6:00")

        # Break-type toggle row
        btype_row = tk.Frame(body, bg=BG)
        btype_row.pack(fill="x", padx=16, pady=(10, 0))
        btype_btns = {}
        BTYPES = [("tv_breaks", "TV Breaks"), ("film_leader", "Film Leader"), ("no_breaks", "No Breaks")]

        tv_panel   = tk.Frame(body, bg=PANEL)
        film_panel = tk.Frame(body, bg=PANEL)

        def _build_tv_panel():
            for w in tv_panel.winfo_children():
                w.destroy()
            _sep(tv_panel)
            inner = tk.Frame(tv_panel, bg=PANEL)
            inner.pack(fill="x", padx=16, pady=10)
            tk.Label(inner, text="break duration", fg=DIM, bg=PANEL,
                     font=F_SMALL, width=14, anchor="w").pack(side="left")
            _dark_entry(inner, v_break_dur, width=12)
            tk.Label(inner, text="  frames or TC  (e.g. 48  or  0:02.00)",
                     fg=DIM, bg=PANEL, font=F_SMALL).pack(side="left")

        def _build_film_panel():
            for w in film_panel.winfo_children():
                w.destroy()
            _sep(film_panel)

            # Leader mode sub-toggle
            lm_row = tk.Frame(film_panel, bg=PANEL)
            lm_row.pack(fill="x", padx=16, pady=(10, 4))
            tk.Label(lm_row, text="leader mode", fg=DIM, bg=PANEL,
                     font=F_SMALL, width=14, anchor="w").pack(side="left")
            lm_lbls = {}

            def _pick_lmode(m):
                v_lmode.set(m)
                _retoggle(lm_lbls, m)

            for mk, ml in [("whole_show", "Whole Show"),
                            ("per_segment", f"Per {v_seg.get()}")]:
                lm_lbls[mk] = _toggle_lbl(
                    lm_row, ml,
                    active=(mk == v_lmode.get()),
                    command=lambda m=mk: _pick_lmode(m),
                    font=F_SMALL, padx=10, pady=3)

            # Head / tail entries
            for lbl_txt, var in [("head leader", v_lhead), ("tail leader", v_ltail)]:
                row_f = tk.Frame(film_panel, bg=PANEL)
                row_f.pack(fill="x", padx=16, pady=4)
                tk.Label(row_f, text=lbl_txt, fg=DIM, bg=PANEL,
                         font=F_SMALL, width=14, anchor="w").pack(side="left")
                _dark_entry(row_f, var, width=12)
                tk.Label(row_f, text="  frames or TC",
                         fg=DIM, bg=PANEL, font=F_SMALL).pack(side="left")
            tk.Frame(film_panel, bg=PANEL, height=8).pack()

        def _refresh_breaks():
            bt = v_btype.get()
            _retoggle(btype_btns, bt)
            if bt == "tv_breaks":
                _build_tv_panel()
                tv_panel.pack(fill="x", before=act_row)
                film_panel.pack_forget()
            elif bt == "film_leader":
                _build_film_panel()
                film_panel.pack(fill="x", before=act_row)
                tv_panel.pack_forget()
            else:
                tv_panel.pack_forget()
                film_panel.pack_forget()
            # Defer re-assertion — calling grab_set() synchronously inside a
            # <Button-1> handler confuses macOS event routing and drops the
            # dialog.  Wait until the click event has fully cleared first.
            def _reassert():
                if not dlg.winfo_exists():
                    return
                try:
                    dlg.attributes("-topmost", True)
                    dlg.lift()
                    if dlg.grab_current() is not dlg:
                        dlg.grab_set()
                except Exception:
                    pass
            dlg.after(250, _reassert)

        for bkey, blabel in BTYPES:
            btype_btns[bkey] = _toggle_lbl(
                btype_row, blabel,
                active=(bkey == v_btype.get()),
                command=lambda bk=bkey: (v_btype.set(bk), _refresh_breaks()))

        # act_row must be packed before _refresh_breaks() is called so that
        # the break panels can use `before=act_row` and always sit above the buttons.
        act_row = tk.Frame(body, bg=BG)
        act_row.pack(fill="x", padx=16, pady=20)

        _refresh_breaks()

        def _save():
            name = v_name.get().strip()
            if not name:
                messagebox.showerror("Missing Name",
                                     "Please enter a project name.", parent=dlg)
                return
            fps_key = v_fps.get()
            goal_f  = parse_tc(v_goal.get().strip(), fps_key) or 0
            bt      = v_btype.get()
            if bt == "tv_breaks":
                break_f = parse_tc(v_break_dur.get().strip(), fps_key) or 0
                lmode, lhead, ltail = "whole_show", 0, 0
            elif bt == "film_leader":
                break_f = 0
                lmode   = v_lmode.get()
                lhead   = parse_tc(v_lhead.get().strip(), fps_key) or 0
                ltail   = parse_tc(v_ltail.get().strip(), fps_key) or 0
            else:
                break_f, lmode, lhead, ltail = 0, "whole_show", 0, 0

            target = max(1, v_count.get())
            if is_new:
                p = new_project(name, fps_key, goal_f, v_seg.get(),
                                bt, break_f, lmode, lhead, ltail,
                                film_format=v_film.get())
                while len(p["segments"]) < target:
                    auto_num = len(p["segments"]) + 1
                    p["segments"].append({"frames": 0,
                                          "name": f"{v_seg.get()} {auto_num}"})
                self._data["projects"].append(p)
                new_id = p["id"]
                save_data(self._data)
                dlg.destroy()
                self._show_project_detail(new_id)
            else:
                proj.update({
                    "name":               name,
                    "goal_frames":        goal_f,
                    "segment_label":      v_seg.get(),
                    "film_format":        v_film.get(),
                    "break_type":         bt,
                    "break_frames":       break_f,
                    "leader_mode":        lmode,
                    "leader_head_frames": lhead,
                    "leader_tail_frames": ltail,
                })
                # Add auto-named segments if count increased
                while len(proj["segments"]) < target:
                    auto_num = len(proj["segments"]) + 1
                    proj["segments"].append({"frames": 0,
                                             "name": f"{v_seg.get()} {auto_num}"})
                save_data(self._data)
                dlg.destroy()
                self._show_project_detail(project_id)

        # Numeric Enter anywhere in the dialog saves the project
        dlg.bind("<KP_Enter>",  lambda _: _save())
        dlg.bind("<ISO_Enter>", lambda _: _save())

        TBtn(act_row, text="Save Project", command=_save,
             bg=ACCENT, fg="#111111", padx=20, pady=8,
             font=F_BOLD).pack(side="left")

        if not is_new:
            def _delete():
                if messagebox.askyesno(
                        "Delete Project",
                        f'Delete "{proj["name"]}"?\n\nThis cannot be undone.',
                        parent=dlg):
                    self._data["projects"] = [
                        p for p in self._data["projects"] if p["id"] != project_id]
                    save_data(self._data)
                    dlg.destroy()
                    self._show_projects_view()

            # Use Label so macOS respects the colour — tk.Button ignores bg on macOS
            _del_hov = _hover_color(BTN)
            _del_lbl = tk.Label(act_row, text="Delete Project", bg=BTN, fg=RED,
                                padx=16, pady=8, cursor="hand2", font=F_MAIN)
            _del_lbl.pack(side="right")
            _del_lbl.bind("<Button-1>", lambda _: _delete())
            _del_lbl.bind("<Enter>",    lambda _: _del_lbl.config(bg=_del_hov))
            _del_lbl.bind("<Leave>",    lambda _: _del_lbl.config(bg=BTN))

    # =========================================================================
    # PROJECT DETAIL VIEW
    # =========================================================================

    def _show_project_detail(self, project_id):
        self._clear()
        if self._data.get("last_project_id") != project_id:
            self._data["last_project_id"] = project_id
            save_data(self._data)
            # Clear sizing memory so the window fits this project on every navigation
            self._last_sized.pop(project_id, None)
        proj = next((p for p in self._data["projects"]
                     if p["id"] == project_id), None)
        if proj is None:
            self._show_projects_view()
            return

        c       = self._content
        fps_key = proj.get("fps_key", "23.98 ndf")
        seg_lbl = proj.get("segment_label", "Act")
        segs    = proj.get("segments", [])
        n       = len(segs)
        content_frames, total_frames = calc_totals(proj)
        goal_frames = proj.get("goal_frames", 0)
        diff_frames = total_frames - goal_frames

        # ── nav bar ────────────────────────────────────────────────────────
        nav = tk.Frame(c, bg=PANEL, pady=4)
        nav.pack(fill="x")
        TBtn(nav, text="‹  Projects", command=self._show_projects_view,
             bg=PANEL, fg=ACCENT, padx=10, pady=6,
             font=F_MAIN).pack(side="left", padx=4)
        tk.Label(nav, text=proj.get("name", ""), fg=TEXT, bg=PANEL,
                 font=F_BOLD).pack(side="left", padx=6)
        TBtn(nav, text="Edit",
             command=lambda: self._open_project_editor(project_id),
             bg=PANEL, fg=ACCENT, padx=10, pady=6,
             font=F_MAIN).pack(side="right", padx=8)
        _sep(c)

        # ── totals ─────────────────────────────────────────────────────────
        tot = tk.Frame(c, bg=BG, pady=14)
        tot.pack(fill="x")

        rmode = self._runtime_mode.get(project_id, "total")
        display_frames = content_frames if rmode == "content" else total_frames
        tc_str = frames_to_tc(display_frames, fps_key)

        big_lbl = tk.Label(tot, text=tc_str, fg=TEXT, bg=BG,
                           font=F_HUGE, cursor="hand2")
        big_lbl.pack()

        def _toggle_runtime(_event=None):
            cur = self._runtime_mode.get(project_id, "total")
            self._runtime_mode[project_id] = "content" if cur == "total" else "total"
            self._show_project_detail(project_id)

        big_lbl.bind("<Button-1>", _toggle_runtime)

        # break subtitle — two lines so long film-leader strings don't run edge to edge
        bt   = proj.get("break_type", "no_breaks")
        sub1 = ""
        sub2 = ""
        if rmode == "content":
            if bt == "tv_breaks":
                sub1 = "content runtime"
                sub2 = "click to show total with TV breaks"
            elif bt == "film_leader":
                sub1 = "content runtime"
                sub2 = "click to show total with leader"
            else:
                sub1 = "content runtime"
                sub2 = "click to show total runtime"
        elif bt == "tv_breaks":
            b_tc = frames_to_tc(proj.get("break_frames", 0), fps_key)
            sub1 = (f"total runtime  ·  {n - 1}×{b_tc} TV breaks"
                    if n > 1 else f"total runtime  ·  TV breaks: {b_tc} each")
            sub2 = "click for content without breaks"
        elif bt == "film_leader":
            lmode = proj.get("leader_mode", "whole_show")
            h_tc  = frames_to_tc(proj.get("leader_head_frames", 0), fps_key)
            t_tc  = frames_to_tc(proj.get("leader_tail_frames", 0), fps_key)
            scope = f"per {seg_lbl.lower()}" if lmode == "per_segment" else "whole show"
            sub1  = f"total runtime  ·  film leader {h_tc} + {t_tc}  ·  {scope}"
            sub2  = "click for content without leader"
        else:
            sub1 = "total runtime  ·  no breaks"
            sub2 = "click for content"
        tk.Label(tot, text=sub1, fg="#b8b8b8", bg=BG, font=F_SMALL).pack()
        if sub2:
            tk.Label(tot, text=sub2, fg=DIM, bg=BG, font=F_SMALL).pack()

        # target / goal display
        if goal_frames > 0:
            goal_tc = frames_to_tc(goal_frames, fps_key)
            tk.Label(tot, text=f"Target  {goal_tc}",
                     fg="#d8d8d8", bg=BG,
                     font=("Avenir Next", 13)).pack(pady=(10, 0))

        # over / under
        if goal_frames > 0:
            cmp_frames = content_frames if rmode == "content" else total_frames
            diff       = cmp_frames - goal_frames
            abs_diff   = abs(diff)
            diff_tc    = frames_to_tc(abs_diff, fps_key)
            pct        = abs_diff / goal_frames * 100
            if diff > 0:
                diff_color = RED
                diff_text  = f"+{diff_tc}"
                pct_text   = f"{pct:.1f}% over"
            elif diff < 0:
                diff_color = GREEN
                diff_text  = f"-{diff_tc}"
                pct_text   = f"{pct:.1f}% under"
            else:
                diff_color = DIM
                diff_text  = "—  on the nose"
                pct_text   = "0.0%"
            tk.Label(tot, text=diff_text, fg=diff_color, bg=BG,
                     font=("Avenir Next", 22, "bold")).pack(pady=(6, 0))
            tk.Label(tot, text=pct_text, fg=DIM, bg=BG,
                     font=("Avenir Next", 14, "bold")).pack()

        # ── proportional bar ───────────────────────────────────────────────
        if n > 0 and content_frames > 0:
            bar_wrap = tk.Frame(c, bg=BG)
            bar_wrap.pack(fill="x", padx=16, pady=(6, 10))
            bar_cv = tk.Canvas(bar_wrap, bg=BG, highlightthickness=0, height=46)
            bar_cv.pack(fill="x")
            bar_cv.bind("<Configure>",
                        lambda e, p=proj: self._draw_bar(bar_cv, p, e.width))
            self.root.after(80, lambda: self._draw_bar(bar_cv, proj, 0))

        _sep(c)

        # ── segment list header ────────────────────────────────────────────
        lhdr = tk.Frame(c, bg=PANEL, pady=4)
        lhdr.pack(fill="x")
        tk.Label(lhdr, text=f"  {seg_lbl.upper()}S",
                 fg=ACCENT, bg=PANEL, font=F_HDR).pack(side="left", padx=(8, 0), pady=6)
        TBtn(lhdr, text=f"＋  Add {seg_lbl}",
             command=lambda: self._add_inline_segment(project_id),
             bg=ACCENT, fg="#111111", padx=10, pady=3,
             font=("Avenir Next", 10, "bold")).pack(side="right", padx=10, pady=5)

        # ── View-mode radio buttons: TC · Feet+Frames · Frames ───────────
        _film_fmt   = proj.get("film_format", "digital")
        _cur_vmode  = self._view_mode.get(project_id, "tc")

        def _set_view(mode):
            self._view_mode[project_id] = mode
            # Clear spot-check overrides when master mode changes
            self._ff_overrides = {k for k in self._ff_overrides
                                  if k[0] != project_id}
            self._show_project_detail(project_id)

        def _vbtn(text, mode):
            active = (_cur_vmode == mode)
            b = TBtn(lhdr, text=text,
                     bg=BTN_HOV if active else BTN,
                     fg=ACCENT  if active else DIM,
                     padx=8, pady=3,
                     font=("Avenir Next", 10, "bold") if active
                          else ("Avenir Next", 10))
            b.pack(side="right", padx=(0, 4), pady=5)
            b.bind("<Button-1>", lambda _e, m=mode: _set_view(m))

        _vbtn("Frames", "frames")
        if _film_fmt != "digital":
            _vbtn("F+F", "ff")
        _vbtn("TC", "tc")

        _sep(c)

        # Resize to fit the current segment count whenever it changes.
        # TC saves don't change n so they never trigger a resize.
        # Navigating to a project clears _last_sized so the first load always fits.
        ROW_H   = 70    # title bar + 22pt TC + 12pt name + separators + padding
        # FIXED_H covers: app title bar + nav + totals + colour bar + seg header + OS chrome.
        # The totals section is taller when a goal is set (target + over/under + pct).
        FIXED_H = 520 if goal_frames > 0 else 430
        last_n  = self._last_sized.get(project_id, -1)
        if n != last_n:
            self._last_sized[project_id] = n
            screen_h = self.root.winfo_screenheight()
            cap_h    = max(560, screen_h - 120)
            new_h    = max(560, min(FIXED_H + max(n, 1) * ROW_H, cap_h))
            cur_w    = self.root.winfo_width() or 560
            self.root.after(20, lambda: self.root.geometry(f"{cur_w}x{new_h}"))

        if n == 0:
            tk.Label(c,
                     text=f'No {seg_lbl.lower()}s yet. Click "＋  Add {seg_lbl}" to begin.',
                     fg=DIM, bg=BG, font=F_MAIN).pack(pady=30)
            return

        sf = ScrollFrame(c, bg=BG)
        sf.pack(fill="both", expand=True)
        self._seg_sf = sf
        for idx, seg in enumerate(segs):
            self._build_segment_row(sf.inner, proj, seg, idx,
                                    project_id, content_frames)

    # ── proportional bar drawing ───────────────────────────────────────────

    def _draw_bar(self, canvas, proj, width):
        w = canvas.winfo_width() if width == 0 else width
        if w < 10:
            canvas.after(80, lambda: self._draw_bar(canvas, proj, 0))
            return
        canvas.delete("all")

        segs   = proj.get("segments", [])
        cf     = sum(s.get("frames", 0) for s in segs)
        if cf == 0:
            return

        _, total = calc_totals(proj)
        goal     = proj.get("goal_frames", 0)
        fps_key  = proj.get("fps_key", "23.98 ndf")

        PAD = 3
        Y0  = 6
        H   = 32
        bar_w = w - PAD * 2

        # Goal boundary bracket (green if at/under, red if over)
        if goal > 0:
            ref     = max(total, goal)
            goal_x  = PAD + bar_w * goal / ref
            color   = GREEN if total <= goal else RED
            canvas.create_rectangle(PAD, Y0, goal_x, Y0 + H,
                                    outline=color, fill="", width=2)

        # Segment blocks — proportional to content
        x = PAD
        for i, seg in enumerate(segs):
            sw2 = max(1, seg.get("frames", 0) / cf * bar_w)
            color = seg.get("color") or SEG_COLORS[i % len(SEG_COLORS)]
            canvas.create_rectangle(x, Y0 + 3, x + sw2 - 1, Y0 + H - 3,
                                     fill=color, outline="")
            x += sw2

    # ── segment rows ────────────────────────────────────────────────────────

    def _build_segment_row(self, parent, proj, seg, idx,
                           project_id, content_frames):
        fps_key    = proj.get("fps_key", "23.98 ndf")
        seg_lbl    = proj.get("segment_label", "Act")
        row_bg     = PANEL if idx % 2 == 0 else PANEL2
        color      = seg.get("color") or SEG_COLORS[idx % len(SEG_COLORS)]
        seg_frames = seg.get("frames", 0)
        seg_name   = seg.get("name", "")

        outer = tk.Frame(parent, bg=row_bg)
        outer.pack(fill="x")
        _sep(outer, height=1)

        # Edit button (right side, packed before mid so it stays right)
        edit_f = tk.Frame(outer, bg=row_bg)
        edit_f.pack(side="right", fill="y", padx=6)
        TBtn(edit_f, text="✎", fg=DIM, bg=row_bg, padx=5, pady=2,
             font=("Avenir Next", 11),
             command=lambda i=idx: self._add_edit_segment(project_id, i)
             ).pack(expand=True)

        # Coloured left strip with number
        strip = tk.Frame(outer, bg=color, width=40, cursor="hand2")
        strip.pack(side="left", fill="y")
        strip.pack_propagate(False)
        strip_lbl = tk.Label(strip, text=str(idx + 1),
                             fg="white", bg=color,
                             font=("Avenir Next", 12, "bold"))
        strip_lbl.pack(expand=True)

        # ── Right-click colour picker (hidden feature) ─────────────────────
        def _show_color_picker(event, _seg=seg, _idx=idx):
            popup = tk.Toplevel(self.root)
            popup.overrideredirect(True)
            popup.attributes("-topmost", True)
            popup.configure(bg="#111111")

            outer_p = tk.Frame(popup, bg="#111111", padx=6, pady=6)
            outer_p.pack()
            tk.Label(outer_p, text="Segment color", fg="#666666", bg="#111111",
                     font=("Avenir Next", 9)).grid(
                         row=0, column=0, columnspan=4, sticky="w", pady=(0, 5))

            cur = _seg.get("color") or SEG_COLORS[_idx % len(SEG_COLORS)]
            SWATCH = 28
            for i, c in enumerate(ALL_SEG_COLORS):
                r   = i // 4 + 1
                col = i %  4
                sf  = tk.Frame(outer_p, bg=c, width=SWATCH, height=SWATCH,
                               cursor="hand2")
                sf.grid(row=r, column=col, padx=2, pady=2)
                sf.pack_propagate(False)
                if c == cur:
                    tk.Label(sf, text="✓", fg="white", bg=c,
                             font=("Avenir Next", 10, "bold")).pack(expand=True)

                def _pick(chosen=c):
                    _seg["color"] = chosen
                    save_data(self._data)
                    popup.destroy()
                    self.root.after(10, lambda: self._show_project_detail(project_id))

                # Return "break" so the click stops here and doesn't bubble up
                # to the popup background handler (_bg_click).
                def _swatch_click(e, fn=_pick):
                    fn()
                    return "break"
                sf.bind("<Button-1>", _swatch_click)
                for child in sf.winfo_children():
                    child.bind("<Button-1>", _swatch_click)

                def _hov_in(e, f=sf, c=c):
                    f.config(bg=_hover_color(c, 0.3))
                def _hov_out(e, f=sf, c=c):
                    f.config(bg=c)
                sf.bind("<Enter>", _hov_in)
                sf.bind("<Leave>", _hov_out)

            reset = tk.Label(outer_p, text="↺  reset to default",
                             fg="#555555", bg="#111111",
                             font=("Avenir Next", 8), cursor="hand2")
            reset.grid(row=len(ALL_SEG_COLORS) // 4 + 2,
                       column=0, columnspan=4, pady=(6, 0))
            reset.bind("<Enter>", lambda e: reset.config(fg="#999999"))
            reset.bind("<Leave>", lambda e: reset.config(fg="#555555"))

            def _reset():
                _seg.pop("color", None)
                save_data(self._data)
                popup.destroy()
                self.root.after(10, lambda: self._show_project_detail(project_id))
            def _reset_click(e):
                _reset()
                return "break"
            reset.bind("<Button-1>", _reset_click)

            # Position near cursor — use raw event coords so the popup
            # appears on whichever display the click happened on.
            popup.update_idletasks()
            x = event.x_root + 6
            y = event.y_root + 6
            popup.geometry(f"+{x}+{y}")
            # Lower the main window's -topmost so the picker wins the z-order.
            self.root.attributes("-topmost", False)
            popup.lift()
            popup.update()

            def _cp_restore():
                self.root.attributes("-topmost", self._stay_on_top.get())

            popup.bind("<Escape>",  lambda e: popup.destroy())
            popup.bind("<Destroy>", lambda e: _cp_restore())

            # grab_set() routes ALL application clicks through the popup, so
            # nothing behind it (nav buttons, segment rows) can fire accidentally.
            # Clicks outside the picker's visible area land on the popup background
            # → dismiss.  Clicks on swatch frames are handled by their own bindings
            # and return "break" so they don't bubble up to this handler.
            try:
                popup.grab_set()
            except Exception:
                pass

            def _bg_click(e):
                # Any click that reaches the popup background (not intercepted by
                # a swatch frame returning "break") closes the picker.
                if popup.winfo_exists():
                    popup.destroy()
            popup.bind("<Button-1>", _bg_click)
            outer_p.bind("<Button-1>", _bg_click)

        for _ev in ("<Button-1>", "<Button-2>", "<Button-3>", "<Control-Button-1>"):
            strip.bind(_ev, _show_color_picker)
            strip_lbl.bind(_ev, _show_color_picker)

        # Main content
        mid = tk.Frame(outer, bg=row_bg)
        mid.pack(side="left", fill="both", expand=True, padx=12, pady=5)

        # ── TC display ────────────────────────────────────────────────────
        film_format = proj.get("film_format", "digital")
        key         = (project_id, idx)
        _master     = self._view_mode.get(project_id, "tc")
        _is_spot    = key in self._ff_overrides
        _eff_mode   = "ff" if _is_spot else _master

        if _eff_mode == "ff":
            tc_str = frames_to_ff(seg_frames, film_format)
        elif _eff_mode == "frames":
            tc_str = str(seg_frames)
        else:
            tc_str = frames_to_tc(seg_frames, fps_key)

        tc_frame = tk.Frame(mid, bg=row_bg)
        tc_frame.pack(fill="x")

        tc_lbl = tk.Label(tc_frame, text=tc_str, fg=TEXT, bg=row_bg,
                          font=("Avenir Next", 22, "bold"), anchor="w", cursor="hand2")
        tc_lbl.pack(fill="x")

        # Small hint shown when this segment has a spot-check ff override active
        ff_hint = tk.Label(mid, text="", fg=DIM, bg=row_bg,
                           font=("Avenir Next", 9), anchor="w")
        if _is_spot:
            _fmthint = "16mm" if film_format == "16mm" else "35mm · 4-perf"
            ff_hint.config(text=f"{_fmthint}  ·  right-click to restore")
            ff_hint.pack(fill="x")

        # Right-click spot-check: flip just this segment to Feet+Frames
        # Only offered on film projects when master view is not already "ff"
        if film_format != "digital" and _master != "ff":
            def _toggle_spot(_e):
                if key in self._ff_overrides:
                    self._ff_overrides.discard(key)
                else:
                    self._ff_overrides.add(key)
                self._show_project_detail(project_id)

            for _ev in ("<Button-2>", "<Button-3>", "<Control-Button-1>"):
                tc_lbl.bind(_ev, _toggle_spot)

        _pending = [None]

        def _do_edit_tc():
            _pending[0] = None
            # Only open if this is still the last row the user clicked
            if self._last_tc_click != key:
                return
            # Guard against stale closures after a full page rebuild
            if not tc_frame.winfo_exists():
                return
            _eff = "ff" if key in self._ff_overrides else self._view_mode.get(project_id, "tc")
            if _eff == "ff":
                return
            # Clear auto_open now that we're actually opening
            self._auto_open_edit = None
            tc_lbl.pack_forget()
            _orig_tc = frames_to_tc(seg.get("frames", 0), fps_key)
            v = tk.StringVar(value=_orig_tc)
            e = tk.Entry(tc_frame, textvariable=v, bg=ENTRY_BG, fg=TEXT,
                         insertbackground=TEXT, relief="flat",
                         font=("Avenir Next", 20, "bold"),
                         highlightthickness=1, highlightbackground="#444444",
                         highlightcolor=ACCENT, width=16)
            e.pack(fill="x")
            e.select_range(0, "end")
            e.focus_set()
            # Scroll so this row is visible (important when advancing with Enter)
            tc_frame.after(30, lambda: self._ensure_row_visible(outer))
            done = [False]

            def _commit_via_key(event=None):
                # Advance to next segment's inline editor on Enter
                next_idx = idx + 1
                if next_idx < len(proj["segments"]):
                    self._auto_open_edit = (project_id, next_idx)
                    self._last_tc_click  = (project_id, next_idx)
                else:
                    self._auto_open_edit = None
                _commit()

            def _commit(event=None):
                if done[0]: return
                done[0] = True
                val = v.get().strip()
                frames = parse_tc(val, fps_key) if val else None
                if frames is not None and frames >= 0:
                    seg["frames"] = frames
                    save_data(self._data)
                    self._show_project_detail(project_id)
                else:
                    e.pack_forget()
                    tc_lbl.pack(fill="x")

            def _cancel(event=None):
                if done[0]: return
                done[0] = True
                self._auto_open_edit = None
                e.pack_forget()
                tc_lbl.pack(fill="x")

            def _undo(event=None):
                v.set(_orig_tc)
                e.select_range(0, "end")
                return "break"

            _ENTER_CODES = {36, 76, 1275068419}  # main Return, KP_Enter (std), KP_Enter (macOS Tk)

            def _on_any_key(event):
                ks = event.keysym or ''
                if 'Return' in ks or 'Enter' in ks or event.keycode in _ENTER_CODES:
                    _commit_via_key()

            e.bind("<Return>",   _commit_via_key)
            e.bind("<KP_Enter>", _commit_via_key)
            e.bind("<Key>",      _on_any_key)
            # NOTE: no <KeyRelease> here — it leaks into the next row's
            # entry when focus transfers during the 80ms auto-open delay,
            # causing every other segment to be skipped.
            e.bind("<Escape>",   _cancel)
            e.bind("<FocusOut>",    _commit)
            e.bind("<Up>",          lambda ev: (e.icursor(0), "break"))
            e.bind("<Down>",        lambda ev: (e.icursor("end"), "break"))
            e.bind("<Command-z>",   _undo)
            e.bind("<Control-z>",   _undo)

        def _on_tc_click(event):
            self._last_tc_click  = key
            self._auto_open_edit = key  # request auto-open after any rebuild
            # Force FocusOut on any open entry and process it synchronously
            try:
                self.root.focus_set()
                self.root.update_idletasks()   # flush FocusOut before timer starts
            except Exception:
                pass
            # If the synchronous FocusOut triggered a rebuild, tc_frame is gone
            if not tc_frame.winfo_exists():
                return  # auto_open will handle opening this row after rebuild
            if _pending[0]:
                tc_frame.after_cancel(_pending[0])
            _pending[0] = tc_frame.after(220, _do_edit_tc)

        tc_lbl.bind("<Button-1>", _on_tc_click)

        # ── Name + pct on one line below TC ──────────────────────────────
        info_frame = tk.Frame(mid, bg=row_bg)
        info_frame.pack(fill="x")

        if content_frames > 0:
            pct = seg_frames / content_frames * 100
            tk.Label(info_frame, text=f"{pct:.1f}%", fg=DIM, bg=row_bg,
                     font=("Avenir Next", 9), anchor="e").pack(side="right")

        name_txt = seg_name if seg_name else "add name…"
        name_fg  = "#d0d0d0" if seg_name else "#787878"
        name_lbl = tk.Label(info_frame, text=name_txt, fg=name_fg, bg=row_bg,
                             font=("Avenir Next", 12), anchor="w", cursor="hand2")
        name_lbl.pack(side="left", fill="x", expand=True)

        def _edit_name(_event=None, nf=info_frame, nl=name_lbl, s=seg):
            nl.pack_forget()
            v = tk.StringVar(value=s.get("name", ""))
            e = tk.Entry(nf, textvariable=v, bg=ENTRY_BG, fg=TEXT,
                         insertbackground=TEXT, relief="flat", font=F_SMALL,
                         highlightthickness=1, highlightbackground=ACCENT,
                         highlightcolor=ACCENT)
            e.pack(side="left", fill="x", expand=True)
            e.select_range(0, "end")
            e.focus_set()
            done = [False]
            def _commit(*_):
                if done[0]: return
                done[0] = True
                s["name"] = v.get().strip()
                save_data(self._data)
                self._show_project_detail(project_id)
            def _cancel(*_):
                if done[0]: return
                done[0] = True
                e.pack_forget()
                nl.pack(side="left", fill="x", expand=True)
            def _name_on_key(event):
                if 'Return' in event.keysym or 'Enter' in event.keysym:
                    _commit()
            e.bind("<Return>",    _commit)
            e.bind("<KP_Enter>",  _commit)
            e.bind("<Key>",       _name_on_key)
            e.bind("<Escape>",    lambda ev: _cancel())
            e.bind("<FocusOut>",  _commit)

        name_lbl.bind("<Button-1>", _edit_name)

        # If a click on this row triggered a full page rebuild, auto-reopen it
        if self._auto_open_edit == key:
            self._auto_open_edit = None
            self._last_tc_click  = key
            tc_frame.after(80, _do_edit_tc)

    # =========================================================================
    # INLINE SEGMENT ADD
    # =========================================================================

    def _add_inline_segment(self, project_id):
        proj = next((p for p in self._data["projects"]
                     if p["id"] == project_id), None)
        if proj is None:
            return
        if self._seg_sf is None:
            return

        fps_key = proj.get("fps_key", "23.98 ndf")
        seg_lbl = proj.get("segment_label", "Act")
        idx     = len(proj["segments"])
        color   = SEG_COLORS[idx % len(SEG_COLORS)]
        ROW_BG  = "#222c3a"   # distinct tint so the live row is visually distinct

        parent = self._seg_sf.inner

        outer = tk.Frame(parent, bg=ROW_BG)
        outer.pack(fill="x")
        _sep(outer, height=1)

        # Left strip (same as existing rows)
        strip = tk.Frame(outer, bg=color, width=40)
        strip.pack(side="left", fill="y")
        strip.pack_propagate(False)
        tk.Label(strip, text=str(idx + 1),
                 fg="white", bg=color,
                 font=("Avenir Next", 12, "bold")).pack(expand=True)

        # Input area
        mid = tk.Frame(outer, bg=ROW_BG)
        mid.pack(side="left", fill="both", expand=True, padx=12, pady=6)

        # Row 1: name + TC entries
        top = tk.Frame(mid, bg=ROW_BG)
        top.pack(fill="x")

        tk.Label(top, text="name", fg=DIM, bg=ROW_BG, font=F_SMALL).pack(side="left")
        v_name = tk.StringVar()
        e_name = tk.Entry(top, textvariable=v_name, bg=ENTRY_BG, fg=TEXT,
                          insertbackground=TEXT, relief="flat", font=F_MAIN,
                          highlightthickness=1, highlightbackground="#444",
                          highlightcolor=ACCENT, width=16)
        e_name.pack(side="left", padx=(4, 14))

        tk.Label(top, text="timecode", fg=DIM, bg=ROW_BG, font=F_SMALL).pack(side="left")
        v_tc = tk.StringVar()
        e_tc = tk.Entry(top, textvariable=v_tc, bg=ENTRY_BG, fg=TEXT,
                        insertbackground=TEXT, relief="flat",
                        font=("Avenir Next", 15, "bold"),
                        highlightthickness=1, highlightbackground="#444",
                        highlightcolor=ACCENT, width=14)
        e_tc.pack(side="left", padx=(4, 0))

        # Row 2: hint
        hint = tk.Label(mid, text="optional name  ·  TC e.g. 21:55:18  or  raw frames",
                        fg=DIM, bg=ROW_BG, font=("Avenir Next", 9))
        hint.pack(anchor="w", pady=(4, 0))

        # Row 3: error message (hidden until needed)
        lbl_err = tk.Label(mid, text="", fg=RED, bg=ROW_BG, font=F_SMALL)
        lbl_err.pack(anchor="w")

        def _save(_event=None):
            tc_str = v_tc.get().strip()
            if not tc_str:
                lbl_err.config(text="Please enter a timecode.")
                e_tc.focus_set()
                return
            frames = parse_tc(tc_str, fps_key)
            if frames is None or frames < 0:
                lbl_err.config(text="Invalid timecode — try  1:23:45:00  or  12345  frames.")
                e_tc.focus_set()
                return
            proj["segments"].append({"frames": frames, "name": v_name.get().strip()})
            save_data(self._data)
            self._show_project_detail(project_id)

        def _cancel(_event=None):
            outer.destroy()

        # Row 4: full-width OK / Cancel buttons below the entry fields
        btn_row = tk.Frame(mid, bg=ROW_BG)
        btn_row.pack(fill="x", pady=(8, 4))
        TBtn(btn_row, text="✓  Save", command=_save,
             bg=GREEN, fg="#111111", padx=20, pady=6,
             font=("Avenir Next", 11, "bold")).pack(side="left", padx=(0, 8))
        TBtn(btn_row, text="✕  Cancel", command=_cancel,
             bg=BTN, fg=DIM, padx=16, pady=6,
             font=F_MAIN).pack(side="left")

        e_name.bind("<Return>",    lambda _: e_tc.focus_set())
        e_name.bind("<KP_Enter>",  lambda _: e_tc.focus_set())
        e_name.bind("<Tab>",       lambda _: (e_tc.focus_set(), "break"))
        def _tc_key(ev):
            if 'Return' in ev.keysym or 'Enter' in ev.keysym:
                _save()
        e_tc.bind("<Return>",    _save)
        e_tc.bind("<KP_Enter>",  _save)
        e_tc.bind("<Key>",       _tc_key)
        e_tc.bind("<Escape>",    _cancel)
        e_name.bind("<Escape>",  _cancel)

        # Scroll to bottom and focus TC
        self._seg_sf._canvas.after(50, lambda: self._seg_sf._canvas.yview_moveto(1.0))
        e_name.focus_set()

    # =========================================================================
    # ADD / EDIT SEGMENT  (modal Toplevel)
    # =========================================================================

    def _add_edit_segment(self, project_id, seg_idx, focus_name=False):
        proj = next((p for p in self._data["projects"]
                     if p["id"] == project_id), None)
        if proj is None:
            return

        fps_key = proj.get("fps_key", "23.98 ndf")
        seg_lbl = proj.get("segment_label", "Act")
        _, _, _, nom = fps_info(fps_key)
        seg    = proj["segments"][seg_idx] if seg_idx is not None else None
        is_new = seg is None
        num    = (seg_idx + 1) if seg_idx is not None else len(proj["segments"]) + 1

        dlg = tk.Toplevel(self.root)
        dlg.title(f"{'Edit' if seg else 'Add'} Segment")
        dlg.configure(bg=BG)
        dlg.resizable(False, False)
        dw, dh = 440, 430
        rx = self.root.winfo_x()
        ry = self.root.winfo_y()
        rw = self.root.winfo_width()
        dlg.geometry(f"{dw}x{dh}+{rx + (rw - dw) // 2}+{ry + 80}")
        dlg.transient(self.root)
        dlg.update_idletasks()
        dlg.grab_set()
        # Lower main window's topmost so the dialog wins
        self.root.attributes("-topmost", False)
        dlg.attributes("-topmost", True)
        dlg.lift()
        dlg.focus_force()

        # Paused while a sub-popup (colour picker) is open so its clicks aren't
        # eaten by the grab being re-asserted on the parent dialog.
        _skip_grab = [False]

        def _keep_top_seg():
            if dlg.winfo_exists():
                # Pause entirely while a sub-popup (colour picker) is open —
                # lift() and -topmost would punch the dialog on top of the picker.
                if not _skip_grab[0]:
                    try:
                        dlg.attributes("-topmost", True)
                        dlg.lift()
                        if dlg.grab_current() is not dlg:
                            dlg.grab_set()
                    except Exception:
                        pass
                dlg.after(120, _keep_top_seg)
        _keep_top_seg()

        def _on_root_focus(e):
            if dlg.winfo_exists():
                dlg.lift()
                dlg.focus_force()
        _root_bind = self.root.bind("<FocusIn>", _on_root_focus, add=True)

        def _cleanup(e):
            # <Destroy> propagates from child widgets — only act when the
            # dialog itself is being destroyed, not one of its children.
            if e.widget is not dlg:
                return
            try:
                self.root.unbind("<FocusIn>", _root_bind)
            except Exception:
                pass
            self.root.attributes("-topmost", self._stay_on_top.get())
        dlg.bind("<Destroy>", _cleanup)

        hdr = tk.Frame(dlg, bg=TITLE_BG, pady=8)
        hdr.pack(fill="x")
        tk.Label(hdr, text=f"  {'Edit' if seg else 'Add'} Segment {num}",
                 fg=ACCENT, bg=TITLE_BG,
                 font=("Avenir Next", 14, "bold")).pack(side="left")

        body = tk.Frame(dlg, bg=BG)
        body.pack(fill="both", expand=True, padx=22, pady=16)

        tk.Label(body, text=f"Project FPS:  {fps_key}  (nominal {nom} fps)",
                 fg=DIM, bg=BG, font=F_SMALL).pack(anchor="w", pady=(0, 12))

        # Optional name
        tk.Label(body, text=f"{seg_lbl} name  (optional):",
                 fg=DIM, bg=BG, font=F_SMALL).pack(anchor="w")
        v_name = tk.StringVar(value=seg.get("name", "") if seg else "")
        e_name = tk.Entry(body, textvariable=v_name, bg=ENTRY_BG, fg=TEXT,
                          insertbackground=TEXT, relief="flat", font=F_MAIN,
                          highlightthickness=1, highlightbackground="#444444",
                          highlightcolor=ACCENT, width=34)
        e_name.pack(anchor="w", pady=(3, 10))

        # ── Segment colour ──────────────────────────────────────────────────
        # Track chosen colour — None means "keep/use the auto-assigned default"
        _default_color = SEG_COLORS[seg_idx % len(SEG_COLORS)] if seg_idx is not None \
                         else SEG_COLORS[0]
        v_color = [seg.get("color") if seg else None]

        clr_row = tk.Frame(body, bg=BG)
        clr_row.pack(anchor="w", pady=(0, 12))
        tk.Label(clr_row, text="Color:", fg=DIM, bg=BG,
                 font=F_SMALL).pack(side="left")

        _swatch_color = v_color[0] or _default_color
        clr_swatch = tk.Frame(clr_row, bg=_swatch_color,
                              width=22, height=22, cursor="hand2")
        clr_swatch.pack(side="left", padx=(8, 6))
        clr_swatch.pack_propagate(False)

        clr_hint = tk.Label(clr_row, text="click to change",
                            fg="#555555", bg=BG,
                            font=("Avenir Next", 9), cursor="hand2")
        clr_hint.pack(side="left")

        def _open_color_popup(event=None):
            popup = tk.Toplevel(dlg)
            popup.overrideredirect(True)
            popup.attributes("-topmost", True)
            popup.configure(bg="#111111")
            outer_p = tk.Frame(popup, bg="#111111", padx=6, pady=6)
            outer_p.pack()
            tk.Label(outer_p, text="Segment color", fg="#666666", bg="#111111",
                     font=("Avenir Next", 9)).grid(
                         row=0, column=0, columnspan=4, sticky="w", pady=(0, 5))

            cur = v_color[0] or _default_color
            SWATCH = 26
            for i, c in enumerate(ALL_SEG_COLORS):
                r   = i // 4 + 1
                col = i %  4
                sf  = tk.Frame(outer_p, bg=c, width=SWATCH, height=SWATCH,
                               cursor="hand2")
                sf.grid(row=r, column=col, padx=2, pady=2)
                sf.pack_propagate(False)
                if c == cur:
                    tk.Label(sf, text="✓", fg="white", bg=c,
                             font=("Avenir Next", 9, "bold")).pack(expand=True)

                def _pick(chosen=c):
                    v_color[0] = chosen
                    clr_swatch.config(bg=chosen)
                    popup.destroy()

                def _swatch_click(e, fn=_pick):
                    fn()
                    return "break"
                sf.bind("<Button-1>", _swatch_click)
                for child in sf.winfo_children():
                    child.bind("<Button-1>", _swatch_click)

                def _hi(e, f=sf, c=c):  f.config(bg=_hover_color(c, 0.3))
                def _lo(e, f=sf, c=c):  f.config(bg=c)
                sf.bind("<Enter>", _hi)
                sf.bind("<Leave>", _lo)

            reset = tk.Label(outer_p, text="↺  reset to default",
                             fg="#555555", bg="#111111",
                             font=("Avenir Next", 8), cursor="hand2")
            reset.grid(row=len(ALL_SEG_COLORS) // 4 + 2,
                       column=0, columnspan=4, pady=(5, 0))
            reset.bind("<Enter>", lambda e: reset.config(fg="#999999"))
            reset.bind("<Leave>", lambda e: reset.config(fg="#555555"))

            def _reset():
                v_color[0] = None
                clr_swatch.config(bg=_default_color)
                popup.destroy()

            def _reset_click(e):
                _reset()
                return "break"
            reset.bind("<Button-1>", _reset_click)

            # Position below the swatch widget — use widget's root coords so
            # the popup appears on whichever display the dialog is on.
            popup.update_idletasks()
            ox = clr_swatch.winfo_rootx()
            oy = clr_swatch.winfo_rooty() + clr_swatch.winfo_height() + 4
            popup.geometry(f"+{ox}+{oy}")
            # Release the dialog grab AND lower its -topmost so the picker
            # can both receive click events and win the z-order.
            # (Tk grab redirects ALL events to the grab window; child Toplevels
            # are not exempt.  We restore grab + topmost when popup closes.)
            try:
                dlg.grab_release()
            except Exception:
                pass
            dlg.attributes("-topmost", False)
            popup.lift()
            popup.update()

            # Pause the keep-top loop while this picker is open.
            _skip_grab[0] = True

            def _on_cp_destroy(e):
                _skip_grab[0] = False
                if dlg.winfo_exists():
                    try:
                        dlg.attributes("-topmost", True)
                        dlg.grab_set()
                    except Exception:
                        pass
            popup.bind("<Destroy>", _on_cp_destroy)
            popup.bind("<Escape>",  lambda e: popup.destroy())

            # grab_set() routes ALL clicks through the popup.
            # Swatch and reset bindings return "break" so they don't reach here.
            # Anything else (background click) dismisses the picker.
            try:
                popup.grab_set()
            except Exception:
                pass

            def _bg_click(e):
                if popup.winfo_exists():
                    popup.destroy()
            popup.bind("<Button-1>", _bg_click)
            outer_p.bind("<Button-1>", _bg_click)

        clr_swatch.bind("<Button-1>", _open_color_popup)
        clr_hint.bind("<Button-1>", _open_color_popup)

        # Input mode toggle
        film_format  = proj.get("film_format", "digital") if proj else "digital"
        _fpf         = 40 if film_format == "16mm" else 16
        v_mode       = tk.StringVar(value="tc")
        _prev_mode   = ["tc"]   # mutable ref so _set_mode can track conversions
        mode_row     = tk.Frame(body, bg=BG)
        mode_row.pack(anchor="w", pady=(0, 6))
        tk.Label(mode_row, text="Enter as:", fg=DIM, bg=BG,
                 font=F_SMALL).pack(side="left")
        mode_lbls = {}

        def _set_mode(m):
            prev = _prev_mode[0]
            _prev_mode[0] = m
            v_mode.set(m)
            cur = v_dur.get().strip()
            if cur:
                # Parse value from the previous mode
                frames = None
                if prev == "tc":
                    frames = parse_tc(cur, fps_key)
                elif prev == "frames":
                    try:    frames = int(cur)
                    except: frames = None
                elif prev == "ff":
                    frames = parse_ff(cur, film_format)
                # Re-format in the new mode
                if frames is not None:
                    if m == "tc":
                        v_dur.set(frames_to_tc(frames, fps_key))
                    elif m == "frames":
                        v_dur.set(str(frames))
                    elif m == "ff":
                        v_dur.set(frames_to_ff(frames, film_format))
            _retoggle(mode_lbls, m)
            lbl_hint.config(text=_hint())

        _mode_options = [("tc", "Timecode"), ("frames", "Frames")]
        if film_format != "digital":
            _mode_options.insert(1, ("ff", "Feet+Frames"))

        for mk, ml in _mode_options:
            mode_lbls[mk] = _toggle_lbl(mode_row, ml,
                                         active=(mk == "tc"),
                                         command=lambda m=mk: _set_mode(m),
                                         font=F_SMALL, padx=10, pady=3)

        def _hint():
            m = v_mode.get()
            if m == "tc":
                return "Format:  H:MM:SS:FF  or  MM:SS:FF"
            if m == "ff":
                return f"Format:  feet+frames  (e.g. 1234+08,  0–{_fpf - 1} frames)"
            return "Enter raw frame count  (e.g. 31630)"

        # Duration entry
        init_val = frames_to_tc(seg.get("frames", 0), fps_key) if seg else ""
        v_dur = tk.StringVar(value=init_val)
        tk.Label(body, text="Duration:", fg=DIM, bg=BG,
                 font=F_SMALL).pack(anchor="w", pady=(6, 2))
        e_dur = tk.Entry(body, textvariable=v_dur, bg=ENTRY_BG, fg=TEXT,
                         insertbackground=TEXT, relief="flat",
                         font=("Avenir Next", 18, "bold"),
                         highlightthickness=1, highlightbackground="#444444",
                         highlightcolor=ACCENT, width=22)
        e_dur.pack(anchor="w")
        def _focus_initial():
            if focus_name:
                e_name.focus_set()
                e_name.select_range(0, "end")
            else:
                e_dur.focus_set()
                e_dur.select_range(0, "end")
                e_dur.icursor("end")
        dlg.after(60, _focus_initial)

        lbl_hint = tk.Label(body, text=_hint(), fg=DIM, bg=BG, font=F_SMALL)
        lbl_hint.pack(anchor="w", pady=(4, 0))

        # Quick Entry hint + auto-tab checkbox
        if seg_idx is not None and seg_idx + 1 < len(proj["segments"]):
            qe_row = tk.Frame(body, bg=BG)
            qe_row.pack(fill="x", pady=(6, 0))
            tk.Label(qe_row, text="↵  Quick Entry — Enter saves and advances to next",
                     fg=ACCENT, bg=BG, font=F_SMALL).pack(side="left")
            tk.Checkbutton(qe_row, text="auto-tab to name",
                           variable=self._quick_entry_to_name,
                           fg=DIM, bg=BG, selectcolor=BG,
                           activebackground=BG, activeforeground=TEXT,
                           font=F_SMALL).pack(side="right")
        else:
            tk.Label(body, text="↵  Press Enter to save",
                     fg=ACCENT, bg=BG, font=F_SMALL).pack(anchor="w", pady=(6, 0))

        lbl_err = tk.Label(body, text="", fg=RED, bg=BG, font=F_SMALL)
        lbl_err.pack(anchor="w", pady=(3, 0))

        btn_row = tk.Frame(body, bg=BG)
        btn_row.pack(fill="x", pady=(14, 0))

        def _save(advance=False):
            dur_str = v_dur.get().strip()
            if not dur_str:
                lbl_err.config(text="Please enter a duration.")
                return
            _m = v_mode.get()
            if _m == "ff":
                frames = parse_ff(dur_str, film_format)
            else:
                frames = parse_tc(dur_str, fps_key, compact=(_m == "tc"))
            if frames is None or frames < 0:
                lbl_err.config(text="Invalid duration — check format and try again.")
                return
            record = {"frames": frames, "name": v_name.get().strip()}
            # v_color[0] is None  → no custom colour (use auto-default)
            # v_color[0] is a hex → save it (user picked, or carried over from existing seg)
            if v_color[0] is not None:
                record["color"] = v_color[0]
            if is_new:
                proj["segments"].append(record)
            else:
                proj["segments"][seg_idx] = record
            save_data(self._data)
            dlg.destroy()
            self._show_project_detail(project_id)
            # Advance to next segment if Enter was used and one exists
            if advance and seg_idx is not None:
                next_idx = seg_idx + 1
                if next_idx < len(proj["segments"]):
                    fn = self._quick_entry_to_name.get()
                    self.root.after(80, lambda: self._add_edit_segment(project_id, next_idx,
                                                                       focus_name=fn))

        def _remove():
            if messagebox.askyesno(f"Remove {seg_lbl}",
                                    f"Remove {seg_lbl} {num}?", parent=dlg):
                proj["segments"].pop(seg_idx)
                save_data(self._data)
                dlg.destroy()
                self._show_project_detail(project_id)

        def _lbtn(parent, text, bg, fg, cmd, font=F_MAIN, padx=16, pady=6, side="left", px=0):
            hov = _hover_color(bg)
            b = tk.Label(parent, text=text, bg=bg, fg=fg, font=font,
                         padx=padx, pady=pady, cursor="hand2")
            b.pack(side=side, padx=px)
            b.bind("<Button-1>", lambda _: cmd())
            b.bind("<Enter>",    lambda _: b.config(bg=hov))
            b.bind("<Leave>",    lambda _: b.config(bg=bg))
            return b

        _lbtn(btn_row, "OK",     ACCENT,    "#111111", _save,       font=F_BOLD, padx=22)
        _lbtn(btn_row, "Cancel", BTN,        TEXT,      dlg.destroy, padx=16,   px=8)
        if not is_new:
            _lbtn(btn_row, f"Remove {seg_lbl}", RED, "white", _remove,
                  font=F_SMALL, padx=12, side="right")

        _saved = [False]
        def _save_once(advance=False):
            if _saved[0]: return
            _saved[0] = True
            _save(advance=advance)

        _ENTER_CODES = {36, 76, 1275068419}
        def _dur_any_key(ev):
            ks = ev.keysym or ''
            if 'Return' in ks or 'Enter' in ks or ev.keycode in _ENTER_CODES:
                _save_once(advance=True)

        e_dur.bind("<Return>",    lambda _: _save_once(advance=True))
        e_dur.bind("<KP_Enter>",  lambda _: _save_once(advance=True))
        e_dur.bind("<ISO_Enter>", lambda _: _save_once(advance=True))
        e_dur.bind("<Key>",       _dur_any_key)
        # NOTE: no <KeyRelease> — it leaks into the next dialog's e_dur when
        # focus transfers during the 80ms auto-advance delay, causing
        # every other segment to be skipped (same bug as inline TC editor).

        # When focus starts on the name field (Quick Entry with auto-tab),
        # pressing Enter/Tab moves to the duration entry rather than saving.
        def _name_to_dur(_event=None):
            e_dur.focus_set()
            e_dur.select_range(0, "end")
            e_dur.icursor("end")
            return "break"
        e_name.bind("<Return>",   _name_to_dur)
        e_name.bind("<KP_Enter>", _name_to_dur)
        e_name.bind("<Tab>",      _name_to_dur)

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
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
                    _app_name = _msg(_objc.objc_getClass(b'NSString'), _objc.sel_registerName(b'stringWithUTF8String:'), b'Reel Time Plus')
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
    ReelTimePlus(root)

    if _IS_WINDOWS:
        # Enable WS_EX_COMPOSITED so Windows renders the whole window
        # off-screen before painting — eliminates widget rebuild flicker.
        def _apply_compositing():
            try:
                import ctypes
                hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
                if not hwnd:
                    hwnd = root.winfo_id()
                GWL_EXSTYLE      = -20
                WS_EX_COMPOSITED = 0x02000000
                style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
                ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE,
                                                    style | WS_EX_COMPOSITED)
            except Exception:
                pass
        root.after(100, _apply_compositing)

    root.mainloop()


if __name__ == "__main__":
    main()

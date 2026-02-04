# -*- coding: utf-8 -*-
# Version: 3.9.3b
# See github page to report issues or to contribute:
# https://github.com/AndreyKaiu/advanced-browser-mod-kaiu-2026
#
# Original author code:
# https://github.com/hssm/advanced-browser

# from . import debug_print # for debugging, output to file "~/anki_print.log"
from . import advancedbrowser

# ========== ⬇⬇⬇⬇⬇ show version information only once ⬇⬇⬇⬇⬇ ==========
import os
from aqt import mw
from aqt.utils import showText
from aqt.qt import QTimer

addon_dir = mw.addonManager.addonFromModule(__name__)
meta = mw.addonManager.addonMeta(addon_dir)
addon_name = meta.get("name", "???")
human_version = meta.get("human_version", "3.9.3b")
version_addon = "Version: " + human_version

msgHTML = """
<style>
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; margin: 0px; padding: 0px; backgrount-color: white;}
    h2 { text-align: center; margin-bottom: 5px; }
    h3 { color: #888; text-align: center; margin-top: 0; font-weight: normal; }
    h4 { color: #4a9eff; margin-top: 20px; margin-bottom: 10px; border-bottom: 1px solid #444; padding-bottom: 5px; }
    .section { margin-bottom: 15px; }
    .shortcut { display: inline-block; font-family: monospace; font-weight: bold; }
    ul { margin: 5px 0; padding-left: 20px; }
    li { margin: 4px 0; }
</style>""" + f"""<h2>{addon_name}<br>{version_addon}</h2>""" + """
<b>Important changes!</b> <br>
Since the "F5" hotkey was used to record audio, and the "F8" hotkey was used to select text color, the hotkeys have changed in this version: <br>
<br>
F5 ⭢ Shift+F9 <br>
F8 ⭢ F10 <br>
"""

def showText_version_addon() -> None:
    global msgHTML, addon_name, version_addon
    showText(msgHTML, type="html", title=f"""Add-on "{addon_name}";  {version_addon}""")

def show_update_once():

    # change the key if you need to show significant changes to the user  
    update_Addon_Key = 'update_Addon_1334324384_20260204'
    try:        
        if mw.pm.profile is None:
            print("ERROR: mw.pm.profile is None")
            return            
        update_Addon = mw.pm.profile.get(update_Addon_Key, '')
        
    except Exception as e:
        print(f"Error getting value: {e}")
        update_Addon = ''

    if update_Addon == '':        
        if mw.pm.profile is not None:
            mw.pm.profile[update_Addon_Key] = 'True'
        showText_version_addon()
    
# shows after 2 seconds so that the profile has time to load    
QTimer.singleShot(2000, show_update_once)


# ========== ⬆⬆⬆⬆⬆ show version information only once ⬆⬆⬆⬆ ==========   

    




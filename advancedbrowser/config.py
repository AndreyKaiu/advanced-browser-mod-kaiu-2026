# -*- coding: utf-8 -*-
# Version: 4.0.3b
# See github page to report issues or to contribute:
# https://github.com/AndreyKaiu/advanced-browser-mod-kaiu-2026
#
# Original author code:
# https://github.com/hssm/advanced-browser
import aqt
from anki.hooks import addHook, remHook
from aqt import mw

from .internal_fields import iff

singleList = False
userOption = None


def getUserOption():
    global userOption
    if userOption is None:
        userOption = aqt.mw.addonManager.getConfig(__name__)
    return userOption


def getCardInfoDialogAlwaysOnTop():
    return getUserOption().get("Card Info Dialog Always On Top", True)


def getEachFieldInSingleList():
    return getUserOption().get("Use a single list for fields", False)   


def getUseInternalFields():
    return getUserOption().get("Show internal fields", False)

def getShowNoteCounts():
    return getUserOption().get("Show note counts", False)

def getNoteModeShortcut():
    return getUserOption().get("Keyboard shortcut for note browser mode", "Ctrl+Alt+N")


def getSelectable():
    return getUserOption().get("Table content", "No interaction")
    
    
def getHideButton():
    quo = getUserOption().get("Hide the button for which the value is set to one", "000000000")
    if quo == "" or quo == "0" or quo == "false":
        quo = "000000000"
    elif quo == "true" or quo == "1":
        quo = "111111111"
    return [x == "1" for x in quo]
    
def getHideALLButton():
    mh = getHideButton()
    return all(mh)
    
def getHideQueryString():
    return getUserOption().get("Hide the query string used to generate the table", False) 

def getHideCustomRrowHighlighting():
    return getUserOption().get("Hide custom row highlighting", False)
    

def getColumnAlignment():
    return getUserOption().get("Column alignment", "Start")

def update(_):
    global userOption
    userOption = None
    processInternal()


def processInternal():
    fn = addHook if getUseInternalFields() else remHook
    fn("advBrowserLoaded", iff.onAdvBrowserLoad)
    fn("advBrowserBuildContext", iff.onBuildContextMenu)


processInternal()

mw.addonManager.setConfigUpdatedAction(__name__, update)

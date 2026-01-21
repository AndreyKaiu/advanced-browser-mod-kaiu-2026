# -*- coding: utf-8 -*-
# Version: 3.9.1b
# See github page to report issues or to contribute:
# https://github.com/AndreyKaiu/advanced-browser-mod-kaiu-2026
#
# Original author code:
# https://github.com/hssm/advanced-browser

from __future__ import annotations # to make it work | in old anki on Python 3.9

# Advanced Browser modules
from . import basic_fields, config, advanced_fields, note_fields
from .core import AdvancedBrowser
import anki.lang
from aqt import mw
from .localization.lang import set_lang
from aqt.utils import (showText, showInfo, tooltip) 

from .localization.lang import q

config = mw.addonManager.getConfig(__name__)
lng = config.get("Language", "")

if lng == "":
    current_language = anki.lang.current_lang #en, pr-BR, en-GB, ru and the like
    sl = set_lang(current_language)
    if not sl:
        text = f"""ERROR ADVANCEDBROWSER! The file '{current_language+".lng"}' was not found or the file's contents could not be loaded correctly."""
        tooltip(text)       
else:
    sl = set_lang(lng)
    if not sl:
        text = f"""ERROR ADVANCEDBROWSER! The file '{lng+".lng"}' was not found or the file's contents could not be loaded correctly."""
        tooltip(text)



from aqt import mw
from aqt.qt import *
from aqt.qt import QTimer, QAction
from aqt.browser import Browser


# Low-level Qt classes (layout engine) take like this
try:
    from PyQt6.QtWidgets import QAbstractItemView, QFrame, QStyle, QLabel, QHBoxLayout, QVBoxLayout, QLayout, QWidgetItem, QSpacerItem, QSizePolicy, QDialogButtonBox
    from PyQt6.QtCore import QRect, QPoint, QSize
    from PyQt6.QtGui import QShortcut, QKeySequence
    pyqt_version = "PyQt6"
except ImportError:
    from PyQt5.QtWidgets import QAbstractItemView, QFrame, QStyle, QLabel, QHBoxLayout, QVBoxLayout, QLayout, QWidgetItem, QSpacerItem, QSizePolicy, QDialogButtonBox
    from PyQt5.QtCore import QRect, QPoint, QSize
    from PyQ5.QtGui import QShortcut, QKeySequence
    pyqt_version = "PyQt5"


original_init = Browser.__init__

def patched_init(self, *args, **kwargs):
    original_init(self, *args, **kwargs)

    # We are waiting for complete initialization
    QTimer.singleShot(50, lambda: self.setup_double_click_handler())
    
    toggle_action = self.findChild(QAction, "actionToggleSidebar")
    if toggle_action:
        toggle_action.setShortcut(QKeySequence("Ctrl+Alt+R"))

    # align not to the center, but to the left, it’s more convenient and cuts off the edges when the name is long
    try:
        view = self.table._view
        header = view.horizontalHeader()
        model = view.model()        
        if pyqt_version == "PyQt6":            
            header.setDefaultAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        else:            
            header.setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        header.update()
    
    except Exception as e:
        print(f"Error updating alignment of column: {e}")



Browser.__init__ = patched_init


original_update_history = Browser.update_history
def patched_update_history(self) -> None:
        assert self.mw.pm.profile is not None

        sh = self.mw.pm.profile.get("searchHistory", [])
        if self._lastSearchTxt in sh:
            sh.remove(self._lastSearchTxt)
        sh.insert(0, self._lastSearchTxt)
        sh = sh[:100] # :30 a little
        self.form.searchEdit.clear()
        self.form.searchEdit.addItems(sh)
        self.mw.pm.profile["searchHistory"] = sh
Browser.update_history = patched_update_history




from aqt.browser.table import Table
from collections.abc import Callable, Sequence


original_search = Table.search
def patched_search(self, txt: str) -> None:
    try:
        if txt == "":
            txt = "deck:*"
        if hasattr(self.browser, '_label_request') and self.browser._label_request:
            self.browser._label_request.setText(txt)
    except:
        pass

    original_search(self, txt)

    def _update_navigation_buttons(self, sah):
        """Updates the state of history navigation buttons."""
        if not hasattr(self.browser, '_btn_back') or not hasattr(self.browser, '_btn_forward'):
            return
        
        # Back button
        if len(sah) > 1 and self.browser._all_history_n < len(sah) - 1:
            self.browser._btn_back.setEnabled(True)
            tooltip = q("q_Back") + " [Alt+Left]  " + sah[self.browser._all_history_n+1]             
        else:
            self.browser._btn_back.setEnabled(False)
            tooltip = q("q_Back") + " [Alt+Left]"
        self.browser._btn_back.setToolTip(tooltip)     

        
        # Forward button
        if self.browser._all_history_n > 0:
            self.browser._btn_forward.setEnabled(True)
            tooltip = q("q_Forward") + " [Alt+Right]  " + sah[self.browser._all_history_n-1]
        else:
            self.browser._btn_forward.setEnabled(False)
            tooltip = q("q_Forward") + " [Alt+Right]"
        self.browser._btn_forward.setToolTip(tooltip)


    sah = self.browser.mw.pm.profile.get("searchlist_all_history", [])
    # Initialize the pointer if it does not exist
    if not hasattr(self.browser, '_all_history_n'):
        self.browser._all_history_n = -1        

    if txt == "deck:current" and self.browser._line_edit().text() == "":
        self.browser._line_edit().setText("deck:current")    
    
    if hasattr(self.browser, '_go_back_or_go_forward') and self.browser._go_back_or_go_forward == True:
        pass # don't remember anything when moving
    else:
        pressF5 = False # Pressing F5 is processed in a special way
        if hasattr(self.browser, '_pressF5') and self.browser._pressF5 == True:
            pressF5 = True

        separator = " cid:"         
        card_ids = self.browser.table.get_selected_card_ids() 
        str_card_ids = ""
        try:  
            if card_ids: 
                str_card_ids = str(card_ids[0]) 
        except:
            str_card_ids = ""

        rq = ""
        cid = ""
        # if the index is correct
        if self.browser._all_history_n >= 0 and self.browser._all_history_n < len(sah):
            try:
                # we get the request itself and cid
                cr_txt = sah[self.browser._all_history_n]            
                index_sep = cr_txt.rfind(separator)
                rq = cr_txt[:index_sep]
                cid = cr_txt[index_sep + len(separator):]   
            except:
                pass
                    
        # if you pressed F5 and the request has not changed, then we will update only the card_ids
        if pressF5 and rq.strip() != "" and rq.strip() == txt.strip() and str_card_ids != "":
            # replace it with it
            sah[self.browser._all_history_n] = rq + separator + str_card_ids    
        else:
            self.browser._all_history_n = 0 # list pointer to 1 element            
            txt += separator + str_card_ids
            # Check if the current search is already the first in history
            if not sah or (sah and sah[0] != txt):            
                # Add to the beginning of the list
                sah.insert(0, txt)        
                # Limiting the history size
                if len(sah) > 100:
                    sah = sah[:100]  # We leave only the last 100 requests

    self.browser._pressF5 = False

    # Update the state of the buttons
    _update_navigation_buttons(self, sah)
    
    self.browser.mw.pm.profile["searchlist_all_history"] = sah 

Table.search = patched_search



original__save_selection = Table._save_selection
def patched__save_selection(self) -> None:
    original__save_selection(self)   

    try:
        if self.is_notes_mode():
            if not hasattr(self, '_self_notes_mode'):                
                self._self_notes_mode = type('SaveObject', (), {})()
            sonm = self._self_notes_mode
        else:
            if not hasattr(self, '_self_cards_mode'):                
                self._self_cards_mode = type('SaveObject', (), {})()
            sonm = self._self_cards_mode 

        try:
            sonm._save_top_row = self._current().row()
        except:
            sonm._save_top_row = None 
        sonm._save_current_column = self._current().column() 
        sonm._save_current_columnVI = self._horizontal_header().visualIndex(sonm._save_current_column)    
        hsbar = self._view.horizontalScrollBar()
        if hsbar is not None:
            sonm._save_horizontalScrollBar_val = hsbar.value() 
            sonm._save_horizontalScrollBar_max = hsbar.maximum()
    except:
        pass
Table._save_selection = patched__save_selection  
        

original__restore_selection = Table._restore_selection
def patched__restore_selection(self, new_selected_and_current: Callable) -> None:
    original__restore_selection(self, new_selected_and_current)  
    
    try:
        if self.is_notes_mode():
            if not hasattr(self, '_self_notes_mode'):                
                self._self_notes_mode = type('SaveObject', (), {})()
            sonm = self._self_notes_mode
        else:
            if not hasattr(self, '_self_cards_mode'):                
                self._self_cards_mode = type('SaveObject', (), {})()
            sonm = self._self_cards_mode 
        
        try:
            sonm._save_top_row = self._current().row()
        except:
            sonm._save_top_row = None 

        if hasattr(sonm, '_save_top_row') and sonm._save_top_row is not None:                                               
            self._set_current(sonm._save_top_row, sonm._save_current_columnVI)            
            hsbar = self._view.horizontalScrollBar()
            if hsbar is not None:
                hsbar.setMaximum(sonm._save_horizontalScrollBar_max)
                hsbar.setValue(sonm._save_horizontalScrollBar_val)
            # self._scroll_to_column(sonm._save_current_columnVI) there's no need for that
               
    except:
        pass
Table._restore_selection = patched__restore_selection
    


from aqt.utils import (
    KeyboardModifiersPressed,
    askUser,
    getOnlyText,
    showInfo,
    showWarning,
    tooltip,
    tr,
)
from anki.collection import (
    Config,
    OpChanges,
    OpChangesWithCount,
    SearchJoiner,
    SearchNode,
)

from aqt.browser.sidebar.tree import SidebarTreeView 

original_update_search = SidebarTreeView.update_search


def patched_update_search(
        self,
        *terms: str | SearchNode,
        joiner: SearchJoiner = "AND",
    ) -> None:
    """Modify the current search string based on modifier keys, then refresh.
    The algorithm has been changed so that simply pressing Ctrl and then Shift again will not create the same query a second time,
    because he will consider this a desire to correct it.
    Ctrl+Shift replaces taking into account the inversion sign -
    Ctrl+Win or Shift+Win will erase when clicking on the same item as before.
    """
    mods = KeyboardModifiersPressed()
        
    # Get current search string
    current_search_text = self.browser.current_search().rstrip()    
    operators = ["AND", "OR"]
    for operator in operators:
        # Remove " operator" pattern (space before operator)
        if current_search_text.endswith(f" {operator}"):
            current_search_text = current_search_text[:-len(operator)-1].rstrip()

    # current_search_text = strip_outer_parentheses(current_search_text) 
    previous = SearchNode(parsable_text=current_search_text)
    current = self.mw.col.group_searches(*terms, joiner=joiner)
    
    # Convert current search node to text for comparison
    current_text = self.col.build_search_string(current).strip()

    if not(mods.control and mods.shift):    
        trimmed_text = ""
        # Check if current search ends with the new search term   
        if current_search_text.strip().endswith(current_text):
            # Remove the current_text from the end of previous search
            trimmed_text = current_search_text.rstrip()
            
            # Remove the current search term from the end
            if trimmed_text.endswith(current_text):
                trimmed_text = trimmed_text[:-len(current_text)].rstrip()

                # Remove trailing minus (negation operator)
                if trimmed_text.endswith("-"):
                    trimmed_text = trimmed_text[:-1].rstrip()
                
                # Remove trailing AND/OR operators and whitespace
                # Handle different possible endings
                operators = ["AND", "OR"]
                for operator in operators:
                    # Remove " operator" pattern (space before operator)
                    if trimmed_text.endswith(f" {operator}"):
                        trimmed_text = trimmed_text[:-len(operator)-1].rstrip()                                    
                
                if trimmed_text:
                    try:
                        previous = SearchNode(parsable_text=trimmed_text)
                    except:
                        previous = None
                else:
                    previous = None

    # if Alt pressed, invert
    if mods.alt and not(mods.control and mods.shift): # error correction when does not replace with Alt
        current = SearchNode(negated=current)

    try:        
        if mods.meta and (mods.control or mods.shift):
            if trimmed_text:
                search = trimmed_text
            else:
                search = current_search_text
        else:
            if previous is None:
                search = self.col.build_search_string(current)    
            else:
                if mods.control and mods.shift:
                    # If Ctrl+Shift, replace searches nodes of the same type.
                    # Use the potentially modified previous node
                    search = self.col.replace_in_search_node(previous, current)                
                    # error correction when does not replace with Alt
                    search = search.replace("-"+current_text, current_text)  
                    if mods.alt:                                       
                        search = search.replace(current_text, "-"+current_text)
                elif mods.control:
                    # If Ctrl, AND with previous
                    search = self.col.join_searches(previous, current, "AND")
                elif mods.shift:
                    # If Shift, OR with previous
                    search = self.col.join_searches(previous, current, "OR")
                else:
                    search = self.col.build_search_string(current)
    except Exception as e:
        showWarning(str(e))
    else:
        self.browser.search_for(search)


SidebarTreeView.update_search = patched_update_search             


 
def setup_double_click_handler(self):
    """Setting up a double click handler."""
    if not hasattr(self, 'table') or not hasattr(self.table, '_view'):
        return
    
    view = self.table._view
    
    def on_double_click(index):
        if not index.isValid():
            return
        
        # print(f"Double click in browser: [{index.row()}, {index.column()}]")
        
        def get_column_name_from_index(browser: Browser, column_index: int) -> str | None:
            """
           Gets the name of a column by its index in the browser table.            
            Args:
                browser: Anki browser object
                column_index: Index of a column in the table                
            Returns:
                Column name (for example 'Front', 'Back') or None
            """
            if not hasattr(browser, 'table') or not hasattr(browser.table, '_model'):
                return None            
            model = browser.table._model            
            #Getting a column by index
            try:
                column = model.column_at_section(column_index)
                if column:
                    return column.key
            except (IndexError, AttributeError):
                pass            
            return None
        

        def get_field_index_from_column_name(browser: Browser, column_name: str) -> int | None:
            """
            Gets the editor field index by column name.            
            Args:
                browser: Anki browser object
                column_name: Column name (eg 'Front', 'Back')                
            Returns:
                Field index in editor or None
            """
            if not browser.editor or not browser.editor.note:
                return None
            
            note = browser.editor.note
            model = note.model()
            
            if not model or 'flds' not in model:
                return None
            
            # We go through the fields and look for the corresponding
            fields = model['flds']
            for field_index, field in enumerate(fields):
                field_name = field.get('name', '')
                # Comparing field names (taking into account possible differences in formatting)
                if field_name.strip().lower() == column_name.strip().lower():
                    return field_index
            
            #trying to find additional fields "_field_"
            fields = model['flds']
            for field_index, field in enumerate(fields):
                field_name = field.get('name', '')
                # Comparing field names (taking into account possible differences in formatting)
                if "_field_"+field_name.strip().lower() == column_name.strip().lower():
                    return field_index


            # If there is no exact match, we try to find by partial match
            column_name_lower = column_name.strip().lower()
            for field_index, field in enumerate(fields):
                field_name = field.get('name', '').strip().lower()
                if column_name_lower in field_name or field_name in column_name_lower:
                    return field_index
            
            return None

        column_name = get_column_name_from_index(self, index.column())

        # print("column_name=", column_name)

        # We get the index of the corresponding field
        field_index = get_field_index_from_column_name(self, column_name)
        
        if field_index is not None:
            # Activate the editor with the selected field
            self.editor.web.setFocus()
            # Using a timer to ensure that focus is set after the editor opens
            QTimer.singleShot(50, lambda: self.editor.loadNote(focusTo=field_index))
        else:
            # # If the field is not found, activate the editor with the first field
            # self.editor.web.setFocus()
            # self.editor.loadNote(focusTo=0)
            pass        
    
    view.doubleClicked.connect(on_double_click)
        


Browser.setup_double_click_handler = setup_double_click_handler







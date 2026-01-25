# -*- coding: utf-8 -*-
# Version: 3.9.2b
# See github page to report issues or to contribute:
# https://github.com/AndreyKaiu/advanced-browser-mod-kaiu-2026
#
# Original author code:
# https://github.com/hssm/advanced-browser

from __future__ import annotations # to make it work | in old anki on Python 3.9

import time
from anki.collection import BrowserColumns
from anki.browser import BrowserConfig
from anki.hooks import runHook, wrap
from anki.utils import pointVersion
from aqt.utils import (showText, showInfo, tooltip, showWarning) 
from aqt import *
from aqt.qt import *
from aqt import gui_hooks
from aqt.browser import Column as BuiltinColumn, DataModel, SearchContext, CardState, NoteState
from anki.errors import NotFoundError, SearchError
from typing import Dict, Optional

from . import config
import datetime
import json
import re
import os
from markdown import markdown
from .column import Column, CustomColumn
from .contextmenu import ContextMenu

from .localization.lang import q


# Low-level Qt classes (layout engine) take like this
try:
    from PyQt6.QtWidgets import QAbstractItemView, QFrame, QStyle, QLabel, QHBoxLayout, QVBoxLayout, QLayout, QWidgetItem, QSpacerItem, QSizePolicy, QDialogButtonBox
    from PyQt6.QtCore import QRect, QPoint, QSize
    from PyQt6.QtGui import QShortcut, QKeySequence
    QMessageBox_No = QMessageBox.StandardButton.No
    QMessageBox_Yes = QMessageBox.StandardButton.Yes
    pyqt_version = "PyQt6"
except ImportError:
    from PyQt5.QtWidgets import QAbstractItemView, QFrame, QStyle, QLabel, QHBoxLayout, QVBoxLayout, QLayout, QWidgetItem, QSpacerItem, QSizePolicy, QDialogButtonBox
    from PyQt5.QtCore import QRect, QPoint, QSize
    from PyQ5.QtGui import QShortcut, QKeySequence   
    QMessageBox_No = QMessageBox.No 
    QMessageBox_Yes = QMessageBox.Yes
    pyqt_version = "PyQt5"

            

def show_wait_cursor():
    """Show wait cursor for the entire application."""
    QApplication.setOverrideCursor(QCursor(Qt.CursorShape.WaitCursor))
    mw.app.processEvents()  # Update UI


def restore_cursor():
    """Restore normal cursor."""
    QApplication.restoreOverrideCursor()
    mw.app.processEvents()            


# ⬇⬇⬇⬇⬇ kaiu: 2026-01-05 SHOW AND COLOR ON SELECTION ⬇⬇⬇⬇⬇ +++++ 
from aqt.browser.table.table import StatusDelegate
from aqt.theme import theme_manager
from anki.collection import BrowserRow
from aqt.qt import QItemDelegate, QBrush, QPalette, QStyleOptionViewItem, QApplication, QColor, QPen, QWidget, QCheckBox, QCursor, QDialog, QFileDialog, QInputDialog, QMenu, QPushButton, QScrollArea, QSizePolicy, QSlider, QThreadPool, QToolTip, QVBoxLayout,QTimer, Qt
from aqt import colors
from anki.consts import *
import copy

def on_fetch_row(card_id, is_note, row, columns):
    if is_note:
        return
    card = mw.col.get_card(card_id)
    note = card.note()
    row.is_marked = note.has_tag("marked")
    row.is_suspended = card.queue == QUEUE_TYPE_SUSPENDED
    row.is_buried = card.queue in (QUEUE_TYPE_MANUALLY_BURIED, QUEUE_TYPE_SIBLING_BURIED)
    row.flag = card.userFlag()
gui_hooks.browser_did_fetch_row.append(on_fetch_row)


def backend_color_to_aqt_color(color) -> dict[str, str] | None:  #This is only possible for Python 3.10+
# def backend_color_to_aqt_color(color) -> Union[Dict[str, str], None]: #Python 3.9 
    
    temp_color = None

    if color == BrowserRow.COLOR_MARKED:
        temp_color = colors.STATE_MARKED
    if color == BrowserRow.COLOR_SUSPENDED:
        temp_color = colors.STATE_SUSPENDED
    if color == BrowserRow.COLOR_BURIED:
        temp_color = colors.STATE_BURIED
    if color == BrowserRow.COLOR_FLAG_RED:
        temp_color = colors.FLAG_1
    if color == BrowserRow.COLOR_FLAG_ORANGE:
        temp_color = colors.FLAG_2
    if color == BrowserRow.COLOR_FLAG_GREEN:
        temp_color = colors.FLAG_3
    if color == BrowserRow.COLOR_FLAG_BLUE:
        temp_color = colors.FLAG_4
    if color == BrowserRow.COLOR_FLAG_PINK:
        temp_color = colors.FLAG_5
    if color == BrowserRow.COLOR_FLAG_TURQUOISE:
        temp_color = colors.FLAG_6
    if color == BrowserRow.COLOR_FLAG_PURPLE:
        temp_color = colors.FLAG_7

    return adjusted_bg_color(temp_color)

def adjusted_bg_color(color: dict[str, str] | None) -> dict[str, str] | None: # This is only possible for Python 3.10+
# def adjusted_bg_color(color: Union[Dict[str, str], None]) -> Union[Dict[str, str], None]: #Python 3.9 
    
    if color:
        adjusted_color = copy.copy(color)
        light = QColor(color["light"]).lighter(150)
        adjusted_color["light"] = light.name()
        dark = QColor(color["dark"]).darker(150)
        adjusted_color["dark"] = dark.name()
        return adjusted_color
    else:
        return None
    
def qcolor_from_br_color(BrowserRowCOLOR):    
    aqt_color = backend_color_to_aqt_color(BrowserRowCOLOR)
    if not aqt_color:
        return None
    return theme_manager.qcolor(aqt_color)


def flag_number_to_qcolor(flag_number: int):
    flag_map = {
        1: BrowserRow.COLOR_FLAG_RED,
        2: BrowserRow.COLOR_FLAG_ORANGE,
        3: BrowserRow.COLOR_FLAG_GREEN,
        4: BrowserRow.COLOR_FLAG_BLUE,
        5: BrowserRow.COLOR_FLAG_PINK,
        6: BrowserRow.COLOR_FLAG_TURQUOISE,
        7: BrowserRow.COLOR_FLAG_PURPLE,
    }

    backend_color = flag_map.get(flag_number)
    if not backend_color:
        return None

    # we get the color taking into account the theme
    aqt_color = backend_color_to_aqt_color(backend_color)
    if not aqt_color:
        return None

    return theme_manager.qcolor(aqt_color)

   
_originalStatusDelegate__init__ = StatusDelegate.__init__
def patched__originalStatusDelegate__init__(self, browser: aqt.browser.Browser, model: DataModel):
        _originalStatusDelegate__init__(self, browser, model)        
        self._browser = browser
StatusDelegate.__init__ = patched__originalStatusDelegate__init__         

_original_paint = StatusDelegate.paint 
def patched_paint(self, painter, option, index):
    rect = option.rect
    row = self._model.get_row(index)         
    is_marked = getattr(row, "is_marked", False)
    is_suspended = getattr(row, "is_suspended", False)
    is_buried = getattr(row, "is_buried", False)
    usfl = getattr(row, "flag", 0)

    issel = (option.state & QStyle.StateFlag.State_Selected)    
    # remove the Selected flag so that Qt does not draw the selection background
    if option.state & QStyle.StateFlag.State_Selected:
        option = QStyleOptionViewItem(option)
        option.state &= ~QStyle.StateFlag.State_Selected
   
    option.textElideMode = self._model.get_cell(index).elide_mode
    if self._model.get_cell(index).is_rtl:
        option.direction = Qt.LayoutDirection.RightToLeft    
    
    if row_color := self._model.get_row(index).color:        
        assert painter
        painter.save()
        
        w = rect.width() 
        if is_suspended or is_buried: # x??
            if is_marked and (usfl > 0):
                w2 = w // 3                
                w3 = w - 2*w2
                rectF = rect.adjusted(0, 0, -w2-w3, 0) # x-- 
            elif (is_marked and not (usfl > 0)) or (not is_marked and (usfl > 0)):
                w1 = w // 2
                w2 = w - w1
                rectF = rect.adjusted(0, 0, -w2, 0) # x-            
            else:
                rectF = rect # xxx
                
            if is_suspended:
                color = qcolor_from_br_color(BrowserRow.COLOR_SUSPENDED)                                                      
            elif is_buried:
                color = qcolor_from_br_color(BrowserRow.COLOR_BURIED)
            painter.fillRect(rectF, QBrush(color))

        if is_marked: # ?x?                       
            if (is_suspended or is_buried) and (usfl > 0):
                w1 = w // 3                
                w3 = w - 2*w1
                rectF = rect.adjusted(w1, 0, -w3, 0) # -x- 
            elif (is_suspended or is_buried) and not (usfl > 0):
                w1 = w // 2                
                rectF = rect.adjusted(w1, 0, 0, 0) # -x 
            elif not (is_suspended or is_buried) and (usfl > 0):
                w1 = w // 2
                w2 = w - w1
                rectF = rect.adjusted(0, 0, -w2, 0) # x- 
            else:
                rectF = rect # xxx 

            color = qcolor_from_br_color(BrowserRow.COLOR_MARKED)
            painter.fillRect(rectF, QBrush(color))

        if usfl > 0: # ??x
            if (is_suspended or is_buried) and (is_marked > 0):
                w1 = w // 3                                               
                rectF = rect.adjusted(w1+w1, 0, 0, 0) # --x 
            elif ((is_suspended or is_buried) and not (is_marked > 0)) or (not (is_suspended or is_buried) and (is_marked > 0)):
                w1 = w // 2                
                rectF = rect.adjusted(w1, 0, 0, 0) # -x            
            else:
                rectF = rect # xxx

            color = flag_number_to_qcolor(usfl)
            if color:
                painter.fillRect(rectF, QBrush(color))

        if not (is_suspended or is_buried) and not is_marked and not (usfl > 0):
            color = theme_manager.qcolor(row_color)
            painter.fillRect(rect, QBrush(color))

            
        painter.restore()

    else:
        if issel:
            assert painter
            painter.save()
            normal_bg_color = option.palette.color(QPalette.ColorRole.Base)            
            normal_bg_color.setAlpha(210)
            painter.fillRect(rect, QBrush(normal_bg_color))                         
            painter.restore()

    QItemDelegate.paint(self, painter, option, index)

    if not painter:
        return
        
    if issel:
        # draw a frame
        painter.save()
        pen = QPen(QColor("blue"))
        pen.setWidth(1)

        # Checking whether this cell is the current one in the table      
        browser_table = self._browser.table              
        if browser_table:
            # Get the currently selected cell
            current_index = browser_table._view.currentIndex()
            # print("current_index=", current_index)
            
            # Compare with the cell being drawn
            is_current = (current_index.isValid() and 
                        current_index.row() == index.row() and 
                        current_index.column() == index.column())
            
            # We get the selection model
            selection_model = browser_table._view.selectionModel()
            if selection_model:
                # Checking if a cell is selected
                is_selected = selection_model.isSelected(index)                
                # Checking whether the cell is active (has focus)
                has_focus = selection_model.currentIndex() == index                
                if has_focus:
                    pen = QPen(QColor("blue")) 
                    pen.setWidth(2)
       
        
        painter.setPen(pen)
        # draw a frame INSIDE the rect
        rect = option.rect.adjusted(1, 1, -2, -2)
        painter.drawRect(rect)
        painter.restore()

StatusDelegate.paint = patched_paint

# ⬆⬆⬆⬆⬆ kaiu: 2026-01-05 SHOW AND COLOR ON SELECTION ⬆⬆⬆⬆⬆ +++++



# ⬇⬇⬇⬇⬇ kaiu: 2026-01-12 Additional panel above the table ⬇⬇⬇⬇⬇ +++++ 


class EnhancedColumnOrderDialog(QDialog):
    """Improved dialogue with additional features."""
    
    def __init__(self, browser, parent=None):
        super().__init__(parent)
        self.browser = browser
        # Determine the browser type (notes or cards)
        if browser.table.is_notes_mode():
            self.browser_type =  'notes'
        else:
            self.browser_type = 'cards'        
        self.setup_ui()
        self.load_columns()
        self.setup_shortcuts()


    def get_current_columns_data(self):
        """Returns the current column data to be saved."""
        columns_data = []
        
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if pyqt_version == "PyQt6":
                col_data = item.data(Qt.ItemDataRole.UserRole)
            else:
                col_data = item.data(Qt.UserRole)
            
            if col_data:
                # We save only necessary information
                saved_data = {
                    'type': col_data.get('type', ''), 
                    'name': col_data.get('name', ''),
                    'logical_index': col_data.get('logical_index', i),
                    'width': col_data.get('width', 100),
                    'position': i  # Current position in the list
                }
                columns_data.append(saved_data)
        
        return columns_data
    


    def load_columns_from_data(self, columns_data):
        """Loads columns from data -ALL saved columns."""
        if not columns_data:
            return
        
        # Just take all the saved columns as they are
        self.original_order = columns_data.copy()
        
        # Clearing and updating the list
        self.list_widget.clear()
        self.update_list()
                


    def apply_columns_to_browser(self):
        """Applies saved columns to the browser."""
        model = self.browser.table._model
        
        # 1. Get ALL available columns
        all_columns = model.columns        
        
        # 2. Creating improved mapping
        name_to_key = self._create_enhanced_mapping(all_columns)
        
        # 3. Converting saved data into keys
        saved_keys = self._convert_names_to_keys(self.original_order, name_to_key)
        
        if not saved_keys:
            print("Could not find speaker keys")
            return
                        
        # 4. Getting the current active columns
        current_keys = model._state.active_columns
        
        # 5. CHECKING: are all keys valid?
        valid_keys = [k for k in saved_keys if k in all_columns]
        
        if not valid_keys:
            print("No valid keys")
            return
        
        # 6. IMPORTANT: We begin a complete reset of the model        
        model.begin_reset()
        
        try:
            # 7. We completely replace active speakers            
            model._state._active_columns[:] = valid_keys
            
            # 8. Save to the database (IMPORTANT: before end_reset!)
            if model._state.is_notes_mode():
                model.col.set_browser_note_columns(valid_keys)                
            else:
                model.col.set_browser_card_columns(valid_keys)                
            
        except Exception as e:
            print(f"Error updating columns: {e}")
        finally:
            # 9. We complete the model reset (this will cause a complete redraw)            
            model.end_reset()
        
        # 10. Checking the result
        final_keys = model._state.active_columns
        
        # 11. IMPORTANT: Set the width of the columns AFTER updating the model
        self._apply_column_widths_properly()
        


    def _apply_column_widths_properly(self):
        """Correctly sets the column width without stretching."""
        if not hasattr(self.browser.table, '_view'):
            return
        
        view = self.browser.table._view
        header = view.horizontalHeader()
        model = self.browser.table._model
        
        if not hasattr(model._state, 'active_columns'):
            return
        
        active_keys = model._state.active_columns
        
        
        # 1. First, SET THE MODE so that there is no stretching
        # Interactive -user can change, but auto-stretch is disabled
        header.setSectionResizeMode(header.ResizeMode.Interactive)
        
        # 2. Getting the saved widths
        width_mapping = {}
        for col_data in self.original_order:
            col_name = col_data.get('name', '').lower()
            width = col_data.get('width')
            if width:
                #We limit immediately
                width = min(width, 300)
                width_mapping[col_name] = width
                # print(f"Saved:'{col_data.get('name')}' = {width}px")
        
        # 3.Set the width for each active column
        for i, key in enumerate(active_keys):
            if key in model.columns:
                column = model.columns[key]
                col_display_name = getattr(column, 'cards_mode_label', 
                                        getattr(column, 'notes_mode_label', key))
                col_name_lower = col_display_name.lower()
                
                # Looking for the saved width
                applied_width = None
                
                # Direct match
                if col_name_lower in width_mapping:
                    applied_width = width_mapping[col_name_lower]
                
                # Partial match
                if not applied_width:
                    for saved_name, width in width_mapping.items():
                        if saved_name in col_name_lower or col_name_lower in saved_name:
                            applied_width = width
                            break
                                                
                # We guarantee restrictions
                applied_width = min(applied_width, 300)
                
                # Setting the width
                view.setColumnWidth(i, applied_width)
                # print(f" Column {i} ('{col_display_name}'): {applied_width}px")
        
        # 4. DO NOT allow stretching of the last column
        # (by default in Anki the last column is stretched)
        if active_keys:
            last_col_index = len(active_keys) - 1
            header.setSectionResizeMode(last_col_index, header.ResizeMode.Interactive) 
        
        # 5.Force display update
        view.viewport().update()
        



    def apply_columns_to_browser_with_type(self):
        """Applies stored columns based on type."""
        model = self.browser.table._model        

        # print("=== USING COLUMNS WITH TYPES ===")        
        # 1. We get ALL available columns
        all_columns = model.columns
        # print(f"Total columns in the system: {len(all_columns)}")
        
        # 2. Create a mapping type -> Column object
        # (now we use type as primary key)
        type_to_column = {key: column for key, column in all_columns.items()}
        
        # 3. Collecting types from saved data
        saved_types = []
        for col_data in self.original_order:
            col_type = col_data.get('type')
            if col_type and col_type not in saved_types:
                saved_types.append(col_type)
                # print(f"  Saved type: '{col_type}' -> '{col_data.get('name')}'")
        
        if not saved_types:
            # print("Could not find types in the saved data")
            # Let's try a simple method
            return self.apply_columns_to_browser()
        
        # print(f"\nTypes to apply: {saved_types}")
        
        # 4. We get the current active columns (by type)
        current_types = model._state.active_columns if hasattr(model._state, 'active_columns') else []
        # print(f"Current types: {current_types}")
        
        # 5. Checking what types exist in the system
        valid_types = []
        missing_types = []
        
        for col_type in saved_types:
            if col_type in all_columns:
                valid_types.append(col_type)
            else:
                missing_types.append(col_type)
                print(f"⚠️ Type '{col_type}' not found in the system!")
        
        if missing_types:
            print(f"Warning: {len(missing_types)} types not found")
        
        if not valid_types:
            print("There are no valid types to use")
            return
        
        # 6. We begin updating the model
        # print("We are starting to update the model...")
        model.begin_reset()
        
        try:
            # 7. Replacing active speakers
            # print(f"Replace active columns: {valid_types}")
            model._state._active_columns[:] = valid_types
            
            # 8. Saving in the database
            if model._state.is_notes_mode():
                model.col.set_browser_note_columns(valid_types)
                # print("Saved as note settings")
            else:
                model.col.set_browser_card_columns(valid_types)
                # print("Saved as card settings")
            
        except Exception as e:
            print(f"Error updating columns: {e}")
        finally:
            # 9. We complete the model reset
            model.end_reset()
            # print("Model updated")
        
        # 10. Apply column width
        self._apply_column_widths_with_types(type_to_column)
        self.browser.table._save_selection()
        self.browser.table._set_sort_indicator()
        self.browser.table._restore_selection(self.browser.table._intersected_selection)
        
        
        # print("Columns successfully applied with types!")

   

    def _apply_column_widths_with_types(self, type_to_column):
        """Applies column widths using types."""
        if not hasattr(self.browser.table, '_view'):
            return
        
        view = self.browser.table._view
        model = self.browser.table._model
        
        if not hasattr(model._state, 'active_columns'):
            return
        
        active_types = model._state.active_columns
        header = view.horizontalHeader()
        
        # print(f"\nApply the width for {len(active_types)} columns...")
        
        # 1. Set the mode so that there is no stretching
        header.setSectionResizeMode(header.ResizeMode.Interactive)
        
        # 2. Create a mapping type -> width from the saved data
        width_by_type = {}
        for col_data in self.original_order:
            col_type = col_data.get('type')
            width = col_data.get('width')
            if col_type and width:
                width_by_type[col_type] = min(width, 300)  # We limit
        
        # 3.Set the width for each active column
        for i, col_type in enumerate(active_types):
            if col_type in type_to_column:
                column = type_to_column[col_type]
                col_display_name = getattr(column, 'cards_mode_label', 
                                        getattr(column, 'notes_mode_label', col_type))
                
                #Determining the width
                applied_width = width_by_type.get(col_type)
                
                if not applied_width:
                    # Smart Default Width
                    if 'question' in col_type.lower() or 'answer' in col_type.lower():
                        applied_width = 200
                    elif 'deck' in col_type.lower():
                        applied_width = 150
                    elif 'tags' in col_type.lower():
                        applied_width = 180
                    else:
                        applied_width = 100
                
                # We limit
                applied_width = min(applied_width, 300)
                
                # Install
                view.setColumnWidth(i, applied_width)
                # print(f"  Column {i} ({col_type}): {applied_width}px")
        
        # 4. We prohibit stretching the last column
        if active_types:
            header.setSectionResizeMode(len(active_types) - 1, header.ResizeMode.Interactive)




    def _create_enhanced_mapping(self, all_columns):
        """Creates improved mapping of names to keys."""
        name_to_key = {}
        key_to_name = {}
        
        for key, column in all_columns.items():
            # Getting all possible names for a column
            names = []
            
            if hasattr(column, 'cards_mode_label') and column.cards_mode_label:
                names.append(column.cards_mode_label)
            
            if hasattr(column, 'notes_mode_label') and column.notes_mode_label:
                names.append(column.notes_mode_label)
            
            # Add the key itself as a name
            names.append(key)
            
            # We create a mapping for each name
            for name in names:
                name_lower = name.lower()
                name_to_key[name_lower] = key
            
            key_to_name[key] = names[0]  # First name as main name
        
        # Additional mappings for frequently used columns
        common_mappings = {
            'card': 'card',
            'note': 'note',
            'deck': 'deck',
            'created': 'noteCrt',
            'modified': 'noteMod',
            'card modified': 'cardMod',
            'tags': 'tags',
            'question': 'question',
            'answer': 'answer',
            'template': 'template',
            'type': 'template',
            'due': 'cardDue',
            'interval': 'cardIvl',
            'ease': 'cardFactor',
            'reviews': 'cardReps',
            'lapses': 'cardLapses',
        }
        
        for eng_name, key in common_mappings.items():
            if key in all_columns:
                name_to_key[eng_name] = key
        
        return name_to_key


    def _convert_names_to_keys(self, original_order, name_to_key):
        """Converts column names into keys."""
        saved_keys = []
        
        for col_data in original_order:
            col_name = col_data.get('name', '').lower()
            
            if not col_name:
                continue
            
            # Trying several search strategies
            
            # 1. Exact match
            if col_name in name_to_key:
                key = name_to_key[col_name]
                if key not in saved_keys:
                    saved_keys.append(key)
                    print(f"  Accurate: '{col_data.get('name')}' -> '{key}'")
                continue
            
            # 2. Partial match
            found = False
            for mapped_name, key in name_to_key.items():
                if (col_name in mapped_name or mapped_name in col_name):
                    if key not in saved_keys:
                        saved_keys.append(key)
                        print(f"  Partial: '{col_data.get('name')}' -> '{key}'")
                    found = True
                    break
            
            if not found:
                print(f"  Not found: '{col_data.get('name')}'")
        
        return saved_keys



        
    def file_name_from_search(self, search: str) -> str:
        ret = search
        try:
            ret = ret.replace('(', '').replace(')', '')
            ret = ret.replace('{', '_').replace('}', '_')
            ret = ret.replace('[', '_').replace(']', '_')    
            ret = ret.replace('<', '_').replace('>', '_') 
            ret = ret.replace('*', '') # we need to remove it, since we will use it as a temporary space in names in ""
            ret = re.sub(r'\s+', ' ', ret)  # Removing multiple spaces
            ret = re.sub(r'_+', '_', ret)  # Removing multiple _

            # you need to replace all spaces between " " with * 
            in_quotes_parts = re.findall(r'"([^"]*)"', ret)    
            # Replace spaces inside quotes with a temporary marker
            for part in in_quotes_parts:
                if ' ' in part:
                    # Replace spaces inside quotes with *(temporary marker)
                    replaced = part.replace(' ', '*')
                    ret = ret.replace(f'"{part}"', f'"{replaced}"')

            ret = ret.replace('::', ' ').replace('"', ' ') # now the name delimiter for deck: there will be only a space
            
            # we look for what starts with note: and if we find it, then we take everything up to the space (together with note:) and write it to ret
            # ELSE we look for what starts with deck: and if we find it, then we take everything up to the space (together with deck:) and write it to ret
            found_prefix = None
            found_text = None    
            # Looking for note:
            note_match = re.search(r'note:([^\s]+)', ret, re.IGNORECASE)
            if note_match:
                found_prefix = 'note:'
                found_text = note_match.group(1)
            else:
                # Looking for deck:
                deck_match = re.search(r'deck:([^\s]+)', ret, re.IGNORECASE)
                if deck_match:
                    found_prefix = 'deck:'
                    found_text = deck_match.group(1)
                
            if found_prefix and found_text:
                ret = found_prefix + found_text    

            ret = ret.replace('*', ' ') # return spaces inside the name            
            unsafe_chars = r':/\\|&'
            for char in unsafe_chars:
                ret = ret.replace(char, '_')
            unsafe_chars = r'<>:"/\\|?*%!@&;,`$^#~=+'
            for char in unsafe_chars:
                ret = ret.replace(char, '')   
            ret = re.sub(r'\s+', ' ', ret)  # Removing multiple spaces
            ret = re.sub(r'_+', '_', ret)  # Removing multiple _
            ret = ret.strip(' _')  # Remove spaces and underscores from ends

            # Limiting the length
            if len(ret) > 100:
                ret = ret[:100]

            return ret
       
        except Exception as e:
            print(f"An error occurred: {e}")
            print(f"Error type: {type(e).__name__}")
            print(f"Module: {e.__class__.__module__}")
            return "ERROR file_name_from_search"
        
    

    def get_file_extension(self):
        """Returns the file extension depending on the browser type."""
        return '.cnt' if self.browser_type == 'notes' else '.ccd'
    
    def get_file_filter(self):
        """Returns the filter for the file selection dialog."""
        ext = self.get_file_extension()
        type_name = q("q_notes") if self.browser_type == 'notes' else q("q_cards")
        q1 = q("q_Column_Settings")        
        q2 = q("q_All_files") 
        return f"{q1} {type_name} (*{ext});;{q2} (*.*)"
    
    def get_default_filename(self):
        """Returns the default file name."""
        ext = self.get_file_extension()
        fn = self.file_name_from_search( self.browser._line_edit().text() )
        return f"{fn}{ext}"


    def get_save_directory(self):
        """Returns the directory for saving settings."""
        home_dir = os.path.expanduser("~")
        backup_dir = os.path.join(home_dir, "Anki_Saved_columns")
        os.makedirs(backup_dir, exist_ok=True)
        return backup_dir 

    

    def save_cols(self):
        """Saving speaker settings to a file."""

        if not self.original_order:
            QMessageBox.warning(self, q("q_Error"), q("q_No_data_to_save"))
            return
        
        # Getting data to save
        data_to_save = {
            'browser_type': self.browser_type,
            'timestamp': datetime.datetime.now().isoformat(),
            'columns': self.get_current_columns_data(),
            'total_columns': len(self.original_order)
        }
        
        # Open the file save dialog
        ext = self.get_file_extension()
        file_filter = self.get_file_filter()        
        default_dir = self.get_save_directory()
        default_name = self.get_default_filename()
        default_name = os.path.join(default_dir, default_name)   

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            q("q_Save_Column_Settings"),
            default_name,
            file_filter
        )
        
        if not file_path:
            return  # User canceled
        
        # Checking the file extension
        if not file_path.endswith(ext):
            q1 = q("q_It_is_recommended_to_save")
            reply = QMessageBox.question(
                self,
                q("q_Incorrect_extension"),
                f"{q1} {ext}\n",
                q("q_Save_it_anyway"),
                QMessageBox_Yes | QMessageBox_No,
                QMessageBox_No
            )
            if reply == QMessageBox_No:
                return
                
        
        try:
            # Saving data in JSON
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, ensure_ascii=False, indent=2)
        
            
            QMessageBox.information(
                self,
                q("q_Success"),
                f'{q("q_Settings_saved_to_file")}:\n{file_path}\n'
                f'{q("q_Columns")}: {len(data_to_save["columns"])}'
            )
            
        except Exception as e:
            QMessageBox.critical(
                self,
                q("q_Error"),
                f'{q("q_Failed_to_save_file")}:\n{str(e)}'
            )
    
    def open_cols(self):
        """Loading speaker settings from a file."""
        # Open the file selection dialog
        ext = self.get_file_extension()
        file_filter = self.get_file_filter()
        default_dir = self.get_save_directory()
        default_name = self.get_default_filename()
        default_name = os.path.join(default_dir, default_name)  

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            q("q_Open_Column_Settings"),
            default_name,
            file_filter
        )
        
        if not file_path:
            return  # User canceled
        
        # Checking the file extension
        if not file_path.endswith(ext):
            reply = QMessageBox.question(
                self,
                q("q_Incorrect_extension"),
                f'{q("q_This_file_has_the_wrong_extension")}.\n'
                f'{q("q_Expected")} {ext} {q("q_for_settings")} {self.browser_type}.\n'
                f'{q("q_Still_open")}?',
                QMessageBox_Yes | QMessageBox_No,
                QMessageBox_No
            )
            if reply == QMessageBox_No:
                return
        
        try:
            # Reading data from a file
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Checking the browser type
            if 'browser_type' in data and data['browser_type'] != self.browser_type:
                reply = QMessageBox.question(
                    self,
                    q("q_Type_mismatch"),
                    f'{q("q_This_file_contains_settings_for")} {data["browser_type"]},\n'
                    f'{q("q_and_you_have_a_browser_open")} {self.browser_type}.\n'
                    f'{q("q_Still_download")}',
                    QMessageBox_Yes | QMessageBox_No,
                    QMessageBox_No
                )
                if reply == QMessageBox_No:
                    return
            
            # We check the availability of the necessary data
            if 'columns' not in data:
                QMessageBox.warning(self, q("q_Error"), q("q_The_file_does_not_contain_column_data"))
                return
            
            # Loading columns
            self.load_columns_from_data(data['columns'])
            
            
            QMessageBox.information(
                self,
                q("q_Success"),
                f'{q("q_Settings_loaded_from_file")}:\n{file_path}\n'
                f'{q("q_Columns")}: {len(data["columns"])}\n'
                f'{q("q_Date_saved")}: {data.get('timestamp', q("q_unknown"))}'
            )
            
        except json.JSONDecodeError:
            QMessageBox.critical(self, q("q_Error"), q("q_The_file_is_damaged_or_incorrectly_formatted"))
        except Exception as e:
            QMessageBox.critical(
                self,
                q("q_Error"),
                f"{q('q_Failed_to_upload_file')}:\n{str(e)}"
            )

    
    def setup_ui(self):
        """Configures the interface."""
        self.setWindowTitle(q("q_Column_order"))
        self.resize(350, 500)
        
        main_layout = QVBoxLayout(self)
        
        # Top search bar
        top_panel = QHBoxLayout()
        
        search_label = QLabel(q("q_Filter") + ":")
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText(q("q_Column_filter") + "...")
        self.search_edit.textChanged.connect(self.filter_columns)
        
        top_panel.addWidget(search_label)
        top_panel.addWidget(self.search_edit)        
        top_panel.addSpacing(10) 

        self.save_btn = self.create_tool_button("💾", "save", q("q_Save") + " (Ctrl+S)")        
        self.open_btn = self.create_tool_button("📂", "open", q("q_Open") + " (Ctrl+O)")          
        top_panel.addWidget(self.save_btn)
        top_panel.addSpacing(10) 
        top_panel.addWidget(self.open_btn)     
        top_panel.addSpacing(2)   
        top_panel.addStretch()
        top_panel.addSpacing(2)        
        
        main_layout.addLayout(top_panel)

        # Column list
        self.list_widget = QListWidget()
        font = QFont()                
        font.setFixedPitch(True)  # First, set the monowidth!
        available_families = QFontDatabase.families()
        if "Consolas" in available_families:
            font.setFamily("Consolas")
        elif "DejaVu Sans Mono" in available_families:
            font.setFamily("DejaVu Sans Mono")
        elif "Monaco" in available_families:
            font.setFamily("Monaco")
        else:
            font.setFamily("monospace")
        font.setPointSize(10)      
        font.setWeight(400)
        self.list_widget.setFont(font)

        if pyqt_version == "PyQt6":            
            self.list_widget.setDragDropMode(QListWidget.DragDropMode.InternalMove)
            self.list_widget.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
            # self.list_widget.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        else:
            self.list_widget.setDragDropMode(QListWidget.InternalMove)
            self.list_widget.setSelectionMode(QListWidget.ExtendedSelection)
            # self.list_widget.setSelectionMode(QListWidget.MultiSelection)
        
        self.list_widget.setDragEnabled(True)
        self.list_widget.setAcceptDrops(True)
        self.list_widget.setDropIndicatorShown(True)
        self.list_widget.setProperty("dragToMove", True)

        self.list_widget.setAlternatingRowColors(True)        
        main_layout.addWidget(self.list_widget)
        
        # Quick Actions Bar
        quick_actions = QHBoxLayout()
        
        # Move group
        move_group = QGroupBox(" " + q("q_Column_Operations") + " ")
        move_layout = QVBoxLayout()
        quick_actions.addSpacing(2)
        quick_actions.addStretch()
        quick_actions.addSpacing(2)
        
        move_buttons_layout = QHBoxLayout()
        self.home_btn = self.create_tool_button("Home", "move-to-home", q("q_To_the_beginning") + " (Ctrl+Home)")
        self.up_btn = self.create_tool_button("↑", "go-up", q("q_Up") + " (Ctrl+Up)")
        self.down_btn = self.create_tool_button("↓", "go-down", q("q_Down") + " (Ctrl+Down)")
        self.end_btn = self.create_tool_button("End", "move-to-end", q("q_To_the_end") + " (Ctrl+End)")
        self.del_btn = self.create_tool_button("Del", "delete-items", q("q_Delete") + " (Ctrl+Del)")
        self.sort_btn = self.create_tool_button("A→Z", "sort-items", q("q_Sort"))
        
        move_buttons_layout.addWidget(self.home_btn)
        move_buttons_layout.addWidget(self.up_btn)
        move_buttons_layout.addWidget(self.down_btn)
        move_buttons_layout.addWidget(self.end_btn)
        move_buttons_layout.addWidget(self.del_btn)
        move_buttons_layout.addWidget(self.sort_btn)
        
        move_layout.addLayout(move_buttons_layout)        
        move_group.setLayout(move_layout)   
       
        quick_actions.addWidget(move_group)    
        quick_actions.addSpacing(2)    
        quick_actions.addStretch() 
        quick_actions.addSpacing(2)       
        main_layout.addLayout(quick_actions)
        
        # Statistics
        self.stats_label = QLabel("")
        main_layout.addWidget(self.stats_label)
        
        # Dialogue buttons
        if pyqt_version == "PyQt6":
            buttons = QDialogButtonBox(
                QDialogButtonBox.StandardButton.Ok | 
                QDialogButtonBox.StandardButton.Cancel | 
                QDialogButtonBox.StandardButton.Apply |
                QDialogButtonBox.StandardButton.Reset
            )
        else:
            buttons = QDialogButtonBox(
                QDialogButtonBox.Ok | 
                QDialogButtonBox.Cancel | 
                QDialogButtonBox.Apply |
                QDialogButtonBox.Reset
            )

        buttons.accepted.connect(self.apply_and_close)
        buttons.rejected.connect(self.reject)
        if pyqt_version == "PyQt6":
            buttons.button(QDialogButtonBox.StandardButton.Apply).clicked.connect(self.apply)
            buttons.button(QDialogButtonBox.StandardButton.Reset).clicked.connect(self.reset)
        else:
            buttons.button(QDialogButtonBox.Apply).clicked.connect(self.apply)
            buttons.button(QDialogButtonBox.Reset).clicked.connect(self.reset)
        
        main_layout.addWidget(buttons)
        
        # Connecting buttons
        self.connect_buttons()
    
    def create_tool_button(self, text, icon_name, tooltip):
        """Creates a button with an icon."""
        btn = QPushButton(text)
        btn.setToolTip(tooltip)
        btn.setFixedSize(60, 30)
        return btn
    
    def connect_buttons(self):
        """Connects buttons to functions."""
        self.home_btn.clicked.connect(self.move_to_home)
        self.end_btn.clicked.connect(self.move_to_end)
        self.up_btn.clicked.connect(self.move_up)
        self.down_btn.clicked.connect(self.move_down)
        self.del_btn.clicked.connect(self.del_items)
        self.sort_btn.clicked.connect(self.sort_items)
        self.save_btn.clicked.connect(self.save_cols)     
        self.open_btn.clicked.connect(self.open_cols)
        
    
    def load_columns(self):
        """Loads columns from a table."""
        if not hasattr(self.browser, 'table'):
            return
        
        self.original_order = self.get_columns_from_table()
        self.update_list()
    
   


    def get_columns_from_table(self):
        """Gets columns from a table, preserving the type."""
        columns = []
        
        if not hasattr(self.browser.table, '_view'):
            return columns
        
        view = self.browser.table._view
        model = self.browser.table._model
        header = view.horizontalHeader()
        
        for visual_pos in range(header.count()):
            logical_index = header.logicalIndex(visual_pos)
            
            if logical_index >= model.len_columns():
                continue
            
            # Getting information about a column from the model
            column = model.column_at_section(visual_pos)
            
            # The column key (type) is the most important!
            column_key = None
            
            # We try to get it in different ways
            if hasattr(column, 'key'):
                column_key = column.key
            elif hasattr(model._state, 'active_columns') and visual_pos < len(model._state.active_columns):
                column_key = model._state.active_columns[visual_pos]
            
            # Display name
            header_text = model.headerData(visual_pos, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole)
            
            if column_key and header_text:
                columns.append({
                    'type': column_key,                     # Column key (most important!)
                    'logical_index': logical_index,         # Logical index
                    'visual_index': visual_pos,             # Visual position
                    'name': str(header_text),               # Display name
                    'width': view.columnWidth(logical_index)
                })
        
        return columns
    
    

    def update_list(self, filter_text=""):
        """Updates the list of columns with type information."""
        
        self.list_widget.clear()
        
        for col in self.original_order:
            # Use type if available, otherwise name
            display_name = col.get('name', 'Unnamed')
            col_type = col.get('type', '')
            
            # Forming the text of the element
            if col_type:
                n = 16 - len(display_name)
                n = 0 if n < 0 else n
                item_text = f"{display_name}{' '*(n+4)}<{col_type}>"                
            else:
                item_text = display_name
            
            if filter_text and filter_text.lower() not in display_name.lower():
                continue
            
            item = QListWidgetItem(item_text)
            
            # Save ALL column data
            if pyqt_version == "PyQt6":
                item.setData(Qt.ItemDataRole.UserRole, col)
            else:            
                item.setData(Qt.UserRole, col)
            
            #Adding a tooltip with information
            # if col_type:
            #     item.setToolTip(f"Type: {col_type}\nName: {display_name}")
            
            item.setIcon(QIcon.fromTheme("view-list-details"))
            item.setForeground(QColor("black"))                       
            self.list_widget.addItem(item)
        
        self.update_stats()



    def update_stats(self):
        """Updates statistics."""
        total = self.list_widget.count()        
        
        self.stats_label.setText(f"{q("q_Columns")}: {total}")
    

    def filter_columns(self, text):
        """Filters columns by text."""        
        self._sync_original_order_from_widget() # Now let's synchronize self.original_order with the new order
        self.update_list(text)
    
    def get_selected_items(self):
        """Returns the selected items."""
        return self.list_widget.selectedItems()
    

    def move_selected_group_simple(self, new_index_func):
        """Easily move a group of selected elements."""
        items = self.get_selected_items()
        if not items:
            return
        
        # Getting the positions of all selected elements
        positions = [self.list_widget.row(item) for item in items]
        
        # Finding the top element of the group
        top_pos = min(positions)
        
        # Calculate the new position for the top element
        new_top_pos = new_index_func(top_pos)
        
        # Limiting the boundaries
        new_top_pos = max(0, new_top_pos)
        new_top_pos = min(self.list_widget.count() - len(items), new_top_pos)
        
        if new_top_pos == top_pos:
            return
        
        # Retrieving all selected elements (from bottom to top so that the indexes do not get lost)
        extracted_items = []
        for pos in sorted(positions, reverse=True):
            item = self.list_widget.takeItem(pos)
            extracted_items.insert(0, item)  # Keeping order
        
        # Insert into a new position
        for i, item in enumerate(extracted_items):
            self.list_widget.insertItem(new_top_pos + i, item)
            item.setSelected(True)

        # Now let's synchronize self.original_order with the new order
        self._sync_original_order_from_widget()

    
    def _sync_original_order_from_widget(self):
        """Synchronizes self.original_order with the current order in list_widget."""
        if not self.original_order:
            return
        
        # Create an empty new list
        new_original_order = []
        
        nj = 0
        # we go through all the elements from self.original_order
        for i in range(len(self.original_order)):
            item_i = self.original_order[i]
            found = None
            lw_count = self.list_widget.count() 
            if nj < lw_count: 
                for j in range(lw_count):
                    item_j = self.list_widget.item(j)
                    if pyqt_version == "PyQt6":
                        widget_data = item_j.data(Qt.ItemDataRole.UserRole)
                    else:
                        widget_data = item_j.data(Qt.UserRole)

                    if not widget_data:
                        continue

                    if (item_i.get('type', '') == widget_data.get('type', '') and
                                    item_i.get('name', '') == widget_data.get('name', '')):
                        found = True
                        break
            
            # if you don’t find it, then just add it
            if found == None:
                new_original_order.append(item_i)
            else:
                # if found, then add the one that is now at index nj
                item_j = self.list_widget.item(nj)
                if pyqt_version == "PyQt6":
                    widget_data = item_j.data(Qt.ItemDataRole.UserRole)
                else:
                    widget_data = item_j.data(Qt.UserRole)
                nj += 1
                new_original_order.append(widget_data)

        # Update original_order
        self.original_order = new_original_order
    



    # Updating handlers
    def move_to_home(self):
        self.move_selected_group_simple(lambda row: 0)

    def move_to_end(self):
        items = self.get_selected_items()
        if items:
            self.move_selected_group_simple(lambda row: self.list_widget.count() - len(items))

    def move_up(self):
        items = self.get_selected_items()
        if items:
            top_pos = min(self.list_widget.row(item) for item in items)
            self.move_selected_group_simple(lambda row: max(0, top_pos - 1))

    def move_down(self):
        items = self.get_selected_items()
        if items:
            bottom_pos = max(self.list_widget.row(item) for item in items)
            new_bottom_pos = min(self.list_widget.count() - 1, bottom_pos + 1)
            new_top_pos = new_bottom_pos - len(items) + 1
            self.move_selected_group_simple(lambda row: new_top_pos)


    def sort_items(self):
        """sort elements by name order"""
        items = self.get_selected_items()
        if not items:
            QMessageBox.information(self, q("q_No_selected"), q("q_Select_items_to_sort"))
            return

        reply = QMessageBox.question(
            self,
            q("q_Sort_selected"),
            f"{q("q_Sort")} {len(items)} {q("q_selected_items_by_name")}",
            QMessageBox_Yes | QMessageBox_No,
            QMessageBox_No
        )
        
        if reply != QMessageBox_Yes:
            return
        
        ascending=True
        selected_data = []
        for item in items:
            if pyqt_version == "PyQt6":
                item_data = item.data(Qt.ItemDataRole.UserRole)
            else:
                item_data = item.data(Qt.UserRole)
            
            if item_data:
                selected_data.append({
                    'item': item,
                    'data': item_data,
                    'original_row': self.list_widget.row(item),
                    'name': item_data.get('name', '').lower()  # For case insensitive sorting
                })
        
        if not selected_data:
            return
        

        self._perform_sort(items, True)



    def _perform_sort(self, items, ascending=True):
        """Performs sorting in the specified direction."""
        # Collecting data
        items_data = []
        for item in items:
            if pyqt_version == "PyQt6":
                item_data = item.data(Qt.ItemDataRole.UserRole)
            else:
                item_data = item.data(Qt.UserRole)
            
            if item_data:
                items_data.append({
                    'item': item,
                    'data': item_data,
                    'original_row': self.list_widget.row(item),
                    'name': item_data.get('name', '').lower()
                })
        
        if not items_data:
            return
        
        # Sort by direction
        items_data.sort(key=lambda x: x['name'], reverse=not ascending)
        
        # Removing and inserting
        positions = sorted([data['original_row'] for data in items_data], reverse=True)
        for pos in positions:
            self.list_widget.takeItem(pos)
        
        top_position = min(positions)
        for i, item_data in enumerate(items_data):
            insert_position = top_position + i
            self.list_widget.insertItem(insert_position, item_data['item'])
            item_data['item'].setSelected(True)

        # Synchronizing
        self._sync_original_order_from_widget()
        
        



    def del_items(self):
        """Removes selected items from the list with confirmation."""
        items = self.get_selected_items()
        if not items:
            QMessageBox.information(self, q("q_No_selected"), q("q_Select_items_to_remove"))
            return
        
        # Confirmation request
        reply = QMessageBox.question(
            self, 
            q("q_Deletion_confirmation"),
            f"{q("q_Delete")} {len(items)} {q("q_selected")}",
            QMessageBox_Yes | QMessageBox_No,
            QMessageBox_No
        )
        
        if reply != QMessageBox_Yes:
            return
        
        # Collecting unique identifiers of selected elements
        selected_ids = set()
        for item in items:
            if pyqt_version == "PyQt6":
                col_data = item.data(Qt.ItemDataRole.UserRole)
            else:
                col_data = item.data(Qt.UserRole)
            
            if col_data:
                # Create a unique identifier
                item_id = self._create_item_id(col_data)
                selected_ids.add(item_id)
        
        if not selected_ids:
            return
        
        # Remove from widget
        for item in items:
            row = self.list_widget.row(item)
            if row >= 0:
                taken_item = self.list_widget.takeItem(row)
                if taken_item:
                    del taken_item
        
        # Remove from original_order
        self._remove_from_original_order_by_ids(selected_ids)
        
        # Updating the display
        self.update_stats()


    def _create_item_id(self, col_data):
        """Creates a unique identifier for a column element."""
        # Combine type and name for uniqueness
        col_type = col_data.get('type', '')
        col_name = col_data.get('name', '')
        logical_index = col_data.get('logical_index', '')

        if col_type and col_name:
            return f"type:{col_type}:name:{col_name.lower()}"        
        else:
            return f"name:{col_name.lower()}"
        

    def _remove_from_original_order_by_ids(self, item_ids):
        """Removes elements from original_order by unique identifiers."""
        if not item_ids or not self.original_order:
            return
        
        new_order = []
        removed_count = 0
        
        for original_item in self.original_order:
            # Create an identifier for the current element
            current_id = self._create_item_id(original_item)
            
            # Checking to see if it needs to be deleted
            if current_id in item_ids:
                removed_count += 1
            else:
                new_order.append(original_item)
        
        self.original_order = new_order
        
        # Checking the quantity matches
        if removed_count != len(item_ids):
            print(f"Debug: Requested to remove {len(item_ids)} items, found and removed {removed_count}")
            print(f"Item IDs requested: {item_ids}")




    def setup_shortcuts(self):
        """Configures hotkeys."""
        shortcuts = [
            (QKeySequence("Ctrl+Home"), self.move_to_home),
            (QKeySequence("Ctrl+End"), self.move_to_end),
            (QKeySequence("Ctrl+Up"), self.move_up),
            (QKeySequence("Ctrl+Down"), self.move_down),
            (QKeySequence("Ctrl+Del"), self.del_items),
            (QKeySequence("Ctrl+S"), self.save_cols),
            (QKeySequence("Ctrl+O"), self.open_cols),
            (QKeySequence("Ctrl+F"), lambda: self.search_edit.setFocus()),        ]
        
        for key_seq, handler in shortcuts:
            shortcut = QShortcut(key_seq, self)
            shortcut.activated.connect(handler)
    
    

    def apply(self):              
        self._original_order_from_list_widget()
        self.apply_columns_to_browser_with_type()


    def _original_order_from_list_widget(self):
        """Synchronizes original_order with the current state of list_widget."""
        self.original_order = []

        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if pyqt_version == "PyQt6":
                col_data = item.data(Qt.ItemDataRole.UserRole)
            else:
                col_data = item.data(Qt.UserRole)
            
            if col_data:
                # Creating the correct format for original_order
                original_format = {
                    'type': col_data.get('type', ''),
                    'logical_index': col_data.get('logical_index', i),
                    'visual_index': i,  # Current visual position
                    'name': col_data.get('name', ''),
                    'width': col_data.get('width', 100)
                }
                self.original_order.append(original_format)


    
    def reset(self):
        """Resets changes."""
        self.load_columns()
        self.search_edit.setText("")
    
    def apply_and_close(self):
        """Applies and closes."""
        self.apply()
        self.accept()





from aqt import gui_hooks
from aqt.browser import Browser
from aqt.qt import QApplication, QHBoxLayout, QWidget, QPushButton, QVBoxLayout

def add_toolbar_between_search_and_table(browser: Browser):
    """Adds a toolbar between the search bar and the table"""
    
    # 1. Finding the left side of the splitter (QWidget with name "widget")
    left_widget = None
    for i in range(browser.form.splitter.count()):
        widget = browser.form.splitter.widget(i)
        if widget and widget.objectName() == "widget":
            left_widget = widget
            break
    
    if not left_widget:
        print("❌ The left part of the splitter (widget) was not found")
        return
    
    # print(f"✅ Found the left side of the splitter: {left_widget}")
    
    # 2. We get verticalLayout_2
    left_layout = left_widget.layout()
    if not left_layout or left_layout.objectName() != "verticalLayout_2":
        print("❌ verticalLayout_2 not found")
        return
    
    # print(f"✅ Found verticalLayout_2 с {left_layout.count()} elements")
    
    # 3. Create a toolbar
    toolbar = create_toolbar_for_left_panel(browser)
    
    # 4.Finding tableView position in layout
    table_index = -1
    for i in range(left_layout.count()):
        item = left_layout.itemAt(i)
        if item and item.widget() == browser.form.tableView:
            table_index = i
            break
    
    if table_index >= 0:
        # Insert a toolbar BEFORE the table
        left_layout.insertWidget(table_index, toolbar)
        # print(f"✅ Toolbar inserted before tableView at position {table_index}")
    else:
        # Add at the end (before tableView)
        left_layout.insertWidget(1, toolbar)  # position 1 (after gridLayout)
        # print("✅ Toolbar inserted at position 1")

def create_toolbar_for_left_panel(browser: Browser):
    """Creates a toolbar for the left panel (between search and table)"""
    from aqt.qt import QFrame
    
    
    # Main container
    main_widget = QWidget()
    main_layout = QVBoxLayout(main_widget)
    main_layout.setContentsMargins(0, 0, 0, 0)
    main_layout.setSpacing(0)

    toolbar = QFrame()
    toolbar.setObjectName("left_panel_toolbar")
    
    style = QApplication.style()
    icon_size = style.pixelMetric(QStyle.PixelMetric.PM_SmallIconSize) + 2
    btn_size = icon_size + 8
    toolbar.setFixedHeight(btn_size+2)
    layout = QHBoxLayout(toolbar)
    layout.setContentsMargins(1, 1, 1, 1)
    layout.setSpacing(10)
    
    
    style_btn_left = """   
        QPushButton {                        
            padding: 0px;
            margin: 0px;                          
            /*border: none;*/
            /*font-family: "Segoe UI Symbol", "Arial Unicode MS", sans-serif;*/
        }        
        """
    
    style_btn_right = """   
        QPushButton {
            font-size: 12px;            
            padding: 0px;
            margin: 0px;                          
            /*border: none;*/
            font-family: "Segoe UI Symbol", "Arial Unicode MS", sans-serif;
        }                      
        """
        
    def btn_create(
                text=None,
                icon=None,
                tooltip="",
                checkable=False,
                style_sheet=None
                ):
        btn = QPushButton(f"{icon}")        
        btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        if text:
            btn.setText(text)
        btn.setToolTip(tooltip)      
        btn.setCheckable(checkable)        
        btn.setIconSize(QSize(icon_size, icon_size))
        btn.setFixedSize(btn_size, btn_size)
        btn.setContentsMargins(0, 0, 0, 0) 
        if style_sheet:
            btn.setStyleSheet(style_sheet)
                
        return btn

    btn_name_toggle_sidebar = q("q_Sidebar")
    if browser:
        if hasattr(browser, 'form'):
            f = browser.form
            if f and hasattr(f, 'actionToggleSidebar'):
                if f.actionToggleSidebar:
                    shortcut = f.actionToggleSidebar.shortcut().toString()
                    if shortcut == "":
                        shortcut = "Ctrl+Alt+R"
                    btn_name_toggle_sidebar += " (" + shortcut + ")"

    btn_toggle_sidebar = btn_create(text="☰", tooltip=btn_name_toggle_sidebar, style_sheet=style_btn_left)    
    btn_toggle_sidebar.clicked.connect(lambda: browser.toggle_sidebar())
    layout.addWidget(btn_toggle_sidebar)
# Switch LEFT
    switch = browser._switch
    switch.setParent(toolbar)    
    layout.addWidget(switch)      



    def table_reset(browser: Browser):   
        try:
            show_wait_cursor()

            browser._pressF5 = True
            try:
                top_row = browser.table._current().row()
            except:
                top_row = None            
            
            if top_row is not None:                         
                ncol = browser.table._current().column()
                ncolVI = browser.table._horizontal_header().visualIndex(ncol)   
                horizontalScrollBar = browser.table._view.horizontalScrollBar()
                if horizontalScrollBar is not None:
                    horizontalScrollBar_val = horizontalScrollBar.value()                        
                try:
                    srch = browser.current_search()                        
                    browser.search_for(srch)
                except Exception as e:
                    pass

                try:   
                    browser.table.reset()             
                    browser.table._set_current(top_row, ncolVI)
                    horizontalScrollBar = browser.table._view.horizontalScrollBar()
                    if horizontalScrollBar is not None:
                        horizontalScrollBar.setValue(horizontalScrollBar_val)                
                except Exception as e:
                    pass            
            else:
                try:
                    srch = browser.current_search()                            
                    browser.search_for(srch)
                except Exception as e:                
                    try:
                        browser.table.reset()
                    except Exception as e:
                        pass

        finally:
            restore_cursor()


        

        

    def go_back(browser):
        """Go to the previous request in the history."""
        if not hasattr(browser, '_all_history_n'):
            browser._all_history_n = 0
        
        sah = browser.mw.pm.profile.get("searchlist_all_history", [])
        
        if not sah or browser._all_history_n >= len(sah) - 1:
            return  # Can't go any further back
        
        # We increase the pointer (go to the past)
        browser._all_history_n += 1
        
        separator = " cid:"
        cr_txt = sah[browser._all_history_n]            
        index_sep = cr_txt.rfind(separator)
        search_query = cr_txt[:index_sep]
        cid = cr_txt[index_sep + len(separator):]     
        
        try:
            normed = browser.col.build_search_string(search_query)
            browser._line_edit().setText(normed)
        except SearchError as err:
            showWarning(markdown(str(err)))
        except Exception as err:
            showWarning(str(err))
        else:
            # Cancel the previous timer if there is one
            if hasattr(browser, '_nav_timer') and browser._nav_timer:
                browser._nav_timer.stop()
                browser._nav_timer.deleteLater()
            
            # Create a new timer            
            browser._nav_timer = QTimer()
            browser._nav_timer.setSingleShot(True)

            # A function that will execute in 400 ms
            def perform_navigation():    
                try:
                    show_wait_cursor()
                    browser._go_back_or_go_forward = True

                    ncol = browser.table._current().column()
                    ncolVI = browser.table._horizontal_header().visualIndex(ncol)
                    horizontalScrollBar = browser.table._view.horizontalScrollBar()
                    if horizontalScrollBar is not None:
                        horizontalScrollBar_val = horizontalScrollBar.value()

                    # Carrying out a search
                    browser.search_for(normed)
                    if cid != "":
                        browser.table.select_single_card(int(cid))

                    top_row = browser.table._current().row()
                    browser.table._set_current(top_row, ncolVI)
                    horizontalScrollBar = browser.table._view.horizontalScrollBar()
                    if horizontalScrollBar is not None:
                        horizontalScrollBar.setValue(horizontalScrollBar_val)

                    browser._go_back_or_go_forward = False
                finally:
                    restore_cursor()
                    # Clear the timer after execution
                    if hasattr(browser, '_nav_timer'):
                        browser._nav_timer = None
            
            # Connecting the function to the timer
            browser._nav_timer.timeout.connect(perform_navigation)
            # Start the timer for 400 ms
            browser._nav_timer.start(400)

        # Updating the state of the buttons
        _update_browser_navigation_buttons(browser, sah)


    def go_forward(browser):
        """Move to the next request in history."""
        if not hasattr(browser, '_all_history_n'):
            browser._all_history_n = -1
        
        sah = browser.mw.pm.profile.get("searchlist_all_history", [])
        
        if not sah or browser._all_history_n <= 0:
            return  # Can't go any further forward
        
        # Decrease the pointer (go to the future)
        browser._all_history_n -= 1
                
        separator = " cid:"
        cr_txt = sah[browser._all_history_n]            
        index_sep = cr_txt.rfind(separator)
        search_query = cr_txt[:index_sep]
        cid = cr_txt[index_sep + len(separator):]             
        
        try:
            normed = browser.col.build_search_string(search_query)
            browser._line_edit().setText(normed)  
        except SearchError as err:
            showWarning(markdown(str(err)))
        except Exception as err:
            showWarning(str(err))
        else:
            # Cancel the previous timer if there is one
            if hasattr(browser, '_nav_timer') and browser._nav_timer:
                browser._nav_timer.stop()
                browser._nav_timer.deleteLater()
            
            # Create a new timer            
            browser._nav_timer = QTimer()
            browser._nav_timer.setSingleShot(True)

            # A function that will execute in 400 ms
            def perform_navigation():    
                try:
                    show_wait_cursor()
                    browser._go_back_or_go_forward = True

                    ncol = browser.table._current().column()
                    ncolVI = browser.table._horizontal_header().visualIndex(ncol)
                    horizontalScrollBar = browser.table._view.horizontalScrollBar()
                    if horizontalScrollBar is not None:
                        horizontalScrollBar_val = horizontalScrollBar.value()

                    # Carrying out a search
                    browser.search_for(normed)
                    if cid != "":
                        browser.table.select_single_card(int(cid))

                    top_row = browser.table._current().row()
                    browser.table._set_current(top_row, ncolVI)
                    horizontalScrollBar = browser.table._view.horizontalScrollBar()
                    if horizontalScrollBar is not None:
                        horizontalScrollBar.setValue(horizontalScrollBar_val)

                    browser._go_back_or_go_forward = False
                finally:
                    restore_cursor()
                    # Clear the timer after execution
                    if hasattr(browser, '_nav_timer'):
                        browser._nav_timer = None
            
            # Connecting the function to the timer
            browser._nav_timer.timeout.connect(perform_navigation)
            # Start the timer for 400 ms
            browser._nav_timer.start(400)

            
        
        # Updating the state of the buttons
        _update_browser_navigation_buttons(browser, sah)


    def _update_browser_navigation_buttons(browser, sah=None):
        """Updates the state of the navigation buttons for the browser."""
        if sah is None:
            sah = browser.mw.pm.profile.get("searchlist_all_history", [])
        
        if not hasattr(browser, '_btn_back') or not hasattr(browser, '_btn_forward'):
            return
        
        # Let's make sure the pointer exists
        if not hasattr(browser, '_all_history_n'):
            browser._all_history_n = -1
        
        # Back button
        if len(sah) > 1 and browser._all_history_n < len(sah) - 1:
            browser._btn_back.setEnabled(True)
            tooltip = q("q_Back") + " [Alt+Left]  " + sah[browser._all_history_n+1]             
        else:
            browser._btn_back.setEnabled(False)
            tooltip = q("q_Back") + " [Alt+Left]"
        browser._btn_back.setToolTip(tooltip)     

        
        # Forward button
        if browser._all_history_n > 0:
            browser._btn_forward.setEnabled(True)
            tooltip = q("q_Forward") + " [Alt+Right]  " + sah[browser._all_history_n-1]
        else:
            browser._btn_forward.setEnabled(False)
            tooltip = q("q_Forward") + " [Alt+Right]"
        browser._btn_forward.setToolTip(tooltip) 




    def show_reorder_columns(browser):        

        if not browser or not hasattr(browser, 'table'):
            QMessageBox.warning(browser, "Error", "Browser not initialized")
            return

        dialog = EnhancedColumnOrderDialog(browser, browser)
        if pyqt_version == "PyQt6":
            dialog.exec()
        else:
            dialog.exec_()

        


    def go_edit_field(browser):

        def trigger_double_click_programmatically(view, row, column):
            """Calls the double-click handler programmatically."""              
            index = view.model().index(row, column)            
            # Find and call connected slots
            connections = view.receivers(view.doubleClicked)            
            # Calling a signal
            view.doubleClicked.emit(index)

        try:
            view = browser.table._view
            current_index = view.currentIndex()
            if current_index.isValid():
                row = current_index.row()
                column = current_index.column()
                trigger_double_click_programmatically(view, row, column)
        except:
            pass


    def run_find_tbl(browser: Browser):
        try:
            show_wait_cursor()

            text = browser.current_search()
            try:
                normed = browser.col.build_search_string(text)
            except SearchError as err:
                showWarning(markdown(str(err)))
            except Exception as err:
                showWarning(str(err))
            else:
                browser.search_for(normed)

        finally:
            restore_cursor()


    # Buttons to the right of the Switch
    btn_back = btn_create(text="←", tooltip=q("q_Back") + " [Alt+Left]", style_sheet=style_btn_right)    
    btn_back.clicked.connect(lambda: go_back(browser))
    btn_back.setShortcut(QKeySequence("Alt+Left"))
    btn_back.setEnabled(False)
    layout.addWidget(btn_back)
    browser._btn_back = btn_back

    btn_forward = btn_create(text="→", tooltip=q("q_Forward") + " [Alt+Right]", style_sheet=style_btn_right)    
    btn_forward.clicked.connect(lambda: go_forward(browser))
    btn_forward.setShortcut(QKeySequence("Alt+Right"))
    btn_forward.setEnabled(False)
    layout.addWidget(btn_forward)
    browser._btn_forward = btn_forward
    browser._all_history_n = 0

    btn_edit_field = btn_create(text="✏️", tooltip=q("q_Edit_field") + " [F2]", style_sheet=style_btn_right)    
    btn_edit_field.clicked.connect(lambda: go_edit_field(browser))
    btn_edit_field.setShortcut(QKeySequence("F2"))
    layout.addWidget(btn_edit_field)

    btn_refresh_tbl = btn_create(text="↻", tooltip=q("q_Update_will_change_the_current_row") + " [F5]", style_sheet=style_btn_right)    
    btn_refresh_tbl.clicked.connect(lambda: table_reset(browser))
    btn_refresh_tbl.setShortcut(QKeySequence("F5"))
    layout.addWidget(btn_refresh_tbl)    

    btn_reorder_columns = btn_create(text="⮂", tooltip=q("q_Column_order") + " [F8]", style_sheet=style_btn_right)    
    btn_reorder_columns.clicked.connect(lambda: show_reorder_columns(browser))
    btn_reorder_columns.setShortcut(QKeySequence("F8"))
    layout.addWidget(btn_reorder_columns)

    btn_run_find_tbl = btn_create(text="🔍", tooltip=q("q_Apply_search_will_remember_the_current_line") + " [F9]", style_sheet=style_btn_right)    
    btn_run_find_tbl.clicked.connect(lambda: run_find_tbl(browser))
    btn_run_find_tbl.setShortcut(QKeySequence("F9"))
    layout.addWidget(btn_run_find_tbl)
    
    # Stretch to the right
    layout.addStretch()

    # Adding a panel with buttons to the main layout
    main_layout.addWidget(toolbar)


    # Bottom line with label
    label_request_panel = QFrame()
    label_request_panel.setObjectName("label_request_panel")
    
    label_request_layout = QHBoxLayout(label_request_panel)
    label_request_layout.setContentsMargins(5, 2, 5, 2)
    
    # Creating a label with the ability to highlight text
    label_request = QLabel("deck:*")
    label_request.setObjectName("label_request")
    
    # Making text stand out
    label_request.setTextInteractionFlags(
        Qt.TextInteractionFlag.TextSelectableByMouse | 
        Qt.TextInteractionFlag.TextSelectableByKeyboard
    )
    browser._label_request = label_request

    label_request_layout.addWidget(label_request)
    main_layout.addWidget(label_request_panel)

    return main_widget


    

gui_hooks.browser_will_show.append(add_toolbar_between_search_and_table)



# ⬆⬆⬆⬆ kaiu: 2026-01-12 Additional panel above the table ⬆⬆⬆⬆ +++++ 




CONF_KEY_PREFIX = 'advbrowse_'

class PersistentMenu(QMenu):
    """Persistent menu to support multiple selection"""
    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() != Qt.MouseButton.LeftButton:
            return super().mouseReleaseEvent(event)

        action = self.actionAt(event.pos())
        if action and action.isCheckable():
            # Get user data associated with the action
            column_type = action.data()
            if column_type:
                table = self.property("table")
                if table:
                    new_state = not action.isChecked()
                    action.setChecked(new_state)
                    table._on_column_toggled(new_state, column_type)

            event.accept()
            return
        elif action:
            return super().mouseReleaseEvent(event)
        else:
            self.close()

class AdvancedBrowser:
    """Maintains state for the add-on."""

    def __init__(self, mw):
        self.mw = mw
        # A list of columns to exclude when building the final column list.
        self.columnsToRemove = []
        # CustomColumn objects maintained by this add-on.
        # {type -> CustomColumn}
        self.customTypes = {}
        # Model->flds cache, similar to self.cardObjs
        self.modelFldObjs = {}

    def _load(self, browser):
        self.browser = browser
        self.table = browser.table
        self.editor = browser.editor
        self.col = browser.col

        # Let add-ons add or remove columns now.
        runHook("advBrowserLoaded", self)

        self.__removeColumns()
        self.setupColumns()

        # Workaround for double-saving (see closeEvent)
        self.saveEvent = False
        if config.getSelectable() != "No interaction":
            self.table._view.setEditTriggers(self.table._view.EditTrigger.DoubleClicked)

    def newCustomColumn(self, type, name, onData, onSort=None,
                        setData=None, sortTableFunction=False):
        """Add a CustomColumn to the browser. See CustomColumn for a
        detailed description of the parameters."""
        cc = CustomColumn(type, name, onData, onSort,
                          sortTableFunction, setData=setData)
        self.customTypes[cc.type] = cc
        return cc

    def removeColumn(self, type):
        """Remove a column from the columns list so that it will not appear
        in the browser. Applies to built-in or custom columns."""
        self.columnsToRemove.append(type)

    def __removeColumns(self):
        self.removedBuiltIns = []
        for type in self.columnsToRemove:
            # Remove from ours
            if type in self.customTypes:
                self.customTypes.pop(type, None)

            # Columns are a dict of str keys and builtin columns
            for column in self.table._model.columns:
                if column == type:
                    self.removedBuiltIns.append(column)
                    del self.table._model.columns[column]

            # Remove it from the active columns if it's there.
            if type in self.table._state.active_columns:
                self.table._on_column_toggled(False, type)

    def setupColumns(self):
        """Build a list of candidate columns. We extend the internal
        self.columns list with our custom types."""
        bc = BrowserColumns.SORTING_NORMAL if pointVersion() <= 49 else BrowserColumns.SORTING_ASCENDING
        for key, column in self.customTypes.items():
            alignmentConfig = config.getColumnAlignment()
            if alignmentConfig == "Start":
                alignment = BrowserColumns.ALIGNMENT_START
            elif alignmentConfig == "Center":
                alignment = BrowserColumns.ALIGNMENT_CENTER

            self.table._model.columns[key] = BuiltinColumn(
                key=key,
                cards_mode_label=column.name,
                notes_mode_label=column.name,
                sorting_notes=bc if column.onSort() else BrowserColumns.SORTING_NONE,
                sorting_cards=bc if column.onSort() else BrowserColumns.SORTING_NONE,
                uses_cell_font=False,
                alignment=alignment,
            )

    def willSearch(self, ctx: SearchContext):
        # If the order is a custom column, apply the column's sorting
        if type(ctx.order) == BuiltinColumn and (cc := self.customTypes.get(ctx.order.key)):
            order = cc.onSort()
            if not order:
                ctx.order = None
            else:
                if self.table._state.sort_backwards:
                    order = order.replace(" asc", " desc")
                ctx.order = order

            self.time = time.time()

            # If this column relies on a temporary table for sorting, build it now
            if cc.sortTableFunction:
                cc.sortTableFunction()

    def didSearch(self, ctx: SearchContext):
        #print("Search took: %dms" % ((time.time() - self.time)*1000))
        pass

    def _column_data(self, item, is_notes_mode, row, active_columns):
        """Fill in data of custom columns."""
        c = self.table._state.get_card(item)
        n = self.table._state.get_note(item)
        for index, key in enumerate(active_columns):
            # Filter for custom types with a data function
            if (custom_type := self.customTypes.get(key)) is None:
                continue
            if custom_type.onData is None:
                continue

            # Get cell content
            try:
                row.cells[index].text = custom_type.onData(c, n, key)
            except Exception as error:
                row.cells[index].text = f"{error}"

            # Get rtl info for field cells
            if key.startswith("_field_"):
                fldName = key[7:]
                model = n.note_type()
                model_id = model["id"]
                if model_id not in self.modelFldObjs:
                    self.modelFldObjs[model_id] = {}
                if fldName not in self.modelFldObjs[model_id]:
                    flds = [f for f in model['flds'] if f['name'] == fldName]
                    if len(flds) == 0:
                        # This model does not have a field with that name
                        self.modelFldObjs[model_id][fldName] = None
                    else:
                        self.modelFldObjs[model_id][fldName] = flds[0]
                fld = self.modelFldObjs[model_id][fldName]
                row.cells[index].is_rtl = bool(fld and fld["rtl"])

    def setData(self, model, index, value, role):
        if role not in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole):
            return False
        if config.getSelectable() != "Editable":
            return False
        old_value = model.get_cell(index).text
        if value == old_value:
            return False
        c = model.get_card(index)

        type = model.column_at(index).key
        if type in self.customTypes:
            r = self.customTypes[type].setData(c, value)
            if r is True:
                model.dataChanged.emit(index, index, [role])
            return r
        else:
            return False

    def _on_header_context(self, table, pos):
        """Override the original onHeaderContext. We are responsible for
        building the entire menu, so we include the original columns as
        well."""

        gpos = table._view.mapToGlobal(pos)
        # Persist the main menu
        main = PersistentMenu()
        main.setProperty("table", table)
        # main = QMenu()
        contextMenu = ContextMenu()

        # We are also a client and we need to add the built-in columns first.
        for key, column in table._model.columns.items():
            if key not in self.customTypes:
                contextMenu.addItem(Column(key, table._state.column_label(column)))

        # Now let clients do theirs.
        runHook("advBrowserBuildContext", contextMenu)

        def addCheckableAction(menu, type, name):
            a = menu.addAction(name)
            a.setCheckable(True)
            # Save column type to user data
            a.setData(type)
            a.setChecked(table._model.active_column_index(type) is not None)
            if not isinstance(menu, PersistentMenu):
                a.toggled.connect(lambda checked, key=type: table._on_column_toggled(checked, key))

        # For some reason, sub menus aren't added if we don't keep a
        # reference to them until exec, so keep them in this list.
        tmp = []
        # Recursively add each item/group.

        def addToSubgroup(menu, items, adv_browser):
            # Support fields reset
            for item in items:                
                if isinstance(item, ContextMenu):
                    # Persist sub menu
                    sub = PersistentMenu(item.name)
                    sub.setProperty("table", table)                    
                    tmp.append(sub)
                    menu.addMenu(sub)
                    addToSubgroup(sub, item.items(), adv_browser)
                else:
                    # fields reset 
                    if item.type == "fields_reset":
                        action = menu.addAction(item.name)
                        action.triggered.connect(lambda: reset_fields(adv_browser))
                    else:
                        addCheckableAction(menu, item.type, item.name)
        # Start adding from the top
        addToSubgroup(main, contextMenu.items(), self)

        main.exec(gpos)

# Fields reset 
def reset_fields(adv_browser):
    """Cancel all selected fields in the 'Fields'sub menu"""
    table = adv_browser.table
    for field_type in adv_browser.customTypes.keys():
        if field_type.startswith("_field_"):
            if table._model.active_column_index(field_type) is not None:
                table._on_column_toggled(False, field_type) 
                
# Table model expansions for editable cells
################################################################################

def wrap_flags(self, index, _old):
    s = _old(self, index)
    if config.getSelectable() != "No interaction":
        s |=  Qt.ItemFlag.ItemIsEditable
    return s


def wrap_data(self, index, role, _old):
    if role == Qt.ItemDataRole.EditRole:
        role = Qt.ItemDataRole.DisplayRole
    return _old(self, index, role)


################################################################################

# Override config keys to use own set of config values
CardState.GEOMETRY_KEY_PREFIX = CONF_KEY_PREFIX + CardState.GEOMETRY_KEY_PREFIX
NoteState.GEOMETRY_KEY_PREFIX = CONF_KEY_PREFIX + NoteState.GEOMETRY_KEY_PREFIX
BrowserConfig.ACTIVE_CARD_COLUMNS_KEY = CONF_KEY_PREFIX + BrowserConfig.ACTIVE_CARD_COLUMNS_KEY
BrowserConfig.ACTIVE_NOTE_COLUMNS_KEY = CONF_KEY_PREFIX + BrowserConfig.ACTIVE_NOTE_COLUMNS_KEY
BrowserConfig.CARDS_SORT_COLUMN_KEY = CONF_KEY_PREFIX + BrowserConfig.CARDS_SORT_COLUMN_KEY
BrowserConfig.NOTES_SORT_COLUMN_KEY = CONF_KEY_PREFIX + BrowserConfig.NOTES_SORT_COLUMN_KEY
BrowserConfig.CARDS_SORT_BACKWARDS_KEY = CONF_KEY_PREFIX + BrowserConfig.CARDS_SORT_BACKWARDS_KEY
BrowserConfig.NOTES_SORT_BACKWARDS_KEY = CONF_KEY_PREFIX + BrowserConfig.NOTES_SORT_BACKWARDS_KEY

# Init AdvancedBrowser
advanced_browser = AdvancedBrowser(mw)

# Hooks
gui_hooks.browser_will_show.append(advanced_browser._load)
gui_hooks.browser_will_search.append(advanced_browser.willSearch)
gui_hooks.browser_did_search.append(advanced_browser.didSearch)
gui_hooks.browser_did_fetch_row.append(advanced_browser._column_data)

# Override table's context menu to include our own columns
aqt.browser.Table._on_header_context = lambda *args: advanced_browser._on_header_context(*args)

# Override table model flags to make cells editable if applicable
DataModel.flags = wrap(DataModel.flags, wrap_flags, "around")

# Override table model data to return data in case of edit role
DataModel.data = wrap(DataModel.data, wrap_data, "around")

# Add setData() to table model (Qt API)
DataModel.setData = lambda *args: advanced_browser.setData(*args)

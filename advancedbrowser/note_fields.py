# -*- coding: utf-8 -*-
# Version: 3.9.1b
# See github page to report issues or to contribute:
# https://github.com/AndreyKaiu/advanced-browser-mod-kaiu-2026
#
# Original author code:
# https://github.com/hssm/advanced-browser

import re
from anki.cards import Card
from anki.hooks import addHook
from anki.utils import pointVersion
from aqt import *
from aqt.utils import showWarning

from .config import getEachFieldInSingleList
from .core import Column

from .localization.lang import q

class NoteFields:

    def onAdvBrowserLoad(self, advBrowser):
        # Dictionary of field names indexed by "type" name. Used to
        # figure out if the requested column is a note field.
        # {type -> name}
        self.fieldTypes = {}

        # Dictionary of dictionaries to get position for field in model.
        # We build this dictionary once to avoid needlessly finding the
        # field order for every single row when sorting. It's
        # significantly faster that way.
        # {mid -> {fldName -> pos}}
        self.modelFieldPos = {}

        # Dictionary of columns. A column can exist in multiple places, because
        # different note types may have the same field name.
        # {fld['name'] -> CustomColumn}}
        self.customColumns = {}

        self.fieldsToMidOrdPairs = {}

        self.advBrowser = advBrowser
        self.buildMappings()

    def onBuildContextMenu(self, contextMenu):
        # Models might have changed so rebuild our mappings.
        # E.g., a field or note type could have been deleted.
        self.buildMappings()

        # ⬇⬇⬇⬇⬇ kaiu: 2026-01-05 Fixed a bug with limiting the size of menu items. ⬇⬇⬇⬇⬇ -----        
        # # Create a new sub-menu for our columns
        # fldGroup = contextMenu.newSubMenu(" - Fields -")
        # if getEachFieldInSingleList():
        #     # And an option for each fields
        #     for model in mw.col.models.all():
        #         for fld in model['flds']:
        #             fldGroup.addItem(self.customColumns[fld['name']])
        # else:
        #     # And a sub-menu for each note type
        #     for model in mw.col.models.all():
        #         modelGroup = fldGroup.newSubMenu(model['name'])
        #         for fld in model['flds']:
        #             modelGroup.addItem(self.customColumns[fld['name']])

        # ⬇⬇⬇⬇⬇ kaiu: 2026-01-05 Fixed a bug with limiting the size of menu items. ⬇⬇⬇⬇⬇ +++++     
        
        unique_fields = set()
        for model in mw.col.models.all():
            for fld in model['flds']:
                unique_fields.add(fld['name'])
        count_flds = len(unique_fields)
        count_models = len(mw.col.models.all())
        
        MAX_ITEMS_PER_MENU = 64
        MAX_GROUPS_PER_LEVEL_F = 64
        ZWSP = "\u200B"       
        v_str = q("q_Fields_all") 
        fldGroup = contextMenu.newSubMenu(f" - {v_str} -")             

        if count_flds <= MAX_ITEMS_PER_MENU:                   
            # And an option for each fields
            for model in mw.col.models.all():
                for fld in model['flds']:                        
                    fldGroup.addItem(self.customColumns[fld['name']])
        else:
            def add_fields_chunked(parent_menu, field_items):
                index = 0
                total = len(field_items)
                groups_created = 0

                while index < total and groups_created < MAX_GROUPS_PER_LEVEL_F:
                    chunk = field_items[index:index + MAX_ITEMS_PER_MENU]
                    index += MAX_ITEMS_PER_MENU
                    groups_created += 1

                    prefix = chunk[0][0][:2].upper()
                    sub = parent_menu.newSubMenu(prefix)

                    for _, action in chunk:                            
                        sub.addItem(action)

                if index < total:
                    more_menu = parent_menu.newSubMenu(ZWSP + "more…")
                    add_fields_chunked(more_menu, field_items[index:])
            
            field_map = {}
            for model in mw.col.models.all():
                for fld in model["flds"]:
                    name = fld["name"]
                    # If the field already exists, skip it.
                    if name not in field_map:
                        field_map[name] = self.customColumns[name]

            field_items = [(name, action) for name, action in field_map.items()]
            field_items.sort(key=lambda x: x[0].lower())                
            add_fields_chunked(fldGroup, field_items)

                
         
        MAX_MODELS_PER_CHUNK = 64  
        MAX_GROUPS_PER_LEVEL_M = 64  
        ZWSP = "\u200B" 
        v_str = q("q_Fields_in_models")
        fldGroup = contextMenu.newSubMenu(f" - {v_str} -")
        
        if count_models <= MAX_MODELS_PER_CHUNK:
            # And a sub-menu for each note type
            for model in mw.col.models.all():                    
                modelGroup = fldGroup.newSubMenu(model['name'])
                for fld in model['flds']:
                    modelGroup.addItem(self.customColumns[fld['name']])
        else:
            def add_models_by_letters(parent_menu, models):
                """
                parent_menu: ContextMenu
                models: list[dict]  
                """            
                models = sorted(models, key=lambda m: m["name"].lower())

                # Remove duplicates by model name
                seen = set()
                unique_models = []
                for m in models:
                    if m["name"] not in seen:
                        seen.add(m["name"])
                        unique_models.append(m)

                # We're building a submenu using the first two letters.
                field_index = 0
                total = len(unique_models)
                groups_created = 0

                while field_index < total and groups_created < MAX_GROUPS_PER_LEVEL_M:
                    chunk = unique_models[field_index:field_index + MAX_MODELS_PER_CHUNK]
                    field_index += MAX_MODELS_PER_CHUNK
                    groups_created += 1
                    
                    prefix = chunk[0]["name"][:2].upper()
                    letter_menu = parent_menu.newSubMenu(prefix)
                    
                    for model in chunk:
                        model_menu = letter_menu.newSubMenu(model["name"])
                        for fld in model["flds"]:
                            model_menu.addItem(self.customColumns[fld["name"]])
                
                if field_index < total:
                    more_menu = parent_menu.newSubMenu(ZWSP + "more…")
                    add_models_by_letters(more_menu, unique_models[field_index:])

            add_models_by_letters(fldGroup, mw.col.models.all())

        # ⬆⬆⬆⬆⬆ kaiu: 2026-01-05 Fixed a bug with limiting the size of menu items. ⬆⬆⬆⬆⬆ +++++


        try:
            # Get the current note
            current_note = self.advBrowser.browser.table.get_current_note()
            if current_note is None:
                current_note = self.advBrowser.browser.table.get_single_selected_card() 
            if current_note:
                # Getting the note model                
                note_model = current_note.note_type()   
                v_str = q("q_Current_note_fields")
                fldCur = contextMenu.newSubMenu(f" - {v_str} -")            
                for fld in note_model['flds']:
                    fldCur.addItem(self.customColumns[fld['name']])                 
            
        except Exception as e:
            print(f"Error getting current model: {e}")
            return None
        
        

        # Add fields reset into the main menu
        v_str = q("q_Fields_Reset")
        reset_column = Column(type="fields_reset", name=f" - {v_str} - ")
        contextMenu.addItem(reset_column)
        
    def buildMappings(self):
        self.fieldsToMidOrdPairs = {}
        for model in mw.col.models.all():
            # For some reason, some mids return as unicode, so convert to int
            mid = int(model['id'])
            # And some platforms get a signed 32-bit integer from SQlite, so
            # we will also provide an index to that as a workaround.
            mid32 = (mid + 2**31) % 2**32 - 2**31
            self.modelFieldPos[mid] = {}
            self.modelFieldPos[mid32] = {}
            # For each field in this model, store the ordinal of the
            # field with the field name as the key.
            for field in model['flds']:
                name = field['name']
                ord = field['ord']
                type = "_field_"+name  # prefix to avoid potential clashes
                self.modelFieldPos[mid][name] = ord
                self.modelFieldPos[mid32][name] = ord
                if type not in self.fieldTypes:  # avoid dupes
                    self.fieldTypes[type] = name
                self.fieldsToMidOrdPairs.setdefault(
                    name, []).append((mid, ord))

        def fldOnData(c, n, t):
            field = self.fieldTypes[t]
            if field in c.note().keys():
                return NoteFields.htmlToTextLine(c.note()[field])

        def setData_(name):
            def setData(c: Card, value: str):
                n = c.note()
                m = n.note_type()
                if not name in n:                    
                    showWarning(q("q_The_field_not_belong_note_type") % (
                        name, m["name"]))
                    return False
                self.advBrowser.editor.loadNote()
                n[name] = value
                return True
            return setData

        for type, name in self.fieldTypes.items():
            if name not in self.customColumns:
                def sortTableFunction(name=name):
                    col = mw.col
                    vals = []
                    col.db.execute("drop table if exists tmp")
                    col.db.execute(
                        "create temp table tmp (nid int primary key, fld text)")
                    for mid, ord in self.fieldsToMidOrdPairs.get(name):
                        notes = mw.col.db.all(
                            f"select id, field_at_index(flds, {ord}) from notes where mid = {mid}"
                        )
                        for note in notes:
                            id = note[0]
                            val = NoteFields.htmlToTextLine(note[1])
                            if not val:
                                val = None
                            vals.append([id, val])
                    mw.col.db.executemany(
                        "insert into tmp values (?,?)", vals
                    )

                select = "(select fld from tmp where nid = n.id)"
                srt = (
                    f"""
                    case when {select} glob '*[^0-9.]*' then {select} else cast({select} AS real) end
                    collate nocase asc nulls last
                    """
                )

                cc = self.advBrowser.newCustomColumn(
                    type=type,
                    name=name,
                    onData=fldOnData,
                    sortTableFunction=sortTableFunction,
                    onSort=lambda: srt,
                    setData=setData_(name),
                )
                self.customColumns[name] = cc
        self.advBrowser.setupColumns()

    def getSortClause(self, fieldName: str) -> str:
        def tuple_to_str(tup) -> str:
            (ntid, ord) = tup
            return f"when n.mid = {ntid} then field_at_index(n.flds, {ord})"

        tups = self.fieldsToMidOrdPairs.get(fieldName, [])
        if not tups:
            # no such field
            return "false"

        whenBody = " ".join(map(tuple_to_str, tups))
        return f"(case {whenBody} else null end) collate nocase asc nulls last"

    # Based on the one in utils.py, but keep media file names
    def htmlToTextLine(s):
        s = s.replace("<br>", " ")
        s = s.replace("<br />", " ")
        s = s.replace("<div>", " ")
        s = s.replace("\n", " ")
        s = reSound.sub("\\1", s)  # this line is different
        s = reType.sub("", s)
        s = anki.utils.stripHTMLMedia(s) if pointVersion() < 50 else anki.utils.strip_html_media(s)
        s = s.strip()
        return s

# Precompile some regexes for efficiency
reSound = re.compile(r"\[sound:([^]]+)\]")
reType = re.compile(r"\[\[type:[^]]+\]\]")

nf = NoteFields()
addHook("advBrowserLoaded", nf.onAdvBrowserLoad)
addHook("advBrowserBuildContext", nf.onBuildContextMenu)

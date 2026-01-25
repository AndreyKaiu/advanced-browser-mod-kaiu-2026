# -*- coding: utf-8 -*-
# Version: 3.9.2b
# See github page to report issues or to contribute:
# https://github.com/AndreyKaiu/advanced-browser-mod-kaiu-2026
#
# Original author code:
# https://github.com/hssm/advanced-browser

import time

from anki.cards import Card
from anki.consts import *
from anki.hooks import addHook
from anki.lang import FormatTimeSpan as FormatTimeSpanContext
from aqt.utils import tr
from aqt import *
from aqt.operations.card import set_card_flag
from aqt.utils import askUser

from .localization.lang import q


class AdvancedFields:

    def onAdvBrowserLoad(self, advBrowser):
        """Called when the Advanced Browser add-on has finished
        loading. Create and add all custom columns owned by this
        module."""

        # Store a list of CustomColumns managed by this module. We later
        # use this to build our part of the context menu.
        self.customColumns = []

        # Convenience method to create lambdas without scope clobbering
        def getOnSort(f): return lambda: f

        # -- Columns -- #

        # ⬇⬇⬇⬇⬇ kaiu: 2026-01-05 https://github.com/AnKing-VIP/advanced-browser/issues/120 ⬇⬇⬇⬇⬇ +++++
        
        def get_card_state(queue: int, type: int) -> str:
            ret = ""
            if type == 0:              
                ret += tr.actions_new()
            if type == 1:
                if ret != "":
                    ret += "; "
                ret += tr.scheduling_learning()
            if type == 2:
                if ret != "":
                    ret += "; "
                ret += tr.browsing_sidebar_card_state_review()
            if type == 3: 
                if ret != "":
                    ret += "; "
                ret += tr.scheduling_learning() + "; " + tr.browsing_sidebar_card_state_review()
            
            if queue in (-2, -3):  # QUEUE_TYPE_MANUALLY_BURIED, QUEUE_TYPE_SIBLING_BURIED  
                if ret == "":
                    ret = tr.browsing_buried()
                else:
                    ret = tr.browsing_buried() + "; " + ret

            if queue == -1:  # QUEUE_TYPE_SUSPENDED
                if ret == "":
                    ret = tr.browsing_suspended()
                else:
                    ret = tr.browsing_suspended() + "; " + ret

            return ret


        def cCardState(c, n, t):
            card = mw.col.get_card(c.id)
            return get_card_state(card.queue, card.type)
           
        cc = advBrowser.newCustomColumn(
            type='cardstate',
            name=q('q_Card_State'),
            onData=cCardState,
            onSort=lambda: """
CASE        
    WHEN c.queue = 0 THEN 0   -- New
    WHEN c.queue IN (1,3) THEN 1  -- Learning
    WHEN c.queue = 2 THEN 2   -- Review
    WHEN c.queue = -1 THEN 3  -- Suspended
    WHEN c.queue = -2 THEN 4  -- Buried
    WHEN c.queue = -3 THEN 5  -- Filtered
    ELSE 6
END
"""
        )
        self.customColumns.append(cc)
        # ------------------------------- #

        # ⬆⬆⬆⬆⬆ kaiu: 2026-01-05 https://github.com/AnKing-VIP/advanced-browser/issues/120 ⬆⬆⬆⬆⬆ +++++


        # ⬇⬇⬇⬇⬇ kaiu: 2026-01-05 nid and cid should be available to non-developers as well ⬇⬇⬇⬇⬇ +++++ 
        
        # nid
        def cNidOnData(c, n, t):
            return n.id

        cc = advBrowser.newCustomColumn(
            type='nid',
            name=q('q_nid'),
            onData=cNidOnData,
            onSort=lambda: "n.id asc nulls last"
        )
        self.customColumns.append(cc)
        # ------------------------------- #

        # cid
        def cCidOnData(c, n, t):
            return c.id

        cc = advBrowser.newCustomColumn(
            type='cid',
            name=q('q_cid'),
            onData=cCidOnData,
            onSort=lambda: "c.id asc nulls last"
        )
        self.customColumns.append(cc)
        # ------------------------------- #

        # ++++ KAIU ++++
        def tags_with_level(note, level: int):
            level -= 1
            return [tag for tag in note.tags if tag.count("::") == level]

        def getSQL_tagN(n : int):
            return f"""
(
select part from (
    WITH RECURSIVE Splitter (part, remainder) AS (
        SELECT '', tags || ' '
        FROM notes where notes.id = n.id
        UNION ALL
        SELECT
            SUBSTR(remainder, 0, INSTR(remainder, ' ')),
            SUBSTR(remainder, INSTR(remainder, ' ') + 1)
        FROM Splitter
        WHERE remainder != ''
    )
    SELECT part
    FROM Splitter
    WHERE part != ''
      AND (LENGTH(part) - LENGTH(REPLACE(part, '::', '')))  = {2*(n-1)}
    ORDER BY part
    LIMIT 1
)
) asc nulls last
""" 

        # Tags (L1)
        def cTag1(c, n, t):
            return " ".join(tags_with_level(n, 1))
        
        sort_sql = getSQL_tagN(1) 
        cc = advBrowser.newCustomColumn(
            type='ctag1',
            name=q('q_Tags_L1'),
            onData=cTag1,
            onSort=getOnSort(sort_sql)
        )
        self.customColumns.append(cc)
        # ------------------------------- #



        # Tags (L2)
        def cTag2(c, n, t):
            return " ".join(tags_with_level(n, 2))
        
        sort_sql = getSQL_tagN(2) 
        cc = advBrowser.newCustomColumn(
            type='ctag2',
            name=q('q_Tags_L2'),
            onData=cTag2,
            onSort=getOnSort(sort_sql)
        )
        self.customColumns.append(cc)
        # ------------------------------- #


        # Tags (L3)
        def cTag3(c, n, t):
            return " ".join(tags_with_level(n, 3))  
             
        sort_sql = getSQL_tagN(3) 
        cc = advBrowser.newCustomColumn(
            type='ctag3',
            name=q('q_Tags_L3'),
            onData=cTag3,
            onSort=getOnSort(sort_sql)
        )
        self.customColumns.append(cc)
        # ------------------------------- #

        # Tags (L4)
        def cTag4(c, n, t):
            return " ".join(tags_with_level(n, 4))  
             
        sort_sql = getSQL_tagN(4) 
        cc = advBrowser.newCustomColumn(
            type='ctag4',
            name=q('q_Tags_L4'),
            onData=cTag4,
            onSort=getOnSort(sort_sql)
        )
        self.customColumns.append(cc)
        # ------------------------------- #

        # Tags (L5)
        def cTag5(c, n, t):
            return " ".join(tags_with_level(n, 5))  
             
        sort_sql = getSQL_tagN(5) 
        cc = advBrowser.newCustomColumn(
            type='ctag5',
            name=q('q_Tags_L5'),
            onData=cTag5,
            onSort=getOnSort(sort_sql)
        )
        self.customColumns.append(cc)
        # ------------------------------- #


        # ⬆⬆⬆⬆⬆ kaiu: 2026-01-05 nid and cid should be available to non-developers as well ⬆⬆⬆⬆⬆ +++++


        # First review
        def cFirstOnData(c, n, t):
            first = mw.col.db.scalar(
                "select min(id) from revlog where cid = ?", c.id)
            if first:
                return time.strftime("%Y-%m-%d", time.localtime(first / 1000))

        cc = advBrowser.newCustomColumn(
            type='cfirst',
            name=q('q_First_Review'),
            onData=cFirstOnData,
            onSort=lambda: "(select min(id) from revlog where cid = c.id) asc nulls last",
        )
        self.customColumns.append(cc)
        # ------------------------------- #

        # Last review
        def cLastOnData(c, n, t):
            last = mw.col.db.scalar(
                "select max(id) from revlog where cid = ?", c.id)
            if last:
                return time.strftime("%Y-%m-%d", time.localtime(last / 1000))

        cc = advBrowser.newCustomColumn(
            type='clast',
            name=q('q_Last_Review'),
            onData=cLastOnData,
            onSort=lambda: "(select max(id) from revlog where cid = c.id) asc nulls last"
        )
        self.customColumns.append(cc)
        # ------------------------------- #

        # Average time
        def cAvgtimeOnData(c, n, t):
            avgtime = mw.col.db.scalar(
                "select avg(time)/1000.0 from revlog where cid = ?", c.id)
            if avgtime:
                return mw.col.format_timespan(avgtime)
            return None

        cc = advBrowser.newCustomColumn(
            type='cavgtime',
            name=q('q_Time_Average'),
            onData=cAvgtimeOnData,
            onSort=lambda: "(select avg(time) from revlog where cid = c.id) asc nulls last"
        )
        self.customColumns.append(cc)
        # ------------------------------- #

        # Total time
        def cTottimeOnData(c, n, t):
            tottime = mw.col.db.scalar(
                "select sum(time)/1000.0 from revlog where cid = ?", c.id)
            if tottime:
                return mw.col.format_timespan(tottime)
            return None

        cc = advBrowser.newCustomColumn(
            type='ctottime',
            name=q('q_Time_Total'),
            onData=cTottimeOnData,
            onSort=lambda: "(select sum(time) from revlog where cid = c.id) asc nulls last"
        )
        self.customColumns.append(cc)
        # ------------------------------- #

        # Fastest time
        def cFasttimeOnData(c, n, t):
            tm = mw.col.db.scalar(
                "select time/1000.0 from revlog where cid = ? "
                "order by time asc limit 1", c.id)
            if tm:
                return mw.col.format_timespan(tm)
            return None

        # Note: capital ASC required to avoid search+replace
        srt = ("(select time/1000.0 from revlog where cid = c.id "
               "order by time ASC limit 1) asc nulls last")

        cc = advBrowser.newCustomColumn(
            type='cfasttime',
            name=q('q_Fastest_Review'),
            onData=cFasttimeOnData,
            onSort=getOnSort(srt)
        )
        self.customColumns.append(cc)
        # ------------------------------- #

        # Slowest time
        def cSlowtimeOnData(c, n, t):
            tm = mw.col.db.scalar(
                "select time/1000.0 from revlog where cid = ? "
                "order by time desc limit 1", c.id)
            if tm:
                return mw.col.format_timespan(tm)
            return None

        srt = ("(select time/1000.0 from revlog where cid = c.id "
               "order by time DESC limit 1) asc nulls last")

        cc = advBrowser.newCustomColumn(
            type='cslowtime',
            name=q('q_Slowest_Review'),
            onData=cSlowtimeOnData,
            onSort=getOnSort(srt)
        )
        self.customColumns.append(cc)
        # ------------------------------- #

        # Overdue interval
        def cOverdueIvl(c, n, t):
            val = self.valueForOverdue(c.queue, c.type, c.due, c.odue)     
            if val is None:
                return       
            # Display days in the first 3 months https://github.com/AnKing-VIP/advanced-browser/issues/87
            if val > 30 and val < 91: 
                d30 = mw.col.format_timespan(30 * 86400, context=FormatTimeSpanContext.INTERVALS)
                if "30" in d30:                        
                    return d30.replace("30", str(val))
                else:                        
                    return mw.col.format_timespan(val * 86400, context=FormatTimeSpanContext.INTERVALS)
            else:
                return mw.col.format_timespan(val * 86400, context=FormatTimeSpanContext.INTERVALS)



        srt = (f"""
        (select
          (case
             when queue = {QUEUE_TYPE_LRN} then null
             when queue = {QUEUE_TYPE_NEW} then null
             when type = {CARD_TYPE_NEW} then null
             when {mw.col.sched.today} - due <= 0 then null
             when odid then ({mw.col.sched.today} - odue)
             when (queue = {QUEUE_TYPE_REV} or queue = {QUEUE_TYPE_DAY_LEARN_RELEARN} or (type = {CARD_TYPE_REV} and queue < 0)) then ({mw.col.sched.today} - due)
           end
          )
        from cards where id = c.id) asc nulls last""")

        cc = advBrowser.newCustomColumn(
            type='coverdueivl',
            name=q("q_Overdue_Interval"),
            onData=cOverdueIvl,
            onSort=getOnSort(srt)
        )
        self.customColumns.append(cc)
        # ------------------------------- #

        # Percentage of scheduled interval
        def cPercentageSchedIvl(c, n, t):
            val = self.reviewCardPercentageDue(c.odid, c.odue, c.queue, c.type, c.due, c.ivl)
            if val:
                return "{0:.2f}".format(val) + " %"

        srt = (f"""
        (select
          (case
             when odue and (type = {CARD_TYPE_REV} or type = {CARD_TYPE_RELEARNING}) then (
                (({mw.col.sched.today} - odue + ivl) * 1.0) / (ivl * 1.0)
                )
             when (type = {CARD_TYPE_REV} or type = {CARD_TYPE_RELEARNING}) then (
                (({mw.col.sched.today} - due + ivl) * 1.0) / (ivl * 1.0)
                )
             else null
           end
          )
        from cards where id = c.id) asc nulls last""")

        cc = advBrowser.newCustomColumn(
            type='cpercentageschedivl',
            name=q("q_per_of_Ivl"),
            onData=cPercentageSchedIvl,
            onSort=getOnSort(srt)
        )
        self.customColumns.append(cc)
        # ------------------------------- #

        # Previous interval
        def cPrevIvl(c, n, t):
            ivl = mw.col.db.scalar(
                "select ivl from revlog where cid = ? "
                "order by id desc limit 1 offset 1", c.id)
            if ivl is None:
                return
            elif ivl == 0:
                return mw.col.format_timespan(0, context=FormatTimeSpanContext.INTERVALS)
            elif ivl > 0:
                # Display days in the first 3 months https://github.com/AnKing-VIP/advanced-browser/issues/87
                if ivl > 30 and ivl < 91: 
                    d30 = mw.col.format_timespan(30 * 86400, context=FormatTimeSpanContext.INTERVALS)
                    if "30" in d30:                        
                        return d30.replace("30", str(ivl))
                    else:                        
                        return mw.col.format_timespan(ivl * 86400, context=FormatTimeSpanContext.INTERVALS)
                else:
                    return mw.col.format_timespan(ivl * 86400, context=FormatTimeSpanContext.INTERVALS)
            else:
                return mw.col.format_timespan(-ivl, context=FormatTimeSpanContext.INTERVALS)

        srt = ("(select ivl from revlog where cid = c.id "
               "order by id desc limit 1 offset 1) asc nulls last")

        cc = advBrowser.newCustomColumn(
            type='cprevivl',
            name=q("q_Previous_Interval"),
            onData=cPrevIvl,
            onSort=getOnSort(srt)
        )
        self.customColumns.append(cc)
        # ------------------------------- #

        # Total Number of 1/Again (also on new and learning cards)
        def cAgainCount(c, n, t):
            val = mw.col.db.scalar(f"select count() from revlog where cid={c.id} and ease=1")
            if val:
                return val

        cc = advBrowser.newCustomColumn(
            type='cAgainCount',
            name=q("q_Again_Count"),
            onData=cAgainCount,
            onSort=lambda: "(select count() from revlog where cid = c.id and ease=1)"
        )
        self.customColumns.append(cc)
        # ------------------------------- #

        # Percent correct
        def cPctCorrect(c, n, t):
            if c.reps > 0:
                return "{:2.0f}%".format(
                    100 - ((c.lapses / float(c.reps)) * 100))
            return None

        cc = advBrowser.newCustomColumn(
            type='cpct',
            name=q('q_Percent_Correct'),
            onData=cPctCorrect,
            onSort=lambda: "cast(c.lapses as real)/c.reps asc nulls last"
        )
        self.customColumns.append(cc)
        # ------------------------------- #

        # Previous duration
        def cPrevDur(c, n, t):
            time = mw.col.db.scalar(
                "select time/1000.0 from revlog where cid = ? "
                "order by id desc limit 1", c.id)
            if time:
                return mw.col.format_timespan(time)
            return None

        srt = ("(select time/1000.0 from revlog where cid = c.id "
               "order by id desc limit 1) asc nulls last")

        cc = advBrowser.newCustomColumn(
            type='cprevdur',
            name=q("q_Previous_Duration"),
            onData=cPrevDur,
            onSort=getOnSort(srt)
        )
        self.customColumns.append(cc)
        # ------------------------------- #

        # Created Time (Note)
        def cDateTimeCrt(c, n, t):
            return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(c.note().id/1000))

        cc = advBrowser.newCustomColumn(
            type='ctimecrtn',
            name=q('q_Created_Time_Note'),
            onData=cDateTimeCrt,
            onSort=lambda: "n.id asc nulls last"
        )
        self.customColumns.append(cc)
        # ------------------------------- #

        # Created Date (Card)
        def cDateTimeCrt(c, n, t):
            return time.strftime("%Y-%m-%d", time.localtime(c.id/1000))

        cc = advBrowser.newCustomColumn(
            type='cdatecrtc',
            name=q('q_Created_Date_Card'),
            onData=cDateTimeCrt,
            onSort=lambda: "c.id asc nulls last"
        )
        self.customColumns.append(cc)
        # ------------------------------- #

        # Created Time (Card)
        def cDateTimeCrt(c, n, t):
            return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(c.id/1000))

        cc = advBrowser.newCustomColumn(
            type='ctimecrtc',
            name=q('q_Created_Time_Card'),
            onData=cDateTimeCrt,
            onSort=lambda: "c.id asc nulls last"
        )
        self.customColumns.append(cc)
        # ------------------------------- #

        # Current Deck (Filtered)
        def setData(c: Card, value: str):
            old_deck = c.col.decks.get(c.did)
            new_deck = c.col.decks.byName(value)
            if new_deck is None:
                v_str = q("q_not_exists_create_deck") 
                if not askUser(
                        f"%s {v_str}" % value,
                        parent=advBrowser,
                        defaultno=True):
                    return False
                new_id = c.col.decks.id(value)
                new_deck = c.col.decks.get(new_id)
            if new_deck["dyn"] == DECK_DYN and old_deck["dyn"] == DECK_STD:
                # ensuring that if the deck is dynamic, then a
                # standard odid is set
                c.col.sched._moveToDyn(new_deck["id"], [c.id])
            else:
                c.did = new_deck["id"]
                if new_deck["dyn"] == DECK_STD and old_deck["dyn"] == DECK_DYN:
                    # code similar to sched.emptyDyn
                    if c.type == CARD_TYPE_LRN:
                        c.queue = QUEUE_TYPE_NEW
                        c.type = CARD_TYPE_NEW
                    else:
                        c.queue = c.type
                    c.due = c.odue
                    c.odue = 0
                    c.odid = 0
                c.flush()
            return True

        def sortTableFunction():
            col = advBrowser.mw.col
            col.db.execute("drop table if exists tmp")
            col.db.execute("create temp table tmp (k int primary key, v text)")
            for deck in col.decks.all():
                advBrowser.mw.col.db.execute(
                    "insert into tmp values (?,?)", deck['id'], deck['name']
                )
        cc = advBrowser.newCustomColumn(
            type="cdeck",
            name=q("q_Current_Deck_Filtered"),
            onData=lambda c, n, t: advBrowser.mw.col.decks.name(c.did),
            sortTableFunction=sortTableFunction,
            onSort=lambda: "(select v from tmp where k = c.did) collate nocase asc",
            setData=setData,
        )
        self.customColumns.append(cc)
        # ------------------------------- #

        # Flags
        def setData(c: Card, value: str):
            try:
                value = int(value)
            except ValueError:
                value = {"":0, "no":0,"red":1, "orange":2, "green":3, "blue":4, "pink":5, "turquoise":6, "purple":7}.get(value.strip().lower())
                if value is None:
                    return False
            if not 0 <= value <= 7:
                return False
            set_card_flag(parent=advBrowser.browser, card_ids=[c.id], flag=value).run_in_background()
            return True

        cc = advBrowser.newCustomColumn(
            type="cflags",
            name=q("q_Flag"),
            onData=lambda c, n, t: f"{c.flags} - {mw.flags.get_flag(c.flags).label}" if c.flags else None,
            onSort=lambda: "(case when c.flags = 0 then null else c.flags end) asc nulls last",
            setData=setData,
        )
        self.customColumns.append(cc)
        # ------------------------------- #


    def onBuildContextMenu(self, contextMenu):
        """Build our part of the browser columns context menu."""

        v_str = q("q_Advanced")
        group = contextMenu.newSubMenu(f"- {v_str} -")
        for column in self.customColumns:
            group.addItem(column)

    def valueForOverdue(self, queue, type, due, odue):
        if queue == QUEUE_TYPE_LRN:
            return
        elif queue == QUEUE_TYPE_NEW or type == CARD_TYPE_NEW:
            return
        else:
            card_due = odue if odue else due
            diff = mw.col.sched.today - card_due
            if diff <= 0:
                return
            if queue in (QUEUE_TYPE_REV, QUEUE_TYPE_DAY_LEARN_RELEARN) or (type == CARD_TYPE_REV and queue < 0):
                return diff
            else:
                return

    def reviewCardPercentageDue(self, odid, odue, queue, type, due, ivl):
        if odid:
            due = odue
        if queue == QUEUE_TYPE_LRN:
            return 0.0
        elif queue == QUEUE_TYPE_NEW or type == CARD_TYPE_NEW:
            return 0.0
        elif queue in (QUEUE_TYPE_REV, QUEUE_TYPE_DAY_LEARN_RELEARN) or (type == CARD_TYPE_REV and queue < 0):
            try:
                last_rev = due - ivl
                elapsed = mw.col.sched.today - last_rev
                p = elapsed/float(ivl) * 100
                return p
            except ZeroDivisionError:
                return 0.0
        return 0.0

af = AdvancedFields()
addHook("advBrowserLoaded", af.onAdvBrowserLoad)
addHook("advBrowserBuildContext", af.onBuildContextMenu)

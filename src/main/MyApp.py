#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 1.0.4 on Sat Feb 18 18:40:35 2023
#
import os 
import sys
import time

import wx
from typing import Dict
from threading import *
from board import Board
from sudokuresolver import SudokuResolver

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


CLASSIC_SUDOKU_MIN_CLUES = 17

# Define notification event for thread completion
EVT_RESULT_ID = wx.ID_ANY
EVT_PARTIAL_RESULT_ID = wx.ID_ANY


def EVT_RESULT(win, func):
    """Define Result Event."""
    win.Connect(-1, -1, EVT_RESULT_ID, func)

def EVT_PARTIAL_RESULT(win, func):
    """Define Partial Result Event."""
    win.Connect(-1, -1, EVT_PARTIAL_RESULT_ID, func)

class ResultEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""
    def __init__(self, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_RESULT_ID)
        self.data = data

class PartialResultEvent(wx.PyEvent):
    """
    Simple event to carry the value of one cell of the board.
    The value might be not the same in the final solution.
    """
    def __init__(self, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_PARTIAL_RESULT_ID)
        self.data = data

# Thread class that executes processing
class ResolverThread(Thread):
    """Worker Thread Class."""
    def __init__(self, notify_window, resolver: SudokuResolver):
        """Init Worker Thread Class."""
        Thread.__init__(self)
        self._notify_window = notify_window
        self._want_abort = False
        self._resolver = resolver
        self.has_next = 1        

    def run(self):
        """Run Worker Thread."""
        # # resolve() completes when the whole solution is found
        # solution = self._resolver.resolve()
        
        # # Here's where the result would be returned (it could be
        # # any Python object)
        # wx.PostEvent(self._notify_window, ResultEvent(solution))

        self._resolver.run(self.callback)

    def callback(self, cell, value) -> None:
        if self._want_abort:
            wx.PostEvent(self._notify_window, PartialResultEvent((None,None)))
            print(f"Aborting...")
            self._resolver.stop()
            return

        self.has_next = value
        if self.has_next:
            wx.PostEvent(self._notify_window, PartialResultEvent((cell, value)))
            time.sleep(0.0000000000000001)
        else:
            print(f"Reached last cell... exiting")
            return

    def abort(self):
        """abort worker thread."""
        # Method for use by main thread to signal an abort
        self._want_abort = True


class CsFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        
        self.clues = {}
        self.worker = None

        # begin wxGlade: CsFrame.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((520, 586))
        self.SetTitle("Classic Sudoku Resolver")

        self.panel_1 = wx.Panel(self, wx.ID_ANY)
        self.panel_1.SetMinSize((510, 510))
        self.panel_1.SetMaxSize((500,500))

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        header = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(header, 1, wx.BOTTOM | wx.EXPAND | wx.TOP, 4)

        self.bt_resolve = wx.Button(self.panel_1, wx.ID_ANY, "Resolve")
        header.Add(self.bt_resolve, 0, 0, 0)

        self.lb_status = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
        self.lb_status.SetBackgroundColour(wx.Colour(233, 233, 233))
        self.lb_status.SetFont(wx.Font(9, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Palatino Linotype"))
        header.Add(self.lb_status, 0, 0, 0)

        self.bt_stop = wx.Button(self.panel_1, wx.ID_ANY, "Stop")
        header.Add(self.bt_stop, 0, 0, 0)

        self.board = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(self.board, 1, wx.EXPAND, 0)

        row_11 = wx.BoxSizer(wx.HORIZONTAL)
        self.board.Add(row_11, 1, wx.EXPAND, 0)

        col_11 = wx.GridSizer(3, 3, 1, 1)
        row_11.Add(col_11, 1, wx.BOTTOM | wx.EXPAND | wx.RIGHT, 1)

        self.cell_11 = wx.TextCtrl(self.panel_1, 11, "")
        self.cell_11.SetMinSize((52, 52))
        self.cell_11.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_11.SetMaxLength(1)
        col_11.Add(self.cell_11, 0, 0, 0)

        self.cell_12 = wx.TextCtrl(self.panel_1, 12, "")
        self.cell_12.SetMinSize((52, 52))
        self.cell_12.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_12.SetMaxLength(1)
        col_11.Add(self.cell_12, 0, 0, 0)

        self.cell_13 = wx.TextCtrl(self.panel_1, 13, "")
        self.cell_13.SetMinSize((52, 52))
        self.cell_13.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_13.SetMaxLength(1)
        col_11.Add(self.cell_13, 0, 0, 0)

        self.cell_21 = wx.TextCtrl(self.panel_1, 21, "")
        self.cell_21.SetMinSize((52, 52))
        self.cell_21.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_21.SetMaxLength(1)
        col_11.Add(self.cell_21, 0, 0, 0)

        self.cell_22 = wx.TextCtrl(self.panel_1, 22, "")
        self.cell_22.SetMinSize((52, 52))
        self.cell_22.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_22.SetMaxLength(1)
        col_11.Add(self.cell_22, 0, 0, 0)

        self.cell_23 = wx.TextCtrl(self.panel_1, 23, "")
        self.cell_23.SetMinSize((52, 52))
        self.cell_23.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_23.SetMaxLength(1)
        col_11.Add(self.cell_23, 0, 0, 0)

        self.cell_31 = wx.TextCtrl(self.panel_1, 31, "")
        self.cell_31.SetMinSize((52, 52))
        self.cell_31.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_31.SetMaxLength(1)
        col_11.Add(self.cell_31, 0, 0, 0)

        self.cell_32 = wx.TextCtrl(self.panel_1, 32, "")
        self.cell_32.SetMinSize((52, 52))
        self.cell_32.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_32.SetMaxLength(1)
        col_11.Add(self.cell_32, 0, 0, 0)

        self.cell_33 = wx.TextCtrl(self.panel_1, 33, "")
        self.cell_33.SetMinSize((52, 52))
        self.cell_33.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_33.SetMaxLength(1)
        col_11.Add(self.cell_33, 0, 0, 0)

        static_line_8 = wx.StaticLine(self.panel_1, wx.ID_ANY, style=wx.LI_VERTICAL)
        static_line_8.SetMinSize((4, 164))
        row_11.Add(static_line_8, 0, wx.EXPAND, 0)

        col_21 = wx.GridSizer(3, 3, 1, 1)
        row_11.Add(col_21, 1, wx.BOTTOM | wx.EXPAND | wx.LEFT | wx.RIGHT, 1)

        self.cell_14 = wx.TextCtrl(self.panel_1, 14, "")
        self.cell_14.SetMinSize((52, 52))
        self.cell_14.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_14.SetMaxLength(1)
        col_21.Add(self.cell_14, 0, 0, 0)

        self.cell_15 = wx.TextCtrl(self.panel_1, 15, "")
        self.cell_15.SetMinSize((52, 52))
        self.cell_15.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_15.SetMaxLength(1)
        col_21.Add(self.cell_15, 0, 0, 0)

        self.cell_16 = wx.TextCtrl(self.panel_1, 16, "")
        self.cell_16.SetMinSize((52, 52))
        self.cell_16.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_16.SetMaxLength(1)
        col_21.Add(self.cell_16, 0, 0, 0)

        self.cell_24 = wx.TextCtrl(self.panel_1, 24, "")
        self.cell_24.SetMinSize((52, 52))
        self.cell_24.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_24.SetMaxLength(1)
        col_21.Add(self.cell_24, 0, 0, 0)

        self.cell_25 = wx.TextCtrl(self.panel_1, 25, "")
        self.cell_25.SetMinSize((52, 52))
        self.cell_25.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_25.SetMaxLength(1)
        col_21.Add(self.cell_25, 0, 0, 0)

        self.cell_26 = wx.TextCtrl(self.panel_1, 26, "")
        self.cell_26.SetMinSize((52, 52))
        self.cell_26.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_26.SetMaxLength(1)
        col_21.Add(self.cell_26, 0, 0, 0)

        self.cell_34 = wx.TextCtrl(self.panel_1, 34, "")
        self.cell_34.SetMinSize((52, 52))
        self.cell_34.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_34.SetMaxLength(1)
        col_21.Add(self.cell_34, 0, 0, 0)

        self.cell_35 = wx.TextCtrl(self.panel_1, 35, "")
        self.cell_35.SetMinSize((52, 52))
        self.cell_35.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_35.SetMaxLength(1)
        col_21.Add(self.cell_35, 0, 0, 0)

        self.cell_36 = wx.TextCtrl(self.panel_1, 36, "")
        self.cell_36.SetMinSize((52, 52))
        self.cell_36.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_36.SetMaxLength(1)
        col_21.Add(self.cell_36, 0, 0, 0)

        static_line_7 = wx.StaticLine(self.panel_1, wx.ID_ANY, style=wx.LI_VERTICAL)
        static_line_7.SetMinSize((4, 164))
        row_11.Add(static_line_7, 0, wx.EXPAND, 0)

        col_31 = wx.GridSizer(3, 3, 1, 1)
        row_11.Add(col_31, 1, wx.BOTTOM | wx.EXPAND | wx.LEFT, 1)

        self.cell_17 = wx.TextCtrl(self.panel_1, 17, "")
        self.cell_17.SetMinSize((52, 52))
        self.cell_17.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_17.SetMaxLength(1)
        col_31.Add(self.cell_17, 0, 0, 0)

        self.cell_18 = wx.TextCtrl(self.panel_1, 18, "")
        self.cell_18.SetMinSize((52, 52))
        self.cell_18.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_18.SetMaxLength(1)
        col_31.Add(self.cell_18, 0, 0, 0)

        self.cell_19 = wx.TextCtrl(self.panel_1, 19, "")
        self.cell_19.SetMinSize((52, 52))
        self.cell_19.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_19.SetMaxLength(1)
        col_31.Add(self.cell_19, 0, 0, 0)

        self.cell_27 = wx.TextCtrl(self.panel_1, 27, "")
        self.cell_27.SetMinSize((52, 52))
        self.cell_27.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_27.SetMaxLength(1)
        col_31.Add(self.cell_27, 0, 0, 0)

        self.cell_28 = wx.TextCtrl(self.panel_1, 28, "")
        self.cell_28.SetMinSize((52, 52))
        self.cell_28.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_28.SetMaxLength(1)
        col_31.Add(self.cell_28, 0, 0, 0)

        self.cell_29 = wx.TextCtrl(self.panel_1, 29, "")
        self.cell_29.SetMinSize((52, 52))
        self.cell_29.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_29.SetMaxLength(1)
        col_31.Add(self.cell_29, 0, 0, 0)

        self.cell_37 = wx.TextCtrl(self.panel_1, 37, "")
        self.cell_37.SetMinSize((52, 52))
        self.cell_37.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_37.SetMaxLength(1)
        col_31.Add(self.cell_37, 0, 0, 0)

        self.cell_38 = wx.TextCtrl(self.panel_1, 38, "")
        self.cell_38.SetMinSize((52, 52))
        self.cell_38.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_38.SetMaxLength(1)
        col_31.Add(self.cell_38, 0, 0, 0)

        self.cell_39 = wx.TextCtrl(self.panel_1, 39, "")
        self.cell_39.SetMinSize((52, 52))
        self.cell_39.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_39.SetMaxLength(1)
        col_31.Add(self.cell_39, 0, 0, 0)

        static_line_1 = wx.StaticLine(self.panel_1, wx.ID_ANY)
        static_line_1.SetMinSize((504, 4))
        static_line_1.SetBackgroundColour(wx.Colour(216, 216, 191))
        self.board.Add(static_line_1, 0, wx.EXPAND, 0)

        row_41 = wx.BoxSizer(wx.HORIZONTAL)
        self.board.Add(row_41, 1, wx.ALL | wx.EXPAND, 1)

        col_41 = wx.GridSizer(3, 3, 1, 1)
        row_41.Add(col_41, 1, wx.BOTTOM | wx.EXPAND | wx.RIGHT | wx.TOP, 1)

        self.cell_41 = wx.TextCtrl(self.panel_1, 41, "")
        self.cell_41.SetMinSize((52, 52))
        self.cell_41.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_41.SetMaxLength(1)
        col_41.Add(self.cell_41, 0, 0, 0)

        self.cell_42 = wx.TextCtrl(self.panel_1, 42, "")
        self.cell_42.SetMinSize((52, 52))
        self.cell_42.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_42.SetMaxLength(1)
        col_41.Add(self.cell_42, 0, 0, 0)

        self.cell_43 = wx.TextCtrl(self.panel_1, 43, "")
        self.cell_43.SetMinSize((52, 52))
        self.cell_43.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_43.SetMaxLength(1)
        col_41.Add(self.cell_43, 0, 0, 0)

        self.cell_51 = wx.TextCtrl(self.panel_1, 51, "")
        self.cell_51.SetMinSize((52, 52))
        self.cell_51.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_51.SetMaxLength(1)
        col_41.Add(self.cell_51, 0, 0, 0)

        self.cell_52 = wx.TextCtrl(self.panel_1, 52, "")
        self.cell_52.SetMinSize((52, 52))
        self.cell_52.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_52.SetMaxLength(1)
        col_41.Add(self.cell_52, 0, 0, 0)

        self.cell_53 = wx.TextCtrl(self.panel_1, 53, "")
        self.cell_53.SetMinSize((52, 52))
        self.cell_53.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_53.SetMaxLength(1)
        col_41.Add(self.cell_53, 0, 0, 0)

        self.cell_61 = wx.TextCtrl(self.panel_1, 61, "")
        self.cell_61.SetMinSize((52, 52))
        self.cell_61.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_61.SetMaxLength(1)
        col_41.Add(self.cell_61, 0, 0, 0)

        self.cell_62 = wx.TextCtrl(self.panel_1, 62, "")
        self.cell_62.SetMinSize((52, 52))
        self.cell_62.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_62.SetMaxLength(1)
        col_41.Add(self.cell_62, 0, 0, 0)

        self.cell_63 = wx.TextCtrl(self.panel_1, 63, "")
        self.cell_63.SetMinSize((52, 52))
        self.cell_63.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_63.SetMaxLength(1)
        col_41.Add(self.cell_63, 0, 0, 0)

        static_line_6 = wx.StaticLine(self.panel_1, wx.ID_ANY, style=wx.LI_VERTICAL)
        static_line_6.SetMinSize((4, 164))
        row_41.Add(static_line_6, 0, wx.EXPAND, 0)

        col_44 = wx.GridSizer(3, 3, 1, 1)
        row_41.Add(col_44, 1, wx.ALL | wx.EXPAND, 1)

        self.cell_44 = wx.TextCtrl(self.panel_1, 44, "")
        self.cell_44.SetMinSize((52, 52))
        self.cell_44.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_44.SetMaxLength(1)
        col_44.Add(self.cell_44, 0, 0, 0)

        self.cell_45 = wx.TextCtrl(self.panel_1, 45, "")
        self.cell_45.SetMinSize((52, 52))
        self.cell_45.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_45.SetMaxLength(1)
        col_44.Add(self.cell_45, 0, 0, 0)

        self.cell_46 = wx.TextCtrl(self.panel_1, 46, "")
        self.cell_46.SetMinSize((52, 52))
        self.cell_46.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_46.SetMaxLength(1)
        col_44.Add(self.cell_46, 0, 0, 0)

        self.cell_54 = wx.TextCtrl(self.panel_1, 54, "")
        self.cell_54.SetMinSize((52, 52))
        self.cell_54.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_54.SetMaxLength(1)
        col_44.Add(self.cell_54, 0, 0, 0)

        self.cell_55 = wx.TextCtrl(self.panel_1, 55, "")
        self.cell_55.SetMinSize((52, 52))
        self.cell_55.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_55.SetMaxLength(1)
        col_44.Add(self.cell_55, 0, 0, 0)

        self.cell_56 = wx.TextCtrl(self.panel_1, 56, "")
        self.cell_56.SetMinSize((52, 52))
        self.cell_56.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_56.SetMaxLength(1)
        col_44.Add(self.cell_56, 0, 0, 0)

        self.cell_64 = wx.TextCtrl(self.panel_1, 64, "")
        self.cell_64.SetMinSize((52, 52))
        self.cell_64.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_64.SetMaxLength(1)
        col_44.Add(self.cell_64, 0, 0, 0)

        self.cell_65 = wx.TextCtrl(self.panel_1, 65, "")
        self.cell_65.SetMinSize((52, 52))
        self.cell_65.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_65.SetMaxLength(1)
        col_44.Add(self.cell_65, 0, 0, 0)

        self.cell_66 = wx.TextCtrl(self.panel_1, 66, "")
        self.cell_66.SetMinSize((52, 52))
        self.cell_66.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_66.SetMaxLength(1)
        col_44.Add(self.cell_66, 0, 0, 0)

        static_line_5 = wx.StaticLine(self.panel_1, wx.ID_ANY, style=wx.LI_VERTICAL)
        static_line_5.SetMinSize((4, 164))
        row_41.Add(static_line_5, 0, wx.EXPAND, 0)

        col_47 = wx.GridSizer(3, 3, 1, 1)
        row_41.Add(col_47, 1, wx.BOTTOM | wx.EXPAND | wx.LEFT | wx.TOP, 1)

        self.cell_47 = wx.TextCtrl(self.panel_1, 47, "")
        self.cell_47.SetMinSize((52, 52))
        self.cell_47.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_47.SetMaxLength(1)
        col_47.Add(self.cell_47, 0, 0, 0)

        self.cell_48 = wx.TextCtrl(self.panel_1, 48, "")
        self.cell_48.SetMinSize((52, 52))
        self.cell_48.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_48.SetMaxLength(1)
        col_47.Add(self.cell_48, 0, 0, 0)

        self.cell_49 = wx.TextCtrl(self.panel_1, 49, "")
        self.cell_49.SetMinSize((52, 52))
        self.cell_49.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_49.SetMaxLength(1)
        col_47.Add(self.cell_49, 0, 0, 0)

        self.cell_57 = wx.TextCtrl(self.panel_1, 57, "")
        self.cell_57.SetMinSize((52, 52))
        self.cell_57.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_57.SetMaxLength(1)
        col_47.Add(self.cell_57, 0, 0, 0)

        self.cell_58 = wx.TextCtrl(self.panel_1, 58, "")
        self.cell_58.SetMinSize((52, 52))
        self.cell_58.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_58.SetMaxLength(1)
        col_47.Add(self.cell_58, 0, 0, 0)

        self.cell_59 = wx.TextCtrl(self.panel_1, 59, "")
        self.cell_59.SetMinSize((52, 52))
        self.cell_59.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_59.SetMaxLength(1)
        col_47.Add(self.cell_59, 0, 0, 0)

        self.cell_67 = wx.TextCtrl(self.panel_1, 67, "")
        self.cell_67.SetMinSize((52, 52))
        self.cell_67.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_67.SetMaxLength(1)
        col_47.Add(self.cell_67, 0, 0, 0)

        self.cell_68 = wx.TextCtrl(self.panel_1, 68, "")
        self.cell_68.SetMinSize((52, 52))
        self.cell_68.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_68.SetMaxLength(1)
        col_47.Add(self.cell_68, 0, 0, 0)

        self.cell_69 = wx.TextCtrl(self.panel_1, 69, "")
        self.cell_69.SetMinSize((52, 52))
        self.cell_69.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_69.SetMaxLength(1)
        col_47.Add(self.cell_69, 0, 0, 0)

        static_line_2 = wx.StaticLine(self.panel_1, wx.ID_ANY)
        static_line_2.SetMinSize((504, 4))
        static_line_2.SetBackgroundColour(wx.Colour(216, 216, 191))
        self.board.Add(static_line_2, 0, wx.EXPAND, 0)

        row_71 = wx.BoxSizer(wx.HORIZONTAL)
        self.board.Add(row_71, 1, wx.ALL | wx.EXPAND, 1)

        col_71 = wx.GridSizer(3, 3, 1, 1)
        row_71.Add(col_71, 1, wx.EXPAND | wx.RIGHT | wx.TOP, 1)

        self.cell_71 = wx.TextCtrl(self.panel_1, 71, "")
        self.cell_71.SetMinSize((52, 52))
        self.cell_71.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_71.SetMaxLength(1)
        col_71.Add(self.cell_71, 0, 0, 0)

        self.cell_72 = wx.TextCtrl(self.panel_1, 72, "")
        self.cell_72.SetMinSize((52, 52))
        self.cell_72.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_72.SetMaxLength(1)
        col_71.Add(self.cell_72, 0, 0, 0)

        self.cell_73 = wx.TextCtrl(self.panel_1, 73, "")
        self.cell_73.SetMinSize((52, 52))
        self.cell_73.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_73.SetMaxLength(1)
        col_71.Add(self.cell_73, 0, 0, 0)

        self.cell_81 = wx.TextCtrl(self.panel_1, 81, "")
        self.cell_81.SetMinSize((52, 52))
        self.cell_81.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_81.SetMaxLength(1)
        col_71.Add(self.cell_81, 0, 0, 0)

        self.cell_82 = wx.TextCtrl(self.panel_1, 82, "")
        self.cell_82.SetMinSize((52, 52))
        self.cell_82.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_82.SetMaxLength(1)
        col_71.Add(self.cell_82, 0, 0, 0)

        self.cell_83 = wx.TextCtrl(self.panel_1, 83, "")
        self.cell_83.SetMinSize((52, 52))
        self.cell_83.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_83.SetMaxLength(1)
        col_71.Add(self.cell_83, 0, 0, 0)

        self.cell_91 = wx.TextCtrl(self.panel_1, 91, "")
        self.cell_91.SetMinSize((52, 52))
        self.cell_91.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_91.SetMaxLength(1)
        col_71.Add(self.cell_91, 0, 0, 0)

        self.cell_92 = wx.TextCtrl(self.panel_1, 92, "")
        self.cell_92.SetMinSize((52, 52))
        self.cell_92.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_92.SetMaxLength(1)
        col_71.Add(self.cell_92, 0, 0, 0)

        self.cell_93 = wx.TextCtrl(self.panel_1, 93, "")
        self.cell_93.SetMinSize((52, 52))
        self.cell_93.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_93.SetMaxLength(1)
        col_71.Add(self.cell_93, 0, 0, 0)

        static_line_3 = wx.StaticLine(self.panel_1, wx.ID_ANY, style=wx.LI_VERTICAL)
        static_line_3.SetMinSize((4, 164))
        row_71.Add(static_line_3, 0, wx.EXPAND, 0)

        col_74 = wx.GridSizer(3, 3, 1, 1)
        row_71.Add(col_74, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 1)

        self.cell_74 = wx.TextCtrl(self.panel_1, 74, "")
        self.cell_74.SetMinSize((52, 52))
        self.cell_74.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_74.SetMaxLength(1)
        col_74.Add(self.cell_74, 0, 0, 0)

        self.cell_75 = wx.TextCtrl(self.panel_1, 75, "")
        self.cell_75.SetMinSize((52, 52))
        self.cell_75.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_75.SetMaxLength(1)
        col_74.Add(self.cell_75, 0, 0, 0)

        self.cell_76 = wx.TextCtrl(self.panel_1, 76, "")
        self.cell_76.SetMinSize((52, 52))
        self.cell_76.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_76.SetMaxLength(1)
        col_74.Add(self.cell_76, 0, 0, 0)

        self.cell_84 = wx.TextCtrl(self.panel_1, 84, "")
        self.cell_84.SetMinSize((52, 52))
        self.cell_84.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_84.SetMaxLength(1)
        col_74.Add(self.cell_84, 0, 0, 0)

        self.cell_85 = wx.TextCtrl(self.panel_1, 85, "")
        self.cell_85.SetMinSize((52, 52))
        self.cell_85.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_85.SetMaxLength(1)
        col_74.Add(self.cell_85, 0, 0, 0)

        self.cell_86 = wx.TextCtrl(self.panel_1, 86, "")
        self.cell_86.SetMinSize((52, 52))
        self.cell_86.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_86.SetMaxLength(1)
        col_74.Add(self.cell_86, 0, 0, 0)

        self.cell_94 = wx.TextCtrl(self.panel_1, 94, "")
        self.cell_94.SetMinSize((52, 52))
        self.cell_94.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_94.SetMaxLength(1)
        col_74.Add(self.cell_94, 0, 0, 0)

        self.cell_95 = wx.TextCtrl(self.panel_1, 95, "")
        self.cell_95.SetMinSize((52, 52))
        self.cell_95.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_95.SetMaxLength(1)
        col_74.Add(self.cell_95, 0, 0, 0)

        self.cell_96 = wx.TextCtrl(self.panel_1, 96, "")
        self.cell_96.SetMinSize((52, 52))
        self.cell_96.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_96.SetMaxLength(1)
        col_74.Add(self.cell_96, 0, 0, 0)

        static_line_4 = wx.StaticLine(self.panel_1, wx.ID_ANY, style=wx.LI_VERTICAL)
        static_line_4.SetMinSize((4, 164))
        row_71.Add(static_line_4, 0, wx.EXPAND, 0)

        col_77 = wx.GridSizer(3, 3, 1, 1)
        row_71.Add(col_77, 1, wx.EXPAND | wx.LEFT | wx.TOP, 1)

        self.cell_77 = wx.TextCtrl(self.panel_1, 77, "")
        self.cell_77.SetMinSize((52, 52))
        self.cell_77.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_77.SetMaxLength(1)
        col_77.Add(self.cell_77, 0, 0, 0)

        self.cell_78 = wx.TextCtrl(self.panel_1, 78, "")
        self.cell_78.SetMinSize((52, 52))
        self.cell_78.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_78.SetMaxLength(1)
        col_77.Add(self.cell_78, 0, 0, 0)

        self.cell_79 = wx.TextCtrl(self.panel_1, 79, "")
        self.cell_79.SetMinSize((52, 52))
        self.cell_79.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_79.SetMaxLength(1)
        col_77.Add(self.cell_79, 0, 0, 0)

        self.cell_87 = wx.TextCtrl(self.panel_1, 87, "")
        self.cell_87.SetMinSize((52, 52))
        self.cell_87.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_87.SetMaxLength(1)
        col_77.Add(self.cell_87, 0, 0, 0)

        self.cell_88 = wx.TextCtrl(self.panel_1, 88, "")
        self.cell_88.SetMinSize((52, 52))
        self.cell_88.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_88.SetMaxLength(1)
        col_77.Add(self.cell_88, 0, 0, 0)

        self.cell_89 = wx.TextCtrl(self.panel_1, 89, "")
        self.cell_89.SetMinSize((52, 52))
        self.cell_89.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_89.SetMaxLength(1)
        col_77.Add(self.cell_89, 0, 0, 0)

        self.cell_97 = wx.TextCtrl(self.panel_1, 97, "")
        self.cell_97.SetMinSize((52, 52))
        self.cell_97.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_97.SetMaxLength(1)
        col_77.Add(self.cell_97, 0, 0, 0)

        self.cell_98 = wx.TextCtrl(self.panel_1, 98, "")
        self.cell_98.SetMinSize((52, 52))
        self.cell_98.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_98.SetMaxLength(1)
        col_77.Add(self.cell_98, 0, 0, 0)

        self.cell_99 = wx.TextCtrl(self.panel_1, 99, "")
        self.cell_99.SetMinSize((52, 52))
        self.cell_99.SetFont(wx.Font(32, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.cell_99.SetMaxLength(1)
        col_77.Add(self.cell_99, 0, 0, 0)

        self.panel_1.SetSizer(sizer_1)

        self.Layout()
        self.Centre()
        EVT_RESULT(self, self.on_result)
        EVT_PARTIAL_RESULT(self, self.on_partial_result)

        self.Bind(wx.EVT_BUTTON, self.on_bt_resolve_pressed, self.bt_resolve)
        self.Bind(wx.EVT_BUTTON, self.on_bt_stop_pressed, self.bt_stop)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_11)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_12)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_13)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_21)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_22)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_23)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_31)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_32)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_33)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_14)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_15)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_16)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_24)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_25)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_26)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_34)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_35)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_36)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_17)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_18)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_19)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_27)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_28)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_29)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_37)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_38)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_39)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_41)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_42)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_43)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_51)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_52)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_53)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_61)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_62)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_63)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_44)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_45)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_46)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_54)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_55)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_56)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_64)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_65)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_66)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_47)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_48)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_49)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_57)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_58)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_59)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_67)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_68)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_69)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_71)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_72)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_73)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_81)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_82)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_83)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_91)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_92)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_93)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_74)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_75)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_76)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_84)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_85)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_86)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_94)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_95)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_96)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_77)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_78)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_79)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_87)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_88)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_89)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_97)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_98)
        self.Bind(wx.EVT_TEXT, self.on_txt, self.cell_99)
        # end wxGlade

    def on_bt_resolve_pressed(self, event):  # wxGlade: CsFrame.<event_handler>
        print("Event handler 'on_bt_resolve_pressed' called!")
        # print("abs path of current dir -->" + os.path.abspath("."))
        # for p in sys.path:
        #     print("path --> "+ p)
        self.lb_status.SetLabel('Processing...')

        self.clues_dict = {
           12:4,14:3,17:6,21:1,22:2,25:7,28:4,36:8,39:1,41:9,56:6,57:5,
           61:4,64:9,67:3,72:1,73:2,75:5,81:3,91:7,93:9,95:2,97:8,98:1
        }

        # validate that there are clues: min is 17 for classic sudoku
        if len(self.clues_dict.keys()) < CLASSIC_SUDOKU_MIN_CLUES:
            wx.MessageBox("Too few clues provided. Minimum expected for classic Sudoku is 17",
            "Error: invalid number of clues", wx.OK)
            print(f"Not enough clues provided: {len(self.clues_dict.keys())}")
            event.Skip()
            return
        
        # start execution
        b = Board(self.clues_dict)
        self.resolver = SudokuResolver(b)
        self.resolver.print_board()

        # load the clue cells first
        self.load_board(b.get_board())
        
        self.worker = ResolverThread(self, resolver=self.resolver)
        self.worker.start()


    def on_result(self, event):
        """Show Result status."""
        # if event.data is None:
        #     # Thread aborted (using our convention of None return)
        #     wx.MessageBox("Computation aborted", "Abort", wx.OK)
        # else:
        #     # Process results here
        #     print("Finished")
        #     # self.load_board(event.data)
        # # In either event, the worker is done
        #     self.worker = None
        # event.Skip()
    
    def load_board(self, board: Dict[int, int]) -> None:
        """
        Load the given resolved sudoku in the GUI 
        """
        for k in board.keys():
            if board[k] == 0:
                continue
            wx_cell = self.FindWindowById(k)
            wx_cell.SetValue(str(board[k]))
            wx_cell.SetForegroundColour(wx.Colour(255, 0, 0))


    def on_partial_result(self, event):
        cell, value = event.data
        if not value:
            wx.MessageBox(message="Stop called: empty event",caption="Info",style=wx.OK)
            self.worker = None
            self.lb_status.SetValue("Stopped")
        else:
            wx_cell = self.FindWindowById(cell)
            wx_cell.SetValue(str(value))
        event.Skip()

    def on_txt(self, event):  # wxGlade: CsFrame.<event_handler>
        """
        Called when something is written in one of the board's cells.
        """
        print("Event handler 'on_txt' called AND ignored!")

        # cell_id = event.GetId()
        # value = event.GetString()
        # print(f"Text entered in cell {str(cell_id)} -> {value}")

        # if value == '':
        #     if cell_id in self.clues.keys():
        #         self.clues.pop(cell_id)
        #         print(f"Emptied cell {cell_id}")
        # else:
        #     try:
        #         value_int = int(value)
        #         if value_int > 0 and value_int < 10:
        #             self.clues[cell_id] = value
        #             print(f"Entered value (cell -> val) {cell_id} -> {value}")
        #         else:
        #             print(f"Invalid value: out of range: {value}")
        #     except ValueError:
        #         # could not parse to int
        #         print(f"Invalid value: not a number: {value}")
    
        event.Skip()

    def on_bt_stop_pressed(self, event) -> None:  # wxGlade: CsFrame.<event_handler>
        print("Event handler 'on_bt_stop_pressed' called")
        if self.worker:
            self.lb_status.SetValue("Stopping...")
            self.worker.abort()
        event.Skip()
# end of class CsFrame

class MyApp(wx.App):
    def OnInit(self):
        self.frame = CsFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

# end of class MyApp

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()

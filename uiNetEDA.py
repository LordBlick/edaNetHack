#!/usr/bin/python2
# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-
# -*- tabstop: 4 -*-

from txtViewSrch import searchTextView
import wgts as wg
gtk, pango =  wg.gtk, wg.pango

class edaNetUI:
	def __init__(ui):
		ui.fontSmall = pango.FontDescription('Univers,Sans Condensed 7')
		ui.fontDesc = pango.FontDescription('Univers,Sans Condensed 8')
		ui.fontFixedDesc = pango.FontDescription('Terminus,Monospace Bold 7')
		ui.uiInit()
		if __name__ == "__main__":
			ui.logView.insert_end("User Interface Test\n Press Clear...\n")
			ui.mainWindow.connect("destroy", lambda w: ui.uiExit())
			ui.buttonExit.connect("clicked", lambda w: ui.uiExit())
			ui.uiEnter()

	uiEnter = lambda ui: gtk.main()
	uiExit = lambda ui: gtk.main_quit()

	def uiInit(ui):
		from os import path as ph
		rp = ui.runpath = ph.dirname(ph.realpath(__file__))
		if __name__ == "__main__":
			ui.cfg = {}
		from gobject import TYPE_STRING as goStr, TYPE_INT as goInt, TYPE_PYOBJECT as goPyObj
		ui.version = .2
		ui.title = "KiCAD netlist spoiller v.%0.2f." % ui.version
		ui.mainWindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
		w, h, ui.hgtLower = (640, 300, wg.Height+50)
		ui.mainWindow.set_geometry_hints(min_width=w, min_height=h)
		ui.mainWindow.resize(w, h)
		ui.mainWindow.set_title(ui.title)
		ui.mainWindow.set_border_width(5)
		ui.accGroup = gtk.AccelGroup()
		ui.mainWindow.add_accel_group(ui.accGroup)
		ui.cfBPixbuf = gtk.gdk.pixbuf_new_from_file(rp+"/pic/logview.png")
		gtk.window_set_default_icon_list(ui.cfBPixbuf, )
		
		baseFx = ui.mnFx = gtk.Fixed()

		ui.logView = wg.TextView(baseFx, 5, 5, 0, 0,
			bEditable=False, bWrap=True, tabSpace=4, fontDesc = ui.fontFixedDesc)
		ui.stv = searchTextView(ui, ui.mainWindow, ui.logView)

		ui.labFilename = wg.Label("File:", baseFx, 0, 0, 30)
		if __name__ == "__main__":
			ui.txtFilename = wg.Butt('Test', baseFx, 0, 0, 0)
		else:
			ui.txtFilename = wg.Label(u'Drag *.net file to log view or use „Open” button →',
				baseFx, 0, 0, 0, xalign=0., selectable=True)
		ui.buttonSelectFile = wg.Butt(None, baseFx, 0, 0, 30, stockID=gtk.STOCK_OPEN)
		ui.buttonSelectFile.set_tooltip_text('Select File')
		ui.buttonAllNetsGlobal = wg.Butt("Globalize", baseFx, 0,0, 60)
		ui.buttonAllNetsGlobal.set_tooltip_text('Globalize all nets in file…')
		ui.buttonRestore = wg.Butt(None, baseFx, 0, 0, 25, stockID=gtk.STOCK_REVERT_TO_SAVED)
		ui.buttonRestore.set_tooltip_text('Restore')

		ui.buttonSearchLog = wg.Butt(None, baseFx, 0, 0, 25, stockID=gtk.STOCK_FIND)
		ui.buttonSearchLog.set_tooltip_text('Search Log View…')
		ui.buttonSearchLog.add_accelerator("clicked", ui.accGroup, ord('F'),
			gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
		ui.buttonSearchLog.connect("clicked", ui.stv.showDlgSrch)


		ui.buttonClear = wg.Butt("Clear log", baseFx, 5, 0, 65)
		ui.buttonClear.set_tooltip_text('Clear Log View…')
		ui.buttonClear.connect("clicked", lambda x: ui.logView.clear_text())
		ui.warn = wg.Label('Disclaimer: use on your own risk…', baseFx, 0, 0, 170)

		ui.checkTest = wg.Check("Test Only", baseFx, 0, 0, 65)
		ui.checkTest.set_active(True)

		ui.buttonExit = wg.Butt("Exit (Ctrl+Q)", baseFx, 0, 0, 70)
		ui.buttonExit.add_accelerator("clicked", ui.accGroup, ord('Q'),
			gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
		
		ui.mainWindow.add(baseFx)
		ui.mainWindow.show_all()
		ui.mainWindow.set_keep_above(True)
		ui.lastWinSize = None
		ui.mainWindow.connect("configure-event", ui.uiSize)
		
		ui.netFilter = gtk.FileFilter()
		ui.netFilter.set_name("KiCad network list (*.net)")
		ui.netFilter.add_pattern("*.net")

	def uiSize(ui, window, event):
		if event.type==gtk.gdk.CONFIGURE:
			w, h = event.width, event.height
			#print ("eventType: %s, w:%d, h:%d" % (event.type, w, h))
			if ui.lastWinSize==(w, h):
				return True
			wgH = wg.Height
			ui.lastWinSize = w, h
			baseFx = ui.mnFx
			ha = h - ui.hgtLower - 5
			ui.logView.size(w-20, ha)
			y = ha + 10
			baseFx.move(ui.labFilename, 5, y)
			baseFx.move(ui.txtFilename, 35, y)
			ui.txtFilename.size(w-180, wgH)
			baseFx.move(ui.buttonSelectFile, w-140, y)
			baseFx.move(ui.buttonAllNetsGlobal, w-105, y)
			baseFx.move(ui.buttonRestore, w-40, y)
			y += 30
			baseFx.move(ui.buttonSearchLog, 5, y)
			baseFx.move(ui.buttonClear, 35, y)
			baseFx.move(ui.warn, 120, y)
			baseFx.move(ui.checkTest, w-150, y)
			baseFx.move(ui.buttonExit, w-85, y)
			return True

	def restoreGeometry(ui):
		if hasattr(ui, 'stv') and(ui.cfg['dlgSrchPos']):
			ui.stv.dlgSrchPos =  tuple(map(lambda k: int(k), ui.cfg['dlgSrchPos'].split(',')))
		ui.rGeo(ui.mainWindow, 'MainWindowGeometry')

	def storeGeometry(ui):
		if hasattr(ui, 'stv'):
			stv = ui.stv
			stv.hideDlgSrch()
			if stv.dlgSrchPos:
				ui.cfg['dlgSrchPos'] = "%i,%i" % stv.dlgSrchPos
		ui.cfg['MainWindowGeometry'] = ui.sGeo(ui.mainWindow)


# Entry point
if __name__ == "__main__":
	edaNetUI()

#!/usr/bin/python2
# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-
# -*- tabstop: 4 -*-

import gtk, pango
from os import path as ph, chdir as cd

class EasyTextView(gtk.TextView):
	def __init__(self):
		super(EasyTextView, self).__init__()
		self.autoscroll = True

	def clear_text(self):
		self.get_buffer().set_text('')

	def set_size_request(self, x, y):
		try:
			parent = self.get_parent()
			bPass = True
		except AttributeError, e:
			bPass = False
		if bPass and(isinstance(parent, gtk.ScrolledWindow)):
			parent.set_size_request(x, y)
		else:
			super(EasyTextView, self).set_size_request(x, y)

	def get_text(self):
		tBuff = self.get_buffer()
		return tBuff.get_text(tBuff.get_start_iter(), tBuff.get_end_iter())

	set_text = lambda self, txt: self.get_buffer().set_text(txt)

	def insert_end(self, txt, tag=None):
		buff = self.get_buffer()
		end = buff.get_end_iter()
		text = txt.encode('utf-8', errors='replace')
		if tag:
			buff.insert_with_tags(end, text, tag)
		else:
			buff.insert(end, text)
		del(end)

	def reScrollV(self, adjV, scrollV):
		"""Scroll to the bottom of the TextView when the adjustment changes."""
		if self.autoscroll:
			adjV.set_value(adjV.upper - adjV.page_size)
			scrollV.set_vadjustment(adjV)
		return

	def setTabSpace(self, spaces, fontDesc=None):
		pangoTabSpc = self.getTabPixelWidth(spaces, fontDesc=fontDesc)
		tabArray =  pango.TabArray(1, True)
		tabArray.set_tab(0, pango.TAB_LEFT, pangoTabSpc)
		self.set_tabs(tabArray)
		return pangoTabSpc

	def getTabPixelWidth(self, spaces, fontDesc=None):
		txtTab = ' ' * spaces
		pangoLayout = self.create_pango_layout(txtTab)
		if fontDesc:
			pangoLayout.set_font_description(fontDesc)
		pangoTabSpc = pangoLayout.get_pixel_size()[0]
		del(pangoLayout)
		return pangoTabSpc

class apw:
	def __init__(self):
		from sys import _current_frames as _cf
		callingFilename = _cf().values()[0].f_back.f_code.co_filename
		self.callDir = ph.dirname(callingFilename)
		self.BGcolor = None
		self.BGcolorA = None
		self.BGcolorEntry = None
		self.FGcolor = None

	def putScroll(self, hFixed, widget, posX, posY, width, height):
		hScroll = gtk.ScrolledWindow()
		hScroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		hScroll.add(widget)
		hScroll.set_size_request(width, height)
		hFixed.put(hScroll, posX, posY)

	def npLabel(self, txtLabel, fontDesc=None, xalign=None, selectable=False):
		hLabel = gtk.Label(txtLabel)
		if fontDesc:
			hLabel.modify_font(fontDesc)
		if type(xalign)==float and(0.<=xalign<=1.):
			yalign = hLabel.get_alignment()[1]
			hLabel.set_alignment(xalign, yalign)
		if type(selectable)==bool:
			hLabel.set_selectable(selectable)
		hLabel.show()

	def Label(self, txtLabel, hFixed, posX, posY, width, height=None, fontDesc=None, xalign=None, selectable=False):
		if not height:
			height=self.Height
		hLabel = gtk.Label(txtLabel)
		if fontDesc:
			hLabel.modify_font(fontDesc)
		if type(xalign)==float and(0.<=xalign<=1.):
			yalign = hLabel.get_alignment()[1]
			hLabel.set_alignment(xalign, yalign)
		if type(selectable)==bool:
			hLabel.set_selectable(selectable)
		hLabel.show()
		hLabel.set_size_request(width, height)
		if hFixed:
			hFixed.put(hLabel, posX, posY)
		return hLabel

	def npEntry(self, startIco=None, clearIco=False, bEditable=True, fontDesc=None):
		hEntry = gtk.Entry()
		if fontDesc:
			hEntry.modify_font(fontDesc)
		if startIco:
			self.textInput.set_icon_from_pixbuf(0, startIco)
		if clearIco:
			hEntry.set_icon_from_stock(1, gtk.STOCK_CLOSE)
			hEntry.set_icon_tooltip_text (1, 'Clear')
			hEntry.connect("icon-release", self.textClr)
		hEntry.set_property("editable", bool(bEditable))
		return hEntry

	def Entry(self, hFixed, posX, posY, width, height=None, startIco=None, clearIco=False, bEditable=True, fontDesc=None):
		if not height:
			height=self.Height
		hEntry = self.npEntry(clearIco=clearIco, bEditable=bEditable, fontDesc=fontDesc)
		hEntry.set_size_request(width, height)
		hFixed.put(hEntry, posX, posY)
		return hEntry

	def Butt(self, txtLabel, hFixed, posX, posY, width, height=None, fileImage=None, stockID=None, fontDesc=None):
		"""If stockID is set, txtLabel set as True means full stock button,
		non-null string - own Label for stock image,
		in other case - button with only stock image"""
		if not height:
			height=self.Height
		if stockID == None and fileImage == None:
			hButt = gtk.Button(label=txtLabel, use_underline=False)
			if fontDesc:
				hLabel = hButt.child
				hLabel.modify_font(fontDesc)
		else:
			if type(txtLabel)==int or type(txtLabel)==float or type(txtLabel)==type(None) or (type(txtLabel)==str and txtLabel==''):
				txtLabel = bool(txtLabel)
			if type(txtLabel)==bool and txtLabel==True or type(txtLabel)==str:
				if stockID:
					hButt = gtk.Button(stock=stockID)
				elif fileImage:
					image = gtk.Image()
					image.set_from_file(fileImage)
					hButt = gtk.Button()
					hButt.add(image)
				if type(txtLabel)==str:
					hLabel = hButt.get_children()[0].get_children()[0].get_children()[1]
					hLabel.set_text(txtLabel)
					if fontDesc:
						hLabel.modify_font(fontDesc)
			else:
				image = gtk.Image()
				if stockID:
					image.set_from_stock(stockID, gtk.ICON_SIZE_BUTTON)
				elif fileImage:
					image.set_from_file(fileImage)
				hButt = gtk.Button()
				hButt.add(image)
		hButt.set_size_request(width, height)
		hFixed.put(hButt, posX, posY)
		return hButt

	def Check(self, txtLabel, hFixed, posX, posY, width, height=None, fontDesc=None):
		if not height:
			height=self.Height
		hCheck = gtk.CheckButton(label=txtLabel, use_underline=False)
		hLabel=hCheck.child
		hCheck.set_size_request(width, height)
		hFixed.put(hCheck, posX, posY)
		return hCheck

	def TextView(self, hFixed, posX, posY, width, height, bWrap=False, bEditable=True, tabSpace=2, fontDesc=None):
		hTextView = EasyTextView()
		hTextView.set_property("editable", bEditable)
		if fontDesc:
			hTextView.modify_font(fontDesc)
			hTextView.setTabSpace(tabSpace, fontDesc=fontDesc)
		if bWrap:
			hTextView.set_wrap_mode(gtk.WRAP_WORD)
		scrollViewTxt = gtk.ScrolledWindow()
		vadj = scrollViewTxt.get_vadjustment()
		vadj.connect('changed', hTextView.reScrollV, scrollViewTxt)
		scrollViewTxt.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		scrollViewTxt.add(hTextView)
		scrollViewTxt.set_size_request(width, height)
		hFixed.put(scrollViewTxt, posX, posY)
		return hTextView

	def dialogChooseFile(self, parent=None, startDir=None, startFile=None, title='Select a file...', act='file_open', bShowHidden=False):
		action = {
			'file_open': gtk.FILE_CHOOSER_ACTION_OPEN,
			'file_save': gtk.FILE_CHOOSER_ACTION_SAVE,
			'dir_open': gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
			'dir_create': gtk.FILE_CHOOSER_ACTION_CREATE_FOLDER,
			}[act]
		hDialog = gtk.FileChooserDialog(title=title, parent=parent, action=action,
			buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK) )
		hDialog.set_default_response(gtk.RESPONSE_OK)
		hDialog.set_show_hidden(bShowHidden)
		if startDir:
			hDialog.set_current_folder(startDir)
		if startFile:
			if act=='file_save':
				hDialog.set_current_name(startFile)
			elif act=='file_open':
				hDialog.set_filename(startFile)
		respFileName = hDialog.run()
		fileName = None
		if respFileName==gtk.RESPONSE_OK:
			fileName = hDialog.get_filename()
		hDialog.destroy()
		return fileName

	def setFrameFont(self, frame, fontDesc):
		for widget in frame.children():
			if isinstance(widget, gtk.Button):
				sbwgt = widget.child
				if sbwgt:
					sbwgt.modify_font(fontDesc)
			elif isinstance(widget, gtk.Frame):
				widget.get_label_widget().child.modify_font(fontDesc)
			elif isinstance(widget, gtk.CellLayout):
				for cell in widget.get_cells():
					if isinstance(cell, gtk.CellRendererText):
						cell.set_property('font-desc', fontDesc)
				if isinstance(widget, gtk.TreeViewColumn):
					ttcLabel = widget.get_widget()
					if ttcLabel:
						ttcLabel.modify_font(fontDesc)
			elif isinstance(widget, gtk.ScrolledWindow):
				self.setFrameFont(widget, fontDesc)

			else:
				widget.modify_font(fontDesc)

class edaNetUI:
	def __init__(ui):
		uapw = ui.apw = apw()
		ui.gtk = gtk
		ui.pango = pango
		ui.fontSmall = pango.FontDescription('Univers,Sans Condensed 7')
		ui.fontDesc = pango.FontDescription('Univers,Sans Condensed 8')
		ui.fontFixedDesc = pango.FontDescription('Terminus,Monospace Bold 7')
		uapw.BGcolor = gtk.gdk.Color('#383430')
		uapw.FGcolor = gtk.gdk.Color('#FFF')
		uapw.BGcolorEntry = gtk.gdk.Color('#201810')
		uapw.Height = 25
		ui.uiInit()
		if __name__ == "__main__":
			ui.logView.insert_end("User Interface Test\n Press Clear...\n")
			ui.mainWindow.connect("destroy", lambda w: ui.uiExit())
			ui.buttonExit.connect("clicked", lambda w: ui.uiExit())
			ui.uiEnter()

	uiEnter = lambda ui: gtk.main()
	uiExit = lambda ui: gtk.main_quit()

	def uiInit(ui):
		from gobject import TYPE_STRING as goStr, TYPE_INT as goInt, TYPE_PYOBJECT as goPyObj
		apw = ui.apw
		ui.version = .2
		ui.title = "PCBnew python module based Panelizator v.%0.2f. For BZR>5161" % ui.version
		ui.mainWindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
		ui.wdhMain, ui.hgtMain, ui.hgtLower = (640, 300, apw.Height+50)
		ui.mainWindow.set_geometry_hints(
			min_width=ui.wdhMain, min_height=ui.hgtMain)
		ui.mainWindow.resize(ui.wdhMain, ui.hgtMain)
		ui.mainWindow.set_title(ui.title)
		ui.mainWindow.set_border_width(5)
		ui.accGroup = gtk.AccelGroup()
		ui.mainWindow.add_accel_group(ui.accGroup)
		ui.mainWindow.modify_bg(gtk.STATE_NORMAL, apw.BGcolor)
		ui.cfBPixbuf = gtk.gdk.pixbuf_new_from_file("/usr/share/icons/hicolor/16x16/apps/logview.png")
		gtk.window_set_default_icon_list(ui.cfBPixbuf, )
		
		mf = ui.mainFrame = gtk.Fixed()

		ui.logView = apw.TextView(mf, 5, 5, 0, 0,
			bEditable=False, bWrap=True, tabSpace=4, fontDesc = ui.fontFixedDesc)

		ui.labFilename = apw.Label("File:", mf, 0, 0, 30)
		if __name__ == "__main__":
			ui.txtFilename = apw.Butt('Test', mf, 0, 0, 0)
		else:
			ui.txtFilename = apw.Label(u'Drag file to log view or use „Open” button →',
				mf, 0, 0, 0, xalign=0., selectable=True)
		ui.buttonSelectFile = ui.apw.Butt(None, mf, 0, 0, 30, stockID=gtk.STOCK_OPEN)
		ui.buttonSelectFile.set_tooltip_text('Select File')
		ui.buttonAllNetsGlobal = apw.Butt("Globalize", mf, 0,0, 60)
		ui.buttonAllNetsGlobal.set_tooltip_text('Globalize all nets in file…')
		ui.buttonRestore = ui.apw.Butt(None, mf, 0, 0, 25, stockID=gtk.STOCK_REVERT_TO_SAVED)
		ui.buttonRestore.set_tooltip_text('Restore')

		ui.buttonSearchLog = apw.Butt(None, mf, 0, 0, 25, stockID=gtk.STOCK_FIND)
		ui.buttonSearchLog.set_tooltip_text('Search Log View…')
		ui.buttonSearchLog.add_accelerator("clicked", ui.accGroup, ord('F'),
			gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
		ui.buttonSearchLog.connect("clicked", ui.showDlgSrch)


		ui.buttonClear = apw.Butt("Clear log", mf, 5, 0, 65)
		ui.buttonClear.set_tooltip_text('Clear Log View…')
		ui.buttonClear.connect("clicked", lambda x: ui.logView.clear_text())
		ui.warn = apw.Label('Disclaimer: use on your own risk…', mf, 0, 0, 170)

		ui.checkTest = apw.Check("Test Only", mf, 0, 0, 65)
		ui.checkTest.set_active(True)

		ui.buttonExit = apw.Butt("Exit (Ctrl+Q)", mf, 0, 0, 70)
		ui.buttonExit.add_accelerator("clicked", ui.accGroup, ord('Q'),
			gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
		
		ui.mainWindow.add(mf)
		ui.mainWindow.show_all()
		ui.mainWindow.set_keep_above(True)
		ui.lastWinSize = None
		ui.mainWindow.connect("configure-event", ui.uiSize)

	def uiSize(ui, window, event):
		if event.type==gtk.gdk.CONFIGURE:
			w, h = event.width, event.height
			#print ("eventType: %s, w:%d, h:%d" % (event.type, w, h))
			if ui.lastWinSize==(w, h):
				return True
			stdH = ui.apw.Height
			ui.lastWinSize = w, h
			mf = ui.mainFrame
			ha = h - ui.hgtLower - 5
			ui.logView.set_size_request(w-20, ha)
			y = ha + 10
			mf.move(ui.labFilename, 5, y)
			mf.move(ui.txtFilename, 35, y)
			ui.txtFilename.set_size_request(w-180, stdH)
			mf.move(ui.buttonSelectFile, w-140, y)
			mf.move(ui.buttonAllNetsGlobal, w-105, y)
			mf.move(ui.buttonRestore, w-40, y)
			y += 30
			mf.move(ui.buttonSearchLog, 5, y)
			mf.move(ui.buttonClear, 35, y)
			mf.move(ui.warn, 120, y)
			mf.move(ui.checkTest, w-150, y)
			mf.move(ui.buttonExit, w-85, y)
			return True

	def dialogFind(ui):
		apw = ui.apw
		dlgSrch = ui.dlgSrch = gtk.Window(gtk.WINDOW_TOPLEVEL)
		dlgSrch.add_accel_group(ui.accGroup)
		dlgSrch.set_border_width(5)
		dlgSrch.set_resizable(False)
		dlgSrch.set_title('Find')
		dlgSrch.set_transient_for(ui.mainWindow)
		dlgSrch.set_destroy_with_parent(True)
		dlgSrch.set_deletable(False)
		dlgSrch.set_skip_taskbar_hint(False)
		dlgSrch.modify_bg(gtk.STATE_NORMAL, ui.apw.BGcolor)
		# # # # # # # # # # # # # # # # # # # # # # # # #
		dlgFrame = gtk.Fixed()
		tempWgtHeight = apw.Height
		apw.Height = 20

		apw.Label("Please enter phrase to find:", dlgFrame, 0, 0, 140)
		dlgSrch.Entry = apw.Entry(dlgFrame, 0, 25, 200, clearIco=True)
		dlgSrch.Entry.connect("changed", ui.searchFor, 'interactive')
		bp = dlgSrch.buttonPrev = apw.Butt("Previous", dlgFrame, 0, 50, 70, stockID=gtk.STOCK_GO_BACK)
		bp.connect("clicked", ui.searchFor, 'backward')
		bn = dlgSrch.buttonNext = apw.Butt("Next", dlgFrame, 80, 50, 70, stockID=gtk.STOCK_GO_FORWARD)
		bn.connect("clicked", ui.searchFor, 'forward')
		hButtonOK = apw.Butt("OK", dlgFrame, 170, 50, 30)
		hButtonOK.connect("clicked", ui.hideDlg, dlgSrch)
		dlgSrch.found = None
		dlgSrch.flags = gtk.TEXT_SEARCH_TEXT_ONLY | gtk.TEXT_SEARCH_VISIBLE_ONLY

		dlgSrch.add(dlgFrame)
		dlgSrch.show_all()
		apw.setFrameFont(dlgFrame, ui.fontSmall)
		apw.Height = tempWgtHeight

	def showDlgSrch(ui, widget):
		if  hasattr(ui, 'dlgSrch') and(ui.dlgSrch):
			#ui.dlgSrch.show()
			ui.dlgSrch.present()
		else:
			ui.dialogFind()
		if hasattr(ui.dlgSrch, 'pos') and(ui.dlgSrch.pos):
			ui.dlgSrch.move(*ui.dlgSrch.pos)
		txtBuff = ui.logView.get_buffer()
		sel = txtBuff.get_selection_bounds()
		if sel:
			ui.dlgSrch.found = sel
			ui.dlgSrch.Entry.set_text(txtBuff.get_text(*sel))
		ui.dlgSrch.set_keep_above(True)

	def hideDlg(ui, widget, hDialog):
		if hDialog.get_property("visible"):
			hDialog.pos = hDialog.get_position()
			hDialog.hide()

	def getFound(ui, txtBuff, srchType, txtSrch):
			#if ui.dlgSrch.found and(not(txtBuff.get_modified())):
			if ui.dlgSrch.found:
				if srchType in ('interactive', 'backward'):
					iterB = ui.dlgSrch.found[0]
				else:
					iterB = ui.dlgSrch.found[1]
			else:
				iterB = None
			if not(iterB):
				if srchType in ('interactive', 'forward'):
					iterB = txtBuff.get_start_iter()
				else:
					iterB = txtBuff.get_end_iter()
			if srchType in ('interactive', 'forward'):
				return iterB.forward_search(txtSrch, ui.dlgSrch.flags, None)
			else:
				return iterB.backward_search(txtSrch, ui.dlgSrch.flags, None)

	def searchFor(ui, widget, srchType):
		txtSrch = ui.dlgSrch.Entry.get_text()
		if txtSrch:
			txtBuff = ui.logView.get_buffer()
			lastfound = ui.dlgSrch.found
			found = ui.dlgSrch.found = ui.getFound(txtBuff, srchType, txtSrch)
			if lastfound and(not(found)):
				found = ui.dlgSrch.found = ui.getFound(txtBuff, srchType, txtSrch)
			if found:
				ui.logView.scroll_to_iter (found[0], 0)
				txtBuff.select_range(*found)


# Entry point
if __name__ == "__main__":
	edaNetUI()

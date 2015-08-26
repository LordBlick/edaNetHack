#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-
# -*- tabstop: 4 -*-

import gtk, pango

Height = 25


def getTxtPixelWidth(widget, txt, fontDesc=None):
	pangoLayout = widget.create_pango_layout(txt)
	if fontDesc:
		pangoLayout.set_font_description(fontDesc)
	pangoTxtSpc = pangoLayout.get_pixel_size()[0]
	del(pangoLayout)
	return pangoTxtSpc

def putScroll(hFixed, widget, posX, posY, width, height):
	hScroll = gtk.ScrolledWindow()
	hScroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
	hScroll.add(widget)
	hScroll.set_size_request(width, height)
	hFixed.put(hScroll, posX, posY)
	return hScroll

class MvWg:
	"This is abctract class !"
	def __init__(it, *args):
		raise TypeError('MvWg.__init__(): abstract class')

	def move(it, x, y):
		it.hFixed.move(it, x, y)

	size = lambda it, w, h: it.set_size_request(w, h)


class Label(gtk.Label, MvWg):
	def __init__(it, txtLabel, hFixed, posX, posY, width, height=None, fontDesc=None, xalign=None, selectable=False):
		it.hFixed = hFixed
		super(it.__class__, it).__init__(txtLabel) # gtk.Label
		if fontDesc:
			it.modify_font(fontDesc)
		if type(xalign)==float and(0.<=xalign<=1.):
			yalign = it.get_alignment()[1]
			it.set_alignment(xalign, yalign)
		if type(selectable)==bool:
			it.set_selectable(selectable)
			it.set_can_focus(False)
		it.show()
		if not height:
			height=Height
		it.set_size_request(width, height)
		hFixed.put(it, posX, posY)

class Butt(gtk.Button, MvWg):
	"""If stockID is set, txtLabel set as True means full stock button,
	non-null string - own Label for stock image,
	in other case - button with only stock image"""
	def __init__(it, txtLabel, hFixed, posX, posY, width, height=None, fileImage=None, stockID=None, fontDesc=None):
		it.hFixed = hFixed
		if stockID == None and fileImage == None:
			super(it.__class__, it).__init__(label=txtLabel, use_underline=False)
			if fontDesc:
				btLabel = it.child
				btLabel.modify_font(fontDesc)
		else:
			if type(txtLabel)==int or type(txtLabel)==float or type(txtLabel)==type(None) or (type(txtLabel)==str and txtLabel==''):
				txtLabel = bool(txtLabel)
			if type(txtLabel)==bool and txtLabel==True or type(txtLabel)==str:
				if stockID:
					super(it.__class__, it).__init__(stock=stockID)
				elif fileImage:
					image = gtk.Image()
					image.set_from_file(fileImage)
					super(it.__class__, it).__init__()
					it.add(image)
				if type(txtLabel)==str:
					btLabel = it.get_children()[0].get_children()[0].get_children()[1]
					btLabel.set_text(txtLabel)
					if fontDesc:
						btLabel.modify_font(fontDesc)
			else:
				image = gtk.Image()
				if stockID:
					image.set_from_stock(stockID, gtk.ICON_SIZE_BUTTON)
				elif fileImage:
					image.set_from_file(fileImage)
				super(it.__class__, it).__init__()
				it.add(image)
		if not height:
			height = Height
		it.set_size_request(width, height)
		hFixed.put(it, posX, posY)

class Check(gtk.CheckButton, MvWg):
	def __init__(it, txtLabel, hFixed, posX, posY, width, height=None, fontDesc=None):
		it.hFixed = hFixed
		super(it.__class__, it).__init__(label=txtLabel, use_underline=False)
		if fontDesc:
			it.child.modify_font(fontDesc)
		if not height:
			height = Height
		it.set_size_request(width, height)
		hFixed.put(it, posX, posY)

class Entry(gtk.Entry, MvWg):
	def __init__(it, hFixed, posX, posY, width, height=None, startIco=None, clearIco=False, bEditable=True, fontDesc=None):
		def entryIcoClr(ed, icoPos, sigEvent):
			if icoPos == gtk.ENTRY_ICON_SECONDARY:
				ed.set_text('')
		it.hFixed = hFixed
		super(it.__class__, it).__init__()
		if fontDesc:
			it.modify_font(fontDesc)
		if startIco:
			textInput.set_icon_from_pixbuf(0, startIco)
		if clearIco:
			it.set_icon_from_stock(1, gtk.STOCK_CLOSE)
			it.set_icon_tooltip_text (1, 'Clear')
			it.connect("icon-release", entryIcoClr)
		it.set_property("editable", bool(bEditable))
		if not height:
			height = Height
		it.set_size_request(width, height)
		hFixed.put(it, posX, posY)

class MvScrolled:
	"This is abctract class !"
	def reScrollV(it, adjV, scrollV):
		'Scroll to the bottom of the TextView when the adjustment changes.'
		if it.autoscroll:
			adjV.set_value(adjV.upper - adjV.page_size)
			scrollV.set_vadjustment(adjV)
		return

	def setup_scroll(it, x, y, w, h):
		scrollViewport = gtk.ScrolledWindow()
		vadj = scrollViewport.get_vadjustment()
		vadj.connect('changed', it.reScrollV, scrollViewport)
		scrollViewport.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		scrollViewport.add(it)
		scrollViewport.set_size_request(w, h)
		it.hFixed.put(scrollViewport, x, y)

	def size(it, x, y):
		try:
			parent = it.get_parent()
			bPass = True
		except AttributeError, e:
			bPass = False
		if bPass and(isinstance(parent, gtk.ScrolledWindow)):
			parent.set_size_request(x, y)
		else:
			super(it.__class__, it).set_size_request(x, y)

	def move(it, x, y):
		try:
			parent = it.get_parent()
			bPass = True
		except AttributeError, e:
			bPass = False
		if bPass and(isinstance(parent, gtk.ScrolledWindow)):
			it.hFixed.move(parent, x, y)
		else:
			it.hFixed.move(it, x, y)

class TextView(gtk.TextView, MvScrolled):
	def __init__(it, hFixed, posX=0, posY=0, width=0, height=0, bWrap=False, bEditable=True, tabSpace=2, fontDesc=None):
		super(it.__class__, it).__init__()
		it.hFixed = hFixed
		it.autoscroll = True
		it.changed = False
		it.set_property("editable", bEditable)
		if fontDesc:
			it.modify_font(fontDesc)
			it.setTabSpace(tabSpace, fontDesc=fontDesc)
		if bWrap:
			it.set_wrap_mode(gtk.WRAP_WORD)
		it.setup_scroll(posX, posY, width, height)

	def set_text(it, txt):
		it.get_buffer().set_text(txt)
		it.changed = True

	clear_text = lambda it: it.set_text('')

	def get_text(it):
		tBuff = it.get_buffer()
		return tBuff.get_text(tBuff.get_start_iter(), tBuff.get_end_iter())
	
	def insert_end(it, txt, tag=None):
		buff = it.get_buffer()
		end = buff.get_end_iter()
		text = txt.encode('utf-8', errors='replace')
		if tag:
			buff.insert_with_tags(end, text, tag)
		else:
			buff.insert(end, text)
		del(end)
		it.changed = True

	def setTabSpace(it, spaces, fontDesc=None):
		pangoTabSpc = getTxtPixelWidth(it, ' '*spaces, fontDesc)
		tabArray =  pango.TabArray(1, True)
		tabArray.set_tab(0, pango.TAB_LEFT, pangoTabSpc)
		it.set_tabs(tabArray)
		return pangoTabSpc

def dialogChooseFile(parent=None, startDir=None, startFile=None, filters=None, title='Select a file...', act='file_open', bShowHidden=False):
	action = {
		'file_open': gtk.FILE_CHOOSER_ACTION_OPEN,
		'file_save': gtk.FILE_CHOOSER_ACTION_SAVE,
		'dir_open': gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
		'dir_create': gtk.FILE_CHOOSER_ACTION_CREATE_FOLDER,
		}[act]
	hDialog = gtk.FileChooserDialog(title=title, parent=parent, action=action,
		buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK) )
	if filters:
		for fnFilter in filters:
			hDialog.add_filter(fnFilter)
		allFilter = gtk.FileFilter()
		allFilter.set_name("All files (*.*)")
		allFilter.add_pattern("*")
		hDialog.add_filter(allFilter)
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

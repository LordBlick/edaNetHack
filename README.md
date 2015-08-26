---
title: edaNetHack
description: Small KiCAD netlist parser, renaming all nets to global, written in Python/gtk+2
author: LordBlick
tags: KiCAD, netlist, global, python, gtk
created:  2015.01.19
modified: 2015.08.26

---

edaNetHack
=======
## Introduction

edaNetHack is a program for easier rename net names to global (without „/”prefixes) in KiCAD netlist file (*.net) by click on „Globalize” button.

By default changes are simulated and displayed in message widget, an can be searched for custom netname. Real changes are done after uncheck „Test Only” checkbox.

Recomended just for one schematic sheet (1 level hierarchy) projects.

## Reason to make this tool
In the case of a draft single sheet, „/” prefix can be perceived as an inconvenience, which KiCAD project managers do not intend to delete because quite right probability complaints from the less experienced users who after selecting globalization would have a problem with a more complex project.

## Running initially testing script.
From command line in dir with script:
> python netEDA

Unix based OS user can set execute privileges to execute as any other shell script:
> chmod +x netEDA

> ./netEDA

To run it it's nessesary to install:
- [Python interpreter] in version 2 (On today newests is 2.7.10). Don't miss with version 3 (On today newests is 3.4.3).
- [GTK Libraries].
[Python interpreter]: https://www.python.org/downloads/
[GTK Libraries]: http://www.gtk.org/download/

TO DO:
- make possible to pack std pypi package

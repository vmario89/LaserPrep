#! /usr/bin/env python
'''
Copyright (C) 2019 Grant Patterson <grant@revoltlabs.co>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
'''

import gettext
import re
import sys

import inkex
import simplepath
#import simplestyle

from synfig_prepare import InkscapeActionGroup, SynfigExportActionGroup
from pathmodifier import PathModifier

debug = False

error = lambda msg: inkex.errormsg(gettext.gettext(msg))
if debug:
    stderr = lambda msg: sys.stderr.write(msg + '\n')
else:
    stderr = lambda msg: None


class FlattenStrokes(inkex.Effect):

    def effect(self):
        # get selected path(s)
        if len(self.selected) == 0:
            error("No selection found")
            return
        
        # Duplicate selection
        pm = PathModifier()
        pm.document = self.document
        duplicates = pm.duplicateNodes(self.selected)

        a = InkscapeActionGroup(self.document)
        for nid in duplicates:
            a.select_id(nid)
        a.verb('EditUnlinkClone')
        a.verb('ObjectToPath')
        a.verb('StrokeToPath')
        for nid in self.selected:
            a.select_id(nid)
        a.verb('EditUnlinkClone')
        a.verb('ObjectToPath')
        a.verb('SelectionUnion')
        self.document = a.run_document()

        for nid in self.selected.keys() + duplicates.keys():
            node = self.getElementById(nid)
            if node is not None:
                node.set('style', 'fill:#000000;stroke:none;')


if __name__ == '__main__':
    fs = FlattenStrokes()
    fs.affect()

#  ThermalReliefVia.py
#
# Copyright (C) 2024 John Hryb
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

import pcbnew
import os

class ThermalReliefVia(pcbnew.ActionPlugin):

    def defaults(self):
        self.name = "Thermal Relief Via"
        self.category = "Via"
        self.description = "Replaces selected via(s) with identical footprint to make thermal relief for soldering."
        self.show_toolbar_button = True # Optional, defaults to False
        self.icon_file_name = os.path.join(os.path.dirname(__file__), 'ThermalReliefVia.png') # Optional, defaults to ""

    def _makeThPad(self, position, padSize, drillSize, net):
        pcb = pcbnew.GetBoard()
        footprint = pcbnew.FOOTPRINT(pcb)
        footprint.SetPosition(position)
        pad = pcbnew.PAD(footprint)
        pad.SetShape(pcbnew.PAD_SHAPE_CIRCLE)
        pad.SetSize(pcbnew.VECTOR2I(padSize, padSize))
        pad.SetDrillSize(pcbnew.VECTOR2I(drillSize, drillSize))
        pad.SetAttribute(pcbnew.PAD_ATTRIB_PTH)
        pad.SetNetCode(net)
        footprint.Add(pad)
        pcb.Add(footprint)

    def Run(self):      
        pcb = pcbnew.GetBoard()
        for item in pcb.GetTracks():
            if item.GetClass() == "PCB_VIA": 
                if item.IsSelected():
                    position = item.GetPosition()
                    drill = item.GetDrillValue()
                    width = item.GetWidth()
                    net = item.GetNetCode()
                    #now create the PTH replacement
                    self._makeThPad(position, width, drill, net)
                    pcb.Remove(item)

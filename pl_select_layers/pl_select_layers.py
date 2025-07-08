#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# "Select layers" GIMP 3 python plugin.
# Selects all visible layers under current selection.
#
# Original author : Pascal Lachat
# Version 0.2 for GIMP 3.0

# ------------------

# License: GPLv3
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY, without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# To view a copy of the GNU General Public License
# visit: http://www.gnu.org/licenses/gpl.html

# ------------------

# Documentation :
# *************
# Selects all layers with non-transparent pixels inside the selection.
# Layer groups and non-visible layers are not selected. Visible layers inside layer 
# groups are (if the layer group is visible).
# Masks and layer modes are not taken into account.
# The plugin runs without any dialog interaction. If installed properly, it should be 
# listed in the "Layer" menu.

# Installation :
# ************
# Unzip and move the "pl_select_layers" folder with its content inside the "plug-ins" 
# user folder.
# The plugin file is already set to executable, but check that first if it doesn't appear 
# after restarting GIMP.

# Changelog:
# 0.1 : first release
# 0.2 : changed pixels detection method from selection intersection to histogram

# To do:
# - Take active layer masks into account ?

#*************************************************************************************


# imports
#--------
import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp
gi.require_version('GimpUi', '3.0')
from gi.repository import GimpUi
# gi.require_version('Gegl', '0.4')
# from gi.repository import Gegl
from gi.repository import GObject
from gi.repository import GLib

import os
import sys
# import math


#*************************************************************************************


class selectLayersClass (Gimp.PlugIn):
    ## GimpPlugIn virtual methods ##
    def do_query_procedures(self):
        return [ "pl-select-layers" ]

    def do_create_procedure(self, name):
        procedure = Gimp.ImageProcedure.new(self, name,
                                            Gimp.PDBProcType.PLUGIN,
                                            selectLayers, None)

        procedure.set_image_types("*")

        procedure.set_menu_label("Select layers")
        procedure.set_icon_name(GimpUi.ICON_GEGL)
        procedure.add_menu_path('<Image>/Layer')

        procedure.set_documentation("Select layers based on selection",
                                    "Select layers based on selection",
                                    name)
        procedure.set_attribution("Pascal L.", "Pascal L.", "2025")


        return procedure


#*************************************************************************************


# routine principale
#-------------------

def selectLayers(procedure, run_mode, monImage, drawables, config, data):

    
    # Undo et contexte
    # ----------------
    
    monImage.undo_group_start()
    
    Gimp.context_push()
    Gimp.context_set_defaults()
    
    #*****************************************************************************
    
    # initialisations
    topLayers = monImage.get_layers()
    allVisibleLayers = []
    selectedLayers = []
    
    # get the complete layers list :
    for thisLayer in topLayers :
        
        if thisLayer.get_visible() == True :
        
            if thisLayer.is_group_layer() :
                
                allVisibleLayers = getLayersInGroup(thisLayer, allVisibleLayers)
                
            else :
                
                allVisibleLayers.append(thisLayer)
    
    # check which layers have visible pixels inside the selection
    for thisLayer in allVisibleLayers :
        
        getHistogram = thisLayer.histogram(0, 0.0, 1.0)
        pixelsInSelection = getHistogram[5] # pixel count
        
        # print(getHistogram)      #debug
        # print(pixelsInSelection) #debug
        
        if pixelsInSelection != 0.0 :
            
            selectedLayers.append(thisLayer)
                
        # end if
    # end for
    
    # set the detected layers to selected state
    if len(selectedLayers) != 0 :
        
        monImage.set_selected_layers(selectedLayers)
        
        # for thisLayer in selectedLayers :                             # debug
            # currentPosition = monImage.get_item_position(thisLayer)   # debug
            # print(currentPosition)                                    # debug
            
    # end if
    
    #*****************************************************************************

    # Finalisations
    # -------------
    
    
    Gimp.context_pop()
    monImage.undo_group_end()
    
    
    
    return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())


#*************************************************************************************

# get layers inside layer groups, recursively
def getLayersInGroup(layerGroup, allVisibleLayers) :
    
    subLayers = layerGroup.get_children()
    
    for thisLayer in subLayers :
        
        if thisLayer.get_visible() == True :
        
            if thisLayer.is_group_layer() :
                
                allVisibleLayers = getLayersInGroup(thisLayer, allVisibleLayers)
                
            else :
                
                allVisibleLayers.append(thisLayer)
                
            # end if
        # end if
    # end for
    
    return allVisibleLayers
    
#*************************************************************************************



Gimp.main(selectLayersClass.__gtype__, sys.argv)


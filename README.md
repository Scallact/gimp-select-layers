# gimp-select-layers
A python plugin for GIMP 3.0

## Documentation :

Selects all layers with non-transparent pixels inside the selection.

Layer groups and non-visible layers are not selected. Visible layers inside layer groups are (if the layer group is visible).

Masks and layer modes are not taken into account.

The plugin runs without any dialog interaction. If installed properly, it should be listed in the "Layer" menu.

## Installation :

Unzip and move the "pl_select_layers" folder with its content inside the "plug-ins" user folder.

Set the .py file to executable if it doesn't appear after restarting GIMP.

Changelog:

* 0.1 : first release
* 0.2 : changed pixels detection method from selection intersection to histogram

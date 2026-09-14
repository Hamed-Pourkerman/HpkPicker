# HPK Picker Upgrade 2026
<img width="448" height="821" alt="image" src="https://github.com/user-attachments/assets/f26f7baf-c1f1-4485-8779-8b2e64e6e08d" />
Here is the demo for this tool 
https://www.youtube.com/watch?v=8KY8_1TZI2k
Please give it a try and let me know if you find any issues or if you have any feature requests

HPK Picker is a Qt-based character-picker editor for Autodesk Maya and 3ds Max. It lets artists place clickable controls over a reference image, associate controls with scene objects, attach host-side Python snippets, and save the result as a portable JSON layout.

This repository contains the 2026 host-neutral upgrade. The legacy picker implementations are intentionally kept outside this package and are not modified by the installer.

## Current status

The repository contains the shared UI, host adapters, installer, bundled picker layouts, and installer smoke tests. The installer can be run from a normal Windows Python prompt and does not import Autodesk APIs during host detection.

The picker UI itself still has an integration issue inherited from the legacy viewer: shape-creation methods in `hpkpicker/viewer.py` reference a module-level `cmds` object that is not defined. As a result, opening the UI may work in a host, but adding shapes can fail until those references are routed through the host adapter. Treat the current package as an upgrade-in-progress and test it in a disposable scene before production use.

## Supported environments

| Host | Minimum tested target | Host APIs used |
| --- | --- | --- |
| Autodesk Maya | 2022+ | Python 3, PySide2, `maya.cmds`, `maya.OpenMayaUI`, `shiboken2` |
| Autodesk 3ds Max | 2024+ | Python 3, PySide2, `pymxs`, `qtmax` |

The project is Windows-oriented because the installer targets Autodesk Windows installation directories. It is not a standalone desktop application: PySide2 and the host APIs are expected to be supplied by Maya or 3ds Max.

## Features

- Create and rename picker tabs.
- Load a PNG, JPG, or JPEG background image for each tab.
- Add ellipse, rectangle, free-drawn polygon, and text controls; existing layouts may also contain regular polygon controls.
- Select, move, resize, scale, recolor, duplicate, mirror, align, and distribute controls.
- Lock and unlock controls while editing.
- Capture the current scene selection as the object list for a control.
- Use an optional namespace/prefix filter in Maya when resolving selected objects.
- Attach a Python script to a control; it runs when the control is released.
- Save and reopen picker layouts as JSON.
- Reuse existing layouts from `resources/UiLayouts` and images from `resources/Images`.

## Installation

### Automatic per-user installation

Run these commands from the repository directory using a regular Windows Python installation:

```text
python install.py
```

The installer detects supported versions and copies `hpkpicker` and `resources` into each user installation. It is safe to rerun because files are copied into the existing package directory rather than deleting the installation directory.

Preview the detected destinations without copying files:

```text
python install.py --dry-run
```

Install only one host family:

```text
python install.py --hosts maya
python install.py --hosts 3dsmax
python install.py --hosts maya,3dsmax
```

The installer reports detected versions and the destination for every installation. If no supported host is found, it exits successfully and prints a message instead of creating an install.

### Installed locations

For Maya, the package is installed under:

```text
%USERPROFILE%\Documents\maya\<version>\scripts\HPKPicker_Upgrade_2026
```

The installer also creates `HPKPicker_Maya_Shelf.py` in that directory.

For 3ds Max, the package is installed under:

```text
%LOCALAPPDATA%\Autodesk\3dsMax\<version>\ENU\scripts\HPKPicker_Upgrade_2026
```

The installer also creates `HPKPicker_3dsMax.mcr` in that directory.

## Launching the picker

### Maya

1. Open Maya.
2. Open the installed `HPKPicker_Maya_Shelf.py` in the Script Editor, or copy its contents to a shelf button.
3. Execute it.

The generated launcher adds the installed package directory to `sys.path` and calls `hpkpicker.maya_entry.run()`.

### 3ds Max

1. Open 3ds Max.
2. Open the installed `HPKPicker_3dsMax.mcr` in the MAXScript Editor.
3. Execute it, then optionally place the resulting macro on a toolbar or menu.

The generated macro invokes `hpkpicker.max_entry.run()` through `python.Execute`.

## Basic workflow

1. Launch the picker in the DCC.
2. Click **New Tab** and enter a tab name.
3. Use **Load Image** to choose the character or rig reference image.
4. Turn off **Lock/Unlock** to enable editing.
5. Add controls with the circle, rectangle, polygon, or text buttons.
6. Select a control, then right-click it and choose **Get Objects** to capture the current scene selection.
7. Add an optional script with the context-menu **Add Script** command.
8. Adjust colors, size, position, alignment, and duplication as needed.
9. Turn locking back on for picker use.
10. Use **Save Tab** to write a `.json` layout, or **Open Tab** to load one.

## Controls and shortcuts

| Action | Shortcut or interaction |
| --- | --- |
| Fit image to view | `F` |
| Select multiple controls | `Ctrl` + left mouse button |
| Scale selected controls | `+` / `-` |
| Change rectangle/ellipse width | `Ctrl` + `+` / `-` |
| Change rectangle/ellipse height | `Alt` + `+` / `-` |
| Move selected controls | `W` / `A` / `S` / `D` |
| Move by larger increments | `Ctrl` + `W` / `A` / `S` / `D` |
| Delete selected controls | `Delete` |
| Pan the canvas | Middle mouse, or `Space` + left mouse |
| Fit view | Double-click middle mouse |
| Finish a free polygon | `Enter` |
| Rename a tab | Double-click the tab name |
| Context actions | Right-click the canvas/control |

While locked, movement, resizing, scaling, and deletion are disabled. The lock state is per tab.

## Context-menu tools

Right-clicking the canvas exposes the following editor operations:

- Get or clear the selected control's object list.
- Align selected controls on X or Y.
- Evenly distribute selected controls on X or Y.
- Copy and paste visual style.
- Duplicate controls along X or Y.
- Duplicate controls mirrored across X or Y.
- Add or edit a Python script.
- Set an explicit scale value.

## Host behavior

Maya captures selected node names without namespaces and resolves them against namespaced scene nodes. The selected prefix is used as a filter when controls are activated.

3ds Max captures selected node names and resolves them with `pymxs.runtime.getNodeByName`; controls activate by selecting the matching nodes.

Scripts are host code, not a separate HPK Picker scripting language. Maya sends each non-empty line through `maya.cmds.evalDeferred`. 3ds Max sends the complete script to `pymxs.runtime.execute`. Only attach scripts you trust: they execute inside the DCC with the permissions of the current user.

Outside Maya or 3ds Max, the package falls back to `NullHost`. This is useful for limited packaging and installer tests, but it does not provide scene selection or script execution and is not a supported way to run the picker UI.

## Layout files

Picker files are JSON arrays. The first element stores tab metadata:

```json
[
  {
    "TabName": "Character",
    "TabPhoto": "path/to/background.png",
    "PrefixList": ["", "Char"]
  }
]
```

The remaining elements describe controls. Common fields include:

- `type`: `ellipse`, `rectangle`, `Polygon`, `DrawPolygon`, or `TextButton`.
- `object_list`: scene node names associated with the control.
- `pos`, `scale`, `color`, and `bounding_rect`: display state.
- `script` and `scriptEnabled`: optional activation script metadata.

Shape-specific fields include `rect` for ellipses/rectangles, `args` for regular polygons, `polygonPointsInOrder` for free-drawn polygons, and `text`/`textcolor` for text controls.

Image paths are stored in the layout. The bundled default image is used for newly created tabs. Keep custom background images available at their saved paths when moving layouts between machines; the current loader does not embed image data in the JSON.

Bundled example layouts are in `resources/UiLayouts`, including the `ClothSim` and `Temp` subdirectories. Bundled images and source artwork are in `resources/Images`.

## Repository structure

```text
hpkpicker/
  viewer.py              Shared Qt editor and layout serialization
  maya_entry.py          Maya launcher entry point
  max_entry.py           3ds Max launcher entry point
  hosts/
    base.py              Offline/null host contract
    maya.py              Maya adapter
    max.py               3ds Max adapter
resources/
  Images/                Picker backgrounds and artwork
  UiLayouts/             Example JSON picker layouts
  icons/                 Toolbar icons
install.py               Host detection and per-user installer
tests/                   Installer smoke tests
ARCHITECTURE.md          Refactor and host-boundary notes
LICENSE                  License terms
```

## Development and verification

The repository has no third-party dependency manifest because the runtime dependencies are provided by the DCC hosts. The installer tests can be run with a regular Python environment that has `pytest` installed:

```text
pytest -q
```

The current test suite covers supported-version constants and the shape of host detection. It does not launch Qt, Maya, or 3ds Max, so successful tests do not yet prove that the in-host picker UI is production-ready.

## Troubleshooting

**No installations are detected**

Run `python install.py --dry-run` from Windows. Maya versions can be discovered from Autodesk folders or registry keys; 3ds Max versions are discovered from Autodesk folders under `Program Files`. Nonstandard installations may need a manual copy or a future installer enhancement.

**The launcher cannot import `hpkpicker`**

Confirm that the generated launcher points to the installed `HPKPicker_Upgrade_2026` directory and that both `hpkpicker` and `resources` exist there. Avoid moving only the launcher file without the package directory.

**A background image is blank after moving a layout**

The JSON stores a file path, not the image itself. Restore the image at that path or edit `TabPhoto` to point to a valid PNG/JPG/JPEG file.

**Adding a control raises `NameError: cmds is not defined`**

This is a known current limitation of the shared viewer. Shape creation still contains legacy direct `cmds` calls instead of using the host adapter. It must be fixed in the implementation before relying on the picker in a production scene.

## License

See [LICENSE](LICENSE) for the terms covering this project.

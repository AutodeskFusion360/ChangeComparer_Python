# Comparer_Python
Add-In that lets the user save a snapshot of the current model then compare it to a later state - written in Python.
The Add-In's idea comes from this idea station post: [Quick difference view between before and after an edit](http://forums.autodesk.com/t5/fusion-360-ideastation-request-a/quick-difference-view-between-before-and-after-an-edit/idi-p/5556293)

## Usage
The Add-In provides a single command added to the "Model" workspace's "Inspect" panel, but it has two states:
- "Save Snapshot For Comparison": this saves a snapshot of the current view. This also saves the current camera, so that the other command will be able to make sure that the other snapshot is taken from the same angle and with the same zoom.

![Save Snapshot For Comparison]
(./resources/readme/Comparer1.png)
- "Compare To Snapshot": this also saves a snapshot of the current view from the same angle as the previous one, but as a different image and then shows the newly created image and the one previously created by the "Save Snapshot For Comparison" command inside a webpage where the user can easily swap between the snapshot of the two states and compare them visually

![Save Snapshot For Comparison]
(./resources/readme/Comparer2.png)

![Save Snapshot For Comparison]
(./resources/readme/Comparer3.png)
 
## License
Samples are licensed under the terms of the [MIT License](http://opensource.org/licenses/MIT). Please see the [LICENSE](LICENSE) file for full details.

## Written by 
Written by [Adam Nagy](http://adndevblog.typepad.com/manufacturing/adam-nagy.html)  <br />
(Autodesk Developer Network)
 

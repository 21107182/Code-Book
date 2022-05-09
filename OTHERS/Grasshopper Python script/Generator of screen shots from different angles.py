#This is a Grasshopper Python script used to get screen shots of objects from different angles. It is developed based on View From Sun from Lady Bug. It improves the limitation of the position of camera in View From Sun. You can freely set the position and focal length of the camera, the size and display mode of the screen shot, etc. At the same time, it also realizes the automatic batch generation of screen shots of objects from different angles. Of course, you can define the angle and quantity you want, and even the name of the output file.

import scriptcontext as sc
import Rhino as rc
import rhinoscriptsyntax as rs
import System

def main(sunVector, cenPt, sunPosition, dispModeStr, width, height, viewNumber, viewID, objID):
    
    viewName = str(objID) + '_' + str(int(360/viewNumber * viewID))
    isView = rc.RhinoDoc.ActiveDoc.Views.Find(viewName, False)
    
    if isView and width and  width != sc.doc.Views.ActiveView.ActiveViewport.Size.Width + 16: isView = False
    elif isView and height and  height != sc.doc.Views.ActiveView.ActiveViewport.Size.Height + 34: isView = False
    
    if not isView:
        # if view is not already created creat a new floating view
        # Thanks to Florian for his help (http://www.grasshopper3d.com/forum/topics/new-floating-viewport-using-rhinocommon)
        if not width: w = sc.doc.Views.ActiveView.ActiveViewport.Size.Width
        else: w = width
        if not height: h = sc.doc.Views.ActiveView.ActiveViewport.Size.Height
        else: h = height
        # print w,h
        if rc.RhinoDoc.ActiveDoc.Views.Find(viewName, False)!= None: rc.RhinoDoc.ActiveDoc.Views.Find(viewName, False).Close()
        
        x = round((System.Windows.Forms.Screen.PrimaryScreen.Bounds.Width - w) / 2)
        y = round((System.Windows.Forms.Screen.PrimaryScreen.Bounds.Height - h) / 2)
        rectangle = System.Drawing.Rectangle(System.Drawing.Point(x, y), System.Drawing.Size(w, h))
        newRhinoView = rc.RhinoDoc.ActiveDoc.Views.Add(viewName, rc.Display.DefinedViewportProjection.Perspective, rectangle, False)
        if newRhinoView:
            newRhinoView.TitleVisible = True;
            isView = rc.RhinoDoc.ActiveDoc.Views.Find(viewName, False)
    
    rc.RhinoDoc.ActiveDoc.Views.ActiveView = isView
    
    try:
        dispMode = rc.Display.DisplayModeDescription.FindByName(dispModeStr)
        sc.doc.Views.ActiveView.ActiveViewport.DisplayMode = dispMode
    except: pass
    
    # modify the view
    sc.doc.Views.ActiveView.ActiveViewport.ChangeToParallelProjection(True)
    sc.doc.Views.ActiveView.ActiveViewport.SetCameraLocation(sunPosition, False)
    sc.doc.Views.ActiveView.ActiveViewport.SetCameraTarget(cenPt, False)
    sc.doc.Views.ActiveView.ActiveViewport.SetCameraDirection(sunVector, False)
    rs.ViewRadius(viewName, _radius_, True)
    
    print viewName
    
if _sunVector!=None and _run_:
    if _cenPt_==None: _cenPt_ = rc.Geometry.Point3d.Origin
    if sunViewPt_!=None: sunPosition = sunViewPt_
    else: sunPosition = rc.Geometry.Point3d.Add(_cenPt_, _sunVector)
    main(_sunVector, _cenPt_, sunPosition, dispMode_, width_, height_, _viewNumber_, _viewID_, _objID_)
    
else:
    print "sunVector is missing."

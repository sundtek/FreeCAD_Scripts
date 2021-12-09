def extend(val, sedge=None):
 sel=Gui.Selection.getSelectionEx()[0].SubObjects

d=None


from PySide import QtCore

SELECT_EDGE=1
LOG_POSITION=2
state=None
selectedEdge=None
extensionDir=None

def extendEdge(edge, val):
   if hasattr(edge, 'Curve'):
      if isinstance(edge.Curve, Part.LineSegment) or isinstance(edge.Curve, Part.Line):
          print("midparam");
          midparam = edge.FirstParameter + 0.5 * (edge.LastParameter - edge.FirstParameter)
          tangent = edge.tangentAt(midparam)
          normal = tangent.cross(FreeCAD.Vector(0, 0, 1))
          e2 = edge.copy()
          e2.translate(normal*val)
          Part.show(e2)

def buttonClick():
   global callback
   view = FreeCADGui.ActiveDocument.ActiveView
   callback = view.addEventCallbackPivy(coin.SoMouseButtonEvent.getClassTypeId(), getMouseClick)


def startSelection():
   global state
   global selectedEdge, extensionDir
   state=SELECT_EDGE
   selectedEdge=None
   extensionDir=None
   buttonClick()

d = None

def getMouseClick(event_cb):
   global callback, v, d, state, extensionDir, selectedEdge
   if state == SELECT_EDGE:
      print("select edge")
      event = event_cb.getEvent()
      pos = event.getPosition().getValue()
      v=FreeCADGui.activeDocument().activeView()
      info = v.getObjectInfo((pos[0],pos[1]))
      print("got info: %s" % (str(info)))
      if info.get('Component').startswith('Edge'):
         obj=App.getDocument(info.get('Document')).getObject(info.get('Object')).Shape.Edges[int(info.get('Component')[4:])-1]
         print("successfully got object")
         selectedEdge=obj
         if d is not None:
            v.removeEventCallback("SoEvent", d)
         d = v.addEventCallback("SoEvent",logPosition)
         state = LOG_POSITION
         print("changing state to LOG_POSITION")
   elif state == LOG_POSITION:
     print("log position")
     #   #self.obj.entryPoint=FreeCAD.Vector(info['x'], info['y'], info['z'])
     state = None
     view = FreeCADGui.ActiveDocument.ActiveView
     event = event_cb.getEvent()
     if extensionDir != None:
        print("Extension DIR IS SET: %d" % (extensionDir))
        extendEdge(selectedEdge, 5*extensionDir)
     if event.getState() == coin.SoMouseButtonEvent.DOWN:
        #v=FreeCADGui.activeDocument().activeView()
        view.removeEventCallback("SoEvent", d)
        d=None
        print("removing callback")
        view.removeEventCallbackPivy(coin.SoMouseButtonEvent.getClassTypeId(), callback)
        # {'x': -16.752037048339844, 'y': -38.52458953857422, 'z': 20.0, 'ParentObject': <body object>, 'SubName': 'Pad.Edge10', 'Document': 'outline3', 'Object': 'Pad', 'Component': 'Edge10'}
        #if info is not None:
            
 

v.removeEventCallback("SoEvent", c)

def ttimeout():
   getvalue()



timer=QtCore.QTimer()
timer.setSingleShot(True)
timer.timeout.connect(ttimeout)
#timer.start(2000)


def logPosition(event):
   global timer
   timer.stop()
   #print("logposition")
   timer.start(100)
   #timer=QtCore.QTimer()
   #timer.setSingleShot(True)
   #timer.timeout.connect(timeout)
   #timer.start(2000)
   #getvalue()
   #print(event['Position'])
   ##print(dir(event))

#v.removeEventCallback("SoEvent", d)
#v=Gui.activeDocument().activeView()
#d = v.addEventCallback("SoEvent",logPosition)
#v.removeEventCallback("SoEvent", c)
#v.addEventCallback("SoEvent",o.logPosition)
#view = FreeCADGui.ActiveDocument.ActiveView
#   callback = view.addEventCallbackPivy(coin.SoMouseButtonEvent.getClassTypeId(), getMouseClick)


def getvalue():
	 global plane
	 if len(Gui.Selection.getSelectionEx())==0:
	  return
	 plane=coin.SbPlane(coin.SbVec3f(0,0,1), Gui.Selection.getSelectionEx()[0].SubObjects[0].BoundBox.ZMax)
	 planeproj=coin.SbPlaneProjector(plane)
	 vpr=Gui.ActiveDocument.ActiveView.getViewer().getSoRenderManager().getViewportRegion() 
	 matrix=coin.SoGetMatrixAction(vpr) 
	 matrix.apply(Gui.ActiveDocument.ActiveView.getSceneGraph())
	 planeproj.setWorkingSpace(matrix.getMatrix())
	 fRatio=vpr.getViewportAspectRatio()
	 sp=vpr.getViewportSizePixels()
	 vvolume=Gui.ActiveDocument.ActiveView.getViewer().getSoRenderManager().getCamera().getViewVolume(fRatio)
	 currentpos=Gui.ActiveDocument.ActiveView.getCursorPos()
	 currentpos=(vpr.getViewportSize().getValue()[0]*currentpos[0]/sp.getValue()[0], vpr.getViewportSize().getValue()[1]*currentpos[1]/sp.getValue()[1])
	 planeproj.setViewVolume(vvolume) 
	 p=planeproj.project(coin.SbVec2f(currentpos))
	 edge=Gui.Selection.getSelectionEx()[0].SubObjects[0]
	 getDirection(edge, p.getValue())

def getDirection(edge, pt):
   global timer, extensionDir
   Bx=edge.Vertexes[1].Point[0]
   Ax=edge.Vertexes[0].Point[0]
   By=edge.Vertexes[1].Point[1]
   Ay=edge.Vertexes[0].Point[1]
   X=pt[0]
   Y=pt[1]
   res=(Bx - Ax) * (Y - Ay) - (By - Ay) * (X - Ax)
   print("RESULT")
   if res>0:
      print("-")
      extensionDir=-1
   else:
      extensionDir=1
      print("+")


#const SbViewportRegion& vp = getView3DIventorPtr()->getViewer()->getSoRenderManager()->getViewportRegion();
#       float fRatio = vp.getViewportAspectRatio();
#      const SbVec2s& sp = vp.getViewportSizePixels();
#        //float dX, dY; vp.getViewportSize().getValue(dX, dY);
#        SbViewVolume vv = getView3DIventorPtr()->getViewer()->getSoRenderManager()->getCamera()->getViewVolume(fRatio);



#(-25.242755889892578, -30.11629295349121, 20.0)
#p=FreeCAD.Vector(-25.242755889892578, -30.11629295349121, 20.0)
#c=Part.Vertex(p)
#c.distToShape(Gui.Selection.getSelectionEx()[0].SubObjects[0])
#info=c.distToShape(Gui.Selection.getSelectionEx()[0].SubObjects[0])
#Part.show(Part.Edge(Part.LineSegment(info[1][0][0],info[1][0][1])))
#(1.3965891101074206, [(Vector (-25.242755889892578, -30.11629295349121, 20.0), Vector (-26.639345, -30.11629295349121, 20.0))], [('Vertex', 0, None, 'Edge', 0, 8.408297046508793)])
#(1.566915681152345, [(Vector (-28.206260681152344, -34.75152587890625, 20.0), Vector (-26.639345, -34.75152587890625, 20.0))], [('Vertex', 0, None, 'Edge', 0, 3.7730641210937534)])


   #print(res)


### end here ###

def timeout():
   global Ax,Bx,Ay,By,X,Y
   res=(Bx - Ax) * (Y - Ay) - (By - Ay) * (X - Ax)
Ax=0
Bx=0
Ay=0
By=0
X=0
Y=0



from PySide import QtCore

        self.timer = QtCore.QTimer()
        self.count = 0
        self.timer.timeout.connect(self.timeout)
        self.timer.start(2000)



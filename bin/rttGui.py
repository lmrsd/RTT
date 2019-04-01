import os
import sys
import MaxPlus
from functools import partial
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
from pymxs import runtime as cmds
#init rtt functions
sys.path.append(os.path.dirname(__file__))
import rttFunctions as rtt
reload(rtt)
#Ui file
uifile = os.path.join(os.path.dirname(os.path.dirname(__file__)), "gui\\rtt.ui")
uiType, baseType = MaxPlus.LoadUiType(uifile)
mainWindow = MaxPlus.GetQMaxMainWindow()

class _GCProtector(object):
	widgets = []

class RttWidget(baseType, uiType) :
	def __init__(self,parent=mainWindow):
		baseType.__init__(self)
		uiType.__init__(self)
		self.setupUi(self)
		self.setUpConnections()
		MaxPlus.AttachQWidgetToMax(self)
		self.guiBindIcons()
		self.storedSettings = dict()
		self.setSettings = dict()

	def setUpConnections(self):

		self.openVfbBtn.clicked.connect(rtt.showlast)
		self.historyBtn.clicked.connect(rtt.openHistory)
		#Prod Btn
		self.prodFullBtn.clicked.connect(partial(self.launchRender,"full",size=1,ipr=False))
		self.prodHalfBtn.clicked.connect(partial(self.launchRender,"full",size=0.5,ipr=False))
		self.prodQuartBtn.clicked.connect(partial(self.launchRender,"full",size=0.25,ipr=False))
		#Draft Btn
		self.draftFullBtn.clicked.connect(partial(self.launchRender,"draft",size=1,ipr=False))
		self.draftHalfBtn.clicked.connect(partial(self.launchRender,"draft",size=0.5,ipr=False))
		self.draftQuartBtn.clicked.connect(partial(self.launchRender,"draft",size=0.25,ipr=False))
		#
		self.iprBtn.clicked.connect(partial(self.launchRender,"draft",size=1,ipr=True))

	def closeEvent(self,e):
		return

	def guiBindIcons(self):
		imgrootDir = os.path.dirname( os.path.dirname(os.path.abspath(__file__)) )
		print imgrootDir
		#Prod Full
		prodFullIcon = QtGui.QIcon()
		prodFullIconPath = os.path.join(imgrootDir,"gui","img","prodFull.png")
		prodFullIcon.addPixmap(QtGui.QPixmap(prodFullIconPath))
		self.prodFullBtn.setIcon(prodFullIcon)
		#Prod Mid
		prodMidIcon = QtGui.QIcon()
		prodMidIconPath = os.path.join(imgrootDir,"gui","img","prodMid.png")
		prodMidIcon.addPixmap(QtGui.QPixmap(prodMidIconPath))
		self.prodHalfBtn.setIcon(prodMidIcon)
		#Prod Quarter
		prodQuarterIcon = QtGui.QIcon()
		prodQuarterIconPath = os.path.join(imgrootDir,"gui","img","prodQuarter.png")
		prodQuarterIcon.addPixmap(QtGui.QPixmap(prodQuarterIconPath))
		self.prodQuartBtn.setIcon(prodQuarterIcon)
		#Draft Full
		draftFullIcon = QtGui.QIcon()
		draftFullIconPath = os.path.join(imgrootDir,"gui","img","draftFull.png")
		draftFullIcon.addPixmap(QtGui.QPixmap(draftFullIconPath))
		self.draftFullBtn.setIcon(draftFullIcon)
		#Draft Mid
		draftMidIcon = QtGui.QIcon()
		draftMidIconPath = os.path.join(imgrootDir,"gui","img","draftMid.png")
		draftMidIcon.addPixmap(QtGui.QPixmap(draftMidIconPath))
		self.draftHalfBtn.setIcon(draftMidIcon)
		#Draft Quarter
		draftQuarterIcon = QtGui.QIcon()
		draftQuarterIconPath = os.path.join(imgrootDir,"gui","img","draftQuarter.png")
		draftQuarterIcon.addPixmap(QtGui.QPixmap(draftQuarterIconPath))
		self.draftQuartBtn.setIcon(draftQuarterIcon)
		#IPR
		iprIcon = QtGui.QIcon()
		iprIconPath = os.path.join(imgrootDir,"gui","img","iprFull.png")
		iprIcon.addPixmap(QtGui.QPixmap(iprIconPath))
		self.iprBtn.setIcon(iprIcon)


        

	def collectStates(self):
		for i in range(self.optionGlay.count()):
			widget = self.optionGlay.itemAt(i).widget()
			if isinstance(widget, QtWidgets.QToolButton):
				splitName = (widget.objectName()).split('Btn')
				if splitName[0] == 'vfb' :
					rtt.getRenderOption(self.setSettings,vfb=widget.isChecked())
				elif splitName[0] == 'dof' :
					rtt.getRenderOption(self.setSettings,dof=widget.isChecked())
				elif splitName[0] == 'mob' :
					rtt.getRenderOption(self.setSettings,mob=widget.isChecked())
				elif splitName[0] == 'hair' :
					rtt.getRenderOption(self.setSettings,hair=widget.isChecked())
				elif splitName[0] == 'isolate' :
					rtt.getRenderOption(self.setSettings,isolate=widget.isChecked())
				elif splitName[0] == 'override' :
					rtt.getRenderOption(self.setSettings,override=widget.isChecked())
				elif splitName[0] == 'renderElem' :
					rtt.getRenderOption(self.setSettings,renderElem=widget.isChecked())
				elif splitName[0] == 'atmo' :
					rtt.getRenderOption(self.setSettings,atmo=widget.isChecked())
				elif splitName[0] == 'forest' :
					rtt.getRenderOption(self.setSettings,forest=widget.isChecked())
				elif splitName[0] == 'debug' :
					rtt.getRenderOption(self.setSettings,debug=widget.isChecked())
				elif splitName[0] == 'disp' :
					rtt.getRenderOption(self.setSettings,disp=widget.isChecked())
		print self.setSettings

	def launchRender(self,setting,size=1,ipr=False):
		#Render Settings Before
		self.storedSettings = rtt.initPref()
		# Ui states :
		self.collectStates()
		# Set render Settings Before Render		print setting
		if cmds.renderSceneDialog.isOpen():
			cmds.renderSceneDialog.close()

		rtt.changeRenderSettings(self.setSettings,setting,ipr)
		cmds.renderWidth = size * self.storedSettings['outWidth']
		cmds.renderHeight = size * self.storedSettings['outHeight']
		#DisableSave
		cmds.rendSaveFile = False

		#Update rendersettings dialog ?
		cmds.renderSceneDialog.commit()
		cmds.renderSceneDialog.update()
		#

		MaxPlus.RenderExecute.QuickRender()
		#Save Bitmap current Render
		bm = cmds.GetLastRenderedImage()
		bm.filename =rtt.previewName(rtt.initPreviewDir())
		cmds.save(bm)
		cmds.close(bm)
		
		#Restore parameters
		rtt.changeRenderSettings(self.setSettings,'default')
		cmds.renderWidth = self.storedSettings['outWidth']
		cmds.renderHeight = self.storedSettings['outHeight']
		#EnableSave
		cmds.rendSaveFile = False
		cmds.renderSceneDialog.commit()
		cmds.renderSceneDialog.update()


def initRttGui():
	#Check if exist and destroy if true
	for child in mainWindow.children() :
		classname = child.__class__.__name__
		if classname == "RttWidget" :
			child.setParent(None)
			child.close()

	if __name__ == "__main__":
		try:
			ui.close()
		except:
			pass
		ui = RttWidget()
		_GCProtector.widgets.append(ui)
		ui.show()

initRttGui()
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
		self.storedSettings = dict()
		self.setSettings = dict()


	def setUpConnections(self):
		self.openVfbBtn.clicked.connect(rtt.showlast)
		self.optionBtn.clicked.connect(self.collectStates)
		#Prod Btn
		self.prodFullBtn.clicked.connect(partial(self.launchRender,"full",size=1))
		self.prodHalfBtn.clicked.connect(partial(self.launchRender,"full",size=0.5))
		self.prodQuartBtn.clicked.connect(partial(self.launchRender,"full",size=0.25))
		#Draft Btn
		self.draftFullBtn.clicked.connect(partial(self.launchRender,"draft",size=1))
		self.darftHalfBtn.clicked.connect(partial(self.launchRender,"draft",size=0.5))
		self.draftQuartBtn.clicked.connect(partial(self.launchRender,"draft",size=0.25))

	def closeEvent(self,e):
		return

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

	def launchRender(self,setting,size=1):
		#Render Settings Before
		self.storedSettings = rtt.initPref()
		# Ui states :
		self.collectStates()
		# Set render Settings Before Render		print setting
		if cmds.renderSceneDialog.isOpen():
			cmds.renderSceneDialog.close()

		rtt.changeRenderSettings(self.setSettings,setting)
		cmds.renderWidth = size * self.storedSettings['outWidth']
		cmds.renderHeight = size * self.storedSettings['outHeight']
		#Update rendersettings dialog ?
		#renderSceneDialog.commit()
		#renderSceneDialog.update()
		#
		#MaxPlus.RenderExecute.QuickRender()
		rtt.changeRenderSettings(self.setSettings,'default')
		cmds.renderWidth = self.storedSettings['outWidth']
		cmds.renderHeight = self.storedSettings['outHeight']

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
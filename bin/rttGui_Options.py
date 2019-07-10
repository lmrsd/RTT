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
uifile = os.path.join(os.path.dirname(os.path.dirname(__file__)), "gui\\rtt_GlobalOption.ui")
uiType, baseType = MaxPlus.LoadUiType(uifile)
mainWindow = MaxPlus.GetQMaxMainWindow()

class _GCProtector(object):
	widgets = []

class RttWidgetGlobalOptions(baseType, uiType) :
	def __init__(self,parent=mainWindow,settings="draft"):
		baseType.__init__(self)
		uiType.__init__(self)
		self.settings = settings
		self.setupUi(self)
		self.populateSettings(self.settings)
		self.setUpConnections()

		MaxPlus.AttachQWidgetToMax(self)

	def setUpConnections(self):
		print "go"

	def populateSettings(self,settings):
		print settings
		dictKey = None
		# Here Open json config file
		
		if settings == "Draft" :
			print "draft"

		elif settings == "Mid" :
			print "mid"

		elif settings == "Hight":
			print "Hight"


def initRttGuiOption():
	#Check if exist and destroy if true
	for child in mainWindow.children() :
		classname = child.__class__.__name__
		if classname == "RttWidgetGlobalOptions" :
			child.setParent(None)
			child.close()

	if __name__ == "__main__":
		try:
			ui.close()
		except:
			pass
		ui = RttWidgetGlobalOptions(settings="Draft")
		_GCProtector.widgets.append(ui)
		ui.show()

initRttGuiOption()
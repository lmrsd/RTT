import PySide2
from pymxs import runtime as cmds

"""

--Vfb
--mo blur
--dof
--displace
hair
forestP
--OverideMtl
RenderEle
--Atmo Ok
--ShowLastVfb
"""
vRay = cmds.renderers.current
renderOpt = dict()
renderElem = cmds.RenderElementMgr
pathToRender = "D:\\00_LOUIS\\000_SCRIPTS\\LM_RTT\\bin\\preview_.tga"
#

def getRenderOption (**kwargs):
		renderOpt.update(kwargs.items())
		# add if same key not update
def setRenderOption(**kwargs):
	print renderOpt.get(kwargs.keys)

# Get Settings First #
getRenderOption(vfb=vRay.output_on)
getRenderOption(dof=vRay.dof_on)
getRenderOption(mob=vRay.moblur_on)
getRenderOption(disp=vRay.options_displacement)
getRenderOption(over=vRay.options_overrideMtl_on)
getRenderOption(outWidth=cmds.renderWidth,outHeigh=cmds.renderHeight)

#CheckEttings
print renderOpt
print (os.path.expanduser('~'))

#Close render dialog
if cmds.renderSceneDialog.isOpen():
	cmds.renderSceneDialog.close()

IOAtmo = False
IORenderElem = False
IODof = False
IOMoBu = False
IOOverride = False
IOVfb = True
IODisplace = False


# SETTINGS

# .SetElementActive(IORenderElem)
# help(PySide2)

vRay.output_on = IOVfb
vRay.dof_on = IODof
vRay.moblur_on = IOMoBu
vRay.options_displacement = IODisplace
# vRay.displace = False

vRay.options_overrideMtl_on = IOOverride
BaseMat = cmds.vRayMtl()
vRay.options_overrideMtl_mtl = BaseMat





cmds.render(outputfile="D:\\00_LOUIS\\000_SCRIPTS\\LM_RTT\\bin\\preview_.tga", vfb=False, renderatmosphericeffects=IOAtmo, renderElements=IORenderElem)
# vRay.vfbcontrol(show=True)
vRay.showLastVFB()
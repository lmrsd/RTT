import os
import json
import subprocess,pprint
from pymxs import runtime as cmds
import MaxPlus
vRay = cmds.renderers.current

#Path
rootDir = os.path.dirname(os.path.dirname(__file__))
configFile = os.path.join (rootDir,'config','rttConfig.json')
storeConfig = os.path.join(rootDir,'config','rttStoreParam.json')
#Global
with open(configFile) as f :
	configData = json.load(f) 

renderElem = cmds.RenderElementMgr

#
def initPreviewDir():
	previewDir = os.path.join(rootDir,configData['previewDir'])
	if not os.path.isdir(previewDir):
		os.mkdir(previewDir)
	return previewDir

def previewName(root):
	previewNumber =len(os.listdir(root))
	previewPath = os.path.join(root , configData['previewDir'] + "_" + str(previewNumber) + configData['previewType'])
	return previewPath

def getRenderOption(cdict,**kwargs):
	cdict.update(kwargs.items())
	# add if same key not update

def keepRegionVfb(width,height):
	if cmds.vrayVFBGetRegionEnabled():
		curWidth = cmds.vrayVFBGetChannelBitmap(1).width
		curHeight = cmds.vrayVFBGetChannelBitmap(1).height
		curRegion = cmds.vrayVFBGetRegion()
		#
		nwLeft = int(width*float(curRegion[0])/curWidth)
		nwTop = int(height*float(curRegion[1])/curHeight)
		nwRight = int(width*float(curRegion[2])/curWidth)
		nwBottom = int(height*float(curRegion[3])/curHeight)

def showlast():
	vRay.showLastVFB()

def openHistory():
	previewDir = os.path.join(rootDir,configData['previewDir'])
	os.startfile(previewDir) 

def changeRenderSettings(dictState,settings,ipr=False):
	#globals
	reMgr = cmds.maxOps.getCurRenderElementMgr()	

	#Full
	if settings == 'full' :
		for i in configData['RenderSettingsHightDefault'] :
			dictState[i] = configData['RenderSettingsHightDefault'][i]
	#Mid
	elif settings == 'mid' :
		for i in configData['RenderSettingsMidDefault'] :
			dictState[i] = configData['RenderSettingsMidDefault'][i]
	#Draft		
	elif settings == 'draft' :
		for i in configData['RenderSettingsDraftDefault'] :
			dictState[i] = configData['RenderSettingsDraftDefault'][i]
	#Default
	elif settings == 'default' :
		return

	#Vfb
	vRay.output_on = dictState['vfb']
	#Dof
	vRay.dof_on = dictState['dof']
	#MotionBlur
	vRay.moblur_on = dictState['mob']
	#Displace
	vRay.options_displacement = dictState['disp']
	#renderElements
	reMgr.SetElementsActive(dictState['renderElem'])
	#Atmosphere
	cmds.rendAtmosphere = dictState['atmo']
	print ('##ATMO : '+ str(dictState['atmo']))
	cmds.rendAtmosphere = dictState['atmo']
	#Override
	vRay.options_overrideMtl_on = dictState['override']
	BaseMat = cmds.vRayMtl()
	BaseMat.name="OVERRIDE_MAT"
	vRay.options_overrideMtl_mtl = BaseMat
	#Isolate
	if dictState['isolate'] == True :
		vRay.imageSampler_renderMask_type = 2
	else :
		vRay.imageSampler_renderMask_type = dictState['isolate']
	#Probalistic
	vRay.options_probabilisticLights = dictState['probabilisticLights']
	vRay.options_probabilisticLightsCount = dictState['probabilisticCount']
	#Filter Maps
	vRay.options_filterMaps = dictState['filterMaps']
	#Image Sampler
	vRay.imageSampler_type = dictState['imageSampler']
	#Min Shading Rate
	vRay.imageSampler_shadingRate = dictState['minShadingRate']
	#Subdivs
	vRay.twoLevel_baseSubdivs = dictState['minSubdiv']
	vRay.twoLevel_fineSubdivs = dictState['maxSubdiv']
	#Buckets
	vRay.twoLevel_bucket_width = dictState['BucketWidth']
	vRay.twoLevel_bucket_height = dictState['BucketWidth']
	#NoiseThreshold
	vRay.twoLevel_threshold = dictState['noiseThreshold']
	#Clamp
	vRay.colorMapping_clampOutput = dictState['clampOutut']
	vRay.colorMapping_clampLevel = dictState['clampLevel']
	#LightCache
	vRay.lightcache_subdivs = dictState['LightCacheSubdivs']
	
	#IPR
	vRay.ipr_progressiveMode = ipr
	
	#Debug Shading Mode
	if dictState['debug'] :
		reMgr.SetElementsActive(True)
		normalPass = cmds.VRayNormals(elementname="[rtt]_Normals")
		normalPass.elementname = "[rtt]_Normals"
		#Uv
		uvTex = cmds.VraySamplerInfoTex()
		uvTex.name = "[rtt]_Uvs"
		uvTex.type = 4
		uvPass = cmds.VRayExtraTex(elementname="[rtt]_Uvs")
		uvPass.texture = uvTex
		uvPass.elementname = "[rtt]_Uvs"
		#Occ
		aoTex = cmds.VrayDirt()
		aoTex.name = "[rtt]_AO"
		aoTex.unoccluded_color = cmds.color(232,232,232)
		aoPass = cmds.VRayExtraTex(elementname="[rtt]_Occ")
		aoPass.texture = aoTex
		aoPass.elmentname = "[rtt]_Occ"
		#Add Passes
		reMgr.AddRenderElement(normalPass)
		reMgr.AddRenderElement(uvPass)
		reMgr.AddRenderElement(aoPass)

		# Render overide light material + texture
		vRay.options_overrideMtl_on = True
		customTexMat = cmds.vRayLightMtl()
		customTexMat.name="OVERRIDE_TEX"
		vRay.options_overrideMtl_mtl = customTexMat

	#End of functin Update in scene dialog
	cmds.renderSceneDialog.commit()
	cmds.renderSceneDialog.update()

# FINAL
def deleteRttPasses():
	print "starting delete...."
	reMgr = cmds.maxOps.getCurRenderElementMgr()
	elemCount = reMgr.numrenderelements()
	for i in range(0,elemCount-1):
		el = reMgr.GetRenderElement(i)
		#print (el.elementName)
		if len((el.elementName).split("[rtt]")) > 1 :
			reMgr.RemoveRenderElement(el)

def initPref():
	getRderOpt = dict()
	reMgr = cmds.maxOps.getCurRenderElementMgr()	
	# Get Global Option from Render Settings
	getRenderOption(getRderOpt,vfb=vRay.output_on)
	getRenderOption(getRderOpt,dof=vRay.dof_on)
	getRenderOption(getRderOpt,mob=vRay.moblur_on)
	getRenderOption(getRderOpt,disp=vRay.options_displacement)
	getRenderOption(getRderOpt,over=vRay.options_overrideMtl_on)
	getRenderOption(getRderOpt,outWidth=cmds.renderWidth,outHeight=cmds.renderHeight)
	getRenderOption(getRderOpt,isolate = vRay.imageSampler_renderMask_type)
	getRenderOption(getRderOpt,renderElem=reMgr.GetElementsActive())
	getRenderOption(getRderOpt,outputFile=cmds.rendOutputFilename)
	getRenderOption(getRderOpt,outputSave=cmds.rendSaveFile)
	# Vray Option from render Settings
	getRenderOption(getRderOpt,probabilisticLights=vRay.options_probabilisticLights)
	getRenderOption(getRderOpt,probabilisticCount=vRay.options_probabilisticLightsCount)
	getRenderOption(getRderOpt,filterMaps=vRay.options_filterMaps)
	getRenderOption(getRderOpt,imageSampler=vRay.imageSampler_type)
	getRenderOption(getRderOpt,minShadingRate=vRay.imageSampler_shadingRate)
	getRenderOption(getRderOpt,minSubdiv=vRay.twoLevel_baseSubdivs)
	getRenderOption(getRderOpt,maxSubdiv=vRay.twoLevel_fineSubdivs)
	getRenderOption(getRderOpt,BucketWidth=vRay.twoLevel_bucket_width)
	getRenderOption(getRderOpt,noiseThreshold=vRay.twoLevel_threshold)
	getRenderOption(getRderOpt,clampOutut=vRay.colorMapping_clampOutput)
	getRenderOption(getRderOpt,clampLevel=vRay.colorMapping_clampLevel)
	getRenderOption(getRderOpt,LightCacheSubdivs=vRay.lightcache_subdivs)
	#
	
	print getRderOpt
	return getRderOpt

def getRenderesParams(render):
	stockedParam = dict()
	renderParams = (dir(render))
	if render :
		for p in renderParams:
			attr = getattr(render,p)
			if type(attr) is bool or type(attr) is float or type(attr) is str or type(attr) is int :
				param = {p:getattr(render,p)}
			else :
				param ={p:'undefined'}
			stockedParam.update(param)
	return stockedParam

def add3DMaxRenderOption(renderDict):
	#Specfic render Param Width, Height,Atmospherics
	renderDict.update({'renderWidth':cmds.renderWidth})
	renderDict.update({'renderHeight':cmds.renderHeight})
	renderDict.update({'renderAtmosphere':cmds.rendAtmosphere})
	return renderDict

def writeParam(rdict):
	with open(storeConfig, 'wb') as outfile:
		json.dump(rdict, outfile)

def retoreParam(file,render):
	if os.path.exists(file):
		with open(file) as f :
			data = json.load(f)
	for p in data :
		#print(p,data[p])
		if data[p] != 'undefined':
			if hasattr(render,p) :
				attr = getattr(render,p)
				if attr != data[p] :
					setattr(render, p, data[p])
		# Special Case:
		if p == 'renderWidth' :
			print ('renderWidth',cmds.renderWidth,data['renderWidth'])
			if cmds.renderWidth != data['renderWidth'] :
				cmds.renderWidth = data['renderWidth']
		elif p == 'renderHeight' :
			if cmds.renderHeight != data['renderHeight'] :
				cmds.renderHeight = data['renderHeight']
		elif p == 'renderAtmosphere' :
			if cmds.rendAtmosphere != data['renderAtmosphere'] :
				cmds.rendAtmosphere = data['renderAtmosphere']


if  __name__=="__main__":
	cmds.renderSceneDialog.close()
	#vrayParams = add3DMaxRenderOption(getRenderesParams(cmds.renderers.current))
	#writeParam(vrayParams)
	
	retoreParam(storeConfig,cmds.renderers.current)
	cmds.renderSceneDialog.open()
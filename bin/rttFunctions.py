import os
import json
import subprocess
from pymxs import runtime as cmds
vRay = cmds.renderers.current

#Path
rootDir = os.path.dirname(os.path.dirname(__file__))
configFile = os.path.join (rootDir,'config','rttConfig.json')
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

deleteRttPasses()
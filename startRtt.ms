fileScriptPath = getThisScriptFilename()
fileParentDir = pathConfig.removePathLeaf fileScriptPath
python.ExecuteFile (fileParentDir+"\\"+"bin"+"\\"+"rttGui.py")
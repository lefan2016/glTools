import maya.cmds as mc

import glTools.tools.controlBuilder

import glTools.utils.base
import glTools.utils.transform

class UserInputError(Exception): pass
class UIError(Exception): pass

def controlBuilderUI():
	'''
	UI for controlBuilder()
	'''
	# Window
	window = 'controlBuilderUI'
	if mc.window(window,q=True,ex=1): mc.deleteUI(window)
	window = mc.window(window,t='Control Builder')
	# Layout
	cl = mc.columnLayout()
	# UI Elements
	nameTFG = mc.textFieldGrp('controlNameTFG',label='Control Name', text='default_ccc')
	typeOMG = mc.optionMenuGrp('controlTypeOMG',label='Control Type')
	for cType in glTools.tools.controlBuilder.ControlBuilder().controlType:
		mc.menuItem(label=str.capitalize(cType)[0]+cType[1:])
	bufferCBG = mc.checkBoxGrp('controlBufferCBG',numberOfCheckBoxes=1,label='Create Buffer',v1=False)
	createB = mc.button('controlBuilderCreateB',l='Create',c='glTools.ui.controlBuilder.controlBuilderFromUI(False)',w=250)
	createCloseB = mc.button('controlBuilderCreateCloseB',l='Create and Close',c='glTools.ui.controlBuilder.controlBuilderFromUI()',w=250)
	closeB = mc.button('controlBuilderCloseB',l='Close',c='mc.deleteUI("'+window+'")',w=250)
	# Show Window
	mc.showWindow(window)

def controlBuilderFromUI(close=True):
	'''
	Execute controlBuilder() from UI
	'''
	# Window
	window = 'controlBuilderUI'
	if not mc.window(window,q=True,ex=1): raise UIError('Control Builder UI does not exist!!')

	# Get UI data
	cName = mc.textFieldGrp('controlNameTFG',q=True,text=True)
	cType = mc.optionMenuGrp('controlTypeOMG',q=True,v=True)
	cType = str.lower(str(cType[0]))+cType[1:]
	cBuffer = mc.checkBoxGrp('controlBufferCBG',q=True,v1=True)

	# Get Active Selection
	tSel = []
	sel = mc.ls(sl=1)
	for obj in sel:
		if glTools.utils.transform.isTransform(obj):
			tSel.append(obj)

	# Execute
	if tSel:
		for obj in tSel:
			glTools.tools.controlBuilder.ControlBuilder().controlShape(transform=obj,controlType=cType)
	else:
		ctrl = glTools.tools.controlBuilder.ControlBuilder().create(controlType=cType,controlName=cName)
		# Buffer
		if cBuffer:
			glTools.utils.base.group(ctrl,groupType=1,center=1,orient=1)

	# Cleanup
	if close: mc.deleteUI(window)

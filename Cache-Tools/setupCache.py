#! python
__version__		= '0.1'
__author__		= 'forgacs.daniel@gmail.com'

# Houdini version 13
# usage:
# sys.path.insert(0, 'd:\Development\Houdini')
# import setupCache as cs
# cs.do_cache_setup()

import hou

def do_cache_setup(cachefolder = '$CACHEFOLDER'):
	try:
		selected_node	= hou.selectedNodes()[0]
	except:
		print('---> NO SELECTION')
		selected_node	= None

	if selected_node:
		root	= hou.node('/obj')
		geo		= selected_node.parent()
		null	= geo.createNode('null', 'to_cache_' + selected_node.name())
		read	= geo.createNode('file')
		
		null.setFirstInput(selected_node)
		read.setFirstInput(null)
		read.setDisplayFlag(True)
		read.setRenderFlag(True)

		parmtemplate	= hou.StringParmTemplate("rop", "rop", 1,
							string_type = hou.stringParmType.NodeReference)
		
		read.addSpareParmTuple(parmtemplate)
		read.parm("filemode").lock(True)
		read.parm('file').set('`chs(chs("rop") + "/sopoutput")`')

		null.moveToGoodPosition()
		read.moveToGoodPosition()
		read.setCurrent(True, clear_all_selected = True)

		if root.node('cache'):
			ropnet	= root.node('cache')
		else:
			ropnet	= root.createNode('ropnet', 'cache')
		
		rop	= ropnet.createNode('geometry', selected_node.name())
		read.parm('rop').set(rop.path())

		rop_parms	= {'soppath'	: null.path(),
						'sopoutput'	: '{0}/$OS/$OS.$F4.bgeo.gz'.format(cachefolder),
						'trange'	: 2,
						'mkpath'	: True,
						'saveretry'	: 2,
						'@f1'		: '$FSTART',
						'@f2'		: '$FEND'
						}

		for key in rop_parms:
			if '@' not in key:
				rop.parm(key).set(rop_parms[key])
			else:
				rop.parm(key[1:]).setExpression(rop_parms[key])
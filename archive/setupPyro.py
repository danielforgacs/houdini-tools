#! python
__author__		= 'forgacs.daniel@gmail.com'
__version__		= '0.1'

# Houdini 13
# WORK IN PROGRESS


import time
import hou


def _message(txt):
	print( '-----> {0}'.format( txt))


def pyro_setup(objroot = False):
	try:
		selection	= hou.selectedNodes()[0]
	except:
		print('SELECTION ERRRRROR')

	if objroot:
		root		= hou.node( '/obj')
	else:
		root		= hou.node( selection.parent().path())

	srcnodes	= {'high' : '', 'low' : ''}
	blasts		= []
	blastCount	= 0
	mixnodes	= {'density' : '', 'vel' : ''}

	for src in srcnodes:
		srcnodes[src]	= selection.createOutputNode('fluidsource',
													'fluidsource_' + src + 
													'_freq')

		for i in range(2):
			blasts.append( srcnodes[src].createOutputNode(
							'blast', 'blast_{}'.format(blastCount)))

			if src == 'high':
				mixkey				= list(mixnodes.keys())[1 - i]
				mixnodes[mixkey]	= blasts[blastCount].createOutputNode(
										'volumemix',
										'volumemix_' + mixkey)

			blastCount += 1

	for k, node in enumerate(mixnodes):
		mixnodes[node].setInput(1, blasts[3 - k])
		mixnodes[node].parm('mixmethod').set(4 if node == 'density' else 1)

	scatter		= blasts[0].createOutputNode('scatter')
	veltrail	= scatter.createOutputNode('volumetrail')
	veltrail.setInput(1, mixnodes['vel'])

	mixmerge	= mixnodes['density'].createOutputNode('merge')
	mixmerge.setInput(1, mixnodes['vel'])
	sourcenull	= mixmerge.createOutputNode('null', 'OUT_smoke_sources')


	for k in range( len(blasts)):
		blasts[k].parm('group').set('@name=density')
		blasts[k].parm('removegrp').set(1)
		blasts[k].parm('negate').set(1 if (k+1) % 2 else 0)

	# node layout
	selection.			setPosition( hou.Vector2(0, 0))
	srcnodes['high'].	setPosition( hou.Vector2(-4, -3))
	srcnodes['low'].	setPosition( hou.Vector2(4, -3))
	blasts[0].			setPosition( hou.Vector2(-6, -5))
	blasts[1].			setPosition( hou.Vector2(-2, -5))
	blasts[2].			setPosition( hou.Vector2(2, -5))
	blasts[3].			setPosition( hou.Vector2(6, -5))
	mixnodes['density'].setPosition( hou.Vector2(-4, -8))
	mixnodes['vel'].	setPosition( hou.Vector2(0, -8))
	scatter.			setPosition( hou.Vector2(-8, -8))
	veltrail.			setPosition( hou.Vector2(-7, -10))
	mixmerge.			setPosition( hou.Vector2(-2, -12))
	sourcenull.			setPosition( hou.Vector2(-2, -14))

	# DOP setup
	_message('DOP setup')

	dopnodes	= {	'solver'			: 'pyrosolver',
					'applyvorticles'	: 'applydata',
					'smokeobject'		: 'smokeobject',
					'vorticlegeo'		: 'gasvorticlegeometry',
					'resize'			: 'gasresizefluiddynamic',
					'mergevel'			: 'merge',
					'vorticleforces'	: 'gasvorticleforces',
					'mergeadvect'		: 'merge',
					'vorticlesadvect'	: 'gasadvect',
					'vorticlestrech'	: 'gasvelocitystretch',
					'vorticlerecyce'	: 'gasvorticlerecycle',
					'mergesource'		: 'merge',
					'source'			: 'sourcevolume',
					'gravity'			: 'gravity',
				}

	dopnet		= root.createNode('dopnet')

	for node in dopnodes:
		dopnodes[node] = dopnet.createNode(dopnodes[node], node)

	dopnodes['solver'].			setInput(0, dopnodes['applyvorticles'])
	dopnodes['applyvorticles'].	setInput(0, dopnodes['smokeobject'])
	dopnodes['applyvorticles'].	setInput(1, dopnodes['vorticlegeo'])
	dopnodes['solver'].			setInput(1, dopnodes['resize'])
	dopnodes['solver'].			setInput(2, dopnodes['mergevel'])
	dopnodes['mergevel'].		setInput(2, dopnodes['vorticleforces'])
	dopnodes['solver'].			setInput(3, dopnodes['mergeadvect'])
	dopnodes['mergeadvect'].	setInput(0, dopnodes['vorticlesadvect'])
	dopnodes['mergeadvect'].	setInput(1, dopnodes['vorticlestrech'])
	dopnodes['mergeadvect'].	setInput(2, dopnodes['vorticlerecyce'])
	dopnodes['solver'].			setInput(4, dopnodes['mergesource'])
	dopnodes['mergesource'].	setInput(4, dopnodes['source'])
	dopnodes['gravity'].		setInput(0, dopnodes['solver'])

	# parameter settings
	scatter.parm('npts').set(250)
	srcnodes['low'].parm('divsize').setExpression(
		'ch("../{}/divsize")'.format(srcnodes['high'].name()))

	parms	= {	'eloc'				: 0.1,
				'size'				: 0,
				'use_noise'			: 1,
				'sharpness'			: 1,
				'grain'				: 0,
				'element_size'		: 0.3,
				}

	for p in parms:
		srcnodes['density'].parm(p).set(parms[p])

	# layouts
	dopnet.						setPosition( hou.Vector2(-2, -16))


_message('#' * 40)
pyro_setup()
_message('DONE')
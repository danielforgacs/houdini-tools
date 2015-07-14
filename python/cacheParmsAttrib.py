#! python3

print("~#~"*25)


__author__ = "forgacs.daniel@gmail.com"
__version__ = "v0.1"


try:
	import hou
except:
	pass


def get_node_parms(node):
	parmnames = []

	for parm in node.parms():
		parmnames.append(parm.name())


	return parmnames


def get_selection():
	nodeslist = hou.selectedNodes()
	return nodeslist


def main(kwargs):
	nodes = get_selection()

	for node in nodes:
		parmslist = get_node_parms(node)


	print(nodes)
	print(parmslist)
# Update button onli available after refresh


import hou


class ShotAssetsSubnet (object):
    def __init__ (self):
        pass

    def create (self):
        sub = hou.node ('/obj').createNode ('subnet')

        for element in sub.parms():
            element.hide (True)

        sub.moveToGoodPosition()
        sub.setCurrent (True, True)

        btn_update = hou.ButtonParmTemplate ('update', 'update')

        scrpt_strng = ('import ShotAssetsSub;'
                       'reload (ShotAssetsSub);'
                       'ShotAssetsSub.update_sub()')

        btn_update.setScriptCallback (scrpt_strng)
        btn_update.setScriptCallbackLanguage (hou.scriptLanguage.Python )
        sub.addSpareParmTuple (btn_update)

    def add_seet_parms (self, asset):
        node        = hou.pwd()
        name        = asset['name']
        label       = name
        maxversion  = int (asset['version'])

        # spares['_display', '_node', '_update', '_delete']


        if not node.parm (name):
            parm_display    = hou.ToggleParmTemplate (name + '_display', 'display', default_value = False, join_with_next = True)
            # items           = ('v1', 'v2')
            items           = ([str(k + 1) for k in range(maxversion)])
            menu            = hou.MenuParmTemplate ('version' + name, asset['asset'], items, default_value = maxversion)
            parm_node       = hou.StringParmTemplate (label, name + '_node', 1, join_with_next = True)
            btn_update      = hou.ButtonParmTemplate ('update' + name, 'update')
            btn_delete      = hou.ButtonParmTemplate ('delete' + name, 'delete')

            parm_display.setJoinWithNext (True)
            parm_node.setJoinWithNext (True)

            parm_node.setStringType( hou.stringParmType.NodeReference )

            node.addSpareParmTuple (parm_display)
            node.addSpareParmTuple (menu)
            node.addSpareParmTuple (parm_node)
            node.addSpareParmTuple (btn_update)
            node.addSpareParmTuple (btn_delete)

    def add_asset_parms(self, asset):
        node            = hou.pwd()
        assetype        = asset['asset']
        assetname       = asset['name']
        parmgroup       = assetype + assetname + '_ParmGroup'
        maxversion      = int (asset['version'])


def get_cameras():
    cameras = [{'asset' : 'mm_cam', 'path' : 'd:/_temp/cams/rendercam', 'name' : 'rend_cam_6', 'version' : '6'},
            {'asset' : 'projection_cam', 'path' : 'd:/_temp/cams/procam', 'name' : 'pr_cam_2', 'version' : '2'},
            {'asset' : 'misc_cam', 'path' : 'd:/_temp/cams/misc', 'name' : 'mcs_cam_1', 'version' : '1'}]

    return cameras[:3]

def update_sub ():
    node        = ShotAssetsSubnet()
    cams        = get_cameras()

    for element in cams:
        # node.add_seet_parms (element)
        node.add_asset_parms (element)

def main():
    sub     = ShotAssetsSubnet()
    sub.create()


def TEST_parmGroup ():
    node = hou.selectedNodes()[0]

    group = hou.ParmTemplateGroup()

    btn1 = hou.ButtonParmTemplate('btn1', 'btn1')
    btn2 = hou.ButtonParmTemplate('btn2', 'btn2')
    btn3 = hou.ButtonParmTemplate('btn3', 'btn3')

    group.addParmTemplate(btn1)
    group.addParmTemplate(btn2)
    group.addParmTemplate(btn3)

    # node.addSpareParmTuple(group)
    folder = hou.FolderParmTemplate('folder', 'folder', folder_type=hou.folderType.Simple)
    # group.appendToFolder (folder.name())
    # node.addSpareParmFolder(folder)
    node.addSpareParmTuple (folder)

    print 'done'
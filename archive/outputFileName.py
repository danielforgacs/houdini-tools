def outputFileName ( element = ''):
    """render folder:
hip folder / render folder / shot name / version / element / filename"""
    
    job     = hou.expandString('$JOB')
    ver     = hou.expandString('$HIPNAME')
    ver     = ver.replace('\\', '/')
    ver     = ver.split('/')
    ver     = ver[len(ver)-1]

    shot    = ver
    shot    = shot[:shot.rfind('.hip')]
    shot    = shot[:-5]

    ver     = ver[:ver.rfind('.hip')][-4:]

    per     = '/'

    if (element == '') or (element == '_current_'):
        element = ''

    return job + '/render/' + shot + per + ver + per + element + per + shot + '_' + element + '_' + ver + '.' + hou.expandString('$F4') + '.exr'

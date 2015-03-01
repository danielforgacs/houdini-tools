#! python


__version__     = '0.0'
__author__      = ('linkedin.com/in/danielforgacs; '
                    'github.com/danielforgacs; '
                    'bitbucket.org/fordan')


__doc__         = """/
Houdini scene setup for pipeline integration

Houdini version: 14.0
Python version: H14.0 default
"""



def _message(text, value = ''):
    print ('--> {}: {}'.format(text, value))


class HouWorkEnv(object):
    """Base Houdini Scene Class"""
    def __init__(self, arg):
        # super(ClassNames, self).__init__()
        pass
        


if __name__ == '__main__':
    pass
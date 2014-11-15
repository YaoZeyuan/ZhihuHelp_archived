import sys  
reload(sys)  
sys.setdefaultencoding('utf8') 

def printDict(data = {}, key = '', prefix = ''):
    if isinstance(data, dict):
        for key in data.keys():
            printDict(data[key], key, prefix + '   ')
    else:
        print prefix + str(key) + ' => ' + str(data)

def getXsrf(content=''):
    import re
    xsrf = re.search(r'(?<=name="_xsrf" value=")[^"]*(?="/>)',content)
    if xsrf == None:
        return ''
    else:
        return '_xsrf=' + xsrf.group(0)

import hashlib

def getmd5(string):
    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    return m.hexdigest()

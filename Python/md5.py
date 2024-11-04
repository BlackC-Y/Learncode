import hashlib, os, re, pathlib

def main():
    spath = 'D:/迅雷下载/Learn/Microsoft leaked source code archive_2020-09-24/'
    md5List = []
    savemd5List = md5List.append
    #print(pathlib.Path(spath).is_file())
    if os.path.isfile(spath):
        savemd5List(computeMd5(spath))
    elif os.path.isdir(spath):
        for root, dirs, files in os.walk(spath):
            for f in files:
                nowfile = '%s/%s' % (root, f)
                savemd5List(computeMd5(nowfile))
            #print(root, '\n', dirs, '\n', files)
    with open('D:/迅雷下载/Learn/md.txt', 'w') as of:
        for i in md5List:
            of.write('%s\r\n' %i)

def computeMd5(Fpath):
    if os.path.getsize(Fpath) / 1024 > 5120:
        onemd5 = hashlib.md5()
        with open(Fpath, 'rb') as of:
            while True:
                fdata = of.read(5120)
                if not fdata:
                    break
                onemd5.update(fdata)  #update添加时会进行计算
            return onemd5.hexdigest()
    else:
        with open(Fpath, 'rb') as of:
            fdata = of.read()
        return hashlib.md5(fdata).hexdigest()


def duidb():
    dbPath = 'D:/迅雷下载/Learn/Microsoft leaked source code archive_2020-09-24/md5.txt'
    with open(dbPath) as dbf:
        line = dbf.readline()
        allLine = []
        saveline = allLine.append
        while line:
            saveline(line)
            line = dbf.readline()
    with open('D:/迅雷下载/Learn/md.txt') as mdf:
        line = mdf.readline()
        mdLine = []
        saveline = mdLine.append
        while line:
            saveline(line.strip())
            line = mdf.readline()
    rig = []
    for i in mdLine:
        for m in allLine:
            if i in m:
                rig.append(i)
    print(len(rig))

if __name__ == "__main__":
    #main()
    duidb()


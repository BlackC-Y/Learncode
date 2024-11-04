import sys
import os
import shutil
from concurrent.futures import ThreadPoolExecutor

#持续监控 强制停止
def monitorFile():
    spath = "源路径"
    files = os.listdir(spath)
    num = len(files)
    #pool = ThreadPoolExecutor(max_workers=2)
    while(1):
        newfiles = os.listdir(spath)
        if len(newfiles) != num:
            st = 1
            while(st):
                newfiles = os.listdir(spath)
                for i in list(set(newfiles).difference(set(files))):
                    try:
                        shutil.copy(spath + i, '目标路径')
                    except:
                        print(i)
                    #os.system(f'copy "{spath}{i}" "目标路径"')
                    #pool.submit(copfile, spath + i)
                if len(newfiles) == num:
                    return

        else:
            continue

def copfile(fil):
    shutil.copy(fil, '目标路径')

if __name__ == "__main__":
    monitorFile()
# -*- coding: UTF-8 -*-
import sys

argList = sys.argv
sys.path.append(argList[1])

import dna


def loadDna(path) -> dna.BinaryStreamReader:
    stream = dna.FileStream(path, dna.FileStream.AccessMode_Read, dna.FileStream.OpenMode_Binary)
    reader = dna.BinaryStreamReader(stream, dna.DataLayer_All)
    reader.read()
    if not dna.Status.isOk():
        status = dna.Status.get()
        raise RuntimeError(f"Error loading DNA: {status.message}")
    return reader

def saveFullDna(path, reader, newReader):
    stream = dna.FileStream(path, dna.FileStream.AccessMode_Write, dna.FileStream.OpenMode_Binary)
    writer = dna.BinaryStreamWriter(stream)
    writer.setFrom(reader)
    writer.setFrom(newReader, dna.DataLayer_Behavior)
    writer.write()

saveFullDna(argList[2], loadDna(argList[2]), loadDna(argList[3]))
#import os
#os.system("pause")

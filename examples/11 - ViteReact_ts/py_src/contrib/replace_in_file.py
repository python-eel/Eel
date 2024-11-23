from io import TextIOWrapper
import re
import os

def readInChunks(fileObj: TextIOWrapper, chunkSize=2048):
    """
    Lazy function to read a file piece by piece.
    Default chunk size: 2kB.

    """
    start_byte = -chunkSize
    end_byte = 0
    while True:
        start_byte += chunkSize
        end_byte += chunkSize
        data = fileObj.read(chunkSize)
        if not data:
            break
        if len(data) < chunkSize:
            print("data size is", len(data))
            end_byte = start_byte + len(data)
        yield data, start_byte, end_byte




def replaceInfile(file_path, search_text_re, replace_text):
    """ 
    Replace a part of a file. Used for changing the host in production mode. Only works with pyinstaller --onedir

    usage: replaceInfile("./dist_vite/assets/index-f8b4bc6c.js", 'ws://localhost:....', 'ws://localhost:6820') 
    """
    with open(file_path, 'r+') as f:
        for chunk, start_byte, end_byte in readInChunks(f):
            if re.search(search_text_re, chunk):
                print("found search text in block", start_byte, "end_byte", end_byte )
                f.seek(start_byte)
                f.write(re.sub(search_text_re, replace_text, chunk, count=1))
                f.close()
                break

def findFileRe(rootdir, regex_str):
    """
    Find a file in a folder based on a regex search

    Usage: findFileRe("./dist_vite/assets", "index.*.js")
    """
    regex = re.compile(regex_str)
    for root, dirs, files in os.walk(rootdir):
        for file in files:
            if regex.match(file):
                return file
    return None


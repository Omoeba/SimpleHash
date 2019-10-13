import hashlib
import pyperclip
import shutil
import getpass

def ts():
    return shutil.get_terminal_size()


def lineSeparator():
    return "━" * ts().columns


def hexPrinter(hexValue):
    i = 1
    endIndex = len(hexValue)
    while True:
        lineIndex = ts().columns * i
        hexValue = list(hexValue)
        if lineIndex >= endIndex:
            break
        else:
            hexValue[lineIndex] = '\n'
            hexValue = "".join(hexValue)
        i = i + 1
    hexValue="".join(hexValue)
    return hexValue


def hasher(target):
    sha_signature = \
        hashlib.sha256(target.encode()).hexdigest()
    return sha_signature

while True:
    print(lineSeparator())
    hash_string = getpass.getpass()
    sha_signature = hasher(hash_string)
    pyperclip.copy(sha_signature)
    print(lineSeparator())
    print(hexPrinter(sha_signature))

import getpass
import hashlib
import shutil

import pyperclip

pass_string = None

def ts():
    return shutil.get_terminal_size()


def lineSeparator():
    return "━" * ts().columns


def printSplitter(inputString):
    i = 1
    endIndex = inputString.rindex(" ", 0, len(inputString))
    while True:
        lineIndex = inputString.rindex(" ", 0, (ts().columns * i))
        inputString = list(inputString)
        if lineIndex == endIndex:
            break
        else:
            inputString[lineIndex] = '\n'
            inputString = "".join(inputString)
        i = i + 1
    inputString = list(inputString)
    inputString.pop()
    inputString = "".join(inputString)
    return inputString


def hashPrinter(hashValue):
    i = 1
    endIndex = len(hashValue)
    while True:
        lineIndex = ts().columns * i
        hashValue = list(hashValue)
        if lineIndex >= endIndex:
            break
        else:
            hashValue.insert(lineIndex, '\n')
            hashValue = "".join(hashValue)
        i = i + 1
    hashValue = "".join(hashValue)
    return hashValue


def hasher(target):
    sha_signature = \
        hashlib.sha256(target.encode()).hexdigest()
    return sha_signature


def hashPass():
    global pass_string
    print(lineSeparator())
    pass_string = getpass.getpass()
    sha_signature = hasher(pass_string)
    pyperclip.copy(sha_signature)
    print(lineSeparator())
    print(hashPrinter(sha_signature))


def newPass():
    global pass_string
    while True:
        print(lineSeparator())
        pass_string = getpass.getpass()
        checkPass_string = getpass.getpass('Confirm Password: ')
        if checkPass_string != pass_string:
            print(lineSeparator())
            print(printSplitter("Password and confirmation do not match. "))
            continue
        sha_signature = hasher(pass_string)
        pyperclip.copy(sha_signature)
        print(lineSeparator())
        print(hashPrinter(sha_signature))
        break


def main():
    global pass_string
    while True:
        print(lineSeparator())
        mode = str(input(printSplitter(
            "Type \"1\" to get the hash of your password, \"2\" to create a new (hashed) password, \"plaintext\" to get the previous inputted password in plaintext form, \"clear\" to clear the program window and previously cached passwords, \"refresh\" to re-display the prompt (useful if you change the size of the program window), and \"quit\" to exit.\n:  ")))
        if mode == "1":
            hashPass()
        elif mode == "2":
            newPass()
        elif mode == "quit":
            print(printSplitter(" " * (ts().columns * ts().lines)))
            break
        elif mode == "plaintext":
            if pass_string != None:
                print(lineSeparator())
                print(pass_string)
            else:
                print(lineSeparator())
                print(printSplitter("No previous inputs. "))
                continue
        elif mode == "clear":
            try:
                pass_string = None
            except:
                pass
            print(printSplitter(" " * (ts().columns * ts().lines)))
            continue
        elif mode == "refresh":
            continue
        else:
            print(lineSeparator())
            print(printSplitter("Invalid option. "))
            continue


main()

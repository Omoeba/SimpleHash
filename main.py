import base64
import getpass
import hashlib
import os
import re
import shutil

import argon2
import numpy as np
import pyperclip

pass_string = None
savelist = None

savefile = os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.path.dirname(__file__))), 'savefile.npy')


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def ts():
    return shutil.get_terminal_size()


def cleanInput(inputString, mode="string"):
    if mode == "string":
        return re.sub(r'[^a-zA-Z0-9]', '', inputString)
    elif mode == "email":
        return re.sub(r'[^a-zA-Z0-9@.]', '', inputString)
    elif mode == "name":
        return re.sub(r'[^a-zA-Z]', '', inputString)


def lineSeparator():
    return "━" * ts().columns


def stringSplitter(inputString):
    outputString = ""
    while len(inputString) >= ts().columns:
        breakIndex = inputString.rindex(" ", 0, ts().columns)
        newString = inputString[:breakIndex] + '\n'
        inputString = inputString[breakIndex + 1:]
        outputString = outputString + newString
    outputString = outputString + inputString
    return outputString


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


def hasher(target, keyName, fullName, email):
    try:
        salt_len = 32 + len(target.decode())
        salt = hashlib.shake_256(keyName + fullName + email).digest(salt_len)
        sha_signature = base64.b64encode(
            argon2.low_level.hash_secret_raw(target, salt, argon2.DEFAULT_TIME_COST, argon2.DEFAULT_MEMORY_COST,
                                             argon2.DEFAULT_PARALLELISM, argon2.DEFAULT_HASH_LENGTH,
                                             argon2.low_level.Type.ID)).decode()
        return sha_signature
    except:
        raise ValueError


def hashPass():
    global pass_string
    while True:
        print(lineSeparator())
        print(stringSplitter("Type \"quit\" to exit."))
        print(lineSeparator())
        keyName = cleanInput(input("Key Name\n: ").lower())
        print(keyName)
        if keyName == "quit":
            break
        try:
            fullName = (base64.b64decode((np.load(savefile))[0])).decode()
            print(lineSeparator())
            print(stringSplitter("Name loaded from save file."))
        except:
            fullName = cleanInput(input("Your Name\n: ").lower(), "name")
            print(fullName)
            if fullName == "quit":
                break
        try:
            email = (base64.b64decode((np.load(savefile))[1])).decode()
            print(lineSeparator())
            print(stringSplitter("Email loaded from save file."))
            print(lineSeparator())
        except:
            email = cleanInput(input("Email\n: ").lower(), "email")
            print(email)
            if email == "quit":
                break
        pass_string = getpass.getpass()
        try:
            sha_signature = hasher(pass_string.encode(), keyName.encode(), fullName.encode(), email.encode())
            pyperclip.copy(sha_signature)
            print(lineSeparator())
            print(hashPrinter(sha_signature))
        except ValueError:
            print(lineSeparator())
            print(stringSplitter("Invalid Password."))
        break


def newPass():
    global pass_string
    global savelist
    helpInfo = stringSplitter("Password is case sensitive.") + '\n\n' + stringSplitter(
        "Key Name should be something easily recognizable, such as the name of the website or service you are "
        "using the generated password for; e.g. \"apple\" or \"gpg\". Key Name is case insensitive.") + '\n\n' + stringSplitter(
        "Name and email are optional and are an easy to remember way to make the resulting hash more random, "
        "thus more secure. No parts of your name or email will be obtainable by attackers attempting to crack the "
        "hash. Type \"save\" after creating a password to save your name and email to disk so you don't have to enter "
        "it again when getting the hash again. Name and email are case insensitive.") + '\n\n' + stringSplitter(
        "Type \"quit\" to exit and \"help\" to re-display the prompt.")
    while True:
        print(lineSeparator())
        print(helpInfo)
        print(lineSeparator())
        keyName = cleanInput(input("Key Name\n: ").lower())
        if keyName == "quit":
            break
        elif keyName == "help":
            continue
        try:
            fullName = (base64.b64decode((np.load(savefile))[0])).decode()
            print(lineSeparator())
            print(stringSplitter("Name loaded from save file."))
        except:
            fullName = cleanInput(input("Your Name\n: ").lower(), "name")
            print(fullName)
            if fullName == "quit":
                break
            elif fullName == "help":
                continue
        try:
            email = (base64.b64decode((np.load(savefile))[1])).decode()
            print(lineSeparator())
            print(stringSplitter("Email loaded from save file."))
            print(lineSeparator())
        except:
            email = cleanInput(input("Email\n: ").lower(), "email")
            print(email)
            if email == "quit":
                break
            elif email == "help":
                continue
        pass_string = getpass.getpass()
        checkPass_string = getpass.getpass('Confirm Password: ')
        if checkPass_string != pass_string:
            print(lineSeparator())
            print(stringSplitter("Password and confirmation do not match."))
            break
        try:
            sha_signature = hasher(pass_string.encode(), keyName.encode(), fullName.encode(), email.encode())
            savelist = [base64.b64encode(fullName.encode()).decode(), base64.b64encode(email.encode()).decode()]
            pyperclip.copy(sha_signature)
            print(lineSeparator())
            print(hashPrinter(sha_signature))
        except ValueError:
            print(lineSeparator())
            print(stringSplitter("Invalid Password"))
        break


def main():
    global pass_string
    global savelist
    global savefile
    while True:
        print(lineSeparator())
        mode = cleanInput(str(input(stringSplitter(
            "Type \"1\" to calculate and existing hash, \"2\" to create a new password hash, \"plaintext\" to get the "
            "previous inputted password in plaintext form, \"clear\" to clear the program window and previously "
            "cached passwords, \"refresh\" to re-display the prompt (useful if you change the size of the program "
            "window), \"delete\" to delete any saved name or email, and \"quit\" to exit.\n: "))).lower())
        if mode == "1":
            hashPass()
        elif mode == "2":
            newPass()
        elif mode == "quit":
            clear()
            break
        elif mode == "plaintext":
            if pass_string is not None:
                print(lineSeparator())
                print(hashPrinter(pass_string))
            else:
                print(lineSeparator())
                print(stringSplitter("No previous inputs."))
        elif mode == "clear":
            pass_string = None
            clear()
        elif mode == "refresh":
            pass
        elif mode == "save":
            if savelist is not None:
                print(lineSeparator())
                print(stringSplitter("Saving..."))
                np.save(savefile, savelist)
                print(stringSplitter("Success!"))
            else:
                print(lineSeparator())
                print(stringSplitter("Nothing to save yet..."))
        elif mode == "delete":
            try:
                print(lineSeparator())
                print(stringSplitter("Deleting..."))
                os.remove(savefile)
                print(stringSplitter("Done!"))
            except:
                print(stringSplitter("Nothing to delete."))
        else:
            print(lineSeparator())
            print(stringSplitter("Invalid option."))


main()

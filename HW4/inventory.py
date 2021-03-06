#!/usr/bin/env python2

from sys import stdin,stderr,exit
import fileinput
import argparse
from itertools import imap
import functions #import my functions

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-f', '--data-file',  metavar='file',
                    help="Data file path to read at startup")

args = parser.parse_args()

if __name__=='__main__':
    data = []
    outFile = args.data_file

    try:
        for line in fileinput.input(outFile):
            if not fileinput.isfirstline():
                temp = line.split(":")
                data.append([temp[0].strip(), temp[1].strip(),
                            temp[2].strip(), int(temp[3])])
    except IOError:
        stderr.write("'" + args.data_file + "' does not exist!\n")
        exit(2)

    while True:
        try:
            # Propmpt for a command
            linein = raw_input()
        except EOFError:    # ^D
            break   # Break out of while loop

        linein = linein.split()

        try:
            if linein[0] == "add": # Add
                data.append(functions.add_record(linein))
                print "Added"
            elif linein[0] == "remove": # Remove
                data = functions.remove_record(data, linein)
                print "Removed"
            elif linein[0] == "set": # Set
                data = functions.set_record(data, linein)
                print "Set"
            elif (linein[0], linein[1]) == ("list", "all"):
                if len(linein) > 2:
                    if linein[2] == "sort": # List all sort
                        data, linein = functions.sort_record(data, linein)
                        functions.list_record(data, linein)
                    else: # List all with
                        functions.list_record(data, linein)
                else: # List all
                    functions.list_record(data, linein)
            else: # No matching command with more than one argument
                stderr.write("Invalid command: " + linein[0] +
                             " " + linein[1] + "\n")
                exit(2)

            functions.toFile(data, outFile) # Update file
        except IndexError: # No matching command with only one argument
            stderr.write("Invalid command: " + linein[0] + "\n")
            exit(2)

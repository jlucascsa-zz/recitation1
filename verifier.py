#!/usr/bin/env python
import subprocess, os, sys, re

EXPECTED_ARRAY = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

EXPECTED_ANSWER = "The sum from 0 to 10 is 45."

def exitWithError(error):
    print error
    sys.exit(1)

def runAndCheckOutput():
    output = ""
    try:
        output = subprocess.check_output("./rollingsum")
    except subprocess.CalledProcessError as e:
        exitWithError("ERROR: runtime error with rollingsum")

    segments = output.strip().split('\n')

    try:
        actual = eval(segments[0])
        if actual != EXPECTED_ARRAY:
            exitWithError('ERROR: actual output: "%s", expected: "%s"' % (segments[0], str(EXPECTED_ARRAY)))
    except subprocess.CalledProcessError as e:
        exitWithError('ERROR: actual output: "%s", expected: "%s"' % (segments[0], str(EXPECTED_ARRAY)))

    if len(segments) >= 2: 
        if segments[1].strip() != EXPECTED_ANSWER:
            exitWithError('ERROR: actual output: "%s", expected: "%s"' % (segments[1].strip(), EXPECTED_ANSWER))
    else:
        print "Looks like you still need to add sum.c / sum.h, but otherwise it looks good."


def runMake():
    try:
        output = subprocess.check_output('make')
    except subprocess.CalledProcessError as e:
        exitWithError('ERROR: make failed')

def runMakeClean():
    try:
        output = subprocess.check_output(['make', 'clean'])
    except subprocess.CalledProcessError as e:
        exitWithError('ERROR: make clean failed')

print "Running verifying script ... "

print "\nChecking that the Makefile exists ... "
if not os.path.isfile('Makefile'):
    exitWithError('ERROR: Makefile does not exist.')
print "Good!"

print "\nChecking that the Makefile doesn't throw an error ... "
runMake()
print "Ok!"

print "\nChecking that the Makefile builds the rollingsum binary ... "
if not os.path.isfile('rollingsum'):
    exitWithError('ERROR: rollingsum binary missing, did you rename it?')
print "Cool!"

print "\nChecking output of rollingsum ... "
runAndCheckOutput()
print "Looks good!"

print "\nChecking 'make clean' ... "
runMakeClean()
if os.path.isfile('rollingsum') or 'main.o' in os.listdir('.'):
    exitWithError('ERROR: after make clean, binary files still exist (ex: rollingsum, main.o).')
print "Sweet!"

print "\nRunning one more time ... "
runMake()
runAndCheckOutput()
runMakeClean()
print "LGTM"

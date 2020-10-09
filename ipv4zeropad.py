#! /usr/bin/python3
#
# @(!--#) @(#) ipv4zeropad.py, version 007, 08-october-2020
#
# pad IPv4 addresses with leading zeroes so they sort correctly
#
# for example change:
#
# 172.28.1.8
# 172.28.1.13
# 172.28.1.200
#
# to:
#
# 172.028.001.008
# 172.028.001.013
# 172.028.001.200
#
# Links
#
#   https://excelribbon.tips.net/T013481_Sorting_IP_Addresses.html
#   https://theexceltrainer.co.uk/how-to-correctly-sort-ip-addresses-in-excel/
#   https://www.extendoffice.com/documents/excel/4946-excel-sort-ip-address.html
#

#################################################################

#
# imports
#

import sys
import os
import argparse
import html
import cgi
import cgitb; cgitb.enable()  # for troubleshooting

#################################################################

def errorpage(errormessage):
    print('Content-type: text/html')
    print('')
    print('</html>')
    print('<head>');
    print('<title>Unexpected error</title>')
    print('</head>');
    print('<body>')

    print('<h1>An unexpected error has occurred</h1>')

    print('<p>')
    print('This web page has encountered an error it cannot (currently) deal with.')
    print('</p>')

    print('<p>')
    print('This is the error message:')
    print('</p>')

    print('<pre>')
    print(html.escape(errormessage))
    print('</pre>')

    print('<p>')
    print('Try again as this may be a temporary error.')
    print('</p>')

    print('<p>')
    print('If the error keeps happening please contact:')
    print('</p>')

    print('<pre>')
    print('andy@cranstonhub.com')
    print('</pre>')

    print('<hr>')

    print('</body>')
    print('</html>')

    return

#################################################################

def unixbasename(filename, extension):
    lenfilename = len(filename)

    lenext = len(extension)

    if lenext < lenfilename:
        if filename[-lenext:] == extension:
            filename = filename[0:lenfilename-lenext]

    return filename

#################################################################

def printenv(envname):
    try:
        envvalue = os.environ[envname]
    except KeyError:
        envvalue = '<undefined>'

    if envvalue == '':
        envvalue = '<null>'

    print('Environment variable {}="{}"'.format(envname, envvalue))

    return

#################################################################

def safefilenamechars(filename):
    filename = filename.lower()

    safefilename = ''

    for c in filename:
        if c in '01234567890abcdefghijklmnopqrstuvwxyz':
            safefilename += c
        elif c in '._-':
            safefilename += c
        else:
            safefilename += '_'

    return safefilename

#################################################################

def uploadfilename(stem):
    try:
        docroot = os.environ['DOCUMENT_ROOT']
    except KeyError:
        return None

    try:
        remoteaddr = os.environ['REMOTE_ADDR']
    except KeyError:
        return None

    remoteaddr = safefilenamechars(remoteaddr)

    pid = os.getpid()

    fname = '{}/uploads/rawconfig_{}_{:05d}_{}'.format(docroot, remoteaddr, pid, stem)

    return fname

#################################################################

def readrawconfig(configfilename):
    global progname

    try:
        configfile = open(configfilename, 'r', encoding='utf-8')
    except IOError:
        print('{}: unable to open config file "{}" for reading'.format(configfilename), file=sys.stderr)
        return None

    config = {}

    linenumber = 0

    for line in configfile:
        linenumber += 1
        line = line.strip()
        if len(line) == 0:
            continue
        if line[0] == '#':
            continue

        equalsposition = line.find('=')

        if equalsposition == -1:
            print('{}: warning: line {} in config file "{}" does not contain an equals sign - ignoring'.format(progname, linenumber, configfilename), file=sys.stderr)
            continue

        key = line[0:equalsposition]
        value = line[equalsposition+1:]

        ### print('+++ {} +++ {} +++'.format(key, value))

        if key in config:
            print('{}: warning: the key "{}" in line {} in config file "{}" is a duplicate - ignoring'.format(progname, equalsposition, linenumber, configfilename), file=sys.stderr)
        else:
            config[key] = value

    configfile.close()

    return config
        
#################################################################

def compareconfigs(first, second):
    diffcount = 0

    # report keys in first config that are not on the second
    for key in first:
        if key not in second:
            diffcount += 1
            print('<div class="key">Key "{}" deleted</div>'.format(key))
            print('<div class="deleted">Old value = "{}"</div>'.format(first[key]))

    # report keys in second config that are not in the first
    for key in second:
        if key not in first:
            diffcount += 1
            print('<div class="key">Key "{}" added</div>'.format(key))
            print('<div class="added">New value = "{}"</div>'.format(second[key]))

    # report keys in both that have a different value
    for key in first:
        if key in second:
            if first[key] != second[key]:
                diffcount += 1
                print('<div class="key">Key "{}" changed</div>'.format(key))
                print('<div class="changed">Old value = "{}"</div>'.format(first[key]))
                print('<div class="changed">New value = "{}"</div>'.format(second[key]))

    if diffcount == 0:
        print('<div class="nodifference">No differences found</div>')
    else:
        print('<br>')
        print('<div class="endcomparison">End of comparison report</div>')

    return 

#################################################################

# determine if a string represents a valid IPv4 address

def validipv4(ipv4address):
    l = len(ipv4address)

    if l < 7:
        return False

    if l > 15:
        return False

    for c in ipv4address:
        if (not c.isdigit()) and (c != '.'):
            return False

    if not ipv4address[0].isdigit():
        return False

    if not ipv4address[-1].isdigit():
        return False

    if ipv4address.count('.') != 3:
        return False

    if '..' in ipv4address:
        return False

    octets = ipv4address.split('.')

    if len(octets) != 4:
        return False

    for octet in octets:
        l = len(octet)

        if l < 1:
            return False

        if l > 3:
            return False

        if l >= 2:
            if octet[0] == '0':
                return False

        for c in octet:
            if not c.isdigit():
                return False

        if int(octet) > 256:
            return False

    return True

#################################################################

# pad out a valid IPv4 address

def padipv4(ipv4address):
    padded = '999.999.999.999'

    octets = ipv4address.split('.')

    if len(octets) == 4:
        o1 = int(octets[0])
        o2 = int(octets[1])
        o3 = int(octets[2])
        o4 = int(octets[3])

        padded = '{:03d}.{:03d}.{:03d}.{:03d}'.format(o1, o2, o3, o4)

    return padded

#################################################################

def main():
    title = 'Pad IPv4 addresses with leading zeroes'

    scriptname = os.path.basename(sys.argv[0])

    cssname = unixbasename(scriptname, '.py') + '.css'

    form = cgi.FieldStorage(encoding="utf-8")
   
    zeropad = form.getfirst('zeropad', '')

    ipv4addresses = form.getfirst('ipv4addresses', '')

    print('Content-type: text/html; charset=utf-8')
    print('')

    print('<!doctype html>')

    print('<html>')

    print('<head>');

    print('<title>{}</title>'.format(html.escape(title)))

    print('<meta charset="utf-8">')

    print('<link rel="stylesheet" type="text/css" href="{}">'.format(cssname))

    print('</head>');

    print('<body>')

    print('<h1>{}</h1>'.format(html.escape(title)))

    print('<p class="instructions">')
    print('Paste IPv4 addresses into the input box on the left and:')
    print('</p>')

    ### print('<pre>')
    ### print(scriptname)
    ### print(cssname)
    ### print(ipv4addresses)
    ### print('</pre>')

    print('<form accept-charset="UTF-8" method="post" action="{}">'.format(scriptname))

    print('<input type="submit" name="zeropad" value="Click to zero pad the IPv4 addresses">')

    print('<p class="instructions">')
    print('then the padded addresses can be copied from the input box on the right.')
    print('</p>')

    print('<textarea class="textareaone" name="ipv4addresses" rows="16" cols="24">', end='')

    if len(ipv4addresses) != 0:
        print(html.escape(ipv4addresses), end='')

    print('</textarea>')

    print('<textarea class="textareatwo" readonly name="readonly" rows="16" cols="24">', end='')

    if zeropad != '':
        for line in ipv4addresses.split('\n'):
            line = line.strip()

            if validipv4(line):
                print(padipv4(line))
            else:
                if line == '':
                    print('')
                else:
                    print('*** {} ***'.format(html.escape(line)))

    print('</textarea>')

    print('</form>')

    print('<hr>')

    print('</body>')

    print('</html>')

    return 0

#################################################################

sys.exit(main())

# end of file

#!/usr/bin/env python

#########################
#
#  System level VPN script.
#
#  Intended to initiate a computer based VPN connection to SU campus when
#  possible. Watches for network connection, and once available script uses
#  AD computer object credentials to authenticate.
#
#  Tim Schutt, Syracuse University.
#  taschutt@syr.edu
#  June, 2016
#
#########################

import subprocess, os, socket, urllib2
import settings
from time import sleep

on = False

# search for exact name of VPN connection
# tolerant of situations like "vpn name 1" etc.
def findVpnName(searchTerm):
    cmd_findVPN = ['/usr/sbin/scutil', '--nc', 'list']
    exec_findVPN = subprocess.Popen(cmd_findVPN, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (vpnResultName, error) = exec_findVPN.communicate()
    for line in vpnResultName:
        if (searchTerm in vpnResultName):
            pieces = vpnResultName.split('"')[1]
    # print pieces
    return pieces

# check if network is active
def networkState(testHostAddress):
    try:
        host = socket.gethostbyname(testHostAddress)
        s = socket.create_connection((host, 443), 2)
        return True
    except:
        pass
    return False

# check if machine is on the campus network
# custom SU server which will respond differently based on client IP address
def campusNetworkState():
    return urllib2.urlopen("http://dainside.ad.syr.edu").read()

# look up AD computer object name
def lookupComputerObject():
    cmd_adComputerObjectLookup = ['/usr/sbin/dsconfigad', '-show']
    exec_adComputerObjectLookup = subprocess.Popen(cmd_adComputerObjectLookup, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (adComputerObj, trash) = exec_adComputerObjectLookup.communicate()
    for line in adComputerObj.splitlines():
        if ("Computer Account" in line):
            pieces = line.split()
            #print pieces
    return pieces[-1]

# check VPN status - returns "Disconnected", "Connecting", and "Connected" states
def checkVPNStatus(vpnName):
    print "VPN Name = " + vpnName
    cmd_checkVpnState = ['/usr/sbin/scutil', '--nc', 'status', vpnName]
    exec_checkVpnState = subprocess.Popen(cmd_checkVpnState, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (vpnStatusOutput, trash) = exec_checkVpnState.communicate()
    return vpnStatusOutput.splitlines()[0]

# look up computer object password from System keychain
def computerObjPass(computerName):
    cmd_lookupCompObjPass = ['/usr/bin/security', 'find-generic-password', '-wa', computerName ]
    exec_lookupCompObjPass = subprocess.Popen(cmd_lookupCompObjPass, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (compObjPass, trash) = exec_lookupCompObjPass.communicate()
    return compObjPass

def main(on):
    if (networkLocation != "Direct Access Inside"):
        if (checkVPNStatus(connectionName) == "Disconnected"):
            adName = lookupComputerObject()
            adPass = computerObjPass(adName)
            # print "AD Name = " + adName
            # print "AD Pass = " + adPass
            cmd_connectVPN = ['/usr/sbin/scutil', '--nc', 'start', connectionName, '--user', adName, '--password', adPass, '--secret', settings.sharedSecret]
            exec_connectVPN = subprocess.Popen(cmd_connectVPN, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (vpnresult, trash) = exec_connectVPN.communicate()
            # print vpnresult
            # print trash
            return False

        elif (checkVPNStatus(campusVPN) == "Connecting"):
            print "Waiting for VPN to connect..."
            sleep(5)
            return False

    else:
        if (on == False):
            print "We're on the campus network."
            return True

if __name__ == '__main__':
    connectionName = findVpnName(settings.campusVPN)
    networkLocation = campusNetworkState();
    # print "Network Location: " + networkLocation ## error checking
    while True:
        if (networkState(settings.testHostAddress)):
            on = main(on)
            sleep(10)
        else:
            print "There is no active connection to the internet."
            sleep(10)
            on = main(on)

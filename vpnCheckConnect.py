#!/usr/bin/env python

import subprocess, os, socket

import settings.py

# check if network is active
def networkState():
    try:
        host = socket.gethostbyname("da.ad.syr.edu")
        s = socket.create_connection((host, 443), 2)
        return True
    except:
        pass
    return False

# check if machine is on the campus network
def campusNetworkState():
    cmd_checkCampusNet = ['curl', 'http\://dainside.ad.syr.edu']
    exec_checkCampusNet = subprocess.Popen(cmd_checkCampusNet, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (campusNetState, trash) = exec_checkCampusNet.communicate()
    return campusNetState

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
    cmd_checkVpnState = ['/usr/sbin/scutil', '--nc', 'status', 'SU VPN']
    exec_checkVpnState = subprocess.Popen(cmd_checkVpnState, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (vpnStatusOutput, trash) = exec_checkVpnState.communicate()
    return vpnStatusOutput.splitlines()[0]

# look up computer object password from System keychain
def computerObjPass(computerName):
    cmd_lookupCompObjPass = ['/usr/bin/security', 'find-generic-password', '-wa', computerName ]
    exec_lookupCompObjPass = subprocess.Popen(cmd_lookupCompObjPass, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (compObjPass, trash) = exec_lookupCompObjPass.communicate()
    return compObjPass


if (networkState()):
    if (campusNetworkState() != "Direct Access Inside"):
        if (checkVPNStatus(campusVPN) == "Disconnected"):
            adName = lookupComputerObject()
            adPass = computerObjPass(adName)
            print "AD Name = " + adName
            print "AD Pass = " + adPass
            cmd_connectVPN = ['/usr/sbin/scutil', '--nc', 'start', 'SU VPN', '--user', adName, '--password', adPass, '--secret', sharedSecret]
            cmd_connectVPN
            exec_connectVPN = subprocess.Popen(cmd_connectVPN, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (vpnresult, trash) = exec_connectVPN.communicate()
            print vpnresult
            print trash

        elif (checkVPNStatus(campusVPN) == "Connecting"):
            print "Waiting for VPN to connect..."
    else:
        print "We're already on the campus network."
else:
    print "We're offline - can not connect to the campus network."

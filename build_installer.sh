#!/bin/bash

# construct the virtual root and script directories.
mkdir -p root/usr/local/SystemVPN_AD
mkdir -p root/Library/LaunchDaemons
mkdir scripts

# copy the items into the appriate locations and create the postinstall script
# to load the launch daemon

cp vpnCheckConnect.py root/usr/local/SystemVPN_AD/
cp edu.syr.ad.vpnconnect.plist root/Library/LaunchDaemons/
echo "#!/bin/bash\nlaunchctl load -w /Library/LaunchDaemons/edu.syr.vpnconnect.plist\nexit 0" > scripts/postinstall

# ensure execution bits are set
chmod +x root/usr/local/SystemVPN_AD
chmod +x scripts/postinstall

# create the install package
pkgbuild --root ./root \
--scripts ./scripts \
--identifier edu.syr.ad.vpnconnect \
--version 1.0 \
--filter "\.DS_Store" \
vpnCheckConnect.pkg

# clean up yer stuff.
rm -Rf ./root
rm -Rf ./scripts

exit 0

#!/bin/bash

mkdir -p root/usr/local/SystemVPN_AD
mkdir -p root/Library/LaunchDaemons
mkdir scripts
cp vpnCheckConnect.py root/usr/local/SystemVPN_AD/
cp edu.syr.ad.vpnconnect.plist root/Library/LaunchDaemons/
echo "#!/bin/bash\nlaunchctl load -w /Library/LaunchDaemons/edu.syr.vpnconnect.plist\nexit 0" > scripts/postinstall
chmod +x root/usr/local/SystemVPN_AD
chmod +x scripts/postinstall
pkgbuild --root ./root --scripts ./scripts --identifier edu.syr.ad.vpnconnect --version 1.0 --filter "\.DS_Store" vpnCheckConnect-1.0.pkg

rm -Rf ./root
rm -Rf ./scripts

exit 0

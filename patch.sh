mount -o remount,rw /
cp ./patch/autostart /etc_org/xdg/openbox/autostart
cp ./patch/rc.local /etc_org/rc.local
/sbin/hwclock -w -f /dev/rtc
chmod +x /opt/welarfid/patch/check_process.sh
rm -rf /opt/welarfid/images
rm /opt/welarfid/rfid.sqlite
echo "DONE"
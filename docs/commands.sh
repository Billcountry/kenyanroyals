cd ~/Downloads/
echo "Do not disconnect from the internet till you see the message 'everything is done'"
echo "Updating packages, please wait..."
sudo apt update>fist-update.txt
echo "Removing unwanted packages"
sudo apt autoremove -y>auto-remove.txt
echo "Checking for a new release and upgrading"
sudo do-release-upgrade>release-upgrade.txt
echo "Checking for new packages for the new release"
sudo apt update>second-update.txt
echo "Upgrading distribution"
sudo apt dist-upgrade -y>dist-upgrade.txt
echo "Everything is done."
echo "Nitumie the files: "
echo "1. first-update.txt"
echo "2. second-update.txt"
echo "3. auto-remove.txt"
echo "4. release-upgrade.txt"
echo "5. dist-upgrade.txt"
echo "Ziko kwa downloads. Tuma whatsapp or mailto:billcountrymwaniki@gmail.com"
echo "Have anice day"


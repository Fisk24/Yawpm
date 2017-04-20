#! /bin/bash

export INSTALL="/opt/Yawpm"

echo "Yawpm will now attempt to update itself"
echo
echo "Would you like to install dependencies? (y/n): "
# Optionaly update dependencies
read opt
if [[ $opt == "y" ]]; then
	echo "Updating dependicies..."
	sudo pacman -S python-pyqt4 wine-staging winetricks
elif [[ $opt == "n" ]]; then
	echo "Skipping dependency update..."
else
	echo "Unknown answer \"$opt\": Update Cancled!"
	exit
fi

# Remove existing install inorder to makeway for the most upto date version
rm -R $INSTALL

# Create installation directory; CD into it; Finally, git clone into the install directory
mkdir $INSTALL
cd "/opt"

# Download yawpm
git clone https://github.com/Fisk24/Yawpm.git

# create launcher
cp Yawpm/yawpm.desktop /usr/share/applications/yawpm.desktop

echo "Finished!"
echo "I recommend installing mscorefonts: (Arch) yaourt ttf-ms-fonts"

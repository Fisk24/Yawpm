#! /usr/bin/bash

export INSTALL="/opt/Yawpm"

# create launcher
cp yawpm.desktop /usr/share/applications/yawpm.desktop

# Remove existing install inorder to makeway for the most upto date version
rm -R $INSTALL

# Create installation directory; CD into it; Finally, git clone into the install directory
mkdir $INSTALL
cd "/opt"

sudo pacman -S python-pyqt4 wine winetricks
git clone https://github.com/Fisk24/Yawpm.git


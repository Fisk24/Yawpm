#! /usr/bin/bash

export INSTALL="/opt/Yawpm"

# Remove existing install inorder to makeway for the most upto date version
rm -R $INSTALL

# Create installation directory; CD into it; Finally, git clone into the install directory
mkdir $INSTALL
cd "/opt"

git clone  

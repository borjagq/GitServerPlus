#!/bin/sh

# Remove the previous one.
rm GitServerPlus.spk

# Create a package.tgz file containing the package folder and files.
cd ./GitServerPlus/package
tar -cvzf ../package.tgz --exclude='.DS_Store' --exclude='.git' *

# Create the SPK file.
# Prevent the package folder and files to be included in the SPK, as they are already in the TGZ.
cd ..
tar -cvf ../GitServerPlus.spk --exclude='package' --exclude='.DS_Store' --exclude='.git' *

# Delete the temp TGZ.
rm ./package.tgz

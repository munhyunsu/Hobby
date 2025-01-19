#!/bin/bash
cd "$(dirname "$0")"

TARGET_DIR=.
TARGET_SIZE=512x512
TARGET_PATH=$TARGET_DIR/AppIcon-512x512.png
convert AppIcon.png -resize $TARGET_SIZE $TARGET_PATH

mkdir -p android/app/src/main/res

TARGET_DIR=android/app/src/main/res/mipmap-hdpi
TARGET_SIZE=72x72
mkdir -p $TARGET_DIR
TARGET_PATH=$TARGET_DIR/ic_launcher.png
convert AppIcon.png -resize $TARGET_SIZE $TARGET_PATH

TARGET_DIR=android/app/src/main/res/mipmap-mdpi
TARGET_SIZE=48x48
mkdir -p $TARGET_DIR
TARGET_PATH=$TARGET_DIR/ic_launcher.png
convert AppIcon.png -resize $TARGET_SIZE $TARGET_PATH

TARGET_DIR=android/app/src/main/res/mipmap-xhdpi
TARGET_SIZE=96x96
mkdir -p $TARGET_DIR
TARGET_PATH=$TARGET_DIR/ic_launcher.png
convert AppIcon.png -resize $TARGET_SIZE $TARGET_PATH

TARGET_DIR=android/app/src/main/res/mipmap-xxhdpi
TARGET_SIZE=144x144
mkdir -p $TARGET_DIR
TARGET_PATH=$TARGET_DIR/ic_launcher.png
convert AppIcon.png -resize $TARGET_SIZE $TARGET_PATH

TARGET_DIR=android/app/src/main/res/mipmap-xxxhdpi
TARGET_SIZE=192x192
mkdir -p $TARGET_DIR
TARGET_PATH=$TARGET_DIR/ic_launcher.png
convert AppIcon.png -resize $TARGET_SIZE $TARGET_PATH


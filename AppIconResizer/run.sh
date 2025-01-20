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


mkdir -p ios/Runner/Assets.xcassets/AppIcon.appiconset

TARGET_DIR=ios/Runner/Assets.xcassets/AppIcon.appiconset
TARGET_SIZE=20x20
mkdir -p $TARGET_DIR
TARGET_PATH=$TARGET_DIR/Icon-App-20x20@1x.png
convert AppIcon.png -resize $TARGET_SIZE $TARGET_PATH

TARGET_DIR=ios/Runner/Assets.xcassets/AppIcon.appiconset
TARGET_SIZE=40x40
mkdir -p $TARGET_DIR
TARGET_PATH=$TARGET_DIR/Icon-App-20x20@2x.png
convert AppIcon.png -resize $TARGET_SIZE $TARGET_PATH

TARGET_DIR=ios/Runner/Assets.xcassets/AppIcon.appiconset
TARGET_SIZE=60x60
mkdir -p $TARGET_DIR
TARGET_PATH=$TARGET_DIR/Icon-App-20x20@3x.png
convert AppIcon.png -resize $TARGET_SIZE $TARGET_PATH

TARGET_DIR=ios/Runner/Assets.xcassets/AppIcon.appiconset
TARGET_SIZE=29x29
mkdir -p $TARGET_DIR
TARGET_PATH=$TARGET_DIR/Icon-App-29x29@1x.png
convert AppIcon.png -resize $TARGET_SIZE $TARGET_PATH

TARGET_DIR=ios/Runner/Assets.xcassets/AppIcon.appiconset
TARGET_SIZE=58x58
mkdir -p $TARGET_DIR
TARGET_PATH=$TARGET_DIR/Icon-App-29x29@2x.png
convert AppIcon.png -resize $TARGET_SIZE $TARGET_PATH

TARGET_DIR=ios/Runner/Assets.xcassets/AppIcon.appiconset
TARGET_SIZE=87x87
mkdir -p $TARGET_DIR
TARGET_PATH=$TARGET_DIR/Icon-App-29x29@3x.png
convert AppIcon.png -resize $TARGET_SIZE $TARGET_PATH

TARGET_DIR=ios/Runner/Assets.xcassets/AppIcon.appiconset
TARGET_SIZE=40x40
mkdir -p $TARGET_DIR
TARGET_PATH=$TARGET_DIR/Icon-App-40x40@1x.png
convert AppIcon.png -resize $TARGET_SIZE $TARGET_PATH

TARGET_DIR=ios/Runner/Assets.xcassets/AppIcon.appiconset
TARGET_SIZE=80x80
mkdir -p $TARGET_DIR
TARGET_PATH=$TARGET_DIR/Icon-App-40x40@2x.png
convert AppIcon.png -resize $TARGET_SIZE $TARGET_PATH

TARGET_DIR=ios/Runner/Assets.xcassets/AppIcon.appiconset
TARGET_SIZE=120x120
mkdir -p $TARGET_DIR
TARGET_PATH=$TARGET_DIR/Icon-App-40x40@3x.png
convert AppIcon.png -resize $TARGET_SIZE $TARGET_PATH

TARGET_DIR=ios/Runner/Assets.xcassets/AppIcon.appiconset
TARGET_SIZE=120x120
mkdir -p $TARGET_DIR
TARGET_PATH=$TARGET_DIR/Icon-App-60x60@2x.png
convert AppIcon.png -resize $TARGET_SIZE $TARGET_PATH

TARGET_DIR=ios/Runner/Assets.xcassets/AppIcon.appiconset
TARGET_SIZE=180x180
mkdir -p $TARGET_DIR
TARGET_PATH=$TARGET_DIR/Icon-App-60x60@3x.png
convert AppIcon.png -resize $TARGET_SIZE $TARGET_PATH

TARGET_DIR=ios/Runner/Assets.xcassets/AppIcon.appiconset
TARGET_SIZE=76x76
mkdir -p $TARGET_DIR
TARGET_PATH=$TARGET_DIR/Icon-App-76x76@1x.png
convert AppIcon.png -resize $TARGET_SIZE $TARGET_PATH

TARGET_DIR=ios/Runner/Assets.xcassets/AppIcon.appiconset
TARGET_SIZE=152x152
mkdir -p $TARGET_DIR
TARGET_PATH=$TARGET_DIR/Icon-App-76x76@2x.png
convert AppIcon.png -resize $TARGET_SIZE $TARGET_PATH

TARGET_DIR=ios/Runner/Assets.xcassets/AppIcon.appiconset
TARGET_SIZE=167x167
mkdir -p $TARGET_DIR
TARGET_PATH=$TARGET_DIR/Icon-App-83.5x83.5@2x.png
convert AppIcon.png -resize $TARGET_SIZE $TARGET_PATH

TARGET_DIR=ios/Runner/Assets.xcassets/AppIcon.appiconset
TARGET_SIZE=1024x1024
mkdir -p $TARGET_DIR
TARGET_PATH=$TARGET_DIR/Icon-App-1024x1024@1x.png
convert AppIcon.png -resize $TARGET_SIZE $TARGET_PATH


mkdir -p ios/Runner/Assets.xcassets/LaunchImage.imageset

TARGET_DIR=ios/Runner/Assets.xcassets/LaunchImage.imageset
TARGET_SIZE=40x40
mkdir -p $TARGET_DIR
TARGET_PATH=$TARGET_DIR/Icon-App-40x40@1x.png
convert AppIcon.png -resize $TARGET_SIZE $TARGET_PATH

TARGET_DIR=ios/Runner/Assets.xcassets/LaunchImage.imageset
TARGET_SIZE=80x80
mkdir -p $TARGET_DIR
TARGET_PATH=$TARGET_DIR/Icon-App-40x40@2x.png
convert AppIcon.png -resize $TARGET_SIZE $TARGET_PATH

TARGET_DIR=ios/Runner/Assets.xcassets/LaunchImage.imageset
TARGET_SIZE=120x120
mkdir -p $TARGET_DIR
TARGET_PATH=$TARGET_DIR/Icon-App-40x40@3x.png
convert AppIcon.png -resize $TARGET_SIZE $TARGET_PATH

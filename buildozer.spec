[app]
title = KidsVoc
package.name = kidsvoc
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,mp3,json,ttf
source.exclude_exts = 
source.include_patterns = assets/fonts/*, assets/images/*, assets/audio/*
source.exclude_dirs = 
source.main = main.py
icon.filename = assets/images/icon/appkidicon.png
version = 1.0
requirements = python3, kivy, kivy[base], pillow, arabic-reshaper, python-bidi, setuptools
orientation = portrait
fullscreen = 1
android.meta_data = android.max_aspect=2.1
android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.ndk_path = /home/myapp/Desktop/kidsvoc/.buildozer/android/platform/android-ndk-r27c
android.sdk_path = /home/myapp/Android/Sdk



[buildozer]
log_level = 2
warn_on_root = 1

[app_android]
android.sdk = 31
android.ndk = 27c
android.api = 31
android.arch = arm64-v8a
android.minapi = 21
android.ndk_api = 21

android.presplash_color = #000000
android.disable_dpi_scaling = 1


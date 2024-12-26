[app]
title = KidsVoc
package.name = kidsvoc
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,mp3,wav
source.exclude_exts = spec
source.include_patterns = assets/*
source.exclude_dirs = tests,docs
version = 1.0
requirements = python3,kivy
icon.filename = assets/images/icon/appkidicon.png
orientation = portrait
fullscreen = 1
android.api = 31
android.minapi = 21
android.sdk = /home/myapp/Android/Sdk
android.ndk = /home/myapp/Desktop/kidsvoc/.buildozer/android/platform/android-ndk-r27c
android.archs = armeabi-v7a,arm64-v8a
android.packaging_mode = standard
p4a.branch = stable
android.permissions = INTERNET

[buildozer]
log_level = 2
warn_on_root = 1

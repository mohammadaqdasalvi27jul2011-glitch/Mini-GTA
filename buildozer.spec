[app]
title = Mini GTA - 4K Edition
package.name = minigta
package.domain = org.minigta

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas
source.exclude_exts = spec

version = 1.0.0
requirements = python3,kivy,numpy,pygame

# Display settings
orientation = landscape
fullscreen = 1
android.api = 31
android.minapi = 21
android.ndk = 25b

# App permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.features = android.hardware.accelerometer

# Features
android.bootstrap = sdl2
android.accept_sdk_license = True

# App metadata
android.icon = assets/icon.png
android.presplash = assets/splash.png
android.presplash_lottie = 

# App features
android.features = android.hardware.accelerometer

# Build optimization
android.gradle_dependencies = 
android.add_src = 

# Permissions and features
android.permissions = INTERNET

p4a.dir = %(source.dir)s/../.buildozer/android/platform/build-{arch}/build/other_builds/python3/armeabi-v7a/python3
p4a.url = https://github.com/kivy/python-for-android/archive/develop.zip

[buildozer]
log_level = 2
warn_on_root = 1

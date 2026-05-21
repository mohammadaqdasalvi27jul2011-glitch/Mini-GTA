# Mini GTA - Google Play Store Deployment Guide

This guide explains how to prepare and publish Mini GTA to the Google Play Store.

## 📱 Prerequisites

Before publishing to Google Play Store, you need:

1. **Google Play Developer Account** - Sign up at https://play.google.com/console ($25 one-time fee)
2. **Buildozer** - Tool to convert Python/Pygame to Android APK
3. **Kivy Framework** - Mobile-friendly Python framework
4. **Java Development Kit (JDK)** - Required for APK compilation
5. **Android SDK** - Required for building Android apps

---

## 🔧 Step 1: Setup Development Environment

### Install Required Tools

```bash
# Install Buildozer and Kivy
pip install kivy
pip install buildozer
pip install cython

# On Ubuntu/Debian, also install dependencies
sudo apt-get install build-essential libssl-dev libffi-dev python3-dev
```

### Install Java Development Kit (JDK)

```bash
# Ubuntu/Debian
sudo apt-get install openjdk-11-jdk openjdk-11-jdk-headless

# macOS (with Homebrew)
brew install openjdk@11
```

---

## 📦 Step 2: Prepare Your Project for Mobile

### Create Mobile-Friendly Version

1. **Create `buildozer.spec` configuration:**

```bash
cd /path/to/Mini-GTA
buildozer init
```

2. **Edit `buildozer.spec` with these settings:**

```ini
[app]
title = Mini GTA
package.name = minigta
package.domain = com.example

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas

version = 1.0

requirements = python3,kivy,numpy

orientation = landscape
fullscreen = 1
android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.features = android.hardware.accelerometer
android.api = 31
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
```

---

## 🏗️ Step 3: Build the APK

### Debug Build (for testing)

```bash
buildozer -v android debug
```

This creates an APK in `bin/minigta-1.0-debug.apk`

### Release Build (for Play Store)

```bash
buildozer -v android release
```

This creates an AAB (Android App Bundle) for Play Store submission.

---

## 🧪 Step 4: Test on Android Device

1. **Connect your Android device via USB**
2. **Install the debug APK:**

```bash
adb install bin/minigta-1.0-debug.apk
```

3. **Test all features thoroughly:**
   - Player movement
   - Shooting mechanics
   - Vehicle controls
   - Police AI
   - Mission system
   - Screen rotation handling

---

## 📸 Step 5: Prepare Store Assets

Create these marketing materials:

### App Icon (512×512 PNG)
- Save as `assets/icon_512.png`
- Should match your game's visual style

### Feature Graphic (1024×500 PNG)
- Save as `assets/feature_graphic.png`
- Eye-catching header for store listing

### Screenshots (at least 2-4)
- Gameplay screenshots
- Resolution: 1080×1920 pixels (portrait) or 1920×1080 pixels (landscape)
- Show main features: open world, combat, vehicles, police

### Promotional Text

**Title (max 50 chars):**
```
Mini GTA - Open World Action Game
```

**Short Description (max 80 chars):**
```
Full-featured GTA-style open world game with combat, vehicles & missions
```

**Full Description:**
```
Mini GTA - 4K Edition: Experience a complete open-world action game built with Python!

🌍 FEATURES:
• 3000x2000 pixel explorable world
• Dynamic police system with 5-star wanted levels
• 3 vehicle types: cars, trucks, motorcycles
• 3 weapons: pistol, rifle, shotgun
• 25 AI NPCs with realistic behavior
• 3 mission types: kill targets, earn money, reach wanted levels
• Complete combat system with shooting mechanics
• High score tracking and statistics

🎮 GAMEPLAY:
• Move with WASD or arrow keys
• Shoot with mouse click
• Switch weapons with 1, 2, 3 keys
• Enter/exit vehicles with E key
• Pause with ESC

📊 TRACK YOUR PROGRESS:
• Money earned from eliminations
• Accuracy percentage
• Kill count
• Mission completion status
• High score leaderboard

Perfect for action game enthusiasts! Build your crime empire in this fully-featured GTA-style experience.

Made with Python & Pygame | Open Source | MIT License
```

---

## 🏪 Step 6: Upload to Google Play Store

### 1. Register as Developer

- Visit https://play.google.com/console
- Pay $25 registration fee
- Accept developer terms

### 2. Create New Application

1. Click "Create app"
2. Fill in app name: `Mini GTA`
3. Choose category: `Games > Action`
4. Select content rating: `Mature (17+)` (for violence/weapons)

### 3. App Details

**Filling out app store listing:**

- **Title:** Mini GTA - 4K Edition
- **Short description:** Full-featured open world action game
- **Full description:** (Use text from Step 5)
- **Category:** Games/Action
- **Content rating:** Mature
- **Privacy policy:** Link to your privacy policy (or create a simple one)

### 4. Upload App Bundle/APK

1. Navigate to "Release" section
2. Create new release
3. Upload your release APK or AAB file
4. Add release notes: "Initial release of Mini GTA"

### 5. Add Store Listing Assets

- Upload app icon (512×512 PNG)
- Upload feature graphic (1024×500 PNG)
- Upload 2-4 gameplay screenshots
- Upload promotional graphic (1024×1024 PNG)

### 6. Content Rating Questionnaire

Complete the IARC questionnaire:
- Violence: Yes (shooting mechanics)
- Mild violence: Yes
- Users interacting: No
- Alcohol/tobacco: No
- In-app purchases: No
- Ads: No

### 7. Target Audience

- Target age: 17+
- No ads
- No in-app purchases
- Single player

### 8. Pricing & Distribution

- Select "Free"
- Choose countries to distribute in
- Accept terms

### 9. Submit for Review

- Review all information
- Click "Submit"
- Wait for Google's review (usually 1-3 hours)

---

## ✅ After Publishing

### Monitor Your App

- Check Play Store Console daily
- Monitor crash reports
- Track user reviews and ratings
- Update with bug fixes

### Update Procedure

1. Increment version in `buildozer.spec`
2. Rebuild APK/AAB
3. Upload new version to Play Store
4. Submit for review

---

## 🔐 Privacy Policy Template

Create a simple privacy policy (save as `PRIVACY_POLICY.md`):

```markdown
# Privacy Policy

## Mini GTA

**Last Updated:** 2025

### Data Collection

Mini GTA does not collect, store, or transmit personal data.

### Local Storage

- Game saves are stored locally on your device
- High scores are saved to device storage only

### Permissions

The game requests:
- Network access (for future features)
- Accelerometer access (for device orientation)

### No Third-Party Sharing

We do not share data with third parties.

### Contact

For privacy concerns: [your email]
```

---

## ⚠️ Common Issues & Solutions

### Issue: Buildozer fails to compile

**Solution:**
```bash
# Clear previous builds
buildozer android clean

# Try again with verbose output
buildozer -v android debug
```

### Issue: APK is too large

**Solution:**
- Remove unused assets
- Compress images
- Use AAB instead of APK

### Issue: Game crashes on Android

**Common causes:**
- Incompatible Pygame code
- Missing imports in buildozer.spec
- Screen size/resolution mismatch
- Missing permissions

---

## 📱 Version Information

**Current Version:** 1.0.0
- Initial release
- Full game features
- Tested on Android 5.0+

---

## 🔗 Useful Resources

- [Kivy Documentation](https://kivy.org/doc/stable/)
- [Buildozer on GitHub](https://github.com/kivy/buildozer)
- [Google Play Console Help](https://support.google.com/googleplay/android-developer/)
- [Android Developer Guidelines](https://developer.android.com/docs)

---

## 📄 License

© 2025 Mohammad Aqdas Alvi - MIT License

---

**Ready to submit? Follow the steps above and launch Mini GTA to millions of Android users!** 🚀

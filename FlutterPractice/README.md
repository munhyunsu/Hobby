# `Flutter` Installation

1. Install requirements

- clang++

```bash
apt install clang cmake ninja-build pkg-config libgtk-3-dev liblzma-dev libstdc++-12-dev
# (Based Ubuntu 20.04) apt install clang cmake ninja-build pkg-config libgtk-3-dev liblzma-dev libstdc++-10-dev
```

- Android studio

  - Download Android SDK
  - Download Commandline tools
  - Setup `$PATH`

  ```bash
  if [ -d "$HOME/.local/share/Android-SDK" ] ; then
    ANDROID_HOME="$HOME/.local/share/Android-SDK"
    PATH="$ANDROID_HOME/platform-tools:$PATH"
    PATH="$ANDROID_HOME/cmdline-tools/latest/bin:$PATH"
  fi
  ```

2. Download `Flutter` SDK
  - [Flutter SDK Archive](https://docs.flutter.dev/release/archive)

3. SET `PATH` environment variable

```bash
if [ -d "$HOME/.local/share/flutter/bin" ] ; then
    PATH="$HOME/.local/share/flutter/bin:$PATH"
fi
```

4. Setup flutter configuration and accept licenses

```bash
flutter config --android-sdk ~/.local/share/Android-SDK/
flutter config --android-studio-dir ~/.local/share/android-studio/
flutter doctor --android-licenses
```

5. Check version

```bash
flutter --version
flutter precache
```

6. Upgrade version

```bash
flutter upgrade
```

7. Check doctor

```bash
flutter doctor
```

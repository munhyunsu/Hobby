# `Flutter` Installation

0. Install requirements

- clang++

```bash
apt install clang
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

1. Download `Flutter` SDK
  - [SDK Archive](https://docs.flutter.dev/release/archive)

2. SET `PATH` environment variable

```bash
if [ -d "$HOME/.local/share/flutter/bin" ] ; then
    PATH="$HOME/.local/share/flutter/bin:$PATH"
fi
```

3. Setup flutter configuration and accept licenses

```bash
flutter config --android-sdk ~/.local/share/Android-SDK/
flutter config --android-studio-dir ~/.local/share/android-studio/
flutter doctor --android-licenses
```

4. Check version

```bash
flutter --version
flutter precache
```

5. Upgrade version

```bash
flutter upgrade
```

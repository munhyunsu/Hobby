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

3. Check version

```bash
flutter --version
flutter precache
```

4. Upgrade version

```bash
flutter upgrade
```

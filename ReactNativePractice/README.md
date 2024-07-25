# Installation

## Download [node.js](https://nodejs.org/en/download/prebuilt-binaries)

```bash
wget https://nodejs.org/dist/v20.12.0/node-v20.12.0-linux-x64.tar.xz
tar -xvf node-v20.12.0-linux-x64.tar.xz
```

## Enable development and execution environment

```
source enable_environments.sh
```

## Disable or add React Native port

- It use 8081
- If other process use it, then 8082 (+1...)

# Metro use port 8081, If you want to change port

- `export RCT_MERTO_PORT=8082`
- [Reference](https://stackoverflow.com/questions/34431052/react-native-change-listening-port/63683065#63683065)
- `npx react-native start --port 8082`

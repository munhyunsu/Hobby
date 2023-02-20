# Simple OBS controller using WebSocket

## Preparation

1. Update OBS up-to-date

2. Tools - WebSocket Server Settings - **Check** Enable WebSocket server

3. Tools - WebSocket Server Settings - Show Connect Info

- `vi secret.py`

```python
ip = ''
port = 
password ''
```

4. **(Important)** Launch OBS

# `obs-control.py`

## Usage

```bash
python3 obs-control.py --job METHOD
```

```bash
python3 obs-control.py --job GetVersion
```

# `main_timered_record.py`

## Usage

```bash
python3 main_timered_record.py --minutes MINUTES
```

```bash
python3 main_timered_record.py --minutes MINUTES --audio_only
```

```bash
python3 main_timered_record.py --minutes 120 --audio_only
```

# References

- [Official OBS websocket information](https://github.com/obsproject/obs-websocket)
- [Official OBS websocket 5.1.0 protocol](https://github.com/obsproject/obs-websocket/blob/master/docs/generated/protocol.md)
- [simpleobsws](https://github.com/IRLToolkit/simpleobsws/tree/master)

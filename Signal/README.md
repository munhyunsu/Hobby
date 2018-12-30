# Signal propagation, catch, handler example

## BUG or Something
1. py3 subprocess.Popen('py3 xxx.py', shell=True)
2. SIGKILL (or SIGINT, etc.) has no effect
- Why?

## File explanation
- \_shell.py : bash-py3-bash-py3
- \_preexec\_fn.py : bash-py3-bash-py3
- \_new\_session.py : bash-py3 | init-py3

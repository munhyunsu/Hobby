#!/bin/bash

if [[ -n "${BASH_SOURCE[0]}" ]]; then
  SCRIPT_PATH="${BASH_SOURCE[0]}"
elif [[ -n "${(%):-%N}" ]]; then
  SCRIPT_PATH="${(%):-%N}"
else
  echo "Unsupported shell. Please use bash or zsh."
  return 1
fi

DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"

export OLD_PATH=$PATH
export OLD_PS1=$PS1

export PATH=${DIR}/.nodejs/bin:${PATH}
export PS1="(.nodejs) $PS1"

deactivate() {
    export PATH=$OLD_PATH
    export PS1=$OLD_PS1
    unset OLD_PATH
    unset OLD_PS1
    unset -f deactivate
}

echo "Environment activated. Use 'deactivate' to revert."


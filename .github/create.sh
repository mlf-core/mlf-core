#!/usr/bin/env bash
set -e

case "$1" in

  pytorch)
    echo -e "\n\n\n\n\nn\n\n\n\nn" | poetry run mlf-core create
    ;;

  tensorflow)
    echo -e "\n\033[B\n\n\n\nn\n\n\n\nn" | poetry run mlf-core create
    ;;

  xgboost)
    echo -e "\n\033[B\033[B\n\n\n\nn\n\n\n\nn" | poetry run mlf-core create
    ;;

  *)
    echo -n "unknown"
    ;;
esac

#!/bin/bash

SCREEN_NAME="minecraft_server"

RUN_SCRIPT="./run.sh"

CHECK_INTERVAL=90

while true; do
    if screen -list | grep -q "$SCREEN_NAME"; then
        echo "$(date): El servidor sigue en ejecución."
    else
        echo "$(date): El servidor se ha detenido. Reiniciando..."
        
        screen -S "$SCREEN_NAME" -dm bash -c "$RUN_SCRIPT"
        
        if screen -list | grep -q "$SCREEN_NAME"; then
            echo "$(date): El servidor se ha reiniciado correctamente."
        else
            echo "$(date): Error al intentar reiniciar el servidor."
        fi
    fi
    
    sleep $CHECK_INTERVAL
done

#!/bin/bash

ps -a | grep 'python' | awk '{print $1}' | xargs sudo kill -9

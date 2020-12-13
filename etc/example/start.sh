#!/bin/bash

source activate
pm2 start etc/daemon.config.yml

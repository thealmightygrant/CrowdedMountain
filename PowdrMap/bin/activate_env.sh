#!/bin/bash

PROJECT_NAME=CrowdedMountain
PROJECT_HOME=$HOME/$PROJECT_NAME/$PROJECT_NAME
WORKON_HOME=$PROJECT_HOME/env

function activate {
    source $PROJECT_HOME/env/bin/activate
} 

activate

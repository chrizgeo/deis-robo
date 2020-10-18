#!/bin/bash

lcm-gen -j example_t.lcm
javac -cp .:lcm.jar *.java exlcm/*.java



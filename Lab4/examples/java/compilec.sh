#!/bin/bash

lcm-gen -c example_t.lcm
gcc send_message.c exlcm_example_t.c -llcm -o send_message

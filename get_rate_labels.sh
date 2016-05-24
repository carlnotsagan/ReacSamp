#!/bin/bash
awk '{print $1}' ./starlib_raw_rates/rates_list.txt > 'rate_labels.txt'
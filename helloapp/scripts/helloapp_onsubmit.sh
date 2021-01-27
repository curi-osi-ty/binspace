#!/bin/bash

if [ $# -ne 1 ]
then
	echo Usage: $0 sample_path
fi

file $1/sample.bin > $1/sample_info.txt


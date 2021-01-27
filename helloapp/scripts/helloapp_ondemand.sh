#!/bin/bash

if [ $# -ne 1 ]
then
	echo Usage: $0 tool_folder_path
fi

# Assume a sample at $1/../sample.bin
echo "Beginning disassembling file" > $1/status.txt
objdump -D $1/../sample.bin > $1/output.txt
echo "Done" > $1/status.txt

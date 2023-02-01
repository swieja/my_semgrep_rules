#!/bin/bash

# Read the file name
file=$1

# Create a dictionary to store the word count
declare -A dict

# Read the file line by line
while read line; do
  # Split the line into words
  for word in $line; do
    # Increment the count of the word in the dictionary
    dict[$word]=$((dict[$word] + 1))
  done
done < $file

# Print the word count
for word in "${!dict[@]}"; do
  echo "$word: ${dict[$word]}"
done

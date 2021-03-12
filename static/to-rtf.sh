#!/usr/bin/env bash

cat $1 | curl -X POST -H "Content-Type: application/rtf" --data-binary  @- "https://mouseagreements.abreidenbach.com/convert" > $(basename $1 .md).rtf


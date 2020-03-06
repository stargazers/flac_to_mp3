# FLAC to MP3

## General

This script search FLAC files from given directory and convert those to mp3. Mostly this is meant to run in cron and poll directory for changes and automatically to convert new FLAC files to mp3 as well.

Paths can be configured directly to the script or use environment variables (see below for example).

## Requirements

Command line tools:
* FLAC
* LAME

## Environment variables

This app supports environment variables:

* FLAC_WATCHFOLDER
* MP3_OUTPUT_FOLDER

## Usage with environment variables

```FLAC_WATCHFOLDER=/home/stargazers/flac/ MP3_OUTPUT_FOLDER=/home/stargazers/mp3/ python3 flac_to_mp3.py```

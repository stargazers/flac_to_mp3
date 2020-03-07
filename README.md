# FLAC to MP3

## General

This script search FLAC files from given directory and convert those to mp3. Mostly this is meant to run in cron and poll directory for changes and automatically to convert new FLAC files to mp3 as well.

Paths can be configured directly to the script or use environment variables (see below for example).

By default we use LAME preset extreme.

## Requirements

Command line tools:
* FLAC
* LAME

## Environment variables

This app supports environment variables:

* FLAC_WATCHFOLDER
    * Path where we search for FLAC files
* MP3_OUTPUT_FOLDER
    * Path where we encode mp3 files
* LAME_PRESET
    * What LAME preset we want to use. If not given "extreme" is used.

## Usage with environment variables

```FLAC_WATCHFOLDER=/home/stargazers/flac/ MP3_OUTPUT_FOLDER=/home/stargazers/mp3/ LAME_PRESET=standard python3 flac_to_mp3.py```


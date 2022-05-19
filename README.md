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
* TEST_RUN
    * If we do not want to generate mp3 but instead see debugging infos etc.
* DO_NOT_USE_COVER_JPG
    * If album cover art is not found on FLAC metadata, we search album art from file in FLAC folder. Use this if you do NOT want to use images.
 * DEFAULT_ALBUM_ART_FILENAME
    * If we need to use external image file from FLAC folder, what filename we should use by default when looking for cover art file? By default this script search for cover-480x480.jpg. Reason for this filename is that Sandisk Mp3 player supports only images with 480x480 px size and I want to keep cover.jpg as big as I find but on mp3 I want to use smaller cover file if that exists in FLAC path.
## Usage with environment variables

```FLAC_WATCHFOLDER=/home/stargazers/flac/ MP3_OUTPUT_FOLDER=/home/stargazers/mp3/ LAME_PRESET=standard python3 flac_to_mp3.py```


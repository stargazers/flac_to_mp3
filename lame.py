# #####################################
#   FLAC to MP3
# #####################################
from pathlib import Path
import os
import re
import subprocess

# #############################################
#   Configurations
# #############################################
# Where we look for FLAC files
flac_watchfolder = '/share2/Audio/flac_to_mp3/'
output_folder = '/share2/Audio/mp3/'

# Overdrive if file exists?
overdrive_existing_file = False

# Metadata what we want to keep
metadata_to_keep = ['Artist', 'Album', 'Title', 'Genre', 'Tracknumber', 'Date']
# #############################################

# ####################################
#   getMetadata
#   @param flac Flac filename
#   @return Dictionary
# ####################################
def getMetadata( flac ):    
    command = 'metaflac ' + str(flac)
    
    for val in metadata_to_keep:
        command = command + ' --show-tag="' + val + '"'
    
    command = command + ' --export-picture-to=' + os.path.dirname(flac) + '/temporary_coverart.jpg '    
    ret = subprocess.run([command], shell=True, stdout=subprocess.PIPE, universal_newlines=True)

    output = ret.stdout
    output = re.split('\n|=', output)
    values = list(filter(None, output))
    metadata = dict(zip(values[::2], values[1::2]))
    print ("Metadata we got: " + str(metadata))
    return metadata



print("****************************************")
print(" FLAC to MP3 conversion")
print("****************************************")
print()

for flac_filename in Path(flac_watchfolder).rglob('*.flac'):
    # Filename without path and extension
    base_filename = os.path.basename(os.path.splitext(flac_filename)[0])

    # Get subfolder structure when generate mp3 files to new path
    dirname = os.path.dirname(flac_filename) + '/'
    flac_subfolder = dirname.replace(flac_watchfolder, '')    
    mp3_output_folder = output_folder + flac_subfolder

    coverart_file = dirname + 'temporary_coverart.jpg'
    
    # Actual filename (with path) for mp3 file
    mp3_file = mp3_output_folder + base_filename + '.mp3'

    # Read metadata fields
    metadata = getMetadata(flac_filename)
    
    # Create metadata parameter for LAME
    lame_metadata_params = '--tt "' + metadata['TITLE'] + '"' \
                            + ' --ta "' + metadata['ARTIST'] + '"' \
                            + ' --tl "' + metadata['ALBUM'] + '"' \
                            + ' --ty "' + metadata['DATE'] + '"' \
                            + ' --tn "' + metadata['TRACKNUMBER'] + '"' \
                            + ' --ti "' + coverart_file + '"'
    lame_params = '--preset extreme ' + lame_metadata_params

    print ('Lame would be ')
    print(lame_metadata_params)
    
    print("Input FLAC file: " + str(flac_filename))
    print("Output MP3 file: " + str(mp3_file))
    print()

    # Make the path if it does not exists
    Path(mp3_output_folder).mkdir(parents=True, exist_ok=True)

    # If we don't want to override files, we must check if file exists already
    if overdrive_existing_file == False and Path(mp3_file).exists():
        print ("File " + mp3_file + " exists! Skipping this file generation..." + '\n\n')
        continue

    # Decode FLAC and pass it to LAME
    command = "flac --decode --stdout " + str(flac_filename) + " | lame " + lame_params + " - " + str(mp3_file)
    print("Executing command: " + command)    
    subprocess.run([command], shell=True)
    
    # Delete temporary cover art file
    os.remove(coverart_file)
    
    print('\n' * 3)
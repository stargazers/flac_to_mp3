# #####################################
#   FLAC to MP3
# #####################################
from pathlib import Path
import os
import subprocess

# Where we look for FLAC files
flac_watchfolder = '/share2/Audio/flac_to_mp3/'
output_folder = '/share2/Audio/mp3/'

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
    
    # Actual filename (with path) for mp3 file
    mp3_file = mp3_output_folder + base_filename + '.mp3'

    print("Input FLAC file: " + str(flac_filename))
    print("Output MP3 file: " + str(mp3_file))
    print()

    # Make the path if it does not exists
    Path(mp3_output_folder).mkdir(parents=True, exist_ok=True)

    # Decode FLAC and pass it to LAME
    command = "flac --decode --stdout " + str(flac_filename) + " | lame --preset extreme - " + str(mp3_file)
    print("Executing command: " + command)    
    subprocess.run([command], shell=True)    
    print('\n' * 3)
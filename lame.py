# #####################################
#   FLAC to MP3
# #####################################
from pathlib import Path
import os
import subprocess

# Where we look for FLAC files
flac_watchfolder = '/share2/Audio/flac_to_mp3/'
output_folder = '/share2/Aduio/mp3/'

for flac_filename in Path(flac_watchfolder).rglob('*.flac'):
    base = os.path.splitext(flac_filename)[0]
    mp3_file = base + '.mp3'
    flac_file = base + '.flac'        
    command = "flac --decode --stdout " + str(flac_file) + " | lame --preset extreme - " + str(mp3_file)
    
    print("Running command: " + command)
    subprocess.run([command], shell=True)    
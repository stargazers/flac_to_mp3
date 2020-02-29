# #####################################
#   FLAC to MP3
# #####################################
from pathlib import Path
import os
import re
import subprocess
import logging

# #############################################
#   Configurations
# #############################################
# Logging level
logging.basicConfig(level=logging.INFO)

flac_watchfolder = '/share2/Audio/flac_to_mp3/'
output_folder = '/share2/Audio/mp3/'

# Overdrive if file exists?
overdrive_existing_file = False

# Metadata what we want to keep
metadata_to_keep = ['ARTIST', 'ALBUM', 'TITLE', 'GENRE', 'TRACKNUMBER', 'DATE']
# #############################################


   
# ####################################
#   getMetadata
#   @param flac Flac filename
#   @return Dictionary
# ####################################
def getMetadata( flac ):    
    logging.info("Reading FLAC metadata from  " + str(flac))    
    command = 'metaflac "' + str(flac) + "\""
    
    for val in metadata_to_keep:
        command = command + ' --show-tag="' + val + '"'
    
    command = command + ' --export-picture-to=' + os.path.dirname(flac) + '/temporary_coverart.jpg '    
    logging.info("Command to fetch metadata: " + command)    
    ret = subprocess.run([command], shell=True, stdout=subprocess.PIPE, universal_newlines=True)

    output = ret.stdout
    output = re.split('\n|=', output)
    values = list(filter(None, output))
    metadata = dict(zip(values[::2], values[1::2]))

    # Be sure we have all required metadata values set
    for val in metadata_to_keep:
        if "val" not in metadata:
            metadata[val] = ""
    
    logging.info("Metadata we got: " + str(metadata))    
    return metadata



def infoScreen():
    logging.info("****************************************")
    logging.info(" FLAC to MP3 conversion")
    logging.info("****************************************")    



def checkWatchfolder():    
    for flac_filename in Path(flac_watchfolder).rglob('*.flac'):
        logging.info("Input FLAC file: " + str(flac_filename))
        # Filename without path and extension
        base_filename = os.path.basename(os.path.splitext(flac_filename)[0])        

        # Get subfolder structure when generate mp3 files to new path
        dirname = os.path.dirname(flac_filename) + '/'
        flac_subfolder = dirname.replace(flac_watchfolder, '')    
        mp3_output_folder = output_folder + flac_subfolder

        # Actual filename (with path) for mp3 file
        mp3_file = mp3_output_folder + base_filename + '.mp3'        
        logging.info("mp3 file to generate: " + mp3_file)

        # If we don't want to override files, we must check if file exists already
        if overdrive_existing_file == False and Path(mp3_file).exists():
            logging.warn("File " + mp3_file  + " exists. Not overwriting since overdrive_existing_file is False.")            
            continue

        # Where to store temporary coverart
        coverart_file = dirname + 'temporary_coverart.jpg'
        logging.info("coverart file to generate: " + coverart_file)
        
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
        logging.info("LAME parameters will be: " + lame_params)
                
        # Make the path if it does not exists
        Path(mp3_output_folder).mkdir(parents=True, exist_ok=True)

        # Decode FLAC and pass it to LAME
        command = "flac --decode --stdout \"" + str(flac_filename) + "\" | lame " + lame_params + " - \"" + str(mp3_file) + "\""
        logging.info("Generating mp3 with LAME from FLAC with this command: " + command)        
        subprocess.run([command], shell=True)
        
        # Delete temporary cover art file
        logging.info("Deleting coverart file: " + coverart_file)
        os.remove(coverart_file)                

infoScreen()
checkWatchfolder()
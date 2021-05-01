# Boxes/Atoms that are supported to parse:
ftyp  
mdat  
moov  
    mvhd  
    trak  
        tkhd  
        udta  
        tsel  

# Required dependencies/libraries:  
pip install pytz  
pip install -U get-video-properties  
Note: Windows command is: pip install -U get-video-properties --user  
Note: get-vedeo-properties is basically ffprobe

# How to run?  
./main.py "path_to_mp4_file"  

# Referenced Project: 
https://github.com/axiomatic-systems/Bento4.git  
https://github.com/DigiDNA/ISOBMFF/tree/master/ISOBMFF/source  
https://github.com/macmade/MP4Parse/tree/master/source  
https://github.com/sannies/mp4parser  

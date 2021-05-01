# Boxes/Atoms that are supported to parse:
The boxes are defined in ISO/IEC 14496-12:  
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

# Sample output:  
Using video from youtube under CC license: https://www.youtube.com/watch?v=-5CdAup0o-I&ab_channel=TeacupPuppiesKimsKennelUS   
![Sample Output1](/assets/images/sample_output1.png)
# Referenced Project: 
https://github.com/axiomatic-systems/Bento4.git  
https://github.com/DigiDNA/ISOBMFF/tree/master/ISOBMFF/source  
https://github.com/macmade/MP4Parse/tree/master/source  
https://github.com/sannies/mp4parser  

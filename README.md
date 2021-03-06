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
Using video from youtube under CC license:  
https://www.youtube.com/watch?v=-5CdAup0o-I&ab_channel=TeacupPuppiesKimsKennelUS     
![Sample Output1](/assets/images/SampleOutput/sample_output1.png)  
Test Video From:  
http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4    
![ElephantsDream1](/assets/images/SampleOutput/ElephantsDream.png)  
Test Video From:  
http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4  
![ForBiggerBlazes1](/assets/images/SampleOutput/ForBiggerBlazes.png)  
# Referenced Project: 
https://github.com/axiomatic-systems/Bento4.git - For BoxMaker(Ap4AtomFactory)  
https://github.com/DigiDNA/ISOBMFF/tree/master/ISOBMFF/source  
https://github.com/macmade/MP4Parse/tree/master/source  
https://github.com/sannies/mp4parser  
https://github.com/essential61/mp4analyser.git - For parsing bytes (struck.unpack())   

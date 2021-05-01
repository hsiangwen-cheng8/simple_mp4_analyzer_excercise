from mp4 import MP4File
import logging
import sys
from videoprops import get_video_properties
from videoprops import get_audio_properties

def main(path):
    if path.endswith('.mp4'):
        mp4file = MP4File(path)
        # The 8 boxes required to parse is lacking some information like codec
        # ... hence, a library that uses ffprobe is used...
        vedioProps = get_video_properties(path)
        audioProps = get_audio_properties(path)
        print('..................Summary..................')
        print('The file has a size of: ', mp4file.fsize)
        print('Major Brand: ', mp4file.boxes['ftyp'].box_info['major_brand'])
        print('Compatible Brands: ', mp4file.boxes['ftyp'].box_info['compatible_brands'])
        duration = mp4file.boxes['moov'].child_boxes['mvhd'].box_info['duration']/mp4file.boxes['moov'].child_boxes['mvhd'].box_info['timescale']
        print('Duration is (in seconds): ', duration)
        print('Appoximate bitrate is: ', mp4file.fsize*8/duration)
        print('...................Video...................')
        print('The codec for video: ' + vedioProps['codec_name'])
        if 'trak0' in mp4file.boxes['moov'].child_boxes:
            if mp4file.boxes['moov'].child_boxes['trak0'].child_boxes['tkhd'].box_info['volume'] == 0:
                print('The width for video: ' + str(mp4file.boxes['moov'].child_boxes['trak0'].child_boxes['tkhd'].box_info['width']))
                print('The height for video: ' + str(mp4file.boxes['moov'].child_boxes['trak0'].child_boxes['tkhd'].box_info['height']))
            else:
                print('The width for video: ' + str(mp4file.boxes['moov'].child_boxes['trak1'].child_boxes['tkhd'].box_info['width']))
                print('The height for video: ' + str(mp4file.boxes['moov'].child_boxes['trak1'].child_boxes['tkhd'].box_info['height']))
        print('The avg_frame_rate for video: ' + str(eval(vedioProps['avg_frame_rate'])))
        print('...................Audio...................')
        print('The codec for audio: ' + audioProps['codec_name'])
        print('The sample rate for audio: ' + audioProps['sample_rate'])
        print('The number of channels for audio: ' + str(audioProps['channels']))
        print('The bit_rate for audio: ' + audioProps['bit_rate'])
    else:
        logging.error('File format not supported')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Usage: main.py full_path_to_mp4_file')
        print('Make sure that the path is in Unix style')
        exit()
    if not sys.argv[1].endswith('.mp4'):
        print('Please enter valid mp4 file...')
    logger = logging.getLogger('mp4')
    # change this to true to enable logging
    logger.propagate = False
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', filename='log.log', filemode='w', level=logging.DEBUG)
    logger.debug('Started')
    main(sys.argv[1])

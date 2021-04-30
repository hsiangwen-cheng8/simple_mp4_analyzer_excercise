from mp4 import MP4File
import logging

def main():
    path = 'C:/Users/poilk/Videos/幸福触手可及/【ENG SUB】《幸福触手可及》第1集 周放宋凛共住酒店（主演：迪丽热巴、黄景瑜、张馨予、胡兵）｜Love Designer EP1 (720p_25fps_H264-128kbit_AAC).mp4'
    if path.endswith('.mp4'):
        mp4file = MP4File(path)
    else:
        logging.error('File format not supported')

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', filename='log.log', filemode='w', level=logging.DEBUG)
    logging.debug('Started')
    main()

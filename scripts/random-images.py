#!/usr/bin/env python
import argparse
import os
import shutil
import random
import urllib

def download_from_iorempixel(path, num=10, max_size=[1200,1200],random_size=True):
    """
        Download pictures from IOrempixel
        to be used for testing
        :param path The path to store the images, it is created if 
        it does not exist
        :param num the amount of pictures to download
        :param max_size The maximum size allowd for the picture
        :param random_size Allow the size of the pcitures to be generated randomly
    """
    min_size = [200,200]
    if not os.path.exists(path):
        os.makedirs(path)

    for i in range(num):
        if random_size:
            pic_size = [random.randint(min_size[0],max_size[0]), 
                        random.randint(min_size[1],max_size[1])]
        else:
            pic_size = max_size
        urllib.urlretrieve("http://lorempixel.com/{}/{}/".format(pic_size[0], pic_size[1]),
                           os.path.join(path,"ph_{}_{}.jpg".format(pic_size[0], pic_size[1])))

def remove_folder(path):
    """
    Remove folder if it exists
    :param path the path to the folfder to erase
    """
    if os.path.exists(path):
        shutil.rmtree(path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a folder with random pictures for testing')
    parser.add_argument('--dest',dest='destination', help='Destination folder for the test pictures', 
                        default=os.path.join(os.path.expanduser('~'),'.pipyframe/images/'))
    parser.add_argument('--num',dest='num', help='How many pictures to download', default=10, type=int)
    parser.add_argument('--random_size',dest='random_size', help='Allow random images size', type=bool,
                       default=True)
    parser.add_argument('--rem',dest='rem', help='Remove old folder if it exist', default=True, type=bool)
    args = parser.parse_args()
    if args.rem:
        remove_folder(args.destination)
    download_from_iorempixel(args.destination, num=args.num, random_size=args.random_size)

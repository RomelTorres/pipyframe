#!/usr/bin/env python

from collections import deque
from magic import Magic, MAGIC_MIME_ENCODING
from random import shuffle
import os

"""
    This class handles the picture buffer and its associated methods
"""

class PicBuffering:

    def __init__(self, buffer_limit=None):
        """ 
        Init function
        :param buffer_limit None to no limit or the limit
        """ 
        self.seen_picture = deque()
        self.next_picture = deque()
        self.buffer_limit = buffer_limit

   
    def add_to_seen(self, path, place='back'):
        """
            This function adds a watched picture to the stack
            :param path: The path to the seen picture
            :param place: either add at the 'front' or the 'back'
            of the queue
        """
        if self.buffer_limit is not None:
            if len(self.seen_picture) >= self.buffer_limit:
                # If the queue is full take out the last saved path
                self.seen_picture.popleft()
        # Add the picture to the queue, depending on the place
        if place == 'back':
            self.seen_picture.append(path)
        else:
            self.seen_picture.appendleft(path)
    
    def add_pics_to_seen(self, paths, place='front'):
        """
            This function adds several pictures to the seen queue
            :param place: either add at the 'front' or the 'back'
            of the queue
            :param paths: A list containing the path to the images seen
        """
        for path in paths:
            if path not in self.seen_picture:
                self.add_to_seen(path, place)

    def get_last_from_seen(self):
        """
            This function gets from the last picture from the last seen queue
            :return the last seen picture path
        """
        return self.seen_picture.popleft()
   
    def get_first_from_seen(self):
       """
            This function gets the first picture (in the queue) from the last seen picture
            queue
            :return The first picture in the queue
       """
       return self.seen_picture.pop()

    def get_next_picture(self,num=1):
        """ 
            This function returns the next num of pictures to be shown
            :param num The amount of pictures to be returned
            :return the next pictures 
        """
        pics = []
        for idx in range(num):
            try:
                pics.append(self.next_picture.pop())
            except IndexError:
                # It is used as cyclic queue, load the first pictures back to the next
                pics.append(self.get_first_from_seen())
        # Add back to 
        return pics

    def add_to_next(self, path, place='back'):
        """
            This function adds a picture to the next_picture queue
            :param path: the path to the picture
            :param place: either add at the 'front' or the 'back'
            of the queue
        """
        if path not in self.seen_picture:
            if self.buffer_limit is not None:
                if len(self.next_picture) >= self.buffer_limit:
                    # If the queue is full take out the last saved path
                    self.next_picture.popleft()
            # Check that this picture is not in the seen pictures
            if place == 'back':
                self.next_picture.append(path)
            else:
                self.next_picture.appendleft(path)

    def add_pics_to_next(self, paths, place= 'front'):
        """
            This function adds several pictures to the next queue
            :param place: either add at the 'front' or the 'back'
            of the queue
            :param paths: A list containing the path to the images seen
        """
        for path in paths:
            self.add_to_next(path, place)
    
    def add_from_folder(self, pathin, allow_shuffle=False):
        """
        Add images from a given folder to the next_picture queue
        :param path: The path to the folder
        """
        with Magic(flags=MAGIC_MIME_ENCODING) as mag:
            files = [os.path.join(path, file) for (path, dirs, files) in os.walk(pathin) 
                     for file in files if 'image' or 'video' in  mag.id_filename(file)]
        if allow_shuffle:
            shuffle(files)        
        for path in files:
            # Check that the new pictures are not in the next picture queue
            if path not in self.next_picture:
                self.add_to_next(path)




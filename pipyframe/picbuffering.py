#!/usr/bin/env python

from collections import deque
from random import shuffle
from PIL import Image
from imghdr import what
from kivy.core.window import Window
import os
import piexif

"""
    This class handles the picture buffer and its associated methods
"""

class PicBuffering:

    def __init__(self, buffer_limit=None, database=None):
        """
        Init function
        :param buffer_limit None to no limit or the limit
        :param The handler to the database being in use
        """
        self.seen_picture = deque()
        self.next_picture = deque()
        self.buffer_limit = buffer_limit
        self.database = database
   
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
        if place in 'back':
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

    def get_last_from_seen(self, num=1):

        """
            This function gets from the last picture from the last seen queue
            :return the last seen picture path
        """
        pics = []
        try:
            pics.append(self.seen_picture.pop())
        except IndexError:
            pics.append(None)
        return pics
   
    def get_first_from_seen(self):
       """
            This function gets the first picture (in the queue) from the last seen picture
            queue
            :return The first picture in the queue
       """
       return self.seen_picture.popleft()

    def get_next_picture(self,num=1):
        """ 
            This function returns the next num of pictures to be shown
            :param num The amount of pictures to be returned
            :return the next pictures 
        """
        pics = []
        for idx in range(num):
            try:
                pic = self.next_picture.popleft()
                pics.append(pic)
            except IndexError:
                # Add the already seen pictures back to the next picture queue
                self.next_picture = self.seen_picture
                # Have an empty queue again for the seen pics
                self.seen_picture = deque()
                pic = self.next_picture.popleft()
                pics.append(pic)
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
            if place in 'back':
                self.next_picture.append(path)
            else:
                self.next_picture.appendleft(path)

    def add_pics_to_next(self, paths, place='back'):
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
        # Get the files from the given folder and analyze if they are
        # images or not
        the_files = []
        for (path, dirs, files) in os.walk(pathin):
            for the_file in files:
                path_file = os.path.join(path, the_file)
                file_type = what(path_file)
                if file_type is not None:
                    self._resize_picture(path_file)
                    the_files.append(path_file)
        # shuffle if requested
        if allow_shuffle:
            shuffle(the_files)
        for path in the_files:
            # Check that the new pictures are not in the next picture queue
            if path not in self.next_picture:
                # If a database has been given, add it to it
                if self.database is not None:
                    blacklisted = True if self.database.is_pic_blisted(path) else False
                    if not blacklisted:
                        self.database.add_picture_to_db(path, os.path.splitext(path)[1])
                self.add_to_next(path)

    def _find_optimal_size(self, path):
        """
            Find the optimal size for an image
        """
        image = Image.open(path)
        width, height = image.size
        exit = False
        step = 0.95
        if (width > Window.width) or (height > Window.height):
            # Image is bigger than the screen we want to desplay it in
            new_width = width
            new_height = height
            while(exit == False):
                # TODO quite slow, can be better
                if ((new_width > Window.width) or (new_height > Window.height)):
                    new_width =new_width*step
                    new_height = new_height*step
                else:
                    exit = True
            return [int(new_width),int(new_height)]
        else:
            return image.size

    def _resize_picture(self, path):
        """
            Resize a picture saving its exif info
            :param path the image's path
        """ 
        image = Image.open(path)
        try:
            exif_dict = piexif.load(image.info["exif"])
        except Exception:
            exif_dict = None
        width, height = image.size
        #So that we don't resize all the time
        if (width > Window.width) or (height > Window.height):
            new_size = self._find_optimal_size(path)
            # This does a resize of the picture and saves it with that name, 
            # TODO: add a setting where we store this pictures resized somewhere
            # as to not damage original data
            file_type = what(path)
            image.thumbnail(new_size, Image.ANTIALIAS)
            if exif_dict:
                """
                if piexif.ImageIFD.Orientation in exif_dict["0th"]:
                    print('Rotating image')
                    orientation = exif_dict["0th"].pop(piexif.ImageIFD.Orientation)
                    if orientation == 2:
                        image = image.transpose(Image.FLIP_LEFT_RIGHT)
                    elif orientation == 3:
                        image = image.rotate(180)
                    elif orientation == 4:
                        image = image.rotate(180).transpose(Image.FLIP_LEFT_RIGHT)
                    elif orientation == 5:
                        image = image.rotate(-90).transpose(Image.FLIP_LEFT_RIGHT)
                    elif orientation == 6:
                        image = image.rotate(-90)
                    elif orientation == 7:
                        image = image.rotate(90).transpose(Image.FLIP_LEFT_RIGHT)
                    elif orientation == 8:
                        image = image.rotate(90)"""
                exif_bytes = piexif.dump(exif_dict)
                image.save(path,file_type, exif=exif_bytes)
            else:
                image.save(path,file_type)

    def remove_blacklisted(self, path):
        """
            This function removes a blacklisted figure from the database and from the 
            queues
            :param path the image's path
            :returns True if removed, false if not present in any of the queues
        """
        # First blacklist it in the database
        self.database.blacklist_pic(path)
        # Trye removing it from the internal queues
        try:
            # Try removing it from the seen queue
            self.seen_picture.remove(path)
            return True
        except ValueError:
            pass
        try:
            self.next_picture.remove(path)
            return True
        except ValueError:
            pass
        # Ig you get until here the picture has never been in the queue
        return False

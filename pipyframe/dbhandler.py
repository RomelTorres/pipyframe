from tinydb import TinyDB, Query
import os

class DbPicture(object):
    """
        This class represents a picture in the database
    """
    def __init__(self, path = None, ext=None, rotation = None, blacklist=False):
        """
            Class initialization
            :param path is the path where the picture is to be found
            :param ext is the extension of the picture i.e. jpg, png, ..
            :param rotation stored if the picture has been rotated
            :param blacklist if the picture has been blacklisted (no show)
        """
        self.type = 'picture'
        self.path = path
        self.ext = ext
        self.rotation = rotation
        self.blacklist = blacklist

    def dump_from_dict(self, dictionary):
        """
            This method dumps the data in a dictionary to the class attributes
            :param dictionary to update
        """
        self.__dict__.update(dictionary)

class DbHandler():
    """
        This class is used to handle the a small database to store information about the
        current state of the application
    """
    def __init__(self, db_path):
        """
            Class initialization
            :param db_path The path where the database is being stored
        """
        self.database = TinyDB(db_path)

    def _pic_from_db(self, path):
        """
            This class gets a picture from the db and returns it as DbPicture obj
            :returns DbPicture object containing the picture information
        """
        query = Query()
        # Query the db for the pic in question
        result = self.database.search(query.path == path)
        if result:
            picture = DbPicture()
            picture.dump_from_dict(result[0])
            return picture
        else:
            return None
        
    def _update_field(self, path, field, value):
        """
            This function updates a field in a picture in the database
            :param path is the path where the picture is to be found
            :param field The field to be updated ['type','path', 'ext','rotation','blacklist']
            :value the value of the field in question
        """
        query = Query()
        # Get current picture from db  
        pic = self._pic_from_db(path)
        # Create a new dictionary for the update with the items from the picture
        # loaded from database
        update_dict = {k: value for k, v in pic.__dict__.items() if k == field}
        print(update_dict)
        # Run the update query
        self.database.update(update_dict, query.path == path)

    def add_picture_to_db(self, path, ext):
        """ This Method adds a picture to the database
            :param path is the path where the picture is to be found
            :param ext is the extension of the picture i.e. jpg, png, ..
        """
        pic = self._pic_from_db(path)
        if not pic:
            picture = DbPicture(path, ext, rotation=[0,0])
            # Since tinydb expects data as a dictionary read the object as one
            dinsert = picture.__dict__
            self.database.insert(dinsert)
 
    def is_pic_blisted(self, path):
        """
            This function asserts if a given picture has been blacklisted
            :return True if blacklisted False if not and None if picture 
            not in db
        """
        pic = self._pic_from_db(path)
        if pic:
            return pic.blacklist
        else:
            return None

    def blacklist_pic(self, path, bl=True):
        """
            This function blacklists a picture in the database
            :param path is the path where the picture is to be found
            :param bl if true the picture will be blacklisted, if false 
            the attribute will be set to false
        """
        self._update_field(path,'blacklist', bl)

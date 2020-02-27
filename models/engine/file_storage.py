#!/usr/bin/python3
'''serializes instances to a JSON file and
deserializes JSON file to instances'''
import json
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class FileStorage:
    '''serializes instances to a JSON file
    and deserializes JSON file to instances'''

    __file_path = 'file.json'
    __objects = {}

    def __init__(self):
        """constructor"""
        pass

    def all(self):
        '''Returns the dictionary __objects'''
        return FileStorage.__objects

    def new(self, obj):
        '''Sets in __objects the obj with key <obj class name>.id
        The object can be from BaseModel or another class like User,
        State or City. Note: Self makes reference to an object of
        FileStorage
        So, there will be a new seted object, example:
            bm_object = BaseModel()
            bm_object.id = 85
            new(bm_object) --> {"BaseModel.85": obj at 'memory adress'}
        This method is called from __init__ of base_model'''

        name = obj.__class__.__name__
        noid = obj.id
        key = "{}.{}".format(name, noid)
        FileStorage.__objects[key] = obj

    def save(self):
        '''Serialize __objects to the JSON file (__file_path).
        Takes the objects in FileStorage.__objets (a dictionary)
        that contain elementos in this way:
        Key: 'BaseModel.41e736d0-9f55-4ae8-b7ef-450c0d3d91ff' and
        Value: <models.base_model.BaseModel object at 0x7f9006aa5400>.
        The value is passed in a temporaly dictionary (new_dict)
        through to_dict method. After that, the FileStorage.__path (a file)
        is opened and written with the serialization of objects in new_dict.'''
        data = {}
        for key, value in self.__objects.items():
            data[key] = value.to_dict()

        namefile = FileStorage.__file_path
        with open(namefile, mode="w", encoding="utf-8") as file:
            json.dump(data, file)

    def reload(self):
        '''Deserializes JSON file to __objects if JSON file __file_path exists.
        The deserialization is stored in new_dict. Accesing to the value
        of new_dict (another dictionary), and getting the class name
        on this, a new object will be created with eval using kwargs (**value)
        for the attributes and its values. This new object will be storaged
        in FileStorage.__objects. It'll always be reloaded because the
        init file in models use storage.reload().'''
        namefile = self.__file_path
        try:
            with open(namefile, encoding="utf-8") as file:
                data = json.load(file)
                for key, value in data.items():
                    nameClass = value["__class__"]
                    newobj = eval(nameClass)(**value)
                    FileStorage.__objects[key] = newobj
        except Exception:
            pass

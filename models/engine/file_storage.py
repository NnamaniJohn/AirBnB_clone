#!/usr/bin/python3

"""File storage module contains one class FileStorge"""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """
    class FileStorage that serializes instances to a JSON
    file and deserializes JSON file to instances
    """

    __file_path = "file.json"
    __objects = {}

    def all(self):
        return type(self).__objects

    def new(self, obj):
        dic = obj.to_dict()
        type(self).__objects.update({"{}.{}".format(dic["__class__"], obj.id): obj})
        return

    def save(self):
        with open(type(self).__file_path, mode="w", encoding="utf-8") as myFile:
            obj = {}
            for key, value in type(self).__objects.items():
                dic = value.to_dict()
                obj.update({key: dic})
            myFile.write(json.dumps(obj))
        return

    def update(self, obj):
        dic = obj.to_dict()
        type(self).__objects.update({"{}.{}".format(dic["__class__"], obj.id): obj})

    def destroy(self, obj):
        del type(self).__objects["{}.{}".format(type(obj).__name__, obj.id)]
        return

    def reload(self):
        try:
            with open(type(self).__file_path, encoding="utf-8") as myFile:
                text = myFile.read()
                dic = json.loads(text)
                for key, value in dic.items():
                    cls = value["__class__"]
                    self.new(eval(cls)(**value))
        except FileNotFoundError:
            return
        return

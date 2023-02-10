#!/usr/bin/python3

"""BaseModel module contains one class BaseModel"""

import uuid
from datetime import datetime
import models


class BaseModel:
    """Base model class that defines all common
    attributes/methods for other classes"""

    def __init__(self, *args, **kwargs):
        if len(kwargs) != 0:
            for key, value in kwargs.items():
                if key != "__class__":
                    if key == "created_at" or key == "updated_at":
                        self.__setattr__(key, datetime.fromisoformat(value))
                    else:
                        self.__setattr__(key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def __str__(self):
        return "[{}] ({}) {}".format(type(self).__name__, self.id, self.__dict__)

    def save(self):
        self.updated_at = datetime.now()
        models.storage.save()
        return

    def destroy(self):
        models.storage.destroy(self)
        models.storage.save()

    def update(self, key, value):
        self.__setattr__(key, value)
        models.storage.update(self)
        models.storage.save()

    def to_dict(self):
        dic = self.__dict__.copy()
        dic.update({"__class__": type(self).__name__})
        dic["created_at"] = dic["created_at"].isoformat()
        dic["updated_at"] = dic["updated_at"].isoformat()
        return dic


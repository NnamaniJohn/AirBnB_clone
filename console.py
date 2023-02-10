#!/usr/bin/python3

"""contains the entry point of the command interpreter"""
import cmd
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """
    HBNBCommand interpreter
    """
    prompt = "(hbnb) "
    classes = ["BaseModel", "User", "State", "City", "Amenity", "Place", "Review"]

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """Quit command to exit the program"""
        return True

    def do_all(self, arg):
        if arg in self.classes:
            objs = storage.all().copy()
            models = []
            for key, value in objs.items():
                if arg == type(value).__name__:
                    models.append(str(value))
            print(models)
        else:
            print("** class doesn't exist **")

    def do_create(self, arg):
        """
        Creates a new instance of BaseModel,
        saves it (to the JSON file) and prints the id
        :param arg:
        :return:
        """
        if arg:
            if arg in self.classes:
                my_model = eval(arg)()
                my_model.save()
                print(my_model.id)
            else:
                print("** class doesn't exist **")
        else:
            print("** class name missing **")

    def do_show(self, arg):
        args = arg.split(" ")
        if len(args) < 1 or not args[0]:
            print("** class name missing **")
        elif len(args) < 2 or not args[1]:
            print("** instance id missing **")
        elif args[0] in self.classes:
            all_objs = storage.all()
            try:
                obj = all_objs["{}.{}".format(args[0], args[1])]
                print(obj)
            except KeyError:
                print("** no instance found **")
        else:
            print("** class doesn't exist **")

    def do_destroy(self, arg):
        args = arg.split(" ")
        if len(args) < 1 or not args[0]:
            print("** class name missing **")
        elif len(args) < 2 or not args[1]:
            print("** instance id missing **")
        elif args[0] in self.classes:
            all_objs = storage.all()
            try:
                obj = all_objs["{}.{}".format(args[0], args[1])]
                obj.destroy()
            except KeyError:
                print("** no instance found **")
        else:
            print("** class doesn't exist **")

    def do_update(self, arg):
        args = arg.split(" ")
        if len(args) < 1 or not args[0]:
            print("** class name missing **")
        elif len(args) < 2 or not args[1]:
            print("** instance id missing **")
        elif len(args) < 3 or not args[2]:
            print("** attribute name missing **")
        elif len(args) < 4 or not args[3]:
            print("** value missing **")
        elif args[0] in self.classes:
            all_objs = storage.all()
            try:
                my_model = all_objs["{}.{}".format(args[0], args[1])]
                dic = my_model.to_dict()
                if type(dic[args[2]]) == str:
                    my_model.update(args[2], str(args[3].strip("\"")))
                if type(dic[args[2]]) == int:
                    my_model.update(args[2], int(args[3].strip("\"")))
                if type(dic[args[2]]) == float:
                    my_model.update(args[2], float(args[3].strip("\"")))
            except KeyError:
                print("** no instance found **")
        else:
            print("** class doesn't exist **")


if __name__ == '__main__':
    HBNBCommand().cmdloop()

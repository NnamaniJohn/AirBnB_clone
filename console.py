#!/usr/bin/python3

"""contains the entry point of the command interpreter"""
import cmd
import re
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
        """Quit command to exit the program
        """
        return True

    def do_EOF(self, arg):
        """Quit command to exit the program
        """
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

    def my_count(self, class_n):
        """
        Method counts instances of a certain class
        """
        count_instance = 0
        for instance_object in storage.all().values():
            if instance_object.__class__.__name__ == class_n:
                count_instance += 1
        print(count_instance)

    def default(self, line):
        """Method to take care of following commands:
        <class name>.all()
        <class name>.count()
        <class name>.show(<id>)
        <class name>.destroy(<id>)
        <class name>.update(<id>, <attribute name>, <attribute value>)
        <class name>.update(<id>, <dictionary representation)
        Description:
            Creates a list representations of functional models
            Then use the functional methods to implement user
            commands, by validating all the input commands
        """
        names = ["BaseModel", "User", "State", "City", "Amenity",
                 "Place", "Review"]

        commands = {"all": self.do_all,
                    "count": self.my_count,
                    "show": self.do_show,
                    "destroy": self.do_destroy,
                    "update": self.do_update}

        args = re.match(r"^(\w+)\.(\w+)\((.*)\)", line)
        if args:
            args = args.groups()
        if not args or len(args) < 2 or args[0] not in names \
                or args[1] not in commands.keys():
            super().default(line)
            return

        if args[1] in ["all", "count"]:
            commands[args[1]](args[0])
        elif args[1] in ["show", "destroy"]:
            commands[args[1]](args[0] + ' ' + args[2])
        elif args[1] == "update":
            params = re.match(r"\"(.+?)\", (.+)", args[2])
            if params.groups()[1][0] == '{':
                dic_p = eval(params.groups()[1])
                for k, v in dic_p.items():
                    commands[args[1]](args[0] + " " + params.groups()[0] +
                                      " " + k + " " + str(v))
            else:
                rest = params.groups()[1].split(", ")
                commands[args[1]](args[0] + " " + params.groups()[0] + " " +
                                  rest[0] + " " + rest[1])


if __name__ == '__main__':
    HBNBCommand().cmdloop()

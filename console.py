#!/usr/bin/python3
'''create a console'''
import cmd
import shlex
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage
from datetime import datetime
listClass = ["BaseModel", "User", "Place",
             "State", "City", "Amenity", "Review"]


class HBNBCommand(cmd.Cmd):
    '''A command interpreter to manage AirBnB objects'''

    prompt = '(hbnb) '

    def do_EOF(self, line):
        '''EOF command to exit the program'''
        print("")
        return True

    def do_quit(self, line):
        '''Quit command to exit the program'''
        return True

    def emptyline(self):
        '''Empty line'''
        return ""

    def do_create(self, line):
        '''Creates a new instance of BaseModel, saves it (to the JSON
        file) and prints the id. Ex: $ create BaseModel'''

        if not line:
            print("** class name missing **")
            return

        data = shlex.split(line)
        nameClass = data[0]

        if data[0] in listClass:
            newBM = eval(nameClass)()
            storage.save()
            print(newBM.id)
        else:
            print("** class doesn't exist **")

    def do_show(self, line):
        '''Prints the string representation of an instance based on the
        class name and id. Ex: $ show BaseModel 1234-1234-1234.'''

        if not line:
            print("** class name missing **")
            return

        data = line.split(" ")
        nameClass = data[0]

        if nameClass in listClass:
            if len(data) == 1:
                print("** instance id missing **")
                return

            try:
                idObject = "{}.{}".format(data[0], data[1])
                dictObj = storage.all()
                print(dictObj[idObject])
            except Exception:
                print("** no instance found **")
        else:
            print("** class doesn't exist **")

    def do_destroy(self, line):
        '''Deletes an instance based on the class name and id (save the
        change into the JSON file). Ex: $ destroy BaseModel 1234-1234-1234'''

        if not line:
            print("** class name missing **")
            return

        data = line.split(" ")
        nameClass = data[0]

        if nameClass in listClass:
            if len(data) == 1:
                print("** instance id missing **")
                return

            idObject = "{}.{}".format(data[0], data[1])
            dictObj = storage.all()
            if idObject in dictObj:
                del dictObj[idObject]
                storage.save()
                return
            print("** no instance found **")
        else:
            print("** class doesn't exist **")

    def do_all(self, line):
        '''Prints all string representation of all instances based or not
        on the class name. Ex: $ all BaseModel or $ all'''

        dictObj = storage.all()

        if not line:
            newList = []
            for value in dictObj.values():
                newList.append(str(value))
            if newList:
                print(newList)
        else:

            data = line.split(" ")
            if data[0] not in listClass:
                print("** class doesn't exist **")
                return
            newList = []
            for value in dictObj.values():
                if(value.__class__.__name__ == data[0]):
                    newList.append(str(value))
            if newList:
                print(newList)

    def do_update(self, line):
        '''Updates an instance based on the class name and id by adding or
        updating attribute (save the change into the JSON file).
        Ex: $ update BaseModel 1234-1234-1234 email "aibnb@holberton.com"'''

        if not line:
            print("** class name missing **")
            return

        data = shlex.split(line)
        dictObj = storage.all()

        if len(data) == 0 or data[0] not in listClass:
            print("** class doesn't exist **")
            return
        if len(data) == 1:
            print("** instance id missing **")
            return

        try:
            obj = dictObj["{}.{}".format(data[0], data[1])]
        except Exception:
            print("** no instance found **")
            return

        if len(data) == 2:
            print("** attribute name missing **")
            return
        if len(data) == 3:
            print("** value missing **")
            return

        setattr(obj, data[2], data[3])
        obj.save()

    def do_count(self, line):
        '''retrieve the number of instances of a
        class: <class name>.count()'''

        if not line:
            print("** class name missing **")
            return

        if line in listClass:
            objcDic = storage.all()
            count = 0
            for values in objcDic.values():
                if values.__class__.__name__ == line:
                    count += 1
            print(count)
        else:
            print("** class doesn't exist **")

    def default(self, line):
        '''others commands. This method is for retrieve the
        number of instances of a class: <class name>.count()'''

        data = line.split(".")
        if len(data) < 2:
            return
        listFn = ["all()", "count()"]
        if data[1] in listFn:
            cmdString = "{}".format(data[0])
            if data[1] == listFn[0]:
                self.do_all(cmdString)
            elif data[1] == listFn[1]:
                self.do_count(cmdString)
        else:
            command = data[0]
            data = data[1].split("(")
            listFn = ["show", "destroy"]
            listFn2 = ["update"]
            if data[0] in listFn:
                data[1] = data[1][:-1]
                data[1] = shlex.split(data[1])
                command += " {}".format(data[1][0])
                fnexc = "self.do_{}('{}')".format(data[0], command)
                eval(fnexc)
            elif data[0] in listFn2:
                fnexc = "self.do_{}".format(data[0])
                fnexc += "('{}".format(command)
                data[1] = data[1].replace("\"", "")
                data[1] = data[1].split(",")
                if len(data[1]) == 1:
                    fnexc += " {}')".format(data[1][0][0:-1].strip())
                elif len(data[1]) == 2:
                    fnexc += " {} {}')".format(data[1][0].strip(),
                                               data[1][1][:-1].strip())
                elif len(data[1]) >= 3:
                    fnexc += " {} {} \"{}\"')".format(data[1][0].strip(),
                                                      data[1][1].strip(),
                                                      data[1][2][:-1].strip())

                eval(fnexc)
            else:
                print("** command doesn't exist **")


if __name__ == "__main__":
    HBNBCommand().cmdloop()

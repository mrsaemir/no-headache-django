import re


class DuplicateException(Exception):
    pass


class Structure:
    def __init__(self):
        raise NotImplementedError("You Should Implement This.")
        
    def get_index(self, text):
        found_list = []

        for res in self.regex.finditer(text):
            found_list.append(res)
        
        for i in range(len(found_list)):
            found_list[i] = found_list[i].span('target')
        
        return found_list
    
    def get_value(self, text):
        # returns what is known as a value to a certain key.
        indexes = self.get_index(text)
        if indexes:
            return [text[index[0]: index[1]] for index in indexes]
        return []
    

class Dictionary(Structure):
    def __init__(self, key=''):
        self.regex = re.compile(
                 "(\s|\n)+" + key + "(\s)*=(?P<target>(\s)*{[\'\"a-zA-Z0-9:\s\[\]\(\),\{\}._\-\=_#]*})"
        )
        
        
class List(Structure):
    def __init__(self, key=''):
        self.regex = re.compile(
                 "(\s|\n)+" + key + "(\s)*=(?P<target>(\s)*\[[\'\"a-zA-Z0-9:\s\[\]\(\),\{\}._/#]*\])"
        )
        
        
class Tuple(Structure):
    def __init__(self, key=''):
        self.regex = re.compile(
                 "(\s|\n)+" + key + "(\s)*=(?P<target>(\s)*\([\'\"a-zA-Z0-9:\s\[\]\(\),\{\}._#]*\))"
        )

        
class DoubleString(Structure):
    def __init__(self, key=''):
        self.regex = re.compile(
                 "(\s|\n)+" + key + """(\s)*=(?P<target>(\s)*"[\[\].\{\}\'\(\)a-zA-Z0-9\-_\\\/\s=@+\%&*!,#\^+$]*")"""
        )
        
        
class SingleString(Structure):
    def __init__(self, key=''):
        self.regex = re.compile(
                 "(\s|\n)+" + key + "(\s)*=(?P<target>(\s)*'[\[\].\{\}\"\(\)a-zA-Z0-9\-_\\\/\s=@+\%&*!,#\^+$]*')"
        )
        
        
class String:
    def __init__(self, key=''):
        self.key = key
        
    def get_index(self, text):
        ss = SingleString(key=self.key)
        ds = DoubleString(key=self.key)
        return ss.get_index(text) + ds.get_index(text)
    
    def get_value(self, text):
        # returns what is known as a value to a certain key.
        ss = SingleString(key=self.key)
        ds = DoubleString(key=self.key)
        return ss.get_value(text) + ds.get_value(text)
        
        
class Variable(Structure):
    def __init__(self, key=''):
        self.regex = re.compile(
                 "(\s|\n)+" + key + "(\s)*=(?P<target>(\s)*[a-zA-Z0-9_][a-zA-Z0-9_.,\[\]\"\'()#]*[^\n])"
        )


class PyEditor:
    def __init__(self, path):
        self.path = path
        self.analyzed_data = {}
        self.structures = ['String', 'Variable', 'Tuple', 'List', 'Dictionary']

        # signing file
        # if you remove this, you will definitely face serious problems,
        # if you don't believe, test it!
        text = None
        with open(self.path, 'r') as f:
            line0 = f.readline()
            if not line0 == '# EDITED BY NO-HEADACHE-DJANGO\n':
                text = line0 + f.read()
                text = '# EDITED BY NO-HEADACHE-DJANGO\n' + text
        if text:
            with open(self.path, 'w') as f:
                f.write(text)

    def analyze(self):
        with open(self.path, 'r') as f:
            text = f.read()
            for struct in self.structures:
                cls = globals()[struct]
                self.analyzed_data[struct] = len(cls().get_index(text))
        
        return self.analyzed_data
    
    def get_index_by_key(self, key):
        found = {}
        n_found = 0

        with open(self.path, 'r') as f:
            text = f.read()
            for struct in self.structures:
                cls = globals()[struct]
                found[struct] = cls(key=key).get_index(text)
                n_found += len(found[struct])

        if n_found > 1:
            print("Important Warning:\n")
            print(found)
            raise DuplicateException(f"Found {n_found} different declarations of variable '{key}'")

        return found

    def show_value_by_index(self, index):
        with open(self.path, 'r') as f:
            text = f.read()
            return text[index[0]: index[1]]

    def exchange(self, key, new_value):
        with open(self.path, 'r') as f:
            text = f.read()

        found = False
        # checking if the wanted key is available in py file.
        # in case of absence it should be added to end of the file
        for k, v in self.get_index_by_key(key).items():
            for i, j in v:
                text = text[:i] + " " + new_value + text[j:]
                found = True

        if not found:
            self.add_to_end(f"\n{key} = {new_value}")
            return

        with open(self.path, 'w') as f:
            f.write(text)

    def bulk_exchange(self, key_val_dict):
        for k, v in key_val_dict.items():
            self.exchange(k, v)
            
    def add_to_end(self, to_add):
        with open(self.path, 'r') as f:
            text = f.read()
           
        text = text + f"\n{to_add}"
        
        with open(self.path, 'w') as f:
            f.write(text)

    def add_to_imports(self, module_to_add):
        with open(self.path, 'r') as f:
            text = f.read()

        if f"import {module_to_add}" not in text:
            loc = text.find('import')
            text = text[:loc] + f"import {module_to_add}\n" + text[loc:]

        with open(self.path, 'w') as f:
            f.write(text)

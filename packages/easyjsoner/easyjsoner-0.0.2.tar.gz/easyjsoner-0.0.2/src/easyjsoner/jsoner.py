import json


class jsoner():
    data = None
    last_path = None
    setted_path = None

    @classmethod
    def read(cls, path):
        if (not cls.data) or (cls.last_path != path):
            with open(path, 'r', encoding='utf-8') as f:
                cls.data = json.load(f)
                cls.last_path = path
        return cls.data


    @classmethod
    def read_from(cls, path, path_in):
        if (not cls.data) or (cls.last_path != path):
            with open(path, 'r', encoding='utf-8') as f:
                cls.data = json.load(f)

        mods = path_in.split('/')
        load = cls.data
        for l in mods:
            try:
                load = load[l]
            except:
                return None
        return load


    @staticmethod
    def write(path, data):
        with open(path, 'w', encoding='utf-8') as f:
            return json.dump(data, f, indent=4)

    @staticmethod
    def file(path):
        return open(path, 'r', encoding='utf-8')

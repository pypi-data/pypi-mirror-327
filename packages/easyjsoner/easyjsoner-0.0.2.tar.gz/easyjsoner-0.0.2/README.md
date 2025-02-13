The simplest module for quick work with json files

**Import**

    from easyjsoner.jsoner import jsoner

**Read**

    file = jsoner.read('path')	# Возвращает json файл

**Read_in**

    file = jsoner.read_from('path_to_json', 'path/to/key')	# Возвращает значение ключа из json файла

**Write**

    file = jsoner.write('path', data)	# Запись в json

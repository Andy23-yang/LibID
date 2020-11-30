import os
from collections import Counter
import pickle
from options import OptionList
import json


def read_file(path):
    with open(path) as f:
        data = f.readlines()
        return data


def process_file(content, file):
    for line in content:
        if line.startswith('-'):
            line = line[:line.index('{')].split() if '{' in line else line.split()
            try:
                key_and_modifier = line[0].split(',')
                key = key_and_modifier[0]
                line = key_and_modifier + line[1:]
            except:
                key = line[0]
            if key in option_list:
                value = '' if len(line) == 1 else ' '.join(line[1:])
                if key not in config_dict.keys():
                    config_dict[key] = [value]
                else:
                    config_dict[key].append(value)


def write_file(file_path, data):
    with open(file_path, 'wb') as f:
        pickle.dump(data, f)

def write_json(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f)
        

if __name__ == "__main__":

    config_path = "config_files"
    output_path = 'output/config.json'
    config_dict = {}
    global option_list, modifier_list
    option_list = OptionList().get_list()
    modifier_list = OptionList().get_modifier()

    for _, _, files in os.walk(config_path):
        for file in files:
            content = read_file("{}/{}".format(config_path, file))
            process_file(content, file)

    for key in config_dict.keys():
        config_dict[key] = Counter(config_dict[key])

    write_json(output_path, config_dict)
    
#     with open('config.pkl', 'rb') as f:
#         data = pickle.load(f)
#         print(data)

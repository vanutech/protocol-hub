import os
import yaml
import sys

def find_first_level_dirs():
    """Return a list of first-level subdirectories in the given directory."""
    return [
        entry.name for entry in os.scandir('.')
        if (entry.is_dir() and not entry.name.startswith('.'))
    ]

def find_yaml_files(directory):
    """Count the number of .yml or .yaml files in a directory."""
    yaml_files = [
        file.name for file in os.scandir(directory)
        if file.is_file() and file.name.endswith(('.yml', '.yaml'))
    ]
    return yaml_files

def find_info_file(directory):
    info_files = [
        file.name for file in os.scandir(directory)
        if file.is_file() and file.name.endswith('.info')
    ]
    if len(info_files) == 1:
        return info_files[0]
    else:
        return None

def load_yaml_with_replaced_tags(file_path):
    """Load a YAML file after replacing custom tags like '!parameter'."""
    with open(file_path, 'r', encoding='utf-8') as f:
        yaml_content = f.read()

    # Replace '!parameter' with a default value (e.g., 'default_value')
    yaml_content = yaml_content.replace('!parameter', 'default_value')

    # Load the modified YAML
    data = yaml.safe_load(yaml_content)
    return data


def evaluate_yaml(file_path):
    """Check if a YAML file is valid and optionally extract metadata."""
    try:
        data = load_yaml_with_replaced_tags(file_path)
        return data
    except yaml.YAMLError as e:
        print(f"{file_path} is invalid: {e}")
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    
    return None
    
def organize_protocols():
    protocolinfos = {}


    first_level_dirs = find_first_level_dirs()
    if not first_level_dirs:
        print(f"No directories found ")
        return
    
    for dir_path in first_level_dirs:
        yaml_files = find_yaml_files(dir_path)
        infofilename = find_info_file(dir_path)
        if (infofilename != None):
            infofilename = infofilename.removesuffix(".info")  # Python 3.9+
            # split on "_" into pairs, then on the first "-" into key/value
            info = dict(part.split("-", 1) for part in infofilename.split("_"))

            sensors = {}
            actuators = {}

            for yamlfile in yaml_files:
                data = evaluate_yaml(dir_path + "/" +yamlfile)

                if (data['pri'] == 'sensor'):
                    sensors[yamlfile] = {"path": yamlfile, "type" : data['type']}
                elif (data['pri'] == 'actuator'):
                    actuators[yamlfile] = {"path": yamlfile, "type" : data['type']}



            protocolinfo = {}
            protocolinfo["path"] = dir_path
            protocolinfo["name"] = info["name"]
            protocolinfo["type"] = info["type"]
            protocolinfo["sensor"] = sensors
            protocolinfo["actuators"] = actuators

            protocolinfos[dir_path] = protocolinfo


        

    return protocolinfos



if __name__ == "__main__":
    organizedprotocol = organize_protocols()
    
    f = open('protocol_info.yaml', 'w+')
    yaml.dump(organizedprotocol, f, allow_unicode=True)
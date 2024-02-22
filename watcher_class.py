import importlib
import configparser
import os
from datetime import datetime 

class HotReloader:
    def __init__(self, target_path = ''):
        #initialize the absolute path current repository (it can be customized.)
        if not target_path == '': 
            self.target_path = target_path
        else:
            self.target_path = os.path.abspath(os.getcwd())
        
        #make the class "ConfigParser" to set the config.ini file.
        self.config_file = configparser.ConfigParser()
        #read the file.
        self.check_repos()
    def check_repos(self):
        self.config_file.read(f'{self.target_path}\\config.ini')
        
        CONFIG_VERSION = self.config_file["CONFIG_VERSION"] #Selecr the section
        if CONFIG_VERSION["last_config"] == 'YYMMDD-hhmmss':#if it is the first time to checking
            files = os.listdir(self.target_path)
            for file in files:
                self.config_file.add_section(file)
                tmp_section = self.config_file[file]
                file_titles = file.split('.')

                if (file_titles[0] is not '') and (len(file_titles) is 2) :
                    print(file_titles)
                    file_name, file_ext = file_titles
                elif not '.' in file:
                    file_name = file
                    file_ext = 'Null'
                else:
                    file_name = 'Null'
                    file_ext = file_titles[0]

                file_last_modified = os.path.getmtime(f'{self.target_path}\\{file}')
                tmp_section['name'] = file_name
                tmp_section['extension'] = file_ext
                print(file_last_modified, type(file_last_modified))
                tmp_section['last_modified'] = str(file_last_modified)

            CONFIG_VERSION["last_config"] = str(datetime.now()) #set the Key - Value

            with open(f'{self.target_path}\\\config.ini', "w") as f: #save them
                self.config_file.write(f)


if __name__ == "__main__":
   #module_names = ["sample1", "sample2"]  # Add all your module names here
    hot_reloader = HotReloader()
    #hot_reloader.run()

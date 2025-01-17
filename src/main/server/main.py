import uvicorn
from ..server.server import *


def run_server(directories_to_watch: list = None, exception_dir: list = None, zipfile_dir: str = None,
               os_named=True, os_list: list = None, os_exception_list: list = None,
               base_directory: str = '', default_name_tail: str = '',
               host: str = "0.0.0.0", port: int = 8000):
    """This function is used to initialize the circumstances of reloading.

        Args:
            directories_to_watch (list): This determines the directories to be watched.
            exception_dir (list): This determines the directories not to be watched.
            zipfile_dir (str): This determines the directory to save the zipped files.
            os_named (str): This checks if the user selected the directory which will be used as OS or the directory which has multiple OS.
            os_list (list): (Optional) This saves the list of OS.
            os_exception_list (list): (Optional) This excludes the directory which should not be identified as an OS.
            Initialized list is ["common", "__pycache__", "zip_files"]
            base_directory (str): This indicates the basic directory which need to all OS.
            default_name_tail (str): This indicates the tail of directory name that always follows.
            host (str):  (Optional) This determines the host of the FastAPI.  Initialized as "127.0.0.1"
            port (int):  (Optional) This determines the port of the FastAPI.  Initialized as "8000"
    """

    if os_list is None:  # Populate the os_list with directories that are not in the exception_list.
        os_list = []
        if os_named:
            for item in directories_to_watch:
                if os.path.isdir(item):
                    tmp_name = os.path.basename(item)
                    if tmp_name not in os_exception_list:
                        os_list.append(tmp_name)

        else:
            for _dir in directories_to_watch:
                for item in os.listdir(_dir):
                    sub_folder = os.path.join(_dir, item)
                    print(f'Checking current directories.... : {sub_folder}')
                    dir_name = item.replace(default_name_tail, '')
                    print(f'A current dir_name is {dir_name}.')
                    if os.path.isdir(sub_folder) and dir_name not in os_exception_list:
                        os_list.append(dir_name)

        print(f'OS list is {os_list}')

    fastAPI_app = start_reloading(directories_to_watch=directories_to_watch, zipfile_dir=zipfile_dir,
                                  os_list=os_list, exception_dir=exception_dir,
                                  base_directory=base_directory, default_name_tail=default_name_tail)

    uvicorn.run(fastAPI_app, host=host, port=port)

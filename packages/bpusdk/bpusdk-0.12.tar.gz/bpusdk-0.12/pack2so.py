from setuptools import setup, Extension
from Cython.Build import cythonize
import os

def find_py_files(package_name,dirpath_list):
    py_files = []
    for dirpath, _, filenames in os.walk(package_name):
        if dirpath in dirpath_list:  
            continue  

        for file in filenames:
            if file.endswith(".py") and file not in ("__init__.py", "__init__.pyc", "BrainpyBase.py"): 
                full_path = os.path.join(dirpath, file)
                py_files.append(full_path)
    return py_files

def list_all_subfolders(root_folder):
    subfolders = []
    for dirpath, dirnames, _ in os.walk(root_folder):
        for dirname in dirnames:
            subfolders.append(os.path.join(dirpath, dirname))
    return subfolders

def build_dirpath_list(package_name):
    root = package_name+"/SNNCompiler"
    dirpath_list = list_all_subfolders(root)
    dirpath_list.append(package_name)
    dirpath_list.append(package_name+"/Models")
    dirpath_list.append(package_name+"/Tests")
    dirpath_list.append(package_name+"/SNNCompiler")
    return dirpath_list

package_name = "bpusdk"
dirpath_list = build_dirpath_list(package_name)
py_modules = find_py_files(package_name,dirpath_list)
setup(ext_modules=cythonize(py_modules, compiler_directives={"language_level": "3"}),)

for dirpath, _, filenames in os.walk(package_name):
    if dirpath in dirpath_list:  
        continue  

    for file in filenames:
        if file.endswith(".py") or file.endswith(".c"):
            if file not in ("__init__.py", "__init__.pyc","BrainpyBase.py"):
                file_path = os.path.join(dirpath, file)
                os.remove(file_path)

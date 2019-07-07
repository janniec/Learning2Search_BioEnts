import numpy as np
import pandas as pd
import zipfile
import tarfile
import os

def unzip(path_to_zip_file, directory_to_extract_to):
    '''
    Extracts files and/or subdirectories within zipfile into designated directory. 
    IN: 
    path_to_zip_file - designated zipfile
    directory_to_extract_to - designated destination of unzipped files and/or subdirectories
    OUT: nothing. But will print names of extracted files & subdirectories
    '''
    before = os.listdir(directory_to_extract_to)
    zip_ref = zipfile.ZipFile(path_to_zip_file, 'r')
    zip_ref.extractall(directory_to_extract_to)
    zip_ref.close()
    after = os.listdir(directory_to_extract_to)
    os.remove(path_to_zip_file)
    print('Unzipped:', list(set(after) - set(before)))
    
def untar(path_to_tar_file, directory_to_extract_to):
    '''
    Extracts files and/or subdirectories within tarfile into designated directory. 
    IN: 
    path_to_tar_file - designated tarfile
    directory_to_extract_to - designated destination of untarred files and/or subdirectories
    OUT: nothing. But will print names of extracted files & subdirectories
    '''    
    before = os.listdir(directory_to_extract_to)
    if (path_to_tar_file.endswith("tar.gz")):
        tar = tarfile.open(path_to_tar_file, "r:gz")
        tar.extractall(directory_to_extract_to)
        tar.close()
    elif (path_to_tar_file.endswith("tar")):
        tar = tarfile.open(path_to_tar_file, "r:")
        tar.extractall(directory_to_extract_to)
        tar.close()
    after = os.listdir(directory_to_extract_to)
    os.remove(path_to_tar_file)
    print('Untarred:', list(set(after) - set(before)))

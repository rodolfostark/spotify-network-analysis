import json
import numpy as np
import pandas as pd



def get_list_of_slices(list_size: int) -> list:
    """
    Generates a list of random file names of the dataset of spotify's playlists

    Parameters:
        list_size (int): size of the list of slices
    Output:
        slices2use (list): list of slices paths
    """
    try:
        from numpy.random import randint
    except ModuleNotFoundError:
        print('Numpy is not installed. Please install it to use this function.')
        return

    # slices goes from 0-999 to 999000-999999
    MIN_VALUE = 0
    MAX_VALUE = 1000000 # top limit is non inclusive
    slices = randint(MIN_VALUE, MAX_VALUE, size=list_size)

    slices2use = []
    for slice_id in slices:
        # normalizing the limits of the slice in the filename (this removes the last 3 digits)
        SLICE_START = int(slice_id/1000) * 1000;
        SLICE_END = SLICE_START + 999;
        slice_path = 'mpd.slice.' + str(SLICE_START) + '-' + str(SLICE_END) + '.json'
        slices2use.append(slice_path)
    
    return slices2use


def list_slices_filepaths(slices_path: str) -> list:
    """
    Generates a list of file names of the dataset of spotify's playlists saved on data/ repository

    Parameters:
        slices_path (str): path to the folder containing the slices
    Output:
        slices2use (list): list of slices paths
    """
    try:
        from os import listdir
    except ModuleNotFoundError:
        print('os is not installed. Please install it to use this function.')
        return

    slices2use = []
    for file in listdir(slices_path):
        slices2use.append(file)
    
    return slices2use


def jsonToCSV(slices2use: list) -> None:
    """
    Converts the json files of the dataset of spotify's playlists  on 'data/' to csv files

    Parameters:
        slices2use (list): list of slices paths
    Output:
        None
    """
    for slice_path in slices2use:
        artist_playlist_array = []

        path = 'data/' + slice_path
        slice_data = json.load(open(path, 'r'))
        slice_df = pd.DataFrame.from_dict(slice_data['playlists'], orient='columns')

        for _, playlist in slice_df.iterrows():
            for track in playlist['tracks']:
                artist_playlist_array.append([track['artist_name'], playlist['pid']])

        artist_playlist_df = pd.DataFrame(artist_playlist_array, columns=['artist_name', 'pid'])
        artist_playlist_df.to_csv('data_CSV/' + slice_path.replace('.json', '') + '.csv', index=False)
#! /usr/bin/env python3
from os.path import isfile
from struct import unpack

class BCI:
    '''Class to represent a BCI file'''
    def __init__(self, data):
        '''``BCI`` constructor

        Args:
            ``data`` (``bytes``): The data of this BCI file

        Returns:
            ``BCI`` object
        '''
        if isinstance(data, str):
            if isfile(data):
                f = open(data, 'rb'); data = f.read(); f.close()
            else:
                raise TypeError("'data' must be a 'bytes' object")
        elif not isinstance(data, bytes):
            raise TypeError("'data' must be a 'bytes' object")
        if len(data) % 8 != 0:
            raise ValueError("Length of 'data' must be a multiple of 8")
        self.data = data

    def __len__(self):
        '''Return the number of tiles in this ``BCI``

        Returns:
            ``int``: The number of tiles in this ``BCI``
        '''
        return int(len(self.data)/8)

    def __getitem__(self, index):
        '''Return the tile record at a given index

        Args:
            ``index`` (``int``): The index to access

        Returns:
            ``tuple``: The (tile number, number of clusters) record for the tile at ``index``
        '''
        return (unpack('i', self.data[index*8 : (index*8)+4])[0], unpack('i', self.data[(index*8)+4 : (index+1)*8])[0])

    def __iter__(self):
        '''Iterate over the (tile number, number of clusters) records for this ``BCI``'''
        for i in range(len(self)):
            yield(self[i])

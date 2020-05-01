#! /usr/bin/env python3

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
        self.data = data

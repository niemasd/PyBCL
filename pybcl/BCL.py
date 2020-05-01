#! /usr/bin/env python3
from gzip import open as gopen
from os.path import isfile
from struct import pack,unpack
NUC_TO_NUM = {'A':0, 'C':1, 'G':2, 'T':3}
NUCS = 'ACGT'

class BCL:
    '''Class to represent a BCL file'''
    def __init__(self, data):
        '''``BCL`` constructor

        Args:
            ``data`` (``bytes``): The data of this BCL file

        Returns:
            ``BCL`` object
        '''
        if isinstance(data, str):
            if isfile(data):
                if data.lower().endswith('.gz') or data.lower().endswith('.bgzf'):
                    f = gopen(data, 'rb')
                else:
                    f = open(data, 'rb')
                data = f.read(); f.close()
            else:
                raise TypeError("'data' must be a 'bytes' object")
        elif not isinstance(data, bytes):
            raise TypeError("'data' must be a 'bytes' object")
        self.data = data
        if len(self) != len(data)-4:
            raise ValueError("Invalid BCL file: number of clusters (first 4 bytes) != number of bytes - 4")

    def __len__(self):
        '''Return the number of bases in this ``BCL``
        
        Returns:
            ``int``: The number of bases in this ``BCL``'''
        return unpack('I', self.data[:4])[0]

    def __getitem__(self, index):
        '''Return the (nucleotide, quality) tuple at a given index

        Args:
            ``index`` (``int``): The index to access

        Returns:
            ``tuple``: The (nucleotide, quality) tuple at ``index``
        '''
        b = self.data[4+index]; q = b >> 2
        if q == 0:
            return ('N', 0)
        return (NUCS[b & 0b00000011], q)

def create_BCL(nucs, quals):
    '''Create a ``BCL`` object from a list of nucleotides and quality scores

    Args:
        ``nucs`` (``list`` of ``str``): The nucleotides ('A', 'C', 'G', or 'T')

        ``quals`` (``list`` of ``int``): The quality scores (in the range [0,63])

    Returns:
        ``BCL`` object
    '''
    if not isinstance(nucs, list):
        raise TypeError("'nucs' must be a 'list' of 'str'")
    if not isinstance(quals, list):
        raise TypeError("'quals' must be a 'list' of 'int'")
    if len(nucs) != len(quals):
        raise ValueError("'nucs' and 'quals' must have the same length")
    out = bytearray()
    out += pack('I', len(nucs))
    for i in range(len(nucs)):
        nuc = nucs[i]; qual = quals[i]
        if not isinstance(nuc, str):
            raise TypeError("'nucs' must be a 'list' of 'str'")
        if nuc not in {'A', 'C', 'G', 'T'}:
            raise ValueError("Invalid nucleotide: %s (must be 'A', 'C', 'G', or 'T')" % nuc)
        if not isinstance(qual, int):
            raise TypeError("'quals' must be a 'list' of 'int'")
        if qual < 0 or qual > 63:
            raise ValueError("Quality score must be in the range [0,63]")
        out += pack('B', (qual << 2) | NUC_TO_NUM[nuc])
    return BCL(bytes(out))

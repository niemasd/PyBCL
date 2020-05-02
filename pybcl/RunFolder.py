#! /usr/bin/env python3
from pybcl.BCI import BCI
from pybcl.BCL import BCL
from glob import glob
from os.path import isdir,isfile
import xml.etree.ElementTree as ET

class RunFolder:
    '''Class to represent a run folder'''
    def __init__(self, path):
        '''``RunFolder`` constructor

        Args:
            ``path`` (``str``): The path of this run folder

        Returns:
            ``RunFolder`` object
        '''
        if not isinstance(path, str):
            raise TypeError("'path' must be a 'str' object")
        if not isdir(path):
            raise ValueError("Path not found: %s" % path)
        self.path = path.rstrip('/')
        run_info_path = '%s/RunInfo.xml' % self.path
        if not isfile(run_info_path):
            raise ValueError("'RunInfo.xml' was not found in the root of the run folder: %s" % self.path)
        self.basecall_lane_paths = list(glob('%s/Data/Intensities/BaseCalls/L*' % self.path))
        self.run_info = ET.parse(run_info_path).getroot()

    def get_flowcell(self):
        '''Return the flowcell of this run

        Returns:
            ``str``: The flowcell of this run
        '''
        curr = None
        for c in self.run_info:
            if c.tag.lower() == 'run':
                curr = c; break
        if curr is None:
            raise ValueError("No 'Run' tag in 'RunInfo.xml'")
        for c in curr:
            if c.tag.lower() == 'flowcell':
                curr = c; break
        if curr.tag.lower() != 'flowcell':
            raise ValueError("No 'Run->Flowcell' tag in 'RunInfo.xml'")
        return curr.text

    def get_instrument(self):
        '''Return the instrument of this run

        Returns:
            ``str``: The instrument of this run
        '''
        curr = None
        for c in self.run_info:
            if c.tag.lower() == 'run':
                curr = c; break
        if curr is None:
            raise ValueError("No 'Run' tag in 'RunInfo.xml'")
        for c in curr:
            if c.tag.lower() == 'instrument':
                curr = c; break
        if curr.tag.lower() != 'instrument':
            raise ValueError("No 'Run->Flowcell' tag in 'RunInfo.xml'")
        return curr.text

    def get_run_num(self):
        '''Return the run number of this run

        Returns:
            ``int``: The run number of this run
        '''
        curr = None
        for c in self.run_info:
            if c.tag.lower() == 'run':
                curr = c; break
        if curr is None:
            raise ValueError("No 'Run' tag in 'RunInfo.xml'")
        return int(curr.attrib['Number'])

    def iter_reads(self):
        '''Iterate over the reads from this run as (ID, sequence, quality) tuples'''
        instrument = self.get_instrument()
        run_num = self.get_run_num()
        flowcell = self.get_flowcell()
        ID_prefix = "@%s:%d:%s" % (instrument, run_num, flowcell)
        for lane_path in self.basecall_lane_paths:
            lane_num = int(lane_path.split('/')[-1].lstrip('L'))
            lane_ID_prefix = "%s:%d" % (ID_prefix, lane_num)
            c_folders = list(glob('%s/C*.*' % lane_path))
            if len(c_folders) == 0:
                s_bcis = glob('%s/s_*.bci' % lane_path)
                if len(s_bcis) == 0:
                    raise ValueError("No s_*.bci files, so not sure how to find tile information")
                elif len(s_bcis) != 1:
                    raise ValueError("Found multiple s_*.bci files, so not sure how to proceed for finding tile information")
                tiles = list(BCI(s_bcis[0]))
                print(tiles); exit()
                for bcl_path in glob('%s/*.bcl*' % lane_path):
                    if bcl_path.endswith('.bci'):
                        continue
                    bcl = BCL(bcl_path)
            else:
                for c in c_folders:
                    cycle = int(c.split('/')[-1].lstrip('C').split('.')[0])
                    for bcl_path in glob('%s/*.bcl*' % c):
                        if bcl_path.endswith('.bci'):
                            continue
                        lane, tile = bcl_path.split('/')[-1].split('.')[0].split('_')[1:]
                        lane = int(lane); tile = int(tile)
                        raise RuntimeError("NOT IMPLEMENTED: C FOLDERS")
            #for 
        print(ID_prefix)

#!/usr/bin/env python
# -*- coding: utf8 -*-

import VideoPic

def main():
    
    mp = VideoPic.VideoPic()

    mp.InitCmdFile()

    # mp.CaptureImage("00:04:15.000","00:04:25.000","/media/hustrc/LinuxData/Download/Video/Mobile Suit Gundam 00 Second Season Batch/E01[The Angels' Second Advent].mkv",30)
    mp.CaptureImage("/media/guolei/L-Data/TV/cmd")
            
if __name__ == '__main__':
    main()

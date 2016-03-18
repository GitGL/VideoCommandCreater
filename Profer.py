#!/usr/bin/env python
# -*- coding: utf8 -*-

import VideoPic

def main():
    
    mp = VideoPic.VideoPic()

    mp.InitCmdFile()

    mp.CaptureImage("01:06:19.001","/media/hustrc/LinuxData/Download/Video/[The.Extreme.Fox].2014.mkv",30,30)
            
if __name__ == '__main__':
    main()

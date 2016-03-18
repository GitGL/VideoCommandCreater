#!/usr/bin/env python
# -*- coding: utf8 -*-

import VideoPic

def main():
    mp.InitCmdFile()

    mp = VideoPic.VideoPic("00:00:00:.001","china-x",30,30)
    mp.CaptureImage()
            
if __name__ == '__main__':
    main()

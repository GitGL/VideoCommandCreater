#!/usr/bin/env python
# -*- coding: utf8 -*-

class VideoPic(object):
    def __init__(self, time_start = "", video_name = "", img_count = 30, intervalTime = 1):
        '''
        intervalTime : Unit: millisecond
        '''
        self.time_start = time_start # "00:00:00.001"
        self.video_name = video_name # "na"
        self.image_count = img_count # 100
        #self.edit_path = "/media/hustrc/LinuxData/Download/Factory"
        self.edit_path = "/media/guolei/L-Data/Download"
        self.intervalTime = intervalTime
        self.file_cmd = "/media/hustrc/LinuxData/Download/Factory"
        
    def InitCmdFile(self):
        open(self.edit_path+"/cmdfactory", 'w').write("")
        
    def CaptureImage(self):
        
        img_number = 1
        
        while img_number <= self.image_count:
            
            if img_number == 1:
                interval_time = 0
            else:
                interval_time = self.intervalTime

            # Start Time
            sec_parts = self.time_start.split(".")
            time_msecond = int(sec_parts[1])
            
            if (time_msecond + interval_time) >= 1000:
                milli_second_mod = (time_msecond + interval_time) % 1000
                time_parts = sec_parts[0].split(":")
                
                time_hour = int(time_parts[0])
                time_minute = int(time_parts[1])
                time_second = int(time_parts[2])
                
                if (time_second + 1) == 60:
                    if (time_minute + 1) == 60:
                        time_hour = time_hour + 1
                        time_minute = 0
                        time_second = 0
                    else:
                        time_minute = time_minute + 1
                        time_second = 0
                else:
                    time_second = time_second + 1
                    
                if time_hour < 10:
                    time_parts[0] = "0" + str(time_hour)
                else:
                    time_parts[0] = str(time_hour)
                    
                if time_minute < 10:
                    time_parts[1] = "0" + str(time_minute)
                else:
                    time_parts[1] = str(time_minute)
                    
                if time_second < 10:
                    time_parts[2] = "0" + str(time_second)
                else:
                    time_parts[2] = str(time_second)
                    
                if milli_second_mod < 10:
                    time_part_milli = '00' + str(milli_second_mod)
                elif milli_second_mod < 100:
                    time_part_milli = '0' + str(milli_second_mod)
                elif milli_second_mod < 1000:
                    time_part_milli = str(milli_second_mod)
                else:
                    pass

                self.time_start = ":".join(time_parts)
                self.time_start = self.time_start + "." + time_part_milli
            else:
                milli_second_new = time_msecond + interval_time

                if milli_second_new < 10:
                    time_part_milli = '00' + str(milli_second_new)
                elif milli_second_new < 100:
                    time_part_milli = '0' + str(milli_second_new)
                elif milli_second_new < 1000:
                    time_part_milli = str(milli_second_new)
                else:
                    pass

                self.time_start = sec_parts[0] + "." + time_part_milli
                
            # Image Name
            time_parts = self.time_start.split(":")
            image_name = "_".join(time_parts)
            image_name = image_name + ".jpg"
            
            # Write CMD
            cmd_cap_img = "ffmpeg -i " + self.video_name + " -f image2 -ss " + self.time_start + " -t 0.001 " + image_name
            open(self.edit_path+"/cmdfactory", 'a').write("%s \n" %(cmd_cap_img))

            img_number += 1

    
'''
$ ffmpeg -i test.avi -f image2 -ss 00:00:01 -t 0.001 test.jpg

$ ffmpeg -i test.avi -f image2 -ss 8 -t 0.001 -s 350x240 test.jpg
$ ffmpeg -i infile (-ss second_offset) -t 0.001 -s msize (-f image_fmt) outfile.jpg

$ ffmpeg -i infile -ss 00:03:03 -t 0.001 -s 800*600 -f image2  outfile.jpg
$ ffmpeg -i infile -ss 00:03:03.001 -t 0.001 -s 800*600 -f image2  outfile.jpg
$ ffmpeg -i infile -ss 00:03:03.100 -t 0.001 -s 800*600 -f image2  outfile.jpg

$ ffmpeg -i infile -ss 00:03:03 -vframes 1 -s 800*600 -f image2  outfile.jpg
$ ffmpeg -i "infile.mp4" -r 1 -q:v 2 -f image2 image-3%d.jpeg
'''

# mp = VideoPic('00:00:00.000','/media/guolei/L-Data/Download/[Harmony].mp4',30,50)
# mp.InitCmdFile()
# mp.CaptureImage()

#!/usr/bin/env python
# -*- coding: utf8 -*-

import commands
import os

class VideoPic(object):
    def __init__(self):

        self.edit_path = "/media/hustrc/LinuxData/Download/Factory"
        #self.edit_path = "/media/guolei/L-Data/Download"
        self.file_cmd = "/media/hustrc/LinuxData/Download/Factory"
        
    def InitCmdFile(self):
        open(self.edit_path+"/cmdfactory", 'w').write("")

    def CreateIndependentSpace(self, name):
        path = self.edit_path
        
        nameFull = name[name.rfind("/")+1:]
        nameNoExtention = nameFull[:nameFull.rfind(".")]

        if not os.path.exists("nameNoExtention"):
            # Write CMD
            cmd_space = "mkdir " + "\"" + nameNoExtention + "\""
            open(path+"/cmdfactory", 'a').write("%s \n" %(cmd_space))
        
        cmd_space = "cd " + "\"" + nameNoExtention + "\""
        open(path+"/cmdfactory", 'a').write("%s \n" %(cmd_space))

    def QuitIndependentSpace(self):
        path = self.edit_path
        
        cmd_space = "cd .."
        open(path+"/cmdfactory", 'a').write("%s \n" %(cmd_space))
        open(path+"/cmdfactory", 'a').write("%s \n" %(""))

    def GetVideoDuration(self, videoFile):
        
        cmd = "ffmpeg -i " + videoFile + " 2>&1 | grep 'Duration' | cut -d ' ' -f 4 | sed s/,//"
        # print("This is ffmpeg cmd=================================: %s" %cmd)
        (status, output) = commands.getstatusoutput(cmd)
        # print(output)
        return output
    
    def TransformTimeToSecond(self, time):
        print("===================TransformSecond")
        return int(time[:2])*3600 + int(time[3:5])*60 + int(time[6:8])
    
    def IncreaseIntervalTime(self, time, interval_time):
        
        time_start = time
        
        # Start Time
        time_parts = time_start.split(".")
        time_millisecond = int(time_parts[1])
        
        if (time_millisecond + interval_time) >= 1000:
            milli_second_mod = (time_millisecond + interval_time) % 1000
            time_parts = time_parts[0].split(":")
            
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

            time_start = ":".join(time_parts)
            time_start = time_start + "." + time_part_milli
        else:
            milli_second_new = time_millisecond + interval_time

            if milli_second_new < 10:
                time_part_milli = '00' + str(milli_second_new)
            elif milli_second_new < 100:
                time_part_milli = '0' + str(milli_second_new)
            elif milli_second_new < 1000:
                time_part_milli = str(milli_second_new)
            else:
                pass

            time_start = time_parts[0] + "." + time_part_milli
                
        return time_start
    
    def CompareTime(self, time1, time2):
        print("===================CompareTime")
        if self.TransformTimeToSecond(time2) > self.TransformTimeToSecond(time1):
            return True
        elif self.TransformTimeToSecond(time2) <= self.TransformTimeToSecond(time1):
            return False
    
    def CaptureImage(self, time_start, time_end, video_name, img_count = 30, intervalTime = 250, copyFlag=0):
        
        """
        intervalTime : Unit: millisecond
        time_start # "00:00:00.001"
        """
        
        if time_end =="":
            video_duration = self.GetVideoDuration(video_name)
            time_end = video_duration
                
        self.CreateIndependentSpace(video_name)
        
        if copyFlag == 1:
            # Copy the to be edited file to Factory
            cmd_copy = "cp " + "\"" + video_name + "\"" + " " + self.edit_path + "/" + "A"
            open(self.edit_path+"/cmdfactory", 'a').write("%s \n" %(cmd_copy))
            
            video_name = "A"
        
        time_img = time_start

        while self.CompareTime(time_img,time_end):
            
            # Image Name
            time_parts = time_img.split(":")
            image_name = "_".join(time_parts)
            image_name = image_name + ".jpg"
            
            # Write CMD
            cmd_cap_img = "ffmpeg -i " + "\"" + video_name + "\"" + " -f image2 -ss " + time_img + " -t 0.001 " + image_name
            open(self.edit_path+"/cmdfactory", 'a').write("%s \n" %(cmd_cap_img))
            
            time_img = self.IncreaseIntervalTime(time_img,intervalTime)

        if copyFlag == 1:
            # Removefile
            cmd_remove = "rm A"
            open(self.edit_path+"/cmdfactory", 'a').write("%s \n" %(cmd_remove))
            
        self.QuitIndependentSpace()
        
'''
$ ffmpeg -i test.avi -f image2 -ss 00:00:01 -t 0.001 test.jpg
'''

# mp = VideoPic('00:00:00.000','00:01:00:000','/media/guolei/L-Data/Download/[Harmony].mp4',30,50)
# mp.InitCmdFile()
# mp.CaptureImage()

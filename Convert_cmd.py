# -*- coding: utf-8 -*-
'''
If have cmd, then read cmd
'''
import os
import datetime

import commands

filePath = "/media/hustrc/Media03/32-TV/01-Korean/[点金神手(Midas)]"
# filePath = "/media/guolei/L-Data/TV"

editPath = "/media/hustrc/LinuxData/Download/Factory"
# editPath = "/media/guolei/L-Data/TV/CMD"

def GetVideoDuration(videoFile):
    
    cmd = "ffmpeg -i " + videoFile + " 2>&1 | grep 'Duration' | cut -d ' ' -f 4 | sed s/,//"
    # print("This is ffmpeg cmd=================================: %s" %cmd)
    (status, output) = commands.getstatusoutput(cmd)
    # print(output)
    return output
    
def GetTime(initTimeStr):
    """
    # if is "" pass
    # if is not "" deal with time
    # -s (start time) : sTime
    # end time : eTime
    # -t : tTime
    """
    # Use Split " " and ":"
    timeUnits = initTimeStr.split(" ")
    # print(timeUnits)
    sTime = timeUnits[0]
    eTime = timeUnits[1]
    #
    sHour = int(sTime[0:2])
    sMinute = int(sTime[3:5])
    sSecond = int(sTime[6:8])

    eHour = int(eTime[0:2])
    eMinute = int(eTime[3:5])
    eSecond = int(eTime[6:8])

    if eSecond < sSecond:
        cSecond = eSecond +60 - sSecond
    else:
        cSecond = eSecond - sSecond

    if eSecond < sSecond:
        if (eMinute -1) < sMinute:
            cMinute = eMinute - 1 + 60 - sMinute
        else:
            cMinute = eMinute - 1 - sMinute
    else:
        if eMinute < sMinute:
            cMinute = eMinute + 60 - sMinute
        else:
            cMinute = eMinute - sMinute

    if eSecond < sSecond:
        if (eMinute -1) < sMinute:
            cHour = eHour - 1 - sHour
        else:
            cHour = eHour - sHour
    elif eMinute < sMinute:
        cHour = eHour - 1 - sHour
    else:
        cHour = eHour - sHour
    
    # Format time => HH:MM:SS
    if cHour < 10:
        cHourStr = "0"+str(cHour)
    else:
        cHourStr = str(cHour)

    if cMinute < 10:
        cMinuteStr = "0"+str(cMinute)
    else:
        cMinuteStr = str(cMinute)
        
    if cSecond < 10:
        cSecondStr = "0"+str(cSecond)
    else:
        cSecondStr = str(cSecond)

    cTime = cHourStr+":"+cMinuteStr+":"+cSecondStr
    
    # print(cTime)
    return sTime+" "+cTime

def InitCmd():
    open(editPath+"/cmdfactory", 'w').write("")

def DealFiles(dealStyle=1):
    '''
    Walk file path
    Deal Style
    '''
    for root, dirs, files in os.walk(filePath):
        
        flgRmvb = False
        cmdCount = 1
        testFileCount =1
        
        InitCmd()
        
        for f in files:
            fileName = f
            # print("%d File Name: %s" %(testFileCount,fileName))
            # print("Full File Path: %s/%s\n" %(root,f))
            # fullFilePath = root + "/" + f
            # print("Full File Path: %s" %(fullFilePath))
            
            # Search Cmd file
            if fileName == "cmd":
                # print("Dir: "+"%s/%s\n" %(root, f))
                # print("Fined cmd file")

                cmdFile = open(root + "/cmd","r")
                testLineCount =1
                cmdLine = cmdFile.readline()
                
                flgLineFileName = False
                
                while cmdLine != "":
                    
                    # print("%d TCMD Line: %s" %(testLineCount,cmdLine))

                    formatCMDLine = cmdLine.strip()
                    
                    if formatCMDLine != "":
                        # Judge is filename or time
                        strJudge = formatCMDLine[0:2]
                        if not strJudge.isdigit():
                            # The line is filename
                            video_file_name = formatCMDLine
                            
                            flgLineFileName = True
                            #print("Line: " + cmdLine)
                
                            # cmdLine = cmdFile.readline()
                            countTime = 1
                            
                        elif strJudge.isdigit():
                        
                            # Find all times

                            # Get Time
                            strTime = GetTime(formatCMDLine)
                            timeUnits = strTime.split(" ")
                            sTime = timeUnits[0]
                            cTime = timeUnits[1]
                            
                            # Write CMD
                            if ".rmvb" in video_file_name:
                                # Copy the to edit file to Factory
                                cpStr = "cp " + "\"" + root + "/" + fileName + "\"" + " " + editPath + "/" + "A"
                                open(editPath+"/cmdfactory", 'a').write("%s \n" %(cpStr))

                                # Deal with Vedio Step 1 => ts
                                veStr = "ffmpeg -i A -an -vcodec libx264 -vbsf h264_mp4toannexb " + "-ss " + sTime + " -t " + cTime + " B.ts"
                                open(editPath+"/cmdfactory", 'a').write("%s \n" %(veStr))

                                # Deal with Vedio Step 2 => mp4
                                veStr = "ffmpeg -i B.ts -an -vcodec copy C.mp4"
                                open(editPath+"/cmdfactory", 'a').write("%s \n" %(veStr))

                                # Deal with Audio
                                auStr = "ffmpeg -i A -vn -f ogg -acodec libvorbis -ac 2 -ab 128k -ar 44100 " + "-ss " + sTime + " -t " + cTime + " D.ogg"
                                open(editPath+"/cmdfactory", 'a').write("%s \n" %(auStr))

                                # Make mkv file
                                mkStr = '"mkvmerge" -o "'+editPath+'/E.mkv"  "--forced-track" "0:no" "-d" "0" "-A" "-S" "-T" \
"--no-global-tags" "--no-chapters" "(" "'+editPath+'/C.mp4" ")" "--forced-track" "0:no" "-a" "0" "-D" "-S" "-T" "--no-global-tags" \
"--no-chapters" "(" "'+editPath+'/D.ogg" ")" "--track-order" "0:0,1:0"'
                                open(editPath+"/cmdfactory", 'a').write("%s \n" %(mkStr))

                                # Rename and Remove file
                                reStr = "mv E.mkv " + fileName + ".mkv"
                                open(editPath+"/cmdfactory", 'a').write("%s \n" %(reStr))
                                reStr = "rm A B.ts C.mp4 D.ogg"
                                open(editPath+"/cmdfactory", 'a').write("%s \n" %(reStr))
                                open(editPath+"/cmdfactory", 'a').write("%s \n" %(""))

                            elif ".avi" in video_file_name:
                                cmStr = "ffmpeg -i " + "\"" + root + "/" + fileName + "\"" + " -f mp4 -acodec libfdk_aac -vcodec libx264 -ss " \
                                        + sTime + " -t " + cTime + " " + "\"" + editPath + "/" + fileName + "-"+str(countTime)+".mp4" + "\"" 
                                open(editPath+"/cmdfactory", 'a').write("%s \n" %(cmStr))
                                open(editPath+"/cmdfactory", 'a').write("%s \n" %(""))
                                
                            elif ".mp4" in video_file_name:
                                cmStr = "ffmpeg -i " + "\"" + root + "/" + fileName + "\"" + " -f mp4 -acodec libfdk_aac -vcodec libx264 -ss " \
                                        + sTime + " -t " + cTime + " " + "\"" + editPath + "/" + fileName + "-"+str(countTime)+".mp4" + "\"" 
                                open(editPath+"/cmdfactory", 'a').write("%s \n" %(cmStr))
                                open(editPath+"/cmdfactory", 'a').write("%s \n" %(""))
                            
                            elif ".mkv" in video_file_name:
                                cmStr = "ffmpeg -i " + "\"" + root + "/" + fileName + "\"" + " -f mp4 -acodec libfdk_aac -vcodec libx264 -ss " \
                                        + sTime + " -t " + cTime + " " + "\"" + editPath + "/" + fileName + "-"+str(countTime)+".mp4" + "\"" 
                                open(editPath+"/cmdfactory", 'a').write("%s \n" %(cmStr))
                                open(editPath+"/cmdfactory", 'a').write("%s \n" %(""))
                            
                            cmdLine = cmdFile.readline()
                            countTime += 1
                                
                    testLineCount += 1
                    cmdLine = cmdFile.readline()
                   
            testFileCount += 1
def main():
    # print("This is a test!!!")
    DealFiles()
            
if __name__ == '__main__':
    main()

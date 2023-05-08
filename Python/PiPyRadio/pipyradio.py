#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" PiPyRadio with Tk GUI """
###############################################################################
#
#  pipyradio.py
#
#  Version 1.0 2023-05-08 (noy yet checked with pylint)
#
#  Copyright 2023 weigu <weigu@weigu.lu>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU
#  General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
###############################################################################
#
# I use the PiFi DAC+ board v2.0
# In config.txt (/boot)
# Switch on resp. add:
# dtparam=i2s=on
# dtoverlay=hifiberry-dacplus
# Comment the 2 following lines:
# #dtparam=audio=on 
# #dtoverlay=vc4-kms-v3d
# 
# Install music player with:
# sudo apt-get install mpd mpc 
# 
# Volume didn’t work. Had to add: 
# mixer_type "software"
# to /etc/mpd.conf
#
#  All infos on: <http://www.weigu.lu/sb-computer/pipyradio/index.html>
#
###############################################################################

from time import sleep
from pipyradio_gui import GUI
import subprocess # Needed for controlling the mpc player
from tkinter import *
import os

my_dir = "/home/weigu/PiPyRadio/"  # Change according your path
stations_txt_file = my_dir + "radio_stations.txt"
image_file = my_dir + "pipyradio_488.png"
station_playing_nr = 1
volume = 65 #0-100
stations = [] # Station Name list ( the same as in the IP radio list )
station_urls = [] # Station Name list ( the same as in the IP radio list )

flag_is_muted = False

# Command pipe for commanding the MPC player
def mpc_command(cmd):
    p = subprocess.Popen (cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    return  p.stdout.read().decode('utf-8').split('\n')

def print2textbox(window,text):
    print (text)
    window.label_song.config(text = text)
    window.mainWin.update_idletasks()

def play(window):
    global station_playing_nr, flag_is_muted
    try:
        station_playing_nr = stations.index(window.station_playing)+1
        mpc_command(['mpc', 'play', str(station_playing_nr)])        
        text = window.station_playing + " playing!"
        flag_is_muted = False
    except:
        text = "Error"
    print(text)    
    #print2textbox(window,text)

def play_first(window):
    global station_playing_nr, volume, flag_is_muted
    try:      
        mpc_out = mpc_command(['mpc', 'play', str(station_playing_nr)])
        title = mpc_out[0]
        mpc_command(['mpc', 'volume', str(volume)])        
        text = stations[station_playing_nr-1] + '   ' + title
        flag_is_muted = False
    except:
        text = "MPC Error while starting"
    print2textbox(window,text)

def mute(window):
    global flag_is_muted, volume
    try:
        if flag_is_muted: # Radio is muted,
            mpc_command(['mpc', 'play']) # unmute the radio,        
            text = "Unmuting!    Volume: " + str(volume) + "%"
            flag_is_muted = False
        else: # Here, the radio is playing, mute the radio
            mpc_command(['mpc', 'stop']) # Mute (stop the MPC player)        
            text = "Muting!    Volume: " + str(volume) + "%"
            flag_is_muted = True
    except:
        text = "Error"               
    print2textbox(window,text)    

def vol_up(window):
    global flag_is_muted, volume
    try:
        mpc_command(['mpc', 'play']) # in case an active mute, unmute the radio
        mpc_command(['mpc', 'volume', '+5']) # Increase audio lever with 5        
        volume += 5
        if volume > 100:
            volume = 100
        text = "Volume UP!    Volume: " + str(volume) + "%"
        flag_is_muted = False
    except:
        text = "Error"
    print2textbox(window,text)    
    
def vol_down(window):
    global flag_is_muted, volume
    try:
        mpc_command(['mpc', 'play']) # in case an active mute, unmute the radio
        mpc_command(['mpc', 'volume', '-5']) # Increase audio lever with 5        
        volume -= 5
        if volume < 0:
            volume = 0
            flag_is_muted = True
        text = "Volume DOWN!    Volume: " + str(volume) + "%"
    except:
        text = "Error"
    print2textbox(window,text)
    
    

#---- MAIN --------------------------------------------------------------------

def main():    
    """setup and mainloop"""
    print("Program started!")
    ''' Get the Stations '''
    try:
        for x in open(stations_txt_file,'r'): # Get the station file
            a = x.split('|') # Split only for the station names 
            stations.append(a[0]) # Put the station names in the Station Name List
            station_urls.append(a[1].strip())        
            mpc_command(['mpc', 'clear'])
            for station_url in station_urls:
                mpc_command(['mpc', 'add', station_url])   
    except FileNotFoundError:
        print("No such file or directory: " + stations_txt_file)
        exit()


    window = GUI()
    window.image = image_file
    window.station_names = stations
    window.number_of_stations = len(stations)        
    sleep(1)
    play_first(window)
    vol_displ_counter = 0
    #-----------------------------------------------------------------------------
    # MAIN LOOP
    #-----------------------------------------------------------------------------
    try:
        while (window.flag_exit == False):
            if window.flag_shutdown == True:
                os.system("shutdown now")
            if window.flag_next==True:                
                window.flag_next=False
            if window.flag_play==True:                
                play(window)
                window.flag_play=False
            if window.flag_vol_up==True:
                vol_displ_counter = 6
                vol_up(window)
                window.flag_vol_up=False
            if window.flag_vol_down==True:
                vol_displ_counter = 6
                vol_down(window)
                window.flag_vol_down=False
            if window.flag_mute==True:                
                mute(window)
                window.flag_mute=False
            sleep(0.3)
            if not flag_is_muted:
                if vol_displ_counter != 0:
                    vol_displ_counter -= 1                        
                else:        
                    mpc_out = mpc_command(['mpc', 'current'])                
                    title = mpc_out[0]
                    text = stations[station_playing_nr-1] + '   ' + title
                    print2textbox(window,text)
    except KeyboardInterrupt:
        print("Keyboard interrupt by user")        
    print("closed by window")
    mpc_command(['mpc', 'stop']) # Mute (stop the MPC player) 
    
main() 

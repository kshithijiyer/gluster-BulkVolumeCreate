#!/usr/bin/python
"""

BulkVolumeCreate - Create Glusterfs Volume in bulk.

Description:
A tool to generate large number of glusterfs volumes.

Supported volume types:
1) Distribute
2) Arbiter (Both distributed and pure.)
3) Replica (Both distributed and pure.)
4) EC (Both distributed and pure.)

Author: Kshithij Iyer
Date: 3/11/2018
Email: kshithij.ki@gmail.com
"""

#imports needed by the script.
from subprocess import check_output
from version import __version__
import os
import argparse
import time
import subprocess

#Supportive Functions.
def glusterd_status_check():
   "Function to check if glusterd is running on the node or not."
   try:
      check_output(["pidof","glusterd"])
      return True
   except subprocess.CalledProcessError:
      print("[FAILED]:Glusterd not running on node!")
      return False


#Create Functions.
def create_dist_volume(hosts_To_bricks,Number_of_bricks,vol_name):
    "This function creates simple distribute volumes."
    command="gluster v create "+str(vol_name)+"  "
    counter=0
    while Number_of_bricks>0:
       command=command+hosts_To_bricks[counter]+vol_name+"_"+str(time.time())+" "
       counter+=1
       Number_of_bricks-=1
       if counter+1==len(hosts_To_bricks):
          counter=0
    if glusterd_status_check()==True:
       if os.system(command)==0:
          print("[INFO]: Volume created successfully.")
       else:
          print("[FAILED]: Volume creation failed.")
    else:
       print("[FAILED]:Command not executed as glusterd check failed!")
       

def create_arb_volume(hosts_To_bricks,Number_of_bricks,vol_name):
    "This function creates arbiter volumes."
    command="gluster v create "+str(vol_name)+" replica 3 arbiter 1 "
    counter=0 
    while Number_of_bricks>0:
       command=command+hosts_To_bricks[counter]+vol_name+"_"+str(time.time())+" "
       counter+=1
       Number_of_bricks-=1
       if counter+1==len(hosts_To_bricks):
          counter=0
    if glusterd_status_check()==True:
       if os.system(command)==0:
          print("[INFO]: Volume created successfully.")
       else:
          print("[FAILED]: Volume creation failed.")
    else:
       print("[FAILED]:Command not executed as glusterd check failed!")


def create_rep_volume(hosts_To_bricks,Number_of_bricks,vol_name,replica_count):
    "This function creates replicate volumes."
    command="gluster v create "+str(vol_name)+" replica "+str(replica_count)+" "
    counter=0
    while Number_of_bricks>0:
       command=command+hosts_To_bricks[counter]+vol_name+"_"+str(time.time())+" "
       counter+=1
       Number_of_bricks-=1
       if counter+1==len(hosts_To_bricks):
          counter=0
    if glusterd_status_check()==True:
       if os.system(command)==0:
          print("[INFO]: Volume created successfully.")
       else:
          print("[FAILED]: Volume creation failed.")
    else:
       print("[FAILED]:Command not executed as glusterd check failed!")


def create_ec_volume(hosts_To_bricks,Number_of_bricks,vol_name,disperse_params):
    "This function creates ec volumes."

    command="gluster v create "+str(vol_name)+" disperse-data "+str(disperse_params[0])+" redundancy "+str(disperse_params[1])+" "
    counter=0
    while Number_of_bricks>0:
       command=command+hosts_To_bricks[counter]+vol_name+"_"+str(time.time())+" "
       counter+=1
       Number_of_bricks-=1
       if counter+1==len(hosts_To_bricks):
          counter=0
    if glusterd_status_check()==True:
       command=command+" force"
       if os.system(command)==0:
          print("[INFO]: Volume created successfully.")
       else:
          print("[FAILED]: Volume creation failed.")
    else:
       print("[FAILED]:Command not executed as glusterd check failed!")


#Main function
       
def main():
   
   #Setting up command line arguments.
   parser=argparse.ArgumentParser(description="Create Glusterfs volumes in bulk.")
   parser.add_argument('-f',"--confg_file",type=str,required=True,dest="Config_File",help="config file with hostnames and brick paths")
   parser.add_argument('-t',"--type",type=str,default="dist",dest="Volume_type",choices=["ec","dist","rep","arb"],help="type of volumes to be created")
   parser.add_argument('-e',"--expression",type=str,default="None",dest="Expression",help="expression to define the configuration of the volume")
   parser.add_argument('-n','--number',type=int,default=1,dest="Number_of_volumes",help="number of volumes to be created")
   parser.add_argument('-p','--prefix',type=str,default="",dest="prefix",help="prefix for volume names")
   parser.add_argument('-v', '--version',action='version',version='%(prog)s {version}'.format(version=__version__))
   args=parser.parse_args()

   #Reading the config file.
   try:   
      Config_file=open(args.Config_File,'r')

      print("[Info]:Reading from",Config_file.name,"config file.")
      hosts=Config_file.readline().replace("\n","").replace(" ","").split("=")
      hosts=hosts[1].split(',')
      bricks=Config_file.readline().replace("\n","").replace(" ","").split("=")
      bricks=bricks[1].split(',')
      vol_name=Config_file.readline().replace("\n","").replace(" ","").split("=")
      vol_name=vol_name[1]
      print("[Info]:Closing config file.")
      
      Config_file.close()
   except FileNotFoundError:
      print("[FAILED]: Configuration file not found!")

   #Calculating all the possible brick paths.
   hosts_To_bricks=[]
   for brick in bricks:
      for host in hosts: 
         hosts_To_bricks.append(host+str(":")+brick)
         
   #Setting up the prefix to volume name if option provided
   prefix=""
   if args.prefix!='':
      prefix=args.prefix+"_"

   #Checking volume type and calling the sutable function.
   if args.Volume_type=="dist":
      try:
         number_of_bricks=int(args.Expression)
         for number in range(0,args.Number_of_volumes):
            name=prefix+vol_name+"_"+str(number)
            create_dist_volume(hosts_To_bricks,number_of_bricks,name)
      except ValueError:
         print("[FAILED]:Volume type and expression don't match!")
         print("[INFO]:The expression for distribute should be as follows: N")
   elif args.Volume_type=="arb":
      try:
         numbers=args.Expression.lower().split("x")
         number_of_bricks=int(numbers[0])*(2+1)
         for number in range(0,args.Number_of_volumes):
            name=prefix+vol_name+"_"+str(number)
            create_arb_volume(hosts_To_bricks,number_of_bricks,name)
      except ValueError:
         print("[FAILED]:Volume type and expression don't match!")
         print("[INFO]:The expression for arbiter should be as follows: Nx(2+1)")
   elif args.Volume_type=="rep":
      try:
         numbers=args.Expression.lower().split("x")
         number_of_bricks=int(numbers[0])*int(numbers[1])
         for number in range(0,args.Number_of_volumes):
            name=prefix+vol_name+"_"+str(number)
            create_rep_volume(hosts_To_bricks,number_of_bricks,name,numbers[1])
      except ValueError:
         print("[FAILED]:Volume type and expression don't match!")
         print("[INFO]:The expression for replica should be as follows: AxB")
   elif args.Volume_type=="ec":
      try:
         numbers=args.Expression.lower().split("x")
         numbers2=numbers[1].split("+")
         number_of_bricks=int(numbers[0])*(int(numbers2[0])+int(numbers2[1]))
         for number in range(0,args.Number_of_volumes):
            name=prefix+vol_name+"_"+str(number)
            create_ec_volume(hosts_To_bricks,number_of_bricks,name,numbers2)
      except ValueError:
         print("[FAILED]:Volume type and expression don't match!")
         print("[INFO]:The expression for EC should be as follows: Nx(A+B)")


if __name__ == "__main__":
   main()

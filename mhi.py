#import sys, os
#sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/Mitsubishi-WF-RAC-Integration/custom_components/mitsubishi-wf-rac")
from sys import argv
from aenum import StrEnum
from wfrac.repository import Repository
from wfrac.rac_parser import RacParser
from wfrac.models.aircon import AirconStat
from datetime import datetime
import os
import logging

import json

import sys
import getopt

#import asyncio


def print_values():    
    #clear = lambda: os.system('clear')
    #clear()
    print ("-------------------- " + date.time().strftime("%H:%M:%S") + " ---------------------")
    print (" IP : " + KLIMA_HOSTNAME + " | PORT : " + str(KLIMA_PORT) )
    print (" Device ID : " + device_id)
    print (" Airco ID : " + airco_id)
    print (" Operator ID used : " + operator_id)
    print (" RemoteList :" + str(stats["remoteList"]))
    print ("---------------------------------------------------")
    print (" Status : " + klima_status_bool + "(" + str(klima_status) + ") | Preset Temp. : " + klima_presettemp + "°C")
    print (" Indoor Temp : " + klima_indoortemp + "°C  | Outdoor Temp. : " + klima_outdoortemp + "°C")
    print (" Modus : " + klima_modus_txt + "(" + klima_modus + ")")
    print ("---------------------------------------------------")
    print (" Fan : " + klima_fanspeed + "(" + klima_airflow + ")")
    print (" Vert. Direction : " + klima_dirud + "(" + klima_windUD + ")")
    print (" Hor. Direction : " + klima_dirlr + "(" + klima_windLR + ")")
    print (" 3D Auto : " + klima_3dauto_bool + "(" + str(klima_3dauto) + ")")
    print ("---------------------------------------------------")    
    print (" LED Status : " + klima_led_bool + "(" + str(klima_led) + ")" )
    print (" ??autoHeating : " + klima_autoheat)
    print (" ??Vacant : " + klima_vacant)
    print (" ??CoolHotJudge : "  + klima_coolhotjudge)
    print (" Energy used : " + klima_strom)
    print (" Error code : " + klima_error)




#logging.basicConfig(level=logging.DEBUG)


show_json = False
show_print = False

USAGE = f"Usage: python {sys.argv[0]} [-h|--help] [-j|--json] [-p|--print] ip-adres"

args = sys.argv[1:]
if not args:
    print("not args")
    raise SystemExit(USAGE)

try:
    options, arguments = getopt.getopt(
        args,                              # Arguments
        'jph',                            # Short option definitions
        ["json", "help", "print"]) # Long option definitions
except getopt.GetoptError:
    print("GetoptError")
    print(USAGE)
    sys.exit(2)   
    
separator = "\n"
#print ("Arguments: " + str(arguments))
#print ("Options: " + str(options))
for o, a in options:
    if o in ("-h", "--help"):
        print(USAGE)
        sys.exit()
    if o in ("--json"):
        show_json = True
        show_print = False
    if o in ("--print"):
        show_json = False
        show_print = True
    if o in ("-s", "--separator"):
        separator = a
if not arguments or len(arguments) > 1:
    print("To many arguments")
    raise SystemExit(USAGE)
#try:
#    operands = [int(arg) for arg in arguments]
#except:
#    print("except")
#    raise SystemExit(USAGE)

KLIMA_HOSTNAME = arguments[0]
#print ("Use ipaddress: " + KLIMA_HOSTNAME)


# KLIMAANLAGE
#KLIMA_HOSTNAME = "192.168.5.184"
KLIMA_PORT = 51443

operator_id = "1"
device_id = "2"
    
r = Repository(hostname=KLIMA_HOSTNAME, port=KLIMA_PORT, operator_id=str(operator_id), device_id=str(device_id))
try:
    details = r.get_info()
except Exception as e: 
    print("Error: Cannot get get_info()", file=sys.stderr)
    print(e, file=sys.stderr)
    sys.exit(2) 

#print(details)
#print(str(details["airconId"]))

date = datetime.now()


#loop = asyncio.get_event_loop() 
#stats = loop.run_until_complete(r.get_aircon_stats())
try:
    stats = r.get_aircon_stats()
except Exception as e: 
    print("Error: Cannot get get_aircon_stats()", file=sys.stderr)
    print(e, file=sys.stderr)
    sys.exit(2) 

par = RacParser()
aircon = par.translate_bytes(stats["airconStat"])

airco_id = str(details["airconId"]) #r.get_airco_id()
operator_id = stats["remoteList"][0]
#print (stats["remoteList"])

if str(aircon.Operation) == "True": klima_status = 1
if str(aircon.Operation) == "False": klima_status = 0
klima_status_bool = str(aircon.Operation).lower()
klima_presettemp = str(aircon.PresetTemp)
    
if str(stats["ledStat"]) == "0": klima_led_bool = "false"
if str(stats["ledStat"]) == "1": klima_led_bool = "true"
klima_led = int(str(stats["ledStat"]))
klima_autoheat = str(stats["autoHeating"])
klima_indoortemp = str(aircon.IndoorTemp)
klima_outdoortemp = str(aircon.OutdoorTemp)
    
klima_airflow = str(aircon.AirFlow)
if str(aircon.AirFlow) == "0": klima_fanspeed = "Auto"
if str(aircon.AirFlow) == "1": klima_fanspeed = "Lowest"
if str(aircon.AirFlow) == "2": klima_fanspeed = "Low"
if str(aircon.AirFlow) == "3": klima_fanspeed = "High"
if str(aircon.AirFlow) == "4": klima_fanspeed = "Highest"
    
klima_modus = str(aircon.OperationMode)
if str(aircon.OperationMode) == "0": klima_modus_txt = "Auto"
if str(aircon.OperationMode) == "1": klima_modus_txt = "Cooling"
if str(aircon.OperationMode) == "2": klima_modus_txt = "Heating"
if str(aircon.OperationMode) == "3": klima_modus_txt = "Fan"
if str(aircon.OperationMode) == "4": klima_modus_txt = "Dry"
    
klima_windUD = str(aircon.WindDirectionUD)
if str(aircon.WindDirectionUD) == "0": klima_dirud = "Auto"
if str(aircon.WindDirectionUD) == "1": klima_dirud = "High"
if str(aircon.WindDirectionUD) == "2": klima_dirud = "Middle"
if str(aircon.WindDirectionUD) == "3": klima_dirud = "Deep"
if str(aircon.WindDirectionUD) == "4": klima_dirud = "Deepest"
    
klima_windLR = str(aircon.WindDirectionLR)
if str(aircon.WindDirectionLR) == "0": klima_dirlr = "Left/Right Auto"
if str(aircon.WindDirectionLR) == "1": klima_dirlr = "Left / Left"
if str(aircon.WindDirectionLR) == "2": klima_dirlr = "Left / Middle"
if str(aircon.WindDirectionLR) == "3": klima_dirlr = "Middle / Mitte"
if str(aircon.WindDirectionLR) == "4": klima_dirlr = "Middle / Right"
if str(aircon.WindDirectionLR) == "5": klima_dirlr = "Right / Right"
if str(aircon.WindDirectionLR) == "6": klima_dirlr = "Left / Right"
if str(aircon.WindDirectionLR) == "7": klima_dirlr = "Right / Left"
    
klima_3dauto_bool = str(aircon.Entrust).lower()
if str(aircon.Entrust) == "True": klima_3dauto = 1
if str(aircon.Entrust) == "False": klima_3dauto = 0
    
klima_vacant = str(aircon.Vacant)
klima_coolhotjudge = str(aircon.CoolHotJudge).lower()
klima_strom = str(aircon.Electric)
klima_error = str(aircon.ErrorCode)
    
if show_json:
    #print json string
    jsonStr = json.dumps(aircon.__dict__)
    print(jsonStr)

if show_print:
    print_values()



import xml.etree.ElementTree as ET
import plistlib
import json
import re

#Dictionary (char tag: string fulltag)
tag_dict = {
    'k': 'key',
    'i': 'integer',
    's': 'string',
    'd': 'dict',
    't': 'true',
    'f': 'false',
    'r': 'real'
}

#Iterates over every element in the tree and changes them tags into the char form
def RecursiveRenameInverse(element):

    for subelement in element:
        subelement.tag = subelement.tag[0]
        if subelement.tag == 'd':
            RecursiveRenameInverse(subelement)

#Iterates over every element in the tree and changes them tags
def RecursiveRename(element):

    for subelement in element:
        subelement.tag = tag_dict[subelement.tag]
        if subelement.tag == 'dict':
            RecursiveRename(subelement)

#Restore the plist tags from the plist
def RestoreXMLTags(xml_stream, inverse=False):
    plist = ET.fromstring(xml_stream)

    if inverse:
        #Rename tags given the xml dict element
        RecursiveRenameInverse(plist[0])
    else:
        #Rename tags given the xml dict element
        RecursiveRename(plist[0])

    #Returns XML stream with plist format. If it's reverse we must clean up the xml so it matches the GD format
    if inverse:
        raw = ET.tostring(plist, xml_declaration=True).decode('ascii')
        gd_xml = raw

        #We must convert round floating points into int. EJ: 1.0 -> 1
        floats = re.findall('-?\d+\.0<', raw)
        for round in floats:
            gd_xml = gd_xml.replace(round, round.split('.')[0] + '<')

        #Fix exponents as well
        exponents = re.findall('\d+\.\d+e\-0+', raw)
        for exponent in exponents:
            gd_xml = gd_xml.replace(exponent, exponent + '0')
        
        #Cleanup whitespaces, tabs and quotes
        gd_xml = gd_xml.replace('\n','').replace('\t','').replace('\'','"')
        gd_xml = gd_xml.replace('<?xml version="1.0" encoding="us-ascii"?><plist version="1.0">','<?xml version="1.0"?><plist version="1.0" gjver="2.0">')
        return gd_xml.encode('ascii')
    else:
        return ET.tostring(plist, xml_declaration=True)

#Parses the xml stream into a plist object
def ParsePlist(xml_stream):

    #Parses the plist if it's given by bytes
    plist = plistlib.loads(xml_stream) if type(xml_stream) != type(dict()) else xml_stream
    return plistlib.dumps(plist, sort_keys=False)

#Retrieves the level data by passing the level's name
def GetLevelByString(xml_stream, lvl_string):

    #Parses the plist if it's given by bytes
    plist = plistlib.loads(xml_stream) if type(xml_stream) != type(dict()) else xml_stream
    levels = plist['LLM_01']

    #Iterate through the array of levels
    for level in levels:
        if level == '_isArr':
            continue
        
        #Get the one with the same title
        if (levels[level]['k2'] == lvl_string):
            return levels[level]['k4'].encode('ascii')
        
#Retrieves the level data by passing the level's offset (From top to bottom)
def GetLevelByOrder(xml_stream, offset):

    #Parses the plist if it's given by bytes
    plist = plistlib.loads(xml_stream) if type(xml_stream) != type(dict()) else xml_stream
    levels = plist['LLM_01']

    #Iterate through the array of levels
    for level in levels:
        if level == '_isArr':
            continue
        
        #Get the one with the same tag
        if (level == 'k_'+str(offset)):
            return levels[level]['k4'].encode('ascii')

#Returns a tag element from the xml stream with the given key
def GetXMLTag(xml_stream, key):
    
    #Parses the plist if it's given by bytes
    plist = plistlib.loads(xml_stream) if type(xml_stream) != type(dict()) else xml_stream

    #Iterate through the array of levels
    for child in plist:
        #Get the desired key
        if (child == key):
            return plist[child]

#Returns a tag element from the xml stream with the given key
def SetXMLTag(xml_stream, key, value):

    #Parses the plist if it's given by bytes
    plist = plistlib.loads(xml_stream) if type(xml_stream) != type(dict()) else xml_stream
    
    for child in plist:
        #Get the desired key and set it's value
        if (child == key):
            plist[key] = value
    return plist

#Parses a level stream into a JSON stream
def LevelToJSON(level_stream):

    level_dict = {'data': []}
    level = level_stream.decode('ascii').split(';')

    #Iterate through each object in the level
    for data in level:
        if not data:
            continue

        #Split data into array, then get pairs to make a dict
        properties = {}
        data_pairs = data.split(',')

        #Group by tuple of (key, value)
        for i in range(0, len(data_pairs), 2):
            pair = data_pairs[i:i+2]
            properties[pair[0]] = pair[1]
        
        #Add the dictionary into the objects array
        level_dict['data'].append(properties)

    #Return a JSON stream containing level data
    return json.dumps(level_dict).encode('ascii')

#Parses a JSON stream into a level stream
def JSONToLevel(json_stream):
    
    level_stream = b''
    level = json.loads(json_stream)

    #Cleanup the stream by removing JSON formatting
    for object in level['data']:
        clean = json.dumps(object).replace('{','').replace('}','').replace(':',',').replace(' ','').replace('"','')
        level_stream += clean.encode('ascii') + b';'
    return level_stream

#Iterates over every element in the tree and changes them tags into the generic ones. Recursion gives me headaches (Especially the inverse ones)
def RecursiveRenameJSONInverse(data, dictionary):
    
    #First need to check if we are working with a dict or a list
    if (type(data) == type(dict())):
        #Make a copy and iterate through it
        temp = data.copy()
        for key in temp.keys():
            #Creates a list of dictionary keys whose values are equal to the current key
            key_list = [dict_key for dict_key, dict_value in dictionary.items() if key == dict_value]
            new_key = key_list[0] if key_list else key
            #If our key was redefined, update the object accordingly
            data[new_key] = data.pop(key)
            RecursiveRenameJSONInverse(data[new_key], dictionary)
    elif (type(data) == type(list())):
        #If we get an array, just iterate through each element with recursion
        for obj in data:
            RecursiveRenameJSONInverse(obj, dictionary)

#Iterates over every element in the tree and changes them tags. Recursion gives me headaches :D
def RecursiveRenameJSON(data, dictionary):
    
    #First need to check if we are working with a dict or a list
    if (type(data) == type(dict())):

        #Make a copy and iterate through it
        temp = data.copy()
        for key in temp.keys():
            #Reasign the new keys into the original dict
            new_key = dictionary.get(key) if dictionary.get(key) else key
            #If our key was redefined, update the object accordingly
            data[new_key] = data.pop(key)
            RecursiveRenameJSON(data[new_key], dictionary)
    elif (type(data) == type(list())):
        #If we get an array, just iterate through each element with recursion
        for obj in data:
            RecursiveRenameJSON(obj, dictionary)

#Rename the properties from the JSON stream
def RenameJSONTags(json_stream, dictionary, inverse=False):

    json_level = json.loads(json_stream)
    parsed_dict = json.loads(dictionary)

    #Rename tags given the xml dict element
    if inverse:
        RecursiveRenameJSONInverse(json_level, parsed_dict)
    else:
        RecursiveRenameJSON(json_level, parsed_dict)

    #Returns a JSON stream with renamed properties
    return json.dumps(json_level, indent=2).encode('ascii')
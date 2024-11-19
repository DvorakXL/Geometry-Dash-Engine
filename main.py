import os
import utils
import ciphergd
import parsergd
import hashlib
import gdlevel.orthographic as orthographic
import gdlevel.triggers as triggers
import gdlevel.objects as objects

def Main():
    #Open the save file + backup file
    LEVELS_PATH = utils.ABSOLUTE_PATH + utils.GD_PATH
    f = open(LEVELS_PATH + '.dat', 'rb')
    f2 = open(LEVELS_PATH + '2.dat', 'rb')

    #Read file and make backup just in case ;)
    stream = f.read()
    stream2 = f2.read()
    f.close()
    f2.close()

    try:
        copy = open('GeometryDash/CCLocalLevels.dat', 'wb')
        copy2 = open('GeometryDash/CCLocalLevels2.dat', 'wb')
    except:
        os.mkdir('GeometryDash')
        copy = open('GeometryDash/CCLocalLevels.dat', 'wb')
        copy2 = open('GeometryDash/CCLocalLevels2.dat', 'wb')

    copy.write(stream)
    copy.close()

    copy2.write(stream2)
    copy2.close()

    #Decrypts the save file and saves it
    parsed_file = open('CCLocalLevels.xml', 'wb')
    raw_data = ciphergd.Decryt(stream)

    #Restore tag names and replace the file
    pl = parsergd.RestoreXMLTags(raw_data)
    parsed_file.write(parsergd.ParsePlist(pl))
    parsed_file.close()

    #Get the level data and save it into a json file
    json = open('level.json', 'wb')
    original_json = open('original.json', 'wb')

    #Decrypt the first level and save it into a json
    order = 0
    level = ciphergd.Decryt(parsergd.GetLevelByOrder(pl, order), xor=False)
    json_level = parsergd.LevelToJSON(level)

    #Redefines the JSON properties to make it readable. (this step is optional but my memory is dogshit)
    json_dictionary = open('level-dictionary.json','rb')
    properties = json_dictionary.read()
    json_dictionary.close()
    json_level = parsergd.RenameJSONTags(json_level, properties)

    #Write a json with the original unmodified level
    original_json.write(json_level)
    original_json.close()

    #This is going into a new file later on.
    json_level = parsergd.json.loads(json_level)

    #This deletes every object. BE CAREFUL!
    json_level['data'] = [json_level['data'][0]]

    #Iterate through each move trigger vertex times
    rotation = 360.0
    res = 40
    length = 10

    #Generate a cube without perspective
    json_level['data'] += orthographic.Quad([[-2,-2,-2],[-2,2,-2],[2,2,-2],[2,-2,-2]], 1).Spawn().Rotate((0,8), rotation, length, res).data
    json_level['data'] += orthographic.Quad([[-2,-2,2],[-2,2,2],[2,2,2],[2,-2,2]], 5).Spawn().Rotate((0,12), rotation, length, res).data

    json_level['data'] += [{
      "id": "2903",
      "x": "135",
      "y": "105",
      "155": "1",
      "156": "2",
      "is_trigger": "1",
      "202": "8",
      "203": "1",
      "204": "2",
      "205": "3",
      "206": "4",
      "207": "1",
      "209": "1",
      "456": "1"
    }]

    json_level['data'] += [{
      "id": "2903",
      "x": "-315",
      "y": "45",
      "155": "1",
      "156": "2",
      "is_trigger": "1",
      "202": "8",
      "203": "1",
      "204": "4",
      "205": "2",
      "206": "3",
      "207": "1",
      "209": "1",
      "456": "1"
    },
    {
      "id": "1914",
      "x": "-315",
      "y": "375",
      "155": "3",
      "is_trigger": "1",
      "easing_rate": "2",
      "target_2": "1",
      "213": "1"
    },
    {
      "id": "2903",
      "x": "-315",
      "y": "75",
      "155": "1",
      "156": "2",
      "is_trigger": "1",
      "202": "8",
      "203": "5",
      "204": "8",
      "205": "6",
      "206": "7",
      "207": "1",
      "209": "2",
      "456": "1"
    },
    {
      "id": "2903",
      "x": "-315",
      "y": "105",
      "155": "1",
      "156": "2",
      "is_trigger": "1",
      "202": "8",
      "203": "5",
      "204": "1",
      "205": "6",
      "206": "2",
      "207": "1",
      "209": "3",
      "456": "1"
    },
    {
      "id": "2903",
      "x": "-315",
      "y": "135",
      "155": "1",
      "156": "2",
      "is_trigger": "1",
      "202": "8",
      "203": "5",
      "204": "1",
      "205": "6",
      "206": "2",
      "207": "1",
      "209": "3",
      "456": "1"
    },
    {
      "id": "2903",
      "x": "-315",
      "y": "165",
      "155": "1",
      "156": "2",
      "is_trigger": "1",
      "202": "8",
      "203": "1",
      "204": "4",
      "205": "5",
      "206": "8",
      "207": "1",
      "209": "4",
      "456": "1"
    },
    {
      "id": "2903",
      "x": "-315",
      "y": "195",
      "155": "1",
      "156": "2",
      "is_trigger": "1",
      "202": "8",
      "203": "2",
      "204": "3",
      "205": "6",
      "206": "7",
      "207": "1",
      "209": "5",
      "456": "1"
    },
    {
      "id": "2903",
      "x": "-315",
      "y": "225",
      "155": "1",
      "156": "2",
      "is_trigger": "1",
      "202": "8",
      "203": "4",
      "204": "8",
      "205": "3",
      "206": "7",
      "207": "1",
      "209": "6",
      "456": "1"
    }]
    #Generate ascii frames

    #Bad Apple

    # ascii_file = open('ascii-generate/output.json', 'rb')
    # ascii_frames = parsergd.json.loads(ascii_file.read())

    

    # json_level['data'] += [{
    #   "id": "901",
    #   "x": "-15",
    #   "y": "2295",
    #   "is_trigger": "1",
    #   "target": "1",
    #   "move_x": "0",
    #   "move_y": "0",
    #   "duration": "999",
    #   "easing": "0",
    #   "easing_rate": "2",
    #   "follow_x": "1"
    # },
    # {
    #   "id": "1007",
    #   "x": "-15",
    #   "y": "2325",
    #   "is_trigger": "1",
    #   "target": "1",
    #   "duration": "-2.0037",
    #   "opacity": "0"
    # },
    # {
    #   "id": "747",
    #   "x": "-29",
    #   "y": "45",
    #   "group": "1",
    #   "z_order": "10",
    #   "54": "2350"
    # },
    # {
    #   "id": "467",
    #   "x": "-15",
    #   "y": "2355",
    #   "group": "1",
    #   "z_order": "3"
    # }]

    # frames_per_second = 1
    # group = 2
    # for frame_n, value in ascii_frames.items():
    #     frame = value[0].replace(';','\n')
    #     frame_n = int(frame_n)

    #     #Split to frames per second columns
    #     if frame_n % frames_per_second == 0:
    #         group += 1

    #         toggle_position_on = ((frame_n-1)*30, 210)
    #         toggle_position_off = ((frame_n-1)*30+frames_per_second*30, 210)

    #         json_level['data'] += triggers.Toggle(toggle_position_on, group, 1).Spawn()
    #         json_level['data'] += triggers.Toggle(toggle_position_off, group, 0).Spawn()
    #         json_level['data'] += triggers.Toggle((0,group*30), group, 0).Spawn()

    #     move_position = (frame_n*30, 180)
    #     json_level['data'] += triggers.Move(move_position, group, (0,-50*30), 0).Spawn()
    #     frame_position = (frame_n+3, 77+(frame_n % frames_per_second)*50)
    #     json_level['data'] += objects.Text(frame_position, frame, group, 0.15).Spawn().data
    json_level = parsergd.json.dumps(json_level, indent=2).encode('utf-8')

    json.write(json_level)
    json.close()

    json_level = parsergd.RenameJSONTags(json_level, properties, inverse=True)
    modified_lvl = ciphergd.Encrypt(parsergd.JSONToLevel(json_level), xor=False, compression=6)

    tree = parsergd.GetXMLTag(pl, 'LLM_01')
    level = parsergd.GetXMLTag(tree, 'k_'+str(order))

    parsergd.SetXMLTag(level, 'k4', modified_lvl.decode('ascii'))
    parsergd.SetXMLTag(tree, 'k_0', level)
    pl = parsergd.SetXMLTag(pl, 'LLM_01', tree)
    
    new_xml = open('CCLocalLevels.xml', 'wb')
    new_xml.write(parsergd.ParsePlist(pl))
    new_xml.close()

    clean_tree = parsergd.RestoreXMLTags(parsergd.ParsePlist(pl), inverse=True)

    #Add CRLF bytes.
    final = ciphergd.Encrypt(clean_tree) + chr(11).encode('utf-8')

    gd_level = open(LEVELS_PATH + '.dat', 'wb')
    gd2_level = open(LEVELS_PATH + '2.dat', 'wb')

    #Overwrite the level file with the new changes. 
    gd_level.write(final)
    gd2_level.write(final)

    #Cleanup files
    gd_level.close()
    gd2_level

    print('Hashes from CCLocalLevels.dat')
    print(hashlib.sha256(stream).hexdigest())
    print(hashlib.sha256(final).hexdigest())

if __name__ == "__main__":
    Main()
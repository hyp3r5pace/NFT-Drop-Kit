import os
import json
import shutil

def main():
    print("Generating JSON files for the assets...")
    filelist = os.listdir('assets')
    # creating a map to store the name of json files in assets
    jsonList = {}
    for file in filelist:
        if file.endswith('.json'):
            jsonList[file] = 1
    
    # format of json file for each image
    data = {
    "name": "Hinata Shoyo",
    "symbol": "",
    "image": "Hinata_Shoyo.png",
    "properties": {
      "files": [
        {
          "uri": "Hinata_Shoyo.png",
          "type": "image/png"
        }
      ],
      "creators": [
        {
          "address": "",
          "share": 100
        }
      ]
    }
  }

    # loop to create associating json files for png files in assets folder
    for file in filelist:
        if file.endswith('.png'):
            if jsonList.get(file[:-4]+'.json'):
                jsonList[file[:-4]+'.json'] += 1
            else:
                with open('assets/' + file[:-4]+'.json', 'w') as f:
                    data['name'] = file[:-4].replace('_', ' ')
                    data['image'] = file
                    data['properties']['files'][0]['uri'] = file
                    json.dump(data, f, ensure_ascii=False, indent=4)
    
    for key in jsonList:
        if jsonList[key] == 1:
            os.remove('assets/' + key)
    
    print('✔️', 'JSON Files generated for the assets')

if __name__ == "__main__":
    main()
    

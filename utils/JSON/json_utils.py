import json

# the simple funtion to generate the JSON
def jsonSimpleGenerate(key, value):
    try:
        data = {}
        data[key] = value
        jsonData = json.dumps(data)
        return jsonData
    except Exception as e:
        raise e
        return -1

def jsonSimpleParser(jsonStr, key):
    try:
        print("String JSON: " + jsonStr)
        print("key: " + key)
        if key not in jsonStr:
            return None
        else:  
            return json.loads(jsonStr) #.decode('utf-8')
    except Exception as e:
        raise e
        return -1

def jsonDoubleGenerate(json_1, json_2):
    try:
        merged = {key: value for (key, value) in (json_1.items() + json_2.items())}
        jsonData = json.dumps(merged)
        print(str(jsonData))
        return jsonData
    except Exception as e:
        raise e
        return -1

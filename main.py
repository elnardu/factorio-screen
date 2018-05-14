from blueprints import *
import json, math

SIZE = 9
ENTITY_ID = 1

def buildDisplayModel(data):
    entities = data['blueprint']['entities']
    result = [[None] * SIZE for _ in range(SIZE)]
    coordNorm = math.floor(SIZE/2)
    for e in entities:
        result[
            e['position']['y'] + coordNorm
        ][
            e['position']['x'] + coordNorm
        ] = e['control_behavior']['circuit_condition']['first_signal']['name']

    print(json.dumps(result, indent=2, sort_keys=True))
    return result

def loadSymbols(path):
    with open(path, "r") as f:
        return json.loads(f.read())

def buildBlueprint(entities):
    data = {
        'blueprint': {
            "entities": entities,
            "icons": [
                {
                    "index": 1,
                    "signal": {
                        "name": "small-lamp",
                        "type": "item"
                    }
                }
            ],
            "item": "blueprint",
            "version": 68721836034
        },
        'version_byte': '0'
    }
    print(json.dumps(data, indent=2, sort_keys=True))
    data = EncodedBlob.from_json_string(json.dumps(data))
    return data.to_exchange_string()

def buildSymbolConst(displayModel, symbolData, x, sy, state):
    global ENTITY_ID
    result = []
    y = sy

    decComb = {
        "connections": {
            "1": {
                "green": [
                    {
                        "entity_id": ENTITY_ID + 1
                    }
                ]
            }
        },
        "control_behavior": {
            "decider_conditions": {
                "comparator": "=",
                "constant": state,
                "copy_count_from_input": True,
                "first_signal": {
                    "name": "signal-S",
                            "type": "virtual"
                },
                "output_signal": {
                    "name": "signal-everything",
                            "type": "virtual"
                }
            }
        },
        "entity_number": ENTITY_ID,
        "name": "decider-combinator",
        "position": {
            "x": x,
            "y": y
        }
    }

    result.append(decComb)
    ENTITY_ID += 1
    y += 1.5

    constEntity = {
        "connections": {
            "1": {
                "green": [
                    {
                        "entity_id": ENTITY_ID - 1
                    }
                ]
            }
        },
        "control_behavior": {
            "filters": []
        },
        "entity_number": ENTITY_ID,
        "name": "constant-combinator",
        "position": {
            "x": x,
            "y": y
        }
    }
    index = 1
    for i in range(SIZE):
        for j in range(SIZE):
            if symbolData[i][j]:
                if index >= 19:
                    constEntity['connections']['2'] = {
                        "green": [
                            {
                                "entity_id": ENTITY_ID + 1
                            }
                        ]
                    }
                    result.append(constEntity)
                    index = 1
                    y += 1
                    ENTITY_ID += 1
                    constEntity = {
                        "control_behavior": {
                            "filters": []
                        },
                        "connections": {
                            "1": {
                                "green": [
                                    {
                                        "entity_id": ENTITY_ID - 1
                                    }
                                ]
                            }
                        },
                        "entity_number": ENTITY_ID,
                        "name": "constant-combinator",
                        "position": {
                            "x": x,
                            "y": y
                        }
                    }

                constEntity['control_behavior']['filters'].append({
                    "count": 1,
                    "index": index,
                    "signal": {
                        "name": displayModel[i][j],
                        "type": "item"
                    }
                })
                index += 1
    
    result.append(constEntity)
    return result




def main():
    displayConfigString = EncodedBlob.from_exchange_string("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")
    # print(json.dumps(displayConfigString.data, indent=4, sort_keys=True))
    
    displayModel = buildDisplayModel(displayConfigString.data)
    print(displayModel[0][8])

    print(displayConfigString.version_byte)

    symbols = loadSymbols('symbols.json')

    entities = []
    # entities += buildSymbolConst(displayModel, symbols['a'], 0, 1)

    x = 0
    y = 0
    state = 1
    s = "Did you ever hear the tragedy of Darth Plagueis The Wise"
    for l in s:
        entities += buildSymbolConst(displayModel, symbols[l.lower()], x, y, state)
        x+=1
        if x >= 15:
            y += 5
            x = 0
        state += 1

    print(buildBlueprint(entities))

    # print(json.dumps(EncodedBlob.from_exchange_string(
    #     "0eNqlltuOmzAQht/F11CFZDebIu1T9LJaIQMDGdXY1tjOQRHv3gGiaNVC1rQ3kezMfHPw7zE3UaoAllB7kd8EVkY7kf+8CYetlmrY81cLIhfooROJ0LIbVoOdl9qnlelK1NIbEn0iUNdwEXnWJ18SaqiwBpoHbPuPRID26BGmfMbFtdChK4E4wjNOIqxx7Gr0EJ1xm0RcRZ5m3145BKfuyaiihKM8IZuzzR1S8H/16OiG3QbJ+eKvOk5IPvDOI4XJIv0hJvrYmDFFzslKGnPKxTs7mOBtWIGEE9DVH1G3E9teOcWgfdGQ6QrUDBO5pwD9FFpD9cg+G35aAtCfG4j12N2+H47oj6Zunx7vQlc3Cy1tUHmgKDGhdkBsPNUY7s1boaUykGYJPOVsIzhwsQTOpc4q9EugXQSokc4/p7xEUCzy5pzza4Sz66RiASlWBGGVWqPmWfuYclTAOj3Lls9+jvEWwSCJKr3bzDEOEQxlWnSeq6mOwA0uQ9MstPf7eppjkct2vknZZj3PSufwBKklcxqGyzw4Ww+WfMe/5MbIfbzlFMaRkZIpjZ9nxSjemjPfQHdGXx3nKTGKH8dVekZaOIYY4SNxNfKyQIiRO0GDGmoefroi8AukGNE7oySxEjTMiz478CheMbmHNwWpCuin5achPqx3C4N99y+DPfv/wf74tkhLY34tjPeP9U8XfxyMgT5F4KD8VrqxiP3hbZsddvvN7qXvfwNyLP73").data, indent=4, sort_keys=True))





if __name__ == '__main__':
    main()

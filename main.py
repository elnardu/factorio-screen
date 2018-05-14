from blueprints import *
import json, math

SIZE = 9
ENTITY_ID = 1
CIRCUIT_ID = 0

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
    global ENTITY_ID, CIRCUIT_ID
    result = []
    y = sy

    CIRCUIT_ID += 1

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
    y += 2.5

    constEntity = {
        "connections": {
            "1": {
                "green": [
                    {   
                        "circuit_id": CIRCUIT_ID,
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
                    constEntity['connections']['1']['green'].append({
                        "entity_id": ENTITY_ID + 1
                    })
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
    y = -1.5
    state = 1
    s = "Did you ever hear the tragedy of Darth Plagueis The Wise"
    # s = "Did"
    # s = "H"
    for l in s:
        entities += buildSymbolConst(displayModel, symbols[l.lower()], x, y, state)
        x+=1
        if x >= 15:
            y += 5
            x = 0
        state += 1

    print(buildBlueprint(entities))

    # print(json.dumps(EncodedBlob.from_exchange_string(
    #     "0eNqlltuOnDAMht8l16QaYHd2itSn6GW1QgEMYzUkUQ5z0Ih3r4HVaNSF2dDeIDnEnx37x+HGKhnAWFSeFTeGtVaOFb9uzGGnhBzX/NUAKxh66FnClOhHa9znhfK81n2FSnht2ZAwVA1cWJEOyZeEBmpswC4DsuE9YaA8eoQ5n8m4lir0FViK8IyTMKMduWo1RifcLmFXVvD02yuFoNS91bKs4ChOSNtpzwekpHfN5OjG1Rat8+Wnc5zQ+kAr9xTmHfwnm+lTYSjFbLR6I+yUVMF+kIcO3oQNTDiBvfojqm6GmyvlGJQvW6v7EhXBWOFtgGGOraC+p5+Oj84CqMcKYjOVdxjGHv1V1expf1fKmq7UtEXpwUapSWrV8aOg3jcclQNLjvN5w1TJTcJ6CsgiAFWwigT1lJNHcOBiLDjHnZHo10AvESCDtLjk/Brh7HohSUeShGGx5kbLZdY+gtXKgA0/i44ksMR4i2BYgZJ/7FliHCIYUnfoPJ2mPoLzvAptu1Le79tpjrQuuuUipbvtPCOcwxNwY/VpHDLL4HQ7WNCn/iU3RvBGn0nv7oy+Pi5TYuS+ciV8hsVIHq1WXFxWuhCje0njhEbQssjSGLU7LYWl9ilYgcTIvdIo13pzoDG8YWqTZ422Duhn82GAj3a+MtTzfxnq2f8P9fuPBa+0/r0yzt+3X1v0ZzAFeohAQemedNMh9oe3LD3k+13+Mgx/AG3A/Ws=").data, indent=4, sort_keys=True))
    # print(json.dumps(EncodedBlob.from_exchange_string(
    #     "0eNrtl8FuozAQht/F53gVIEmzSPsUe1xVkQFDRmtsNLaTRhHvvgNEVdWF1KRV20MuiXDsf8bj3x+TM8uUlw2Cdiw9M8iNtiz9c2YWKi1UN+ZOjWQpAydrtmBa1N1TIXMoJPLc1Blo4QyydsFAF/KJpVG7eFOgC+SEduMKcfu4YFI7cCCHfPqH0077OpNIIa5lsmCNsbTU6C48yXGafuq+fqwpBoV2aNQuk3txAJpPky4qO/qt6FfabrQEtG73304OgM7TyHMOwwz+mw3q/cb6HCmpRmCfVMp+0QLjXeNnSMqDxJPbg64G7eZEKXrtdiWaegeaxFjq0Mt2CK1l/px91H1UKKV+WUEoWLpqH9u2O6RXVY1nVXX5FUWNv21R1xNFTWYV9Uucmnzbom4mirq6CpIpAEQTNS1BOYlB4FNGV3wvCFMFB20l0sJhw/5y52dA8KpAHCCQedRkqKs6SYCOfGpQWstto8BNCa0ChBqgwbHF64DFthaKjKTIGQg5b4wa19oEaJXKQ8GPoiIPjGk8BGigAMUvc8Y0tgEaylRgHe0m30vreObLcqK8P0Pfmuj7m8PRZMaNe28ZclTmSNaxR3D5flwlxML9reVHwPGjikJcDEi7EU8TCiH+RVmCphtJ9clRugmlEANbowTyRmg5fuZRkJGdFDV3HglIE7lsgmWkriZVQlycGVBTjNoSXmfQuOtoAHMPbnicgPN6HpyXdzZ/CptLQQC6qhLi7QyqD0K0MuQK4+Agbyb0K7o2wlqS4w2aQ9ck3Uzt8b83NyFbkR/Jw+p2UL+JpOhjkBR/CJKSdyIpxMnP/1l5ZszfKU7PQlschrbNPLTd285723lvO+9t573tfE/bmYyx+XExBHzxNqDgB+Jpj9/N9iGOtslmmaza9h/oNQIJ").data, indent=4, sort_keys=True))





if __name__ == '__main__':
    main()

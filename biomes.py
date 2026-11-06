BIOMES = {
    "shallow": {
        "name": "OCEANO RASO",
        "color": (15, 85, 115)
    },

    "deep": {
        "name": "OCEANO PROFUNDO",
        "color": (3, 12, 35)
    },

    "reef": {
        "name": "RECIFES",
        "color": (12, 95, 90)
    }
}


def get_biome(x, y):

    if x < 1500 and y < 1500:
        return BIOMES["shallow"]

    elif x >= 1500 and y < 1500:
        return BIOMES["deep"]

    else:
        return BIOMES["reef"]
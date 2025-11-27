"""Parse JSON"""
import json
import argparse
from PIL import Image


def rgb_to_hex(r: int, g: int, b: int):
    """
    Takes RGB and transforms it into a string I can actually use
    """
    return f"#{r:02x}{g:02x}{b:02x}"


def is_arbitrary(hexa: str, configuration: dict, colors_config: list) -> bool:
    """
    Checks if the 'hexa' color is an 'arbitrary' color
    that should go in a separate overlay
    """
    for c in colors_config:
        if hexa == c["color"] and c["name"] in configuration["arbitrary"]:
            return True
    return False


def get_color_index(he: str, configuration: dict, colors_config: list) -> int:
    """
    Get the index of an 'arbitrary' color.
    """
    for c in colors_config:
        if he == str(c["color"]):
            return configuration["arbitrary"].index(c["name"])
    return 0


def is_free(hexa: str, colors_config: list) -> bool:
    """
    Checks if the 'hexa' color is a 'free' color
    that should go in the free overlay
    """
    for c in colors_config:
        if hexa == c["color"] and not c["isPremium"]:
            return True
    return False


def is_premium(hexa: str, colors_config: list) -> bool:
    """
    Checks if the 'hexa' color is a 'premium' color
    that should go in the premium overlay
    """
    for c in colors_config:
        if hexa == c["color"] and c["isPremium"]:
            return True
    return False


def main(colors_config: list, configuration: dict, image_name: str):
    """
    Main function, you doof
    """
    image = Image.open(image_name)
    premium_overlay = Image.new(mode="RGBA", size=image.size)
    free_overlay = Image.new(mode="RGBA", size=image.size)
    arbitrary_overlays = [
        Image.new(mode="RGBA", size=image.size)
        for a in configuration["arbitrary"]
    ]
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            r, g, b, a = image.getpixel((x, y))
            if a == 0:
                continue
            hexa = rgb_to_hex(r, g, b)
            if is_arbitrary(hexa, configuration, colors_config):
                arbitrary_overlays[
                    get_color_index(hexa, configuration, colors_config)
                ].putpixel((x, y), (r, g, b, 255))
                continue
            if is_free(hexa, colors_config):
                free_overlay.putpixel((x, y), (r, g, b, 255))
                continue
            if is_premium(hexa, colors_config):
                premium_overlay.putpixel((x, y), (r, g, b, 255))
                continue
    premium_overlay.save("premium_overlay_" + image_name)
    free_overlay.save("free_overlay_" + image_name)
    for i in enumerate(arbitrary_overlays):
        i[1].save("arbitrary_overlay_" + str(i[0]) + "_" + image_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="wplace overlay separator",
        description="Separates overlays for wplace overlay pro."
        " This is to make it clearer to work on bigger projects.",
        epilog="Made by 5BNeumann for Timber-being-made-of-15000-dark-slate"
        " shaped reasons."
    )
    parser.add_argument("filename")
    parser.add_argument("-c", "--config")
    # WTF would you even use that for but whatever
    parser.add_argument("-C", "--colors")
    args = parser.parse_args()
    if not args.filename:
        print(
            "\x1B[31mERROR: YOU STUPID USER DID NOT PROVIDE A FILENAME\x1B[0m"
        )
    configname = args.config if args.config else "config.json"
    with open(configname, encoding="ASCII") as f:
        config = json.load(f)
    colorsname = args.colors if args.colors else "wplace-colors.json"
    with open(colorsname, encoding="ASCII") as f:
        colors = json.load(f)
    main(colors, config, args.filename)

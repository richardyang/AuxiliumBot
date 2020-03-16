conf = {}
with open("CONFIG") as config_file:
    for line in config_file:
        # Ignore # which are comments
        if not line.startswith("#") and "=" in line:
            key, value = line.strip("\n").split("=")
            if key == "RATE_CHANNELS":
                value = value.split(",")
            conf[key] = value

conf["LEVEL_IMAGES"] = {}

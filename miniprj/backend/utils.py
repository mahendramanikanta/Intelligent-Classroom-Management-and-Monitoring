def validate_input(data):
    required_fields = [
        "temperature",
        "humidity",
        "light_level",
        "sound_level",
        "air_quality",
        "motion"
    ]
    for field in required_fields:
        if field not in data:
            return False, f"Missing field: {field}"
    return True, "Valid input"

def prepare_features(data):
    return [[
        data["temperature"],
        data["humidity"],
        data["light_level"],
        data["sound_level"],
        data["motion"]
    ]]

def format_prediction(fan_pred, light_pred):
    return {
        "fan": int(fan_pred),
        "light": int(light_pred),
        "status": "success"
    }

"""
Configuration loader for YAML files.
"""
import yaml
import os

def load_config():
    """Load main configuration from config.yaml."""
    config_path = 'config/config.yaml'
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"{config_path} not found")

    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    return config

def load_questionnaire_fields(config):
    """Load questionnaire fields from configured file."""
    questionnaire_file = config['settings'].get(
        'questionnaire_fields_file',
        'config/questionnaire_fields.yaml'
    )

    if not os.path.exists(questionnaire_file):
        print(f"[WARNING] {questionnaire_file} not found, using empty questionnaire fields")
        return []

    with open(questionnaire_file, 'r') as file:
        all_fields = yaml.safe_load(file)
        if all_fields is None:
            return []

    # Filter only active fields
    return [field for field in all_fields if field.get('active', False)]

def load_rating_scales(config):
    """Load rating scales from configured file."""
    rating_scales_file = config['settings'].get(
        'rating_scales_file',
        'config/rating_scales.yaml'
    )

    if not os.path.exists(rating_scales_file):
        print(f"[WARNING] {rating_scales_file} not found, using empty rating scales")
        return []

    with open(rating_scales_file, 'r') as file:
        all_scales = yaml.safe_load(file)
        if all_scales is None:
            return []

    # Filter only active scales
    return [scale for scale in all_scales if scale.get('active', False)]

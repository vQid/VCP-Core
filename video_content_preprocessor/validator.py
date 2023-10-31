from pathlib import Path

import yaml
from pydantic import ValidationError

from video_content_preprocessor.model.schema import VCP


def _load_and_validate_yaml(configuration_path: Path):
    """ Function to validate the content of configuration file."""
    try:
        # Load YAML-File
        with open(configuration_path, 'r') as f:
            daten = yaml.safe_load(f)
            print(daten)

        # Validate Input with pydantic
        config = VCP(**daten)
        print("Validated Data:", config)
        return config

    except yaml.YAMLError as e:
        print("Error at loading of the YAML-File:", e)
    except ValidationError as e:
        print("Error at validating of the YAML-File:", e)


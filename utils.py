"""
Utility functions for Leaf Disease Detection
===========================================

Provides functions to convert image files/bytes to base64 and test the
LeafDiseaseDetector directly.
"""

import json
import sys
import base64
from pathlib import Path



# Adjust the import path to your Leaf Disease Detector module
sys.path.insert(0, str(Path(__file__).parent))

try:
    from detector import LeafDiseaseDetector
except ImportError as e:
    print(f'{{"error": "Could not import LeafDiseaseDetector: {str(e)}"}}')
    sys.exit(1)


def test_with_base64_data(base64_image_string: str):
    """
    Test disease detection with base64 image data

    Args:
        base64_image_string (str): Base64 encoded image data
    """
    try:
        detector = LeafDiseaseDetector()
        result = detector.analyze_leaf_image_base64(base64_image_string)
        print(json.dumps(result, indent=2))
        return result
    except Exception as e:
        print(f'{{"error": "{str(e)}"}}')
        return None


def convert_image_to_base64_and_test(image_input):
    """
    Convert image file path or bytes to base64 and test it

    Args:
        image_input (str | bytes): Image file path as string OR image bytes
    """
    try:
        # Handle file path string
        if isinstance(image_input, str):
            image_path = Path(image_input)
            if not image_path.exists():
                print(f'{{"error": "File not found: {image_input}"}}')
                return None
            with open(image_path, "rb") as f:
                image_bytes = f.read()
        elif isinstance(image_input, bytes):
            image_bytes = image_input
        else:
            print('{"error": "Invalid input type. Provide bytes or file path string."}')
            return None

        if not image_bytes:
            print('{"error": "No image data found"}')
            return None

        # Convert to base64
        base64_string = base64.b64encode(image_bytes).decode("utf-8")
        print(f"Converted image to base64 ({len(base64_string)} characters)")
        return test_with_base64_data(base64_string)

    except Exception as e:
        print(f'{{"error": "{str(e)}"}}')
        return None


def main():
    """Test with base64 conversion from file path"""
    test_image = "Media/brown-spot-4 (1).jpg"
    convert_image_to_base64_and_test(test_image)


if __name__ == "__main__":
    main()

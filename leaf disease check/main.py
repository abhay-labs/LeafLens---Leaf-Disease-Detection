import os
import json
import logging
import sys
from typing import Dict, Optional, List
from dataclasses import dataclass
from datetime import datetime

from groq import Groq
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class DiseaseAnalysisResult:
    """Data class for storing comprehensive disease analysis results."""
    disease_detected: bool
    disease_name: Optional[str]
    disease_type: str
    severity: str
    confidence: float
    symptoms: List[str]
    possible_causes: List[str]
    treatment: List[str]
    analysis_timestamp: str = datetime.now().astimezone().isoformat()


class LeafDiseaseDetector:
    """Advanced Leaf Disease Detection System using AI Vision Analysis."""

    MODEL_NAME = "meta-llama/llama-4-scout-17b-16e-instruct"
    DEFAULT_TEMPERATURE = 0.3
    DEFAULT_MAX_TOKENS = 1024

    def __init__(self, api_key: Optional[str] = None):
        load_dotenv()
        self.api_key = api_key or os.environ.get("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        self.client = Groq(api_key=self.api_key)
        logger.info("Leaf Disease Detector initialized")

    def create_analysis_prompt(self) -> str:
        return """IMPORTANT: First determine if this image contains a plant leaf or vegetation...
        (same JSON instructions as you provided, no changes needed)
        """

    def analyze_leaf_image_base64(self, base64_image: str,
                                  temperature: float = None,
                                  max_tokens: int = None) -> Dict:
        """Analyze base64 encoded image data for leaf diseases and return JSON result."""
        try:
            logger.info("Starting analysis for base64 image data")

            if not isinstance(base64_image, str):
                raise ValueError("base64_image must be a string")
            if not base64_image:
                raise ValueError("base64_image cannot be empty")
            if base64_image.startswith('data:'):
                base64_image = base64_image.split(',', 1)[1]

            temperature = temperature or self.DEFAULT_TEMPERATURE
            max_tokens = max_tokens or self.DEFAULT_MAX_TOKENS

            completion = self.client.chat.completions.create(
                model=self.MODEL_NAME,
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": self.create_analysis_prompt()},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                    ]
                }],
                temperature=temperature,
                max_completion_tokens=max_tokens,
                top_p=1,
                stream=False,
                stop=None,
            )

            logger.info("API request completed successfully")
            result = self._parse_response(completion.choices[0].message.content)
            return result.__dict__

        except Exception as e:
            logger.error(f"Analysis failed: {str(e)}")
            raise

    def _parse_response(self, response_content: str) -> DiseaseAnalysisResult:
        """Parse and validate API response."""
        try:
            cleaned = response_content.strip()
            if cleaned.startswith('```json'):
                cleaned = cleaned.replace('```json', '').replace('```', '').strip()
            elif cleaned.startswith('```'):
                cleaned = cleaned.replace('```', '').strip()

            disease_data = json.loads(cleaned)
            logger.info("Response parsed successfully as JSON")

            return DiseaseAnalysisResult(
                disease_detected=bool(disease_data.get('disease_detected', False)),
                disease_name=disease_data.get('disease_name'),
                disease_type=disease_data.get('disease_type', 'unknown'),
                severity=disease_data.get('severity', 'unknown'),
                confidence=float(disease_data.get('confidence', 0)),
                symptoms=disease_data.get('symptoms', []),
                possible_causes=disease_data.get('possible_causes', []),
                treatment=disease_data.get('treatment', [])
            )

        except json.JSONDecodeError:
            import re
            json_match = re.search(r'\{.*\}', response_content, re.DOTALL)
            if json_match:
                disease_data = json.loads(json_match.group())
                logger.info("JSON extracted and parsed successfully")
                return DiseaseAnalysisResult(
                    disease_detected=bool(disease_data.get('disease_detected', False)),
                    disease_name=disease_data.get('disease_name'),
                    disease_type=disease_data.get('disease_type', 'unknown'),
                    severity=disease_data.get('severity', 'unknown'),
                    confidence=float(disease_data.get('confidence', 0)),
                    symptoms=disease_data.get('symptoms', []),
                    possible_causes=disease_data.get('possible_causes', []),
                    treatment=disease_data.get('treatment', [])
                )
            logger.error(f"Could not parse response as JSON: {response_content}")
            raise ValueError("Unable to parse API response as JSON")

def main():
    try:
        detector = LeafDiseaseDetector()
        print("Leaf Disease Detector initialized successfully!")
        print("Use analyze_leaf_image_base64() with base64 image data.")

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

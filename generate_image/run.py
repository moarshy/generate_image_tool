import os
import base64
import requests
from PIL import Image
from io import BytesIO
from pathlib import Path
from dotenv import load_dotenv
from generate_image.schemas import InputSchema
from naptha_sdk.utils import get_logger
from typing import Dict

load_dotenv()
STABILITY_API_HOST = "https://api.stability.ai"
DEFAULT_FILENAME = "output.png"
DEFAULT_ENGINE = "stable-diffusion-xl-1024-v1-0"

logger = get_logger(__name__)

def run(inputs: InputSchema, worker_nodes = None, orchestrator_node = None, flow_run = None, cfg: Dict = None):
    """Run the module to generate image from text prompt using Stability API"""
    logger.info(f"Generating image from prompt: {inputs.prompt}")
    
    # Get api key from environment variable
    api_key = os.environ['STABILITY_API_KEY']

    if api_key is None:
        raise ValueError("API key is not set")

    url = f"{STABILITY_API_HOST}/v1/generation/{DEFAULT_ENGINE}/text-to-image"
    data = {
        "cfg_scale": 7,
        "clip_guidance_preset": "FAST_BLUE",
        "height": 1024,
        "width": 1024,
        "sampler": "K_DPM_2_ANCESTRAL",
        "samples": 1,
        "steps": 30,
        "text_prompts": [
            {
            "text": inputs.prompt,
            "weight": 1
            }
        ]
        }
    response = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {api_key}"
        },
        json=data
    )

    if response.status_code != 200:
        logger.error(f"Failed to generate image: {response.text}")
        raise ValueError(f"Failed to generate image: {response.text}")
    
    result = response.json()

    image_b64 = result['artifacts'][0]['base64']
    image = Image.open(BytesIO(base64.b64decode(image_b64)))

    if inputs.output_path:
        output_path = inputs.output_path
        Path(output_path).mkdir(parents=True, exist_ok=True)
        image.save(f"{output_path}/{DEFAULT_FILENAME}")

        return f"Image saved to {output_path}/{DEFAULT_FILENAME}"

    return "Image generated successfully"


if __name__ == "__main__":
    inputs = InputSchema(
        prompt="expansive landscape rolling greens with gargantuan yggdrasil, intricate world-spanning roots towering under a blue alien sky, masterful, ghibli",
        output_path="output"
    )
    run(inputs)
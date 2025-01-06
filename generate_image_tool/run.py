import os
import base64
import requests
from PIL import Image
from io import BytesIO
from pathlib import Path
from dotenv import load_dotenv
import logging
from typing import Dict
from generate_image_tool.schemas import InputSchema
from naptha_sdk.schemas import ToolDeployment, ToolRunInput

logger = logging.getLogger(__name__)

load_dotenv()

class GenerateImageTool():

    def __init__(self, tool_deployment: ToolDeployment):
        self.tool_deployment = tool_deployment
        self.api_key = os.environ['STABILITY_API_KEY']

        if self.api_key is None:
            raise ValueError("API key is not set")


    def generate_image_tool(self, inputs: InputSchema):
        """Run the module to generate image from text prompt using Stability API"""
        logger.info(f"Generating image from prompt: {inputs.tool_input_data}")

        default_engine = self.tool_deployment.config.llm_config.model
        default_filename = self.tool_deployment.data_generation_config.default_filename
        url = f"{self.tool_deployment.config.llm_config.api_base}/v1/generation/{default_engine}/text-to-image"

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
                "text": inputs.tool_input_data,
                "weight": 1
                }
            ]
            }

        response = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {self.api_key}"
            },
            json=data
        )

        if response.status_code != 200:
            logger.error(f"Failed to generate image: {response.text}")
            raise ValueError(f"Failed to generate image: {response.text}")

        result = response.json()

        image_b64 = result['artifacts'][0]['base64']
        image = Image.open(BytesIO(base64.b64decode(image_b64)))

        if self.tool_deployment.data_generation_config.save_outputs_path:
            output_path = self.tool_deployment.data_generation_config.save_outputs_path
            Path(output_path).mkdir(parents=True, exist_ok=True)
            image.save(f"{output_path}/{default_filename}")

            return f"Image saved to {output_path}/{default_filename}"

        return "Image generated successfully"

def run(module_run: Dict, *args, **kwargs):
    """Run the module to generate image from text prompt using Stability API"""
    module_run = ToolRunInput(**module_run)
    module_run.inputs = InputSchema(**module_run.inputs)
    generate_image_tool = GenerateImageTool(module_run.deployment)

    method = getattr(generate_image_tool, module_run.inputs.tool_name, None)

    if not method:
        raise ValueError(f"Method {module_run.inputs.tool_name} not found")

    result = method(module_run.inputs)

    return result


if __name__ == "__main__":
    import asyncio
    from naptha_sdk.client.naptha import Naptha
    from naptha_sdk.configs import setup_module_deployment

    naptha = Naptha()

    deployment = asyncio.run(setup_module_deployment("tool", "generate_image_tool/configs/deployment.json", node_url = os.getenv("NODE_URL")))

    input_params = {
        "tool_name": "generate_image_tool",
        "tool_input_data": "expansive landscape rolling greens with gargantuan yggdrasil, intricate world-spanning roots towering under a blue alien sky, masterful, ghibli"
    }

    module_run = {
        "inputs": input_params,
        "deployment": deployment,
        "consumer_id": naptha.user.id,
    }

    response = run(module_run)

    print("Response: ", response)
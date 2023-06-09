from langchain.tools import BaseTool
from transformers import BlipProcessor, BlipForConditionalGeneration, DetrImageProcessor, DetrForObjectDetection
from PIL import Image
import torch


class ImageCaptionTool(BaseTool):
    name = "Image captioner"
    description = "Use this tool when given the path to an image that you would like to be described. " \
            "It will return three song suggestions based on properties of the image. " \
            "It will return artists and songs in the format: " \
            "1. Song_name, Artist \n" \
            "2. Song_name2, Artist2 \n" \
            "3. Song_name3, Artist3 \n"

    def _run(self, img_path):
        image = Image.open(img_path).convert('RGB')

        model_name = "Salesforce/blip-image-captioning-large"
        device = "cpu"

        processor = BlipProcessor.from_pretrained(model_name)
        model = BlipForConditionalGeneration.from_pretrained(model_name).to(device)

        inputs = processor(image, return_tensors='pt').to(device)
        output = model.generate(**inputs, max_new_tokens=20) # Run inference

        caption = processor.decode(output[0], skip_special_tokens=True)

        return caption

    def _arun(self, query: str):
        raise NotImplementedError("This tool does not support async")
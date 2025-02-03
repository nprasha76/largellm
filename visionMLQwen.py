import gradio as gr
from openai import OpenAI
import base64
import requests

# Initialize OpenAI client (do this only once)
client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")


def get_base_64_img(image_path):
    """Converts an image from a local file path to base64 encoding."""
    try:
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            return base64_image
    except FileNotFoundError:
        return "Error: Image file not found."
    except Exception as e:
        return f"Error encoding image: {e}"


def process_image(image_path, question):
    """Processes the image and generates a completion."""

    base64_image = get_base_64_img(image_path)
    if "Error:" in base64_image: # Check for errors from get_base_64_img
      return base64_image
    
    try:
        completion = client.chat.completions.create(
            model="local-model",  # Your model name
            temperature=0,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": question},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"  # Or appropriate MIME type
                            },
                        },
                    ],
                }
            ],
            max_tokens=1000,
            stream=False  # Set stream=False for simple text output in Gradio
        )
        return completion.choices[0].message.content.strip()  # Extract the text response

    except Exception as e:
        return f"Error during completion: {e}"


with gr.Blocks() as demo:
    gr.Markdown("# Vision Explainer")  # Added heading
    image_input = gr.File(label="Upload or select an image")     
    #image_input = gr.Textbox(label="Enter local image path") # Changed to Textbox for local image path
    question_input = gr.Textbox(label="Enter your question on image")
    output_text = gr.Textbox(label="Response")
    submit_button = gr.Button("Submit")

    submit_button.click(
        process_image,
        inputs=[image_input, question_input], # Pass both image path and question
        outputs=output_text,
    )

demo.launch()

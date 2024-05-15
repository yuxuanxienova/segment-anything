from flask import Flask, request, send_file
from PIL import Image
from io import BytesIO
from image_processor import ImageProcessor
import logging

# Initialize the ImageProcessor object
processor = ImageProcessor()

app = Flask(__name__)
# Set up logging
logging.basicConfig(level=logging.INFO)
# Define the function to convert the image to a standard format
def convert_to_standard_format(image_bytes):
    pil_image = Image.open(BytesIO(image_bytes))
    pil_image = pil_image.convert('RGB')  # Convert to RGB format
    return pil_image

@app.route('/', methods=['POST'])
def predict():
    # Log the incoming request
    logging.info(f"Incoming request from {request.remote_addr} - {request.method} {request.url}")
    #1.PrePorcess
    #1.1 check if image file is included in the request
    if 'file' not in request.files:
        logging.error("No file part in the request")
        return "No file part",400
    file = request.files['file']
    #1.2 check if the file is not empty
    if file.filename == '':
        logging.error("File name is empty")
        return "File name is empty",400
    #1.3 check if is an allowed format
    allowed_extensions = {'png','jpg','jpeg','gif'}
    if '.' not in file.filename or file.filename.rsplit('.',1)[1].lower() not in allowed_extensions:
        logging.error("Unsupported file format")
        return "Unsupported file format",400
    
    
    #2.Read the image file
    image_bytes = file.read()
    
    # Convert the image to a standard format
    pil_image = convert_to_standard_format(image_bytes) 
    
    #3.Process the image
    pil_image = processor.process_SetOfMask(pil_image)
    

    # Save and Response
    output_image_bytes = BytesIO()
    # Save the processed image as JPEG
    pil_image.save(output_image_bytes, format='JPEG')
    output_image_bytes.seek(0)

    # Return the processed image as JPEG
    logging.info("Image processed successfully")
    return send_file(output_image_bytes, mimetype='image/jpeg')
     

if __name__ == "__main__":
    app.run(debug=True)
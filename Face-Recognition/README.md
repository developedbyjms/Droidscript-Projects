# Face Recognition App with FaceAPI
A Face Recognition App built using FaceAPI for detecting age, gender, expressions, and identifying faces from images. Includes features like facial landmark detection, bounding box annotation, and user-friendly image selection. Ideal for developers looking to integrate AI-powered facial analysis into their applications.

![Demo](https://github.com/developedbyjms/Droidscript-Projects/blob/main/Face-Recognition/Img/Screenshot_20250113-082333_1.png)

## Description
This project is a Face Recognition App built using the FaceAPI plugin. It detects faces in images and provides details like:
- Age
- Gender
- Expressions (with confidence levels)
- Facial landmarks
- Name (based on loaded models)

The app is ideal for showcasing AI capabilities in real-time facial analysis.

---

## Features
- **Face Detection**: Identify faces in images with bounding box visualization.
- **Age & Gender Analysis**: Predict age and gender of detected faces.
- **Expression Recognition**: Detect facial expressions with confidence percentages.
- **Facial Landmarks**: Annotate detected faces with detailed facial landmark points.
- **Custom Models**: Load models like `avengers.json` to enhance recognition.

---

## How It Works
1. **Load the App**: The app initializes FaceAPI with the required models.
2. **Choose an Image**: Users can upload an image via a file picker.
3. **Face Recognition**: The app processes the image to identify and annotate faces.
4. **Display Results**: Bounding boxes, landmarks, and information (age, gender, etc.) are drawn on the canvas.

---

## Installation
1. Clone this repository:  
   ```bash
   git clone https://github.com/developedbyjms/Droidscript-Projects.git

2. Load the required FaceAPI plugin in your project.


3. Place the models/avengers.json file in the correct path (assets/models).




---

Usage

Start the app and wait for FaceAPI to load.

Click "CHOOSE PIC" to upload an image.

The app will analyze the image and display results on the screen.



---

Requirements

FaceAPI Plugin: Ensure the FaceAPI plugin is installed and available.

Supported Models: Use JSON-based models for better accuracy.



---

Future Improvements

Add support for video streams.

Enhance model accuracy with better training data.

Add error handling for unsupported file types or empty image uploads.



---

License

This project is licensed under the MIT License. See the LICENSE file for details.


---

Author

Developed by José Sixpenze. Contributions are welcome!

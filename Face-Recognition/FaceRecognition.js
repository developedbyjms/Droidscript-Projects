// Load the FaceAPI plugin
app.LoadPlugin("FaceAPI");

function OnStart() {    
    // Show progress message while loading FaceAPI
    app.ShowProgress("LOADING FACE-API.");

    // Initialize the FaceAPI with specific features (age, gender, expression, recognition) and callback onLoad
    faceApi = app.CreateFaceAPI("agegender, expression, recognition", onLoad);

    // Create a vertical, fill layout for UI elements
    lay = app.CreateLayout("Linear", "VCenter,FillXY");

    // Create a frame layout to hold the image and canvas
    frame = app.AddLayout(lay, "Frame");

    // Add an image view to display the selected image
    img = app.AddImage(frame, "Img/6.jpg", 0.9, 0.4);

    // Add a canvas for drawing annotations (e.g., bounding boxes, landmarks)
    canvas = app.AddImage(frame, null, 0.9, 0.4, "alias");
    canvas.SetPaintColor("#00ffff"); // Set paint color for annotations
    canvas.SetPaintStyle("Fill"); // Default paint style
    canvas.SetLineWidth(1); // Set line width for drawing
    canvas.SetAutoUpdate(false); // Disable auto-update for performance optimization
    
    // Add a button to let users choose an image
    btn = app.AddButton(lay, "CHOOSE PIC");
    btn.SetOnTouch(btn_OnTouch); // Set button's touch event handler

    // Add the layout to the app
    app.AddLayout(lay);
}

// Callback for the "CHOOSE PIC" button
function btn_OnTouch() {
    // Open a file chooser dialog for the user to select an image
    app.ChooseFile("Choose a File", "*/*", OnChoose);
}

// Callback when a file is selected
function OnChoose(file) {
    // Clear previous drawings on the canvas
    canvas.Clear();
    canvas.Update();

    // Update the image view with the selected image
    img.SetImage(file);
    img.Update();

    // Show progress while processing the image
    app.ShowProgress("RECOGNIZING.");

    // Perform face recognition on the selected image
    faceApi.IdentifyFaces(img, onResult);
}

// Callback when FaceAPI is loaded
function onLoad() {
    // Show progress message while recognizing faces
    app.ShowProgress("RECOGNIZING.");

    // Load a face recognition model (assumes "avengers.json" is available in assets)
    faceApi.SetModel(faceApi.getAsset("models/avengers.json"));

    // Perform face recognition on the initial image
    faceApi.IdentifyFaces(img, onResult);
}

// Callback for face recognition results
function onResult(data) {
    // Hide progress indicator
    app.HideProgress();

    // Check if any faces were detected
    if (data.length) {
        // Clear canvas for fresh annotations
        canvas.Clear();

        // Iterate through detected faces
        data.forEach(face => {
            // Draw facial landmarks as small circles
            face.landmarks.forEach(m => {
                canvas.SetPaintStyle("Fill");
                canvas.DrawCircle(m.x / face.imageWidth, m.y / face.imageHeight, 0.0050);
            });

            // Draw a bounding rectangle around the face
            canvas.SetPaintStyle("Line");
            canvas.SetPaintColor("#00FFFF");
            canvas.DrawRectangle(
                face.x / face.imageWidth,
                face.y / face.imageHeight,
                (face.x + face.width) / face.imageWidth,
                (face.y + face.height) / face.imageHeight
            );

            // Annotate the face with name, gender, age, and expression
            canvas.SetPaintStyle("Fill");
            canvas.SetTextSize(10);
            
            // Draw name
            canvas.DrawText(
                "Name: " + face.name,
                face.x / face.imageWidth - 0.005,
                (face.y + face.height) / face.imageHeight + 0.028
            );

            // Draw gender
            canvas.DrawText(
                "Gender: " + face.gender,
                face.x / face.imageWidth - 0.005,
                (face.y + face.height) / face.imageHeight + 0.058
            );

            // Draw age
            canvas.DrawText(
                "Age: " + Math.round(face.age),
                face.x / face.imageWidth - 0.005,
                (face.y + face.height) / face.imageHeight + 0.085
            );

            // Determine and annotate the most prominent expression
            const emotion = Object.entries(face.expressions).reduce((max, entry) => {
                return entry[1] > max[1] ? entry : max;
            });

            canvas.DrawText(
                "Expression: " + emotion[0] + " (" + Math.round(emotion[1] * 100) + "%)",
                face.x / face.imageWidth - 0.005,
                (face.y + face.height) / face.imageHeight + 0.115
            );
        });

        // Update the canvas to show annotations
        canvas.Update();
    }
}


/*
  ~ DevelopedByJMS™
  ~ José Sixpenze
  ~ 13/01/2025
*/





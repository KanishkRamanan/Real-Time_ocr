import cv2
import pytesseract

# Configure pytesseract path (update this to your Tesseract installation path)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update for your installation

# Function to start OCR detection and return text
def start_ocr_detection(update_callback):
    cap = cv2.VideoCapture(0)  # Open the default webcam

    last_detected_text = ""  # Store the last detected text to avoid redundant prints

    while True:
        ret, frame = cap.read()  # Capture frame-by-frame
        if not ret:
            break

        # Convert the frame to grayscale for better OCR results
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Use pytesseract to detect text in the frame
        ocr_result = pytesseract.image_to_data(gray_frame, output_type=pytesseract.Output.DICT)

        # Extract text and locations
        text_data = []
        n_boxes = len(ocr_result['text'])
        for i in range(n_boxes):
            if int(ocr_result['conf'][i]) > 60:  # Only consider confident text detections
                (x, y, w, h) = (ocr_result['left'][i], ocr_result['top'][i], ocr_result['width'][i], ocr_result['height'][i])
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Draw bounding box
                detected_text = ocr_result['text'][i].strip()  # Strip any leading/trailing spaces
                if detected_text:
                    text_data.append(detected_text)
                
                    # Add detected text to the frame
                    cv2.putText(frame, detected_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

        # If there's detected text, print it only if it's new
        if text_data:
            recognized_text = " ".join(text_data)
            if recognized_text != last_detected_text:
                print(f"Recognized Text: {recognized_text}")  # Print recognized text to console
                last_detected_text = recognized_text  # Update the last detected text
            update_callback(recognized_text)  # Send detected text to GUI

        # Show the frame with bounding boxes and detected text
        cv2.imshow("OCR Webcam Feed", frame)

        # Press 'q' to quit the webcam stream
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

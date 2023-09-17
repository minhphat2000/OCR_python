import pytesseract
import argparse
import cv2
import os

# Construct the argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
    help="Path to the input image")
ap.add_argument("-p", "--preprocess", type=str, default="thresh",
    help="Preprocessing method (thresh or blur)")
ap.add_argument("-o", "--output", type=str, default="output.txt",
    help="Path to the output text file")
args = vars(ap.parse_args())

# Read the input image using OpenCV
try:
    image = cv2.imread(args["image"])
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Check if preprocessing is required
    if args["preprocess"] == "thresh":
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    elif args["preprocess"] == "blur":
        gray = cv2.medianBlur(gray, 3)

    # Temporary file to save the processed image
    temp_filename = "temp.jpg"
    cv2.imwrite(temp_filename, gray)

    # Perform OCR using Tesseract
    text = pytesseract.image_to_string(temp_filename, lang='vie')

    # Print the recognized text
    print(text)

    # Save the recognized text to the output file
    with open(args["output"], "w", encoding="utf-8") as output_file:
        output_file.write(text)

    # Display the original and processed images
    cv2.imshow("Original Image", image)
    cv2.imshow("Processed Image", gray)

    # Wait for a key press and then close the image windows
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Remove the temporary image file
    os.remove(temp_filename)

except Exception as e:
    print(f"An error occurred: {str(e)}")

import time
import pytesseract
import cv2
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# Set path to Tesseract (adjust if needed)
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

# Launch the browser and open the CAPTCHA page
driver = webdriver.Chrome()  
driver.get("file:///Users/sashank810/Desktop/Code Folders/CAPTCHA/CAPTCHA11.html")  # Change this to your file path

time.sleep(3)  # Wait for page to load

def solve_captcha():
    """Solves the CAPTCHA by recognizing the text and entering it."""
    global driver

    while True:
        try:
            # Check if CAPTCHA input box still exists
            input_box = driver.find_element(By.ID, "captchaInput")
        except:
            print("❌ Bot detected! CAPTCHA input box disappeared.")
            break  # Exit if CAPTCHA box is gone (bot detected)

        # Capture CAPTCHA image
        captcha_element = driver.find_element(By.ID, "captcha")
        location = captcha_element.location
        size = captcha_element.size
        driver.save_screenshot("full_page.png")

        # Process image
        image = cv2.imread("full_page.png")
        x, y, w, h = int(location["x"]), int(location["y"]), int(size["width"]), int(size["height"])
        captcha_image = image[y : y + h, x : x + w]
        

        # OCR to extract text
        def preprocess_image(image):
            """Preprocesses the CAPTCHA image to improve OCR accuracy."""
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
            _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)  # Convert to binary
            kernel = np.ones((2,2), np.uint8)  # Define a kernel for noise removal
            denoised = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)  # Remove small noise
            return denoised
        captcha_gray = preprocess_image(captcha_image)


        captcha_text = pytesseract.image_to_string(captcha_gray, config="--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789").strip()
        print("Detected CAPTCHA:", captcha_text)

        # Simulate typing like a bot
        actions = ActionChains(driver)
        actions.move_to_element(input_box).perform()
        input_box.clear()

        for char in captcha_text:
            input_box.send_keys(char)
            time.sleep(0.15)  # Slight delay to appear bot-like

        time.sleep(0.5)

        # Click "Verify" button
        verify_button = driver.find_element(By.CLASS_NAME, "verify-btn")
        actions.move_to_element(verify_button).click().perform()

        time.sleep(2)  # Allow message to appear

        # Check response message
        try:
            message_element = driver.find_element(By.ID, "message")
            message_text = message_element.text.strip()
        except:
            message_text = ""

        print("Response:", message_text)

        if "Successful, Human Identified" in message_text:
            print("✅ CAPTCHA solved successfully!")
            break  # Stop if solved
        elif "Not Verified, Robot Identified" in message_text:
            print("❌ Bot detected! Stopping.")
            break  # Stop if bot detected
        else:
            print("❌ Incorrect CAPTCHA, retrying...")
            # Click "New CAPTCHA" button
            new_captcha_button = driver.find_element(By.CLASS_NAME, "refresh-btn")
            actions.move_to_element(new_captcha_button).click().perform()
            time.sleep(2)  # Wait for new CAPTCHA to load

solve_captcha()

# Close browser after completion
time.sleep(2)
driver.quit()
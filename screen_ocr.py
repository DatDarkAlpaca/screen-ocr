import keyboard
import tempfile
import pyperclip
import subprocess
import pytesseract
import clipboard_monitor

from PIL import ImageGrab

# Todo: handle tesseract not found
tesseract_path = r'D:\\Program Files\\Tesseract-OCR\\tesseract.exe'
tesseract_config = r"-l eng+jpn+jpn_vert --psm 6"
ocr_hotkey = 'ctrl+F1'
is_screenshot_valid = False


def on_clipboard_image_update():
    global is_screenshot_valid

    if not is_screenshot_valid:
        return

    image = ImageGrab.grabclipboard()

    result_string = pytesseract.image_to_string(image, config=tesseract_config)
    pyperclip.copy(result_string)

    is_screenshot_valid = False


def execute_screen_ocr(*_):
    global is_screenshot_valid

    _ = subprocess.call(['explorer.exe', 'ms-screenclip:'])
    is_screenshot_valid = True


def on_update_dummy():
    pass


def main():
    pytesseract.pytesseract.tesseract_cmd = tesseract_path

    clipboard_monitor.on_image(on_clipboard_image_update)
    clipboard_monitor.on_update(lambda: None)

    keyboard.add_hotkey(ocr_hotkey, execute_screen_ocr, args =('hotkey', 'detected'))
    keyboard.wait()


if __name__ == '__main__':
    main()

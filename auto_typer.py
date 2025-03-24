import time
import pyautogui
import keyboard
import pyperclip
import win32clipboard
import win32con

# Fail-safe feature - quickly move mouse to corner to stop
pyautogui.FAILSAFE = True

# Global flag to control typing
should_stop_typing = False

def get_clipboard_text():
    """Get text from clipboard using win32clipboard"""
    try:
        win32clipboard.OpenClipboard()
        if win32clipboard.IsClipboardFormatAvailable(win32con.CF_UNICODETEXT):
            data = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
            win32clipboard.CloseClipboard()
            return data.decode('utf-8')
        win32clipboard.CloseClipboard()
        return None
    except:
        try:
            win32clipboard.CloseClipboard()
        except:
            pass
        return None

def stop_typing():
    global should_stop_typing
    should_stop_typing = True
    print("Stopping typing...")

def type_with_delay(text, delay=0.05):
    """Type text with a consistent delay between characters"""
    global should_stop_typing
    should_stop_typing = False
    
    print("Starting to type in 3 seconds...")
    print("Make sure your cursor is where you want to type!")
    time.sleep(3)
    
    # Type the text
    for char in text:
        if should_stop_typing:
            print("Typing stopped!")
            break
        try:
            pyautogui.write(char)
            time.sleep(delay)
        except Exception as e:
            print(f"Error typing character: {e}")
            break

print("Auto-typer started!")
print("Instructions:")
print("1. Copy your text (Ctrl+C)")
print("2. Place your cursor where you want to type")
print("3. Press 'F8' to start typing")
print("4. Press 'F4' to stop typing in the middle")
print("5. Press 'Esc' to quit")
print("6. Move mouse to screen corner to force-stop")

# Register the stop typing hotkey
keyboard.on_press_key('f4', lambda _: stop_typing())

while True:
    try:
        if keyboard.is_pressed('esc'):
            print("Exiting...")
            break
            
        if keyboard.is_pressed('f8'):
            # Try both clipboard methods
            text = get_clipboard_text() or pyperclip.paste()
            if text:
                print(f"Found text in clipboard ({len(text)} characters)")
                type_with_delay(text)
            else:
                print("No text found in clipboard!")
            time.sleep(1)  # Prevent multiple triggers
            
        time.sleep(0.1)  # Reduce CPU usage
        
    except Exception as e:
        print(f"Error occurred: {e}")
        time.sleep(1) 
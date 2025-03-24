import time
import pyautogui
import keyboard
import pyperclip
import win32clipboard
import win32con

# Fail-safe feature - quickly move mouse to corner to stop
pyautogui.FAILSAFE = True

# Global flags to control typing
should_stop_typing = False
is_paused = False

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

def clean_text(text):
    """Remove tab spaces at the start of each line"""
    # Split text into lines and remove leading tabs from each line
    lines = text.split('\n')
    cleaned_lines = [line.lstrip('\t') for line in lines]
    # Join the lines back together
    return '\n'.join(cleaned_lines)

def stop_typing():
    global should_stop_typing
    should_stop_typing = True
    print("Stopping typing...")

def toggle_pause():
    global is_paused
    is_paused = not is_paused
    print("Paused" if is_paused else "Resumed")

def type_text(text):
    """Type text as fast as possible"""
    global should_stop_typing, is_paused
    should_stop_typing = False
    is_paused = False
    
    # Clean the text before typing
    text = clean_text(text)
    
    print("Starting to type in 2 seconds...")
    print("Make sure your cursor is where you want to type!")
    time.sleep(2)
    
    # Type the text
    for char in text:
        if should_stop_typing:
            print("Typing stopped!")
            break
            
        while is_paused:
            time.sleep(0.1)  # Small delay while paused
            
        try:
            pyautogui.write(char)
        except Exception as e:
            print(f"Error typing character: {e}")
            break

print("Fast Auto-typer started!")
print("Instructions:")
print("1. Copy your text (Ctrl+C)")
print("2. Place your cursor where you want to type")
print("3. Press 'F8' to start typing")
print("4. Press 'F4' to stop typing in the middle")
print("5. Press 'F9' to pause/resume typing")
print("6. Press 'Esc' to quit")
print("7. Move mouse to screen corner to force-stop")

# Register the hotkeys
keyboard.on_press_key('f4', lambda _: stop_typing())
keyboard.on_press_key('f9', lambda _: toggle_pause())

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
                type_text(text)
            else:
                print("No text found in clipboard!")
            time.sleep(0.5)  # Prevent multiple triggers
            
        time.sleep(0.1)  # Reduce CPU usage
        
    except Exception as e:
        print(f"Error occurred: {e}")
        time.sleep(1) 
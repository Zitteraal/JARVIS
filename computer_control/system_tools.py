import pyautogui
import ctypes
import time
import os
from datetime import datetime
from pathlib import Path
from core.tool_result import ToolResult

class SystemTools:
    @staticmethod
    def control_volume(action: str) -> ToolResult:
        try:
            if action == "up":
                for _ in range(5): pyautogui.press('volumeup')
                return ToolResult.success("Volume increased.")
            elif action == "down":
                for _ in range(5): pyautogui.press('volumedown')
                return ToolResult.success("Volume decreased.")
            elif action == "mute":
                pyautogui.press('volumemute')
                return ToolResult.success("Volume muted/unmuted.")
            return ToolResult.failure("Invalid volume action.")
        except Exception as e:
            return ToolResult.failure(f"Error controlling volume: {e}")

    @staticmethod
    def lock_pc() -> ToolResult:
        try:
            ctypes.windll.user32.LockWorkStation()
            return ToolResult.success("PC locked.")
        except Exception as e:
            return ToolResult.failure(f"Error locking PC: {e}")

    @staticmethod
    def take_screenshot() -> ToolResult:
        try:
            screenshots_dir = Path(os.path.expanduser("~")) / "Pictures" / "EVOX_Screenshots"
            screenshots_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = screenshots_dir / f"evox_{timestamp}.png"
            
            screenshot = pyautogui.screenshot()
            screenshot.save(file_path)
            
            return ToolResult.success(f"Screenshot saved to {file_path}")
        except Exception as e:
            return ToolResult.failure(f"Error taking screenshot: {e}")
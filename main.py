import os
import sys
import shutil
import time
import random
import numpy as np
from PIL import Image

from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.graphics import Color, Line, Rectangle, RoundedRectangle
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty, BooleanProperty, ListProperty, DictProperty
from kivy.utils import platform

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.slider import Slider
from kivy.uix.checkbox import CheckBox

# ---------- Register Custom Fonts ----------
# ---------- Register Custom Fonts ----------
# ---------- Register Custom Fonts ----------
if platform == 'win':
    LabelBase.register(
        name="RobotoMono-Regular",
        fn_regular=r"C:\Users\EintsWaveX\AppData\Local\Microsoft\Windows\Fonts\RobotoMono-Regular.ttf"
    )
    LabelBase.register(
        name="RobotoMono-Bold",
        fn_regular=r"C:\Users\EintsWaveX\AppData\Local\Microsoft\Windows\Fonts\RobotoMono-Bold.ttf"
    )
elif platform == 'android':
    LabelBase.register(
        name="RobotoMono-Regular",
        fn_regular="assets/fonts/RobotoMono-Regular.ttf"
    )
    LabelBase.register(
        name="RobotoMono-Bold",
        fn_regular="assets/fonts/RobotoMono-Bold.ttf"
    )
# ---------- Register Custom Fonts ----------
# ---------- Register Custom Fonts ----------
# ---------- Register Custom Fonts ----------

# ---------- Kivy UI Definition ----------
# ---------- Kivy UI Definition ----------
# ---------- Kivy UI Definition ----------
KV = """
<RootUI>:
    orientation: "vertical"
    padding: 6
    spacing: 6

    # ───────── Camera Area ─────────
    BoxLayout:
        size_hint_y: 0.45
        spacing: 6

        Image:
            id: cam_view
            source: ""
            fit_mode: "contain"

        Image:
            id: raw_view
            source: ""
            fit_mode: "contain"

    # ───────── Results ─────────
    BoxLayout:
        size_hint_y: 0.25
        orientation: "vertical"
        spacing: 6

        Label:
            text: root.result_text
            font_size: "20sp"
            bold: True

        Label:
            text: root.metric_text
            font_size: "14sp"
            font_name: "RobotoMono-Bold"
            # bold: True

        # ── Plastic ──
        BoxLayout:
            size_hint_y: None
            height: "26dp"

            Label:
                text: f"Plastic  {root.disp_plastic*100:.2f}%"
                size_hint_x: 0.25
                font_name: "RobotoMono-Bold"

            BoxLayout:
                canvas.before:
                    Color:
                        rgba: root.bar_colors[0]
                    Rectangle:
                        pos: self.pos
                        size: (self.width * root.disp_plastic, self.height)

                canvas.after:
                    # Inner glow
                    Color:
                        rgba: (0.8, 1, 0.8, root.glow_alpha * 0.7) if root.winner_class == "plastic" else (0, 0, 0, 0)
                    Line:
                        width: 2
                        rectangle: [self.x, self.y, self.width * root.disp_plastic, self.height]
                    
                    # Outer glow
                    Color:
                        rgba: (0.4, 1, 0.4, root.glow_alpha * 0.4) if root.winner_class == "plastic" else (0, 0, 0, 0)
                    Line:
                        width: 4
                        rectangle: [self.x-2, self.y-2, self.width * root.disp_plastic + 4, self.height + 4]

        # ── Paper ──
        BoxLayout:
            size_hint_y: None
            height: "26dp"

            Label:
                text: f"Paper    {root.disp_paper*100:.2f}%"
                size_hint_x: 0.25
                font_name: "RobotoMono-Bold"

            BoxLayout:
                canvas.before:
                    Color:
                        rgba: root.bar_colors[1]
                    Rectangle:
                        pos: self.pos
                        size: (self.width * root.disp_paper, self.height)
                
                canvas.after:
                    # Inner glow
                    Color:
                        rgba: (0.8, 1, 0.8, root.glow_alpha * 0.7) if root.winner_class == "paper" else (0, 0, 0, 0)
                    Line:
                        width: 2
                        rectangle: [self.x, self.y, self.width * root.disp_paper, self.height]
                    
                    # Outer glow
                    Color:
                        rgba: (0.4, 1, 0.4, root.glow_alpha * 0.4) if root.winner_class == "paper" else (0, 0, 0, 0)
                    Line:
                        width: 4
                        rectangle: [self.x-2, self.y-2, self.width * root.disp_paper + 4, self.height + 4]

        # ── Metal ──
        BoxLayout:
            size_hint_y: None
            height: "26dp"

            Label:
                text: f"Metal    {root.disp_metal*100:.2f}%"
                size_hint_x: 0.25
                font_name: "RobotoMono-Bold"

            BoxLayout:
                canvas.before:
                    Color:
                        rgba: root.bar_colors[2]
                    Rectangle:
                        pos: self.pos
                        size: (self.width * root.disp_metal, self.height)

                canvas.after:
                    # Inner glow
                    Color:
                        rgba: (0.8, 1, 0.8, root.glow_alpha * 0.7) if root.winner_class == "metal" else (0, 0, 0, 0)
                    Line:
                        width: 2
                        rectangle: [self.x, self.y, self.width * root.disp_metal, self.height]
                    
                    # Outer glow
                    Color:
                        rgba: (0.4, 1, 0.4, root.glow_alpha * 0.4) if root.winner_class == "metal" else (0, 0, 0, 0)
                    Line:
                        width: 4
                        rectangle: [self.x-2, self.y-2, self.width * root.disp_metal + 4, self.height + 4]
    
        # ───────── Status ─────────
        Label:
            text:
                "[PAUSED]" if root.is_paused else (
                "[RUNNING]" if root.is_running else "[STOPPED]"
                )
            font_name: "RobotoMono-Bold"
            font_size: "20sp"
            # bold: True
            color: (1,0,0,1) if root.is_paused or not root.is_running else (0,1,0,1)

    # ───────── Settings ─────────
    BoxLayout:
        size_hint_y: None
        height: "40dp"
        spacing: 10
        
        # ── Mode Selector ──
        BoxLayout:
            orientation: "horizontal"
            spacing: 5
            size_hint_x: 0.25 if root.run_mode == "esp32" else 0.35
            
            Label:
                text: "Select Running Mode:"
                font_size: "16sp"
                bold: True
                color: (1, 1, 0, 1)
                size_hint_x: 0.4
                halign: "right"
                valign: "middle"
            
            Spinner:
                text: "Simulation"
                values: ["Simulation", "ESP32-CAM"]
                on_text:
                    root.run_mode = "simulation" if self.text == "Simulation" else "esp32"
                    root._on_mode_changed()
                size_hint_x: 0.6
                background_color: (0.65, 0.65, 0.15, 1) if not root.is_running else (0.3, 0.3, 0.3, 1)
                disabled: True if root.is_running else False
        
        # ── ESP32-CAM IP Input ──
        BoxLayout:
            orientation: "horizontal"
            spacing: 5
            size_hint_x: 0.35 if root.run_mode == "esp32" else 0.001  # Tiny but not zero
            opacity: 1 if root.run_mode == "esp32" else 0
            
            Label:
                text: "Insert ESP32-CAM IP:"
                font_size: "16sp"
                bold: True
                color: (0, 1, 1, 1)
                size_hint_x: 0.3
                halign: "right"
                valign: "middle"
            
            TextInput:
                id: esp32_ip_input
                text: root.esp32_ip
                hint_text: "x.x.x.x"
                multiline: False
                font_name: "RobotoMono-Regular"
                font_size: "20sp"
                size_hint_x: 0.7
                on_text_validate: root.esp32_ip = self.text
                on_focus: if not self.focus: root.esp32_ip = self.text
        
        # ── Model Selector ──
        BoxLayout:
            orientation: "horizontal"
            spacing: 5
            size_hint_x: 0.40 if root.run_mode == "esp32" else 0.65
            
            Label:
                text: "Select Model:"
                font_size: "16sp"
                bold: True
                color: (1, 0, 1, 1)
                size_hint_x: 0.3
                halign: "right"
                valign: "middle"
            
            Spinner:
                text: root.selected_model
                font_name: "RobotoMono-Bold"
                values: root.available_models
                on_text:
                    root.on_model_selected(self.text)
                size_hint_x: 0.7
                background_color: (0.65, 0.15, 0.65, 1)

    # ───────── Main Control Panel ─────────
    BoxLayout:
        size_hint_y: 0.30
        spacing: 8

        # ── Controls Panel ──
        BoxLayout:
            orientation: "vertical"
            size_hint_x: 0.60
            spacing: 4
            padding: 4
            
            canvas.before:
                Color:
                    rgba: 0.15, 0.15, 0.15, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
                    
            # ── Top Row: Mode Selection + Clear Log Button ──
            BoxLayout:
                size_hint_y: None
                height: "40dp"
                spacing: 10

                # Mode Selection Group
                BoxLayout:
                    size_hint_x: 0.7
                    spacing: 5
                    
                    Label:
                        text: "Inference Mode:"
                        size_hint_x: 0.2
                        font_name: "RobotoMono-Bold"
                        font_size: "14sp"
                        color: (1, 1, 1, 1)
                        halign: "right"
                        valign: "middle"
                    
                    BoxLayout:
                        orientation: "vertical"
                        size_hint_x: 0.4
                        spacing: 2
                        
                        CheckBox:
                            group: "mode"
                            active: True
                            size_hint_y: 0.5
                        
                        Label:
                            text: "Single Frame"
                            font_size: "12sp"
                            size_hint_y: 0.5
                            halign: "left"
                            valign: "middle"
                    
                    BoxLayout:
                        orientation: "vertical"
                        size_hint_x: 0.4
                        spacing: 2
                        
                        CheckBox:
                            group: "mode"
                            size_hint_y: 0.5
                        
                        Label:
                            text: "Temporal Vote"
                            font_size: "12sp"
                            size_hint_y: 0.5
                            halign: "left"
                            valign: "middle"

                # Clear Debug Log Button
                BorderedButton:
                    text: "[CLEAR LOG]"
                    font_name: "RobotoMono-Bold"
                    font_size: "14sp"
                    size_hint_x: 0.3
                    background_color: (0.3, 0.3, 0.5, 1)
                    border_color: (0.45, 0.45, 0.65, 1)
                    border_radius: 2.5
                    corner_radius: 5
                    on_release: root.clear_debug_log()

            # ── Confidence Threshold ──
            Label:
                text: "Confidence Threshold (30-60%)"
                font_size: "12sp"

            # ── Confidence Slider ──
            BoxLayout:
                size_hint_y: None
                height: "36dp"
                spacing: 8
                
                Label:
                    text: "30%"
                    size_hint_x: None
                    width: "40dp"
                    font_name: "RobotoMono-Bold"
                    font_size: "14sp"
                    halign: "left"

                Slider:
                    id: confidence_slider
                    min: 30
                    max: 60
                    value: 45

                Label:
                    text: f"{int(confidence_slider.value)}%"
                    size_hint_x: None
                    width: "40dp"
                    font_name: "RobotoMono-Bold"
                    font_size: "14sp"
                    color: (0, 1, 0.6, 1)
                    halign: "right"

            # ── Frames per Capture ──
            Label:
                text: "Frames per Capture (1-10)"
                font_size: "12sp"

            # ── Frames Slider ──
            BoxLayout:
                size_hint_y: None
                height: "36dp"
                spacing: 8
                
                Label:
                    text: "1"
                    size_hint_x: None
                    width: "40dp"
                    font_name: "RobotoMono-Bold"
                    font_size: "14sp"
                    halign: "left"

                Slider:
                    id: frames_slider
                    min: 1
                    max: 10
                    value: 1

                Label:
                    text: f"{int(frames_slider.value)}"
                    size_hint_x: None
                    width: "40dp"
                    font_name: "RobotoMono-Bold"
                    font_size: "14sp"
                    color: (0, 1, 0.6, 1)
                    halign: "right"

            # ── Capture Interval ──
            Label:
                text: "Capture Interval (0.1-5s)"
                font_size: "12sp"

            # ── Interval Slider ──
            BoxLayout:
                size_hint_y: None
                height: "36dp"
                spacing: 8
                
                Label:
                    text: "0.1s"
                    size_hint_x: None
                    width: "40dp"
                    font_name: "RobotoMono-Bold"
                    font_size: "14sp"
                    halign: "left"

                Slider:
                    id: interval_slider
                    min: 1
                    max: 50
                    value: 10
                    on_value: root._on_interval_change()

                Label:
                    text: f"{(interval_slider.value / 10):.1f}s"
                    size_hint_x: None
                    width: "40dp"
                    font_name: "RobotoMono-Bold"
                    font_size: "14sp"
                    color: (0, 1, 0.6, 1)
                    halign: "right"

            # ── Control Buttons ──
            BoxLayout:
                size_hint_y: None
                height: "42dp"
                spacing: 6

                BorderedButton:
                    text: "[START]" if not root.is_paused else "[RESUME]"
                    font_name: "RobotoMono-Bold"
                    font_size: "14sp"
                    disabled: True if root.is_running and not root.is_paused else False
                    background_color: (0, 0.5, 0, 1)    if not root.is_running or root.is_paused else (0.3, 0.3, 0.3, 1)
                    border_color: (0.15, 0.65, 0.15, 1) if not root.is_running or root.is_paused else (0.45, 0.45, 0.45, 1)
                    border_radius: 2.5
                    corner_radius: 5
                    on_release: root.start()

                BorderedButton:
                    text: "[PAUSE]"
                    font_name: "RobotoMono-Bold"
                    font_size: "14sp"
                    disabled: True if not root.is_running or root.is_paused else False
                    background_color: (1, 0.5, 0, 1)    if root.is_running and not root.is_paused else (0.3, 0.3, 0.3, 1)
                    border_color: (1, 0.65, 0.15, 1)    if root.is_running and not root.is_paused else (0.45, 0.45, 0.45, 1)
                    border_radius: 2.5
                    corner_radius: 5
                    on_release: root.pause()

                BorderedButton:
                    text: "[STOP]"
                    font_name: "RobotoMono-Bold"
                    font_size: "14sp"
                    disabled: True if not root.is_running else False
                    background_color: (1, 0, 0, 1)      if root.is_running else (0.3, 0.3, 0.3, 1)
                    border_color: (1, 0.15, 0.15, 1)    if root.is_running else (0.45, 0.45, 0.45, 1)
                    border_radius: 2.5
                    corner_radius: 5
                    on_release: root.stop()

                BorderedButton:
                    text: "[RESTART]"
                    font_name: "RobotoMono-Bold"
                    font_size: "14sp"
                    disabled: True if not root.is_running else False
                    background_color: (0, 0.5, 1, 1)    if root.is_running else (0.3, 0.3, 0.3, 1)
                    border_color: (0.15, 0.65, 1, 1)    if root.is_running else (0.45, 0.45, 0.45, 1)
                    border_radius: 2.5
                    corner_radius: 5
                    on_release: root.restart()

        # ── Debug Log Panel ──
        BoxLayout:
            orientation: "vertical"
            size_hint_x: 0.40
            padding: 4
            
            canvas.before:
                Color:
                    rgba: 0.15, 0.15, 0.15, 1
                Rectangle:
                    pos: self.pos
                    size: self.size

            Label:
                text: "DEBUG LOG"
                size_hint_y: None
                height: "24dp"
                bold: True

            ScrollView:
                do_scroll_x: False

                TextInput:
                    id: debug_log
                    readonly: True
                    font_name: "RobotoMono-Regular"
                    text: root.debug_text
                    size_hint_y: None
                    height: self.minimum_height
"""
# ---------- Kivy UI Definition ----------
# ---------- Kivy UI Definition ----------
# ---------- Kivy UI Definition ----------

# ---------- Interpreter Import Based on Platform ----------
# ---------- Interpreter Import Based on Platform ----------
# ---------- Interpreter Import Based on Platform ----------
if platform == 'android':
    # First try tflite_runtime (faster, smaller)
    try:
        from tflite_runtime.interpreter import Interpreter
        print("[INFO] Using tflite_runtime on Android")
    except ImportError:
        # Fall back to full tensorflow if tflite_runtime not available
        try:
            from tensorflow.lite.python.interpreter import Interpreter
            print("[INFO] Using tensorflow.lite on Android")
        except ImportError:
            print("[ERROR] No TensorFlow Lite implementation found!")
            # Create a mock interpreter for testing
            class MockInterpreter:
                def allocate_tensors(self): pass
                def set_tensor(self, *args): pass
                def invoke(self): pass
                def get_tensor(self, *args): return [0.33, 0.33, 0.34]
                def get_input_details(self): 
                    return [{'shape': [1, 224, 224, 3], 'dtype': np.uint8}]
                def get_output_details(self): 
                    return [{'quantization': (1.0, 0)}]
            Interpreter = MockInterpreter
else:
    # Windows/Linux - use full tensorflow
    from tensorflow.lite.python.interpreter import Interpreter
    print("[INFO] Using tensorflow.lite on PC")

if platform == 'android':
    from android.storage import app_storage_path
    from jnius import autoclass
    
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    context = PythonActivity.mActivity
    
    files_dir = context.getFilesDir().getPath()
    
    APP_DIR = files_dir
    DATASET_ROOT = os.path.join(APP_DIR, 'dataset')
    MODEL_DIR = os.path.join(APP_DIR, 'assets', 'models', 'best_save')
    
    # os.makedirs(DATASET_ROOT, exist_ok=True)
    # os.makedirs(MODEL_DIR, exist_ok=True)  
else:
    DATASET_ROOT = r"C:\Users\EintsWaveX\Documents\TestPy\IWSS_KivyApp\dataset"
    MODEL_DIR = os.path.join(DATASET_ROOT, "..", "assets", "models", "best_save")
# ---------- Interpreter Import Based on Platform ----------
# ---------- Interpreter Import Based on Platform ----------
# ---------- Interpreter Import Based on Platform ----------

class BorderedButton(Button):
    border_color = ListProperty([1, 1, 1, 1])  # White by default
    border_width = NumericProperty(1.5)
    corner_radius = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bind(
            pos=self._update_canvas,
            size=self._update_canvas,
            border_color=self._update_canvas,
            background_color=self._update_canvas,
            disabled=self._update_canvas
        )
    
    def _update_canvas(self, *args):
        self.canvas.before.clear()

        if self.disabled:
            border = (0.45, 0.45, 0.45, 1)
            bg = (0.3, 0.3, 0.3, 1)
        else:
            border = self.border_color
            bg = self.background_color

        with self.canvas.before:
            Color(*border)
            if self.corner_radius > 0:
                Line(
                    width=self.border_width,
                    rounded_rectangle=(
                        self.x, self.y,
                        self.width, self.height,
                        self.corner_radius
                    )
                )
            else:
                Line(
                    width=self.border_width,
                    rectangle=(self.x, self.y, self.width, self.height)
                )

            Color(*bg)
            if self.corner_radius > 0:
                RoundedRectangle(
                    pos=(self.x + self.border_width, self.y + self.border_width),
                    size=(
                        self.width - 2*self.border_width,
                        self.height - 2*self.border_width
                    ),
                    radius=[self.corner_radius]
                )
            else:
                Rectangle(
                    pos=(self.x + self.border_width, self.y + self.border_width),
                    size=(
                        self.width - 2*self.border_width,
                        self.height - 2*self.border_width
                    )
                )

class RootUI(BoxLayout):
    if platform == 'android':
        DATASET_ROOT = DATASET_ROOT  # Use Android path
        MODEL_DIR = MODEL_DIR        # Use Android path
    else:
        DATASET_ROOT = r"C:\Users\EintsWaveX\Documents\TestPy\IWSS_KivyApp\dataset"
        MODEL_DIR = os.path.join(DATASET_ROOT, "..", "assets", "models", "best_save")
    
    CLASSES = ["plastic", "paper", "metal"]          # UI order
    MODEL_CLASSES = ["metal", "paper", "plastic"]    # Model output order
    MODEL_PATH, MODEL_NAME = "", ""
    
    model_map = {} # name → path
    first_run = True
    
    # --------------------------------------------------
    available_models = ListProperty([])
    selected_model   = StringProperty("")
    
    is_running = BooleanProperty(False)
    is_paused  = BooleanProperty(False)
    esp32_ip   = StringProperty("192.168.4.1")  # Default ESP32-CAM IP
    run_mode   = StringProperty("simulation")  # "simulation" | "esp32"
    
    result_text = StringProperty("Label: --- (--.--%)")
    metric_text = StringProperty("Model: --- (--x--) | Inference: -- ms | FPS: --/--")

    disp_plastic = NumericProperty(0.0)
    disp_paper   = NumericProperty(0.0)
    disp_metal   = NumericProperty(0.0)
    
    target_probs = DictProperty({
        "plastic": 0.0,
        "paper": 0.0,
        "metal": 0.0
    })
    bar_colors = ListProperty([
        (1, 0, 0, 1),   # Plastic
        (1, 0.5, 0, 1), # Paper
        (0, 1, 0, 1),   # Metal
    ])
    
    winner_class = StringProperty("")
    glow_alpha   = NumericProperty(0.0)

    debug_text = StringProperty("[INFO] System ready...\n")
    # --------------------------------------------------
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(run_mode=self._update_ip_input_state)
        
        # Initialize platform-specific paths
        if platform == 'android':
            from android.storage import app_storage_path
            
            app_dir = app_storage_path()
            self.DATASET_ROOT = os.path.join(app_dir, 'dataset')
            self.MODEL_DIR = os.path.join(app_dir, 'models')
        else:
            self.DATASET_ROOT = r"C:\Users\EintsWaveX\Documents\TestPy\IWSS_KivyApp\dataset"
            self.MODEL_DIR = os.path.join(self.DATASET_ROOT, "..", "assets", "models", "best_save")
        
        # Create directories if they don't exist
        if platform == 'android':
            os.makedirs(self.DATASET_ROOT, exist_ok=True)
            os.makedirs(self.MODEL_DIR, exist_ok=True)

    def on_kv_post(self, base_widget):
        if platform == 'android':
            success = self.copy_models_simple()
            if not success:
                self.debug_text += "[WARNING] Using fallback model path\n"
                from android.storage import app_storage_path
                self.MODEL_DIR = app_storage_path()
        
        self._load_dataset()
        
        self.model_map = self.discover_models()
        self.available_models = sorted(self.model_map.keys())

        if self.available_models:
            self.selected_model = self.available_models[0]
            self.MODEL_PATH = self.model_map[self.selected_model]
            self._load_model()

        self.last_time = time.time()
        self.update_event = None
    
    def copy_models_simple(self):
        """Copy models from APK assets to app storage"""
        if platform != 'android':
            return True
        
        try:
            from android.storage import app_storage_path
            
            # Get app's private storage directory
            app_dir = app_storage_path()
            android_model_dir = os.path.join(app_dir, 'models')
            os.makedirs(android_model_dir, exist_ok=True)
            
            # Copy from assets if they exist
            try:
                from jnius import autoclass
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                context = PythonActivity.mActivity
                asset_manager = context.getAssets()
                
                # List asset files (you need to know your model filenames)
                model_files = [
                    'waste_classifier-96-32-85.42.tflite',
                    'waste_classifier-128-58-88.33.tflite',
                    'waste_classifier-160-52-88.75.tflite',
                    'waste_classifier-224-60-86.67.tflite'
                ]
                
                for model_file in model_files:
                    # Try to open asset
                    try:
                        asset = asset_manager.open(model_file)
                        target_path = os.path.join(android_model_dir, model_file)
                        
                        with open(target_path, 'wb') as f:
                            f.write(asset.read())
                        self.debug_text += f"  ✓ {model_file}\n"
                        asset.close()
                    except Exception as e:
                        self.debug_text += f"  ⚠ {model_file}: {str(e)}\n"
                        
            except Exception as e:
                self.debug_text += f"[WARN] Couldn't access assets: {e}\n"
            
            self.MODEL_DIR = android_model_dir
            return True
            
        except Exception as e:
            self.debug_text += f"[ERROR] Model setup failed: {e}\n"
            return False
    
    # -─────────────── Control Handlers ───────────────
    # -─────────────── Control Handlers ───────────────
    # -─────────────── Control Handlers ───────────────

    def _clear_visuals(self):
        Animation.cancel_all(self)
        Animation(
            disp_plastic=0.0,
            disp_paper=0.0,
            disp_metal=0.0,
            duration=0.25
        ).start(self)
        Clock.schedule_once(lambda dt: self._set_zero_bars(), 0.25)
        
        self.target_probs = {
            "plastic": 0.0,
            "paper": 0.0,
            "metal": 0.0
        }
        
        self.image_index = 0
        self.current_class = random.choice(self.CLASSES)

        self.winner_class = ""
        self.glow_alpha = 0.0

        self.result_text = "Label: --- (--.--%)"
        self.metric_text = f"Model: {self.MODEL_NAME} ({self.input_w}x{self.input_h}) | Inference: -- ms | FPS: --/--"

        self.ids.cam_view.source = ""
        self.ids.raw_view.source = ""
        self.ids.cam_view.texture = None
        self.ids.raw_view.texture = None
    
    def _set_zero_bars(self):
        self.disp_plastic = 0.0
        self.disp_paper = 0.0
        self.disp_metal = 0.0
    
    def _on_interval_change(self):
        """Update the interval when slider changes"""
        if self.is_running and not self.is_paused and self.update_event:
            self.update_event.cancel()
            
            interval = self.ids.interval_slider.value / 10
            self.update_event = Clock.schedule_interval(
                self.update_from_dataset, interval
            )
    
    def _on_mode_changed(self):
        if self.run_mode == "esp32":
            self.debug_text += f"[MODE] ESP32-CAM mode selected. IP: {self.esp32_ip}\n"
            self.debug_text += "[INFO] ESP32-CAM mode: Waiting for camera stream...\n"
        else:
            self.debug_text += "[MODE] Simulation mode selected\n"
        
        if self.is_running:
            self.stop()
    
    def _validate_ip_address(self, ip):
        parts = ip.split('.')
        if len(parts) != 4:
            return False
        for part in parts:
            if not part.isdigit():
                return False
            num = int(part)
            if num < 0 or num > 255:
                return False
        return True
    
    def _update_ip_input_state(self, instance, value):
        if hasattr(self, 'ids'):
            esp32_ip_input = self.ids.get('esp32_ip_input')
            if esp32_ip_input:
                if value == "esp32":
                    esp32_ip_input.disabled = False
                    esp32_ip_input.opacity = 1
                else:
                    esp32_ip_input.disabled = True
                    esp32_ip_input.opacity = 0
    
    def start(self):
        if self.run_mode == "esp32":
            ip = self.esp32_ip
            if not ip or ip == "x.x.x.x":
                self.debug_text += "[ERROR] Please enter a valid ESP32-CAM IP address!\n"
                return
            if not self._validate_ip_address(ip):
                self.debug_text += "[ERROR] Invalid IP address format!\n"
                return
            
            self.debug_text += f"[INFO] Connecting to ESP32-CAM at {ip}...\n"
            # Here you would add code to connect to ESP32-CAM
            # For now, just show a message
            self.debug_text += "[INFO] ESP32-CAM connection not implemented yet...!\n"
            
            return
        
        # Existing simulation mode code continues...
        if self.is_paused:
            self.is_paused = False
            self.debug_text += "[STATUS] RESUMED!\n"
        else:
            self.debug_text += "[STATUS] STARTED!\n"

        if self.update_event is None:
            interval = self.ids.interval_slider.value / 10
            self.update_event = Clock.schedule_interval(
                self.update_from_dataset, interval
            )

        self.is_running = True

    def pause(self):
        if not self.is_running or self.is_paused:
            return

        if self.update_event:
            self.update_event.cancel()
            self.update_event = None

        self.is_paused = True
        self.debug_text += "[STATUS] PAUSED!\n"
    
    def stop(self):
        if self.update_event:
            self.update_event.cancel()
            self.update_event = None

        self.is_running = False
        self.is_paused = False

        self._clear_visuals()

        self.debug_text += "[STATUS] STOPPED!\n"
    
    def restart(self):
        self.stop()
        self.start()
    
    def clear_debug_log(self):
        old_text = self.debug_text
        self.debug_text = ""
        timestamp = time.strftime("%H:%M:%S")
        self.debug_text = f"[INFO] Debug log cleared at {timestamp}\n"
        
        self.ids.debug_log.background_color = (0.8, 0.8, 1, 0.3)
        Animation(background_color=(1, 1, 1, 1), duration=0.3).start(self.ids.debug_log)
    
    # -─────────────── Control Handlers ───────────────
    # -─────────────── Control Handlers ───────────────
    # -─────────────── Control Handlers ───────────────
    
    # -────────────── Dataset & Model Loading ───────────────
    # -────────────── Dataset & Model Loading ───────────────
    # -────────────── Dataset & Model Loading ───────────────
    
    def _load_dataset(self):
        self.dataset = {}
        for cls in self.CLASSES:
            folder = os.path.join(self.DATASET_ROOT, cls)
            self.dataset[cls] = [
                os.path.join(folder, f)
                for f in os.listdir(folder)
                if f.lower().endswith(".jpg")
            ]

        # self.current_class = self.CLASSES[-1]
        self.current_class = random.choice(self.CLASSES)
        self.image_index = 0
        self.debug_text += "[INFO] Dataset loaded!\n"

    def _load_model(self):
        try:
            from tflite_runtime.interpreter import Interpreter  # For Android
        except ImportError:
            from tensorflow.lite.python.interpreter import Interpreter  # For PC
        
        self.interpreter = Interpreter(
            model_path=os.path.join(self.MODEL_PATH)
        )
        self.interpreter.allocate_tensors()

        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        
        self.input_dtype  = self.input_details[0]["dtype"]
        self.output_dtype = self.output_details[0]["dtype"]

        self.input_h = self.input_details[0]["shape"][1]
        self.input_w = self.input_details[0]["shape"][2]

        self.in_scale, self.in_zero = self.input_details[0]["quantization"]
        self.out_scale, self.out_zero = self.output_details[0]["quantization"]
        
        self.MODEL_NAME = self.MODEL_PATH.split("\\")[-1]
        
        self.debug_text += (
            f"[INFO] Model loaded!\n"
        )

        # Also log from Python for comparison!
        self.debug_text += "[PYTHON COMPARISON NEEDED]\n"
        self.debug_text += "  Please run in Python and share:\n"
        self.debug_text += f"  - input_details[0]['dtype'] = {self.input_details[0]['dtype']}\n"
        self.debug_text += f"  - input_details[0]['quantization'] = {self.input_details[0]['quantization']}\n"
        self.debug_text += f"  - output_details[0]['dtype'] = {self.output_details[0]['dtype']}\n"
        self.debug_text += f"  - output_details[0]['quantization'] = {self.output_details[0]['quantization']}\n"
    
    def discover_models(self):
        models = {}
        
        # Use self.MODEL_DIR which is now platform-specific
        if os.path.exists(self.MODEL_DIR):
            for root, _, files in os.walk(self.MODEL_DIR):
                for f in files:
                    if f.endswith(".tflite"):
                        models[f] = os.path.join(root, f)
        
        if platform == 'android':
            self.debug_text += f"[INFO] Found {len(models)} model(s) in Android storage\n"
        else:
            self.debug_text += f"[INFO] Found {len(models)} model(s) in PC directory\n"
        
        return models
    
    def on_model_selected(self, model_name):
        if not model_name:
            return

        self.MODEL_PATH = self.model_map[model_name]
        self.MODEL_NAME = model_name

        if self.is_running:
            self.stop()

        self._load_model()
        self.metric_text = f"Model: {self.MODEL_NAME} ({self.input_w}x{self.input_h}) | Inference: -- ms | FPS: --/--"
        self.debug_text += f"[INFO] Model switched to: {model_name}\n"
    
    # ─────────────── Dataset & Model Loading ───────────────
    # ─────────────── Dataset & Model Loading ───────────────
    # ─────────────── Dataset & Model Loading ───────────────
    
    # ─────────────── Inference & UI Update ───────────────
    # ─────────────── Inference & UI Update ───────────────
    # ─────────────── Inference & UI Update ───────────────

    def _preprocess_input(self, img_np):
        """
        img_np: uint8 RGB image (H,W,3)
        INT8 CNN expects centered pixels
        Automatically adapts to model input type
        """
        if self.input_dtype == np.int8:
            img = img_np.astype(np.int16) - 128
            img = np.clip(img, -128, 127).astype(np.int8)
        else:
            img = img_np.astype(np.float32) / 255.0

        return np.expand_dims(img, axis=0)

    def _dequantize_output(self, output):
        return (output.astype(np.float32) - self.out_zero) * self.out_scale

    def update_from_dataset(self, dt):
        # interval = self.ids.interval_slider.value / 10  # later bind to slider
        # now = time.time()
        # if now - self.last_time < interval:
        #     return
        # self.last_time = now

        images = self.dataset[self.current_class]
        if not images:
            return

        img_path = images[self.image_index]
        self.image_index = (self.image_index + 1) % len(images)

        # ── Load image ──
        img = Image.open(img_path).convert("RGB")
        img_resized = img.resize((self.input_w, self.input_h))
        img_np = np.array(img_resized, dtype=np.uint8)

        # ── UI display ──
        img_resized.save("temp_display.jpg")
        self.ids.cam_view.source = "temp_display.jpg"
        self.ids.raw_view.source = "temp_display.jpg"
        self.ids.cam_view.reload()
        self.ids.raw_view.reload()

        # ── Preprocess (INT8) ──
        input_data = self._preprocess_input(img_np)

        # ── Inference ──
        t0 = time.time()
        self.interpreter.set_tensor(
            self.input_details[0]["index"], input_data
        )
        self.interpreter.invoke()

        raw_output = self.interpreter.get_tensor(
            self.output_details[0]["index"]
        )[0]

        # Dequantize if needed
        if self.output_dtype == np.int8:
            logits = (raw_output.astype(np.float32) - self.out_zero) * self.out_scale
        else:
            logits = raw_output.astype(np.float32)

        # Apply softmax ONLY if output is not already normalized
        if np.max(logits) > 1.0 or np.min(logits) < 0.0:
            exp = np.exp(logits - np.max(logits))
            preds = exp / np.sum(exp)
        else:
            preds = logits
        
        infer_ms = (time.time() - t0) * 1000

        # ── Update UI ──
        prob_map = dict(zip(self.MODEL_CLASSES, preds))
        
        new_winner = max(prob_map, key=prob_map.get)
        if new_winner != self.winner_class:
            self.trigger_pulse()
        
        self.target_probs = prob_map.copy()
        self.update_bar_colors()

        Animation.cancel_all(self, "disp_plastic", "disp_paper", "disp_metal")
        Animation(disp_plastic=float(prob_map["plastic"]), duration=0.25).start(self)
        Animation(disp_paper=float(prob_map["paper"]), duration=0.25).start(self)
        Animation(disp_metal=float(prob_map["metal"]), duration=0.25).start(self)
         
        best_idx = int(np.argmax(preds))
        label = self.MODEL_CLASSES[best_idx]
        conf = preds[best_idx] * 100
        
        actual_fps = 1.0 / dt if dt > 0 else 0
        target_interval = self.ids.interval_slider.value / 10
        target_fps = 1.0 / target_interval if target_interval > 0 else 0

        self.result_text = f"Label: {label.upper()} ({conf:.2f}%)"
        self.metric_text = f"Model: {self.MODEL_NAME} ({self.input_w}x{self.input_h}) | Inference: {infer_ms:.1f} ms | FPS: {int(actual_fps)}/{int(target_fps)}"

        self.debug_text += f"[INFER] {os.path.basename(img_path)} → {label}\n"

        # ── Switch class ──
        if self.image_index == 0:
            self.current_class = random.choice(self.CLASSES)
    
    def update_bar_colors(self):
        if self.is_paused:
            return
        
        probs = self.target_probs
        sorted_items = sorted(probs.items(), key=lambda x: x[1])
        
        self.winner_class = sorted_items[2][0]  # highest prob

        color_map = {
            sorted_items[0][0]: (1, 0, 0, 1),    # red
            sorted_items[1][0]: (1, 0.6, 0, 1),  # orange
            sorted_items[2][0]: (0, 1, 0, 1),    # green
        }
        
        self.bar_colors = [
            color_map["plastic"],
            color_map["paper"],
            color_map["metal"],
        ]
    
    def trigger_pulse(self):
        if self.is_paused or not self.is_running:
            return

        Animation.cancel_all(self, "glow_alpha")
        self.glow_alpha = 0.0

        # More visible glow sequence
        anim_in = Animation(glow_alpha=1.0, duration=0.2)
        anim_sustain = Animation(glow_alpha=0.8, duration=0.3)
        anim_out = Animation(glow_alpha=0.0, duration=0.5)
        
        # Chain animations
        anim_in.bind(on_complete=lambda *args: anim_sustain.start(self))
        anim_sustain.bind(on_complete=lambda *args: anim_out.start(self))
        anim_in.start(self)
    
    # ─────────────── Inference & UI Update ───────────────
    # ─────────────── Inference & UI Update ───────────────
    # ─────────────── Inference & UI Update ───────────────

class WasteSorterApp(App):
    def build(self):
        Builder.load_string(KV)
        return RootUI()

if __name__ == "__main__":
    WasteSorterApp().run()

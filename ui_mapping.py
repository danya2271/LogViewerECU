import tkinter as tk
from tkinter import ttk, messagebox
import os
import json

PRESETS_FILE = 'log_presets.json'

DEFAULT_PRESETS = {
    "OpenDiag (Январь 7.2 / Бош)": {
        "TIME": "Время, с",
        "RPM": "Скорость вращения двигателя (об/мин)",
        "TPS": "Положение дроссельной заслонки (%)",
        "UOS": "Угол опережения зажигания (°ПКВ)",
        "KNOCK": "Отскок УОЗ при детонации (°ПКВ)",
        "MAF": "Массовый расход воздуха (кг/час)",
        "GBC": "Цикловой расход воздуха (мг/такт)",
        "AFR": "Соотношение воздух/топливо",
        "INJ": "Время впрыска (мс)",
        "IAC": "Текущее положение РХХ (шаг)",
        "T_WATER": "Температура охлаждающей жидкости (°С)",
        "T_AIR": "Температура воздуха на впуске",
        "SPEED": "Скорость автомобиля (км/ч)"
    }
}

class MappingDialog:
    def __init__(self, parent, columns):
        self.top = tk.Toplevel(parent)
        self.top.title("Настройка параметров лога")
        self.top.geometry("600x750")
        
        self.columns =["<Не использовать>"] + list(columns)
        self.result = None
        self.presets = self.load_presets()

        frame_preset = ttk.LabelFrame(self.top, text="Пресеты конфигурации")
        frame_preset.pack(fill="x", padx=10, pady=5)
        self.preset_combo = ttk.Combobox(frame_preset, values=list(self.presets.keys()), state="readonly")
        self.preset_combo.pack(side="left", padx=5, pady=5, fill="x", expand=True)
        self.preset_combo.bind("<<ComboboxSelected>>", self.apply_preset)

        frame_map = ttk.LabelFrame(self.top, text="Укажите колонки данных:")
        frame_map.pack(fill="both", expand=True, padx=10, pady=5)

        self.vars = {}
        # Расширенный список параметров
        labels = {
            "TIME": "Ось времени (Сек):",
            "RPM": "Обороты двигателя (RPM):", 
            "SPEED": "Скорость авто (км/ч):",
            "TPS": "Дроссельная заслонка (%):", 
            "MAF": "ДМРВ (кг/ч) [Для мощности]:", 
            "GBC": "Цикловое наполнение (мг/ц):",
            "AFR": "Смесь (AFR / Воздух-топливо):",
            "INJ": "Время впрыска (мс):",
            "UOS": "Угол опережения зажигания (Град):", 
            "KNOCK": "Отскок УОЗ (Детонация):",
            "IAC": "Шаги РХХ:",
            "T_WATER": "Температура ОЖ (°C):",
            "T_AIR": "Температура впуска (°C):"
        }
        
        for key, text in labels.items():
            row = ttk.Frame(frame_map)
            row.pack(fill="x", pady=4, padx=5)
            ttk.Label(row, text=text, width=32).pack(side="left")
            cb = ttk.Combobox(row, values=self.columns, state="readonly", width=35)
            cb.set("<Не использовать>")
            cb.pack(side="right", fill="x", expand=True)
            self.vars[key] = cb

        frame_save = ttk.Frame(self.top)
        frame_save.pack(fill="x", padx=10, pady=5)
        self.new_preset_name = ttk.Entry(frame_save)
        self.new_preset_name.pack(side="left", fill="x", expand=True, padx=5)
        ttk.Button(frame_save, text="Сохранить как пресет", command=self.save_preset).pack(side="right", padx=5)

        ttk.Button(self.top, text="Построить графики", command=self.on_ok, style="Accent.TButton").pack(pady=15)

        if self.presets:
            self.preset_combo.set(list(self.presets.keys())[0])
            self.apply_preset()

    def load_presets(self):
        if os.path.exists(PRESETS_FILE):
            try:
                with open(PRESETS_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except: pass
        return DEFAULT_PRESETS.copy()

    def save_preset(self):
        name = self.new_preset_name.get().strip()
        if not name: return
        current_mapping = {k: v.get() for k, v in self.vars.items() if v.get() != "<Не использовать>"}
        self.presets[name] = current_mapping
        with open(PRESETS_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.presets, f, ensure_ascii=False, indent=4)
        self.preset_combo['values'] = list(self.presets.keys())
        self.preset_combo.set(name)
        messagebox.showinfo("Успех", f"Пресет '{name}' сохранен!")

    def apply_preset(self, event=None):
        preset_name = self.preset_combo.get()
        if preset_name in self.presets:
            mapping = self.presets[preset_name]
            for key, cb in self.vars.items():
                if key in mapping and mapping[key] in self.columns:
                    cb.set(mapping[key])
                else:
                    cb.set("<Не использовать>")

    def on_ok(self):
        self.result = {k: v.get() for k, v in self.vars.items() if v.get() != "<Не использовать>"}
        self.top.destroy()
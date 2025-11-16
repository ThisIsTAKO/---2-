import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import math

class VoIPSecurityGuide:
    def __init__(self, root):
        self.root = root
        self.root.title("🔒 Справочник по безопасности VoIP - Кейс 'Искра Технологии'")
        
        # Автоматическое полноэкранное отображение
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='#2c3e50')
        
        # Добавляем кнопку выхода из полноэкранного режима (опционально)
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.exit_fullscreen)
        
        # Переменные для масштабирования
        self.scale_factor = 1.0
        self.min_scale = 0.5
        self.max_scale = 3.0
        self.last_scale = 1.0
        self.canvas_width = 0
        self.canvas_height = 0
        
        # Переменные для анимации угроз
        self.current_threat = None
        self.animation_items = []
        self.protection_active = False
        
        # Создаем отдельные словари для каждой вкладки
        self.expanded_measures_cards = {}
        self.expanded_technical_cards = {}
        self.expanded_requirements_cards = {}
        self.expanded_threats_cards = {}
        
        # Стили
        self.setup_styles()
        
        # Переменные для изображения
        self.scheme_image = None
        self.photo = None
        self.original_image = None
        
        # Создаем основной фрейм
        self.main_frame = ttk.Frame(root, style='Dark.TFrame')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        self.create_widgets()
        self.load_scheme_image()
        
    def toggle_fullscreen(self, event=None):
        """Переключение полноэкранного режима по F11"""
        self.root.attributes('-fullscreen', not self.root.attributes('-fullscreen'))
        
    def exit_fullscreen(self, event=None):
        """Выход из полноэкранного режима по Escape"""
        self.root.attributes('-fullscreen', False)
        
    def setup_styles(self):
        """Настройка стилей для красивого интерфейса"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Цветовая схема
        colors = {
            'primary': '#3498db',
            'secondary': '#2ecc71', 
            'accent': '#e74c3c',
            'dark_bg': '#2c3e50',
            'darker_bg': '#34495e',
            'light_bg': '#ecf0f1',
            'text_light': '#ffffff',
            'text_dark': '#2c3e50'
        }
        
        # Настройка стилей
        style.configure('Dark.TFrame', background=colors['dark_bg'])
        style.configure('Light.TFrame', background=colors['light_bg'])
        
        style.configure('Title.TLabel', 
                       background=colors['dark_bg'],
                       foreground=colors['text_light'],
                       font=('Arial', 28, 'bold'))
        
        style.configure('Card.TLabelframe',
                       background=colors['darker_bg'],
                       foreground=colors['text_light'],
                       font=('Arial', 16, 'bold'))
        
        style.configure('Threat.TButton',
                       background='#e74c3c',
                       foreground='white',
                       font=('Arial', 14, 'bold'),
                       padding=(14, 8))
        
        style.configure('Protection.TButton',
                       background='#2ecc71', 
                       foreground='white',
                       font=('Arial', 14, 'bold'),
                       padding=(14, 8))
        
        style.map('Threat.TButton',
                 background=[('active', '#c0392b'),
                           ('pressed', '#a93226')])
        
        style.map('Protection.TButton',
                 background=[('active', '#27ae60'),
                           ('pressed', '#229954')])
        
        style.configure('Custom.TNotebook', background='#34495e')
        style.configure('Custom.TNotebook.Tab',
                       background='#34495e',
                       foreground='#bdc3c7',
                       padding=(22, 14),
                       font=('Arial', 16))
        style.map('Custom.TNotebook.Tab',
                 background=[('selected', '#3498db'),
                           ('active', '#2980b9')],
                 foreground=[('selected', 'white'),
                           ('active', 'white')])
        
    def create_widgets(self):
        # Заголовок
        self.create_header()
        
        # Создаем Notebook
        self.create_notebook()
        
        # Футер с подсказками управления
        self.create_footer()
        
    def create_header(self):
        """Создание заголовка"""
        header_frame = ttk.Frame(self.main_frame, style='Dark.TFrame')
        header_frame.pack(fill=tk.X, pady=(0, 25))
        
        title_label = tk.Label(header_frame,
                             text="🔒 Справочник по безопасности VoIP",
                             font=('Arial', 28, 'bold'),
                             bg='#2c3e50',
                             fg='#3498db',
                             pady=30)
        title_label.pack()
        
        subtitle_label = tk.Label(header_frame,
                                text="Кейс: АО «Искра Технологии» • Значимый объект КИИ 3-й категории",
                                font=('Arial', 18),
                                bg='#2c3e50', 
                                fg='#ecf0f1')
        subtitle_label.pack()
        
    def create_notebook(self):
        """Создание Notebook с вкладками"""
        self.notebook = ttk.Notebook(self.main_frame, style='Custom.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Создаем вкладки
        self.create_architecture_tab()
        self.create_tasks_tab()
        self.create_threats_tab()
        self.create_measures_tab()
        self.create_technical_tab()
        self.create_requirements_tab()
        self.create_regulations_tab()
        
    def create_scrollable_frame(self, parent):
        """Создает прокручиваемый фрейм с канвасом и скроллбарами (вертикальными и горизонтальными)"""
        # Основной фрейм для скроллинга
        container = ttk.Frame(parent, style='Light.TFrame')
        
        # Создаем канвас для скроллинга
        canvas = tk.Canvas(container, bg='#ecf0f1', highlightthickness=0)
        
        # Вертикальный и горизонтальный скроллбары
        v_scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        h_scrollbar = ttk.Scrollbar(container, orient="horizontal", command=canvas.xview)
        
        # Прокручиваемый фрейм
        scrollable_frame = ttk.Frame(canvas, style='Light.TFrame')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Упаковываем элементы
        h_scrollbar.pack(side="bottom", fill="x")
        v_scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        # Привязываем колесо мыши к канвасу
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _on_shift_mousewheel(event):
            canvas.xview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind("<MouseWheel>", _on_mousewheel)
        scrollable_frame.bind("<MouseWheel>", _on_mousewheel)
        
        # Привязываем Shift+колесо мыши для горизонтальной прокрутки
        canvas.bind("<Shift-MouseWheel>", _on_shift_mousewheel)
        scrollable_frame.bind("<Shift-MouseWheel>", _on_shift_mousewheel)
        
        return container, scrollable_frame, canvas

    def create_architecture_tab(self):
        """Вкладка с архитектурой - ИСПРАВЛЕННАЯ ВЕРСИЯ"""
        self.arch_frame = ttk.Frame(self.notebook, style='Light.TFrame')
        self.notebook.add(self.arch_frame, text="🏗️ Архитектура сети")
        
        # Заголовок
        arch_title = tk.Label(self.arch_frame,
                            text="Архитектура VoIP Сети",
                            font=('Arial', 28, 'bold'),
                            bg='#ecf0f1',
                            fg='#2c3e50',
                            pady=20)
        arch_title.pack()
        
        # Основной контейнер для схемы и панели управления
        main_content = ttk.Frame(self.arch_frame, style='Light.TFrame')
        main_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # ЛЕВАЯ ПАНЕЛЬ - управление атаками и защитой
        left_panel = ttk.Frame(main_content, style='Light.TFrame', width=400)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        left_panel.pack_propagate(False)
        
        # ПРАВАЯ ПАНЕЛЬ - схема (занимает всё оставшееся пространство)
        right_panel = ttk.Frame(main_content, style='Light.TFrame')
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # === ЛЕВАЯ ПАНЕЛЬ: Управление атаками и защитой ===
        
        # Заголовок панели управления
        control_title = tk.Label(left_panel,
                               text="🎯 Управление безопасностью",
                               font=('Arial', 18, 'bold'),
                               bg='#ecf0f1',
                               fg='#2c3e50',
                               pady=15)
        control_title.pack()
        
        # Описание
        desc_label = tk.Label(left_panel,
                             text="Выберите угрозу для визуализации, затем активируйте защиту",
                             font=('Arial', 12),
                             bg='#ecf0f1',
                             fg='#7f8c8d',
                             wraplength=350,
                             justify=tk.CENTER)
        desc_label.pack(pady=(0, 20))
        
        # Фрейм для кнопок угроз и защиты
        threats_frame = ttk.Frame(left_panel, style='Light.TFrame')
        threats_frame.pack(fill=tk.BOTH, expand=True)
        
        # Кнопки угроз - вертикальное расположение с меньшими отступами
        self.threats_data = [
            ("🔄 DDoS атаки", "ddos", "#e74c3c", "Атака на доступность сервисов"),
            ("🔓 Взлом портала", "hack", "#e67e22", "Взлом веб-интерфейсов управления"),
            ("📞 Подмена номера", "spoofing", "#f1c40f", "Caller ID спуфинг для vishing-атак"),
            ("👂 Перехват трафика", "eavesdrop", "#3498db", "Прослушивание голосовых разговоров"),
            ("🖥️ Атака на виртуализацию", "virtualization", "#9b59b6", "Компрометация гипервизора KVM")
        ]
        
        for threat_text, threat_id, color, tooltip in self.threats_data:
            btn_frame = ttk.Frame(threats_frame, style='Light.TFrame')
            btn_frame.pack(fill=tk.X, pady=5, padx=10)  # Уменьшил отступы между кнопками
            
            btn = tk.Button(btn_frame,
                          text=threat_text,
                          font=('Arial', 14, 'bold'),  # Немного уменьшил шрифт
                          bg=color,
                          fg='white',
                          relief='raised',
                          bd=2,
                          padx=15,
                          pady=10,  # Уменьшил вертикальные отступы
                          command=lambda tid=threat_id: self.show_threat(tid))
            btn.pack(fill=tk.X)
            self.create_tooltip(btn, tooltip)
            self.add_hover_effect(btn, color, self.darken_color(color, 20))
        
        # Отступ перед кнопкой защиты
        ttk.Frame(threats_frame, style='Light.TFrame', height=20).pack()
        
        # Кнопка активации защиты
        protection_btn_frame = ttk.Frame(threats_frame, style='Light.TFrame')
        protection_btn_frame.pack(fill=tk.X, pady=15, padx=10)
        
        self.protection_btn = tk.Button(protection_btn_frame,
                                      text="🛡️ АКТИВИРОВАТЬ ЗАЩИТУ",
                                      font=('Arial', 16, 'bold'),  # Немного уменьшил шрифт
                                      bg='#2ecc71',
                                      fg='white',
                                      relief='raised',
                                      bd=3,
                                      padx=20,
                                      pady=12,  # Уменьшил вертикальные отступы
                                      command=self.activate_protection,
                                      state='disabled')
        self.protection_btn.pack(fill=tk.X)
        self.add_hover_effect(self.protection_btn, '#2ecc71', '#27ae60')
        
        # === ПРАВАЯ ПАНЕЛЬ: Схема архитектуры ===
        
        scheme_frame = ttk.Frame(right_panel, style='Light.TFrame')
        scheme_frame.pack(fill=tk.BOTH, expand=True)
        
        # Canvas для изображения схемы (без масштабирования)
        self.canvas = tk.Canvas(scheme_frame,
                              bg='white',
                              highlightthickness=2,
                              highlightbackground='#3498db',
                              relief='sunken')
        
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind('<Configure>', self.resize_image_fixed)
        
        # Загружаем схему
        self.load_scheme_image()

    def resize_image_fixed(self, event=None):
        """Отображение изображения в фиксированном размере (без масштабирования)"""
        if not self.original_image:
            return
            
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            return
            
        # Отображаем изображение в максимальном размере с сохранением пропорций
        img_width, img_height = self.original_image.size
        
        # Вычисляем коэффициенты масштабирования
        width_ratio = canvas_width / img_width
        height_ratio = canvas_height / img_height
        scale_ratio = min(width_ratio, height_ratio, 1.0)  # Не увеличиваем больше оригинала
        
        display_width = int(img_width * scale_ratio)
        display_height = int(img_height * scale_ratio)
        
        resized_image = self.original_image.resize((display_width, display_height), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(resized_image)
        
        self.canvas.delete("all")
        # Центрируем изображение
        x = (canvas_width - display_width) // 2
        y = (canvas_height - display_height) // 2
        self.canvas.create_image(x, y, image=self.photo, anchor=tk.NW)

    def darken_color(self, color, percent):
        """Затемнение цвета для эффекта hover"""
        import colorsys
        # Конвертируем hex в RGB
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        
        # Конвертируем RGB в HSL
        h, l, s = colorsys.rgb_to_hls(rgb[0]/255.0, rgb[1]/255.0, rgb[2]/255.0)
        
        # Уменьшаем lightness
        l = max(0, l * (100 - percent) / 100)
        
        # Конвертируем обратно в RGB
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        
        # Конвертируем в hex
        return '#{:02x}{:02x}{:02x}'.format(int(r*255), int(g*255), int(b*255))

    def show_threat(self, threat_id):
        """Визуализация выбранной угрозы"""
        self.clear_animations()
        self.current_threat = threat_id
        self.protection_btn.config(state='normal')
        
        # Обновляем координаты для новой компоновки
        threat_positions = {
            'ddos': {'x': 600, 'y': 100, 'targets': [(800, 200), (1000, 200)]},
            'hack': {'x': 800, 'y': 150, 'targets': [(900, 250)]},
            'spoofing': {'x': 1000, 'y': 100, 'targets': [(1100, 150)]},
            'eavesdrop': {'x': 500, 'y': 100, 'targets': [(600, 200), (700, 200)]},
            'virtualization': {'x': 1100, 'y': 150, 'targets': [(900, 250)]}
        }
        
        if threat_id in threat_positions:
            pos = threat_positions[threat_id]
            self.animate_threat(threat_id, pos['x'], pos['y'], pos['targets'])

    def animate_threat(self, threat_id, start_x, start_y, targets):
        """Анимация угрозы"""
        source_size = 40
        target_size = 30
        
        # Отображаем источник угрозы
        source = self.canvas.create_oval(start_x-source_size, start_y-source_size, 
                                       start_x+source_size, start_y+source_size,
                                       fill='#e74c3c', outline='#c0392b', width=3)
        self.animation_items.append(source)
        
        threat_texts = {
            'ddos': "DDoS\nАтака",
            'hack': "Взлом\nПортала", 
            'spoofing': "Подмена\nНомера",
            'eavesdrop': "Перехват\nТрафика",
            'virtualization': "Атака на\nВиртуализацию"
        }
        
        text = self.canvas.create_text(start_x, start_y, 
                                     text=threat_texts.get(threat_id, "Угроза"),
                                     fill='white', font=('Arial', 12, 'bold'),
                                     justify=tk.CENTER)
        self.animation_items.append(text)
        
        # Анимация атаки на цели
        for i, (target_x, target_y) in enumerate(targets):
            self.root.after(i * 500, lambda tx=target_x, ty=target_y: 
                          self.animate_attack(start_x, start_y, tx, ty, threat_id, target_size))

    def animate_attack(self, start_x, start_y, target_x, target_y, threat_id, target_size):
        """Анимация атаки от источника к цели"""
        line = self.canvas.create_line(start_x, start_y, target_x, target_y,
                                     arrow=tk.LAST, arrowshape=(12, 15, 8),
                                     fill='#e74c3c', width=4, dash=(4, 2))
        self.animation_items.append(line)
        
        target = self.canvas.create_oval(target_x-target_size, target_y-target_size, 
                                       target_x+target_size, target_y+target_size,
                                       fill='#e74c3c', outline='#c0392b', width=3)
        self.animation_items.append(target)
        
        target_texts = {
            'ddos': "Сервер",
            'hack': "Веб-портал",
            'spoofing': "SIP\nСервер",
            'eavesdrop': "RTP\nПоток",
            'virtualization': "Гипервизор"
        }
        
        target_label = self.canvas.create_text(target_x, target_y, 
                                             text=target_texts.get(threat_id, "Цель"),
                                             fill='white', font=('Arial', 10, 'bold'),
                                             justify=tk.CENTER)
        self.animation_items.append(target_label)
        
        self.blink_target(target, 3)

    def blink_target(self, target, count):
        """Мигание цели атаки"""
        if count > 0:
            current_color = self.canvas.itemcget(target, 'fill')
            new_color = '#f39c12' if current_color == '#e74c3c' else '#e74c3c'
            self.canvas.itemconfig(target, fill=new_color)
            self.root.after(300, lambda: self.blink_target(target, count - 1))

    def activate_protection(self):
        """Активация защиты против текущей угрозы"""
        if not self.current_threat:
            return
            
        self.protection_active = True
        self.protection_btn.config(state='disabled')
        
        protection_data = {
            'ddos': {'type': 'firewall', 'position': (600, 100)},
            'hack': {'type': 'waf', 'position': (800, 150)},
            'spoofing': {'type': 'sbc', 'position': (1000, 100)},
            'eavesdrop': {'type': 'encryption', 'position': (500, 100)},
            'virtualization': {'type': 'hypervisor', 'position': (1100, 150)}
        }
        
        if self.current_threat in protection_data:
            data = protection_data[self.current_threat]
            self.animate_protection(data['type'], data['position'])

    def animate_protection(self, protection_type, position):
        """Анимация работы защиты - ИСПРАВЛЕННАЯ ВЕРСИЯ"""
        x, y = position
        
        protection_configs = {
            'firewall': {'text': 'NGFW\nЗащита', 'color': '#2ecc71'},
            'waf': {'text': 'WAF\nБлокировка', 'color': '#3498db'},
            'sbc': {'text': 'SBC\nВалидация', 'color': '#9b59b6'},
            'encryption': {'text': 'Шифрование\nSRTP/TLS', 'color': '#f1c40f'},
            'hypervisor': {'text': 'Гипервизор\nЗащита', 'color': '#1abc9c'}
        }
        
        config = protection_configs.get(protection_type, {'text': 'Защита', 'color': '#2ecc71'})
        
        shield = self.canvas.create_rectangle(x-60, y-35, x+60, y+35,
                                            fill=config['color'], outline='#27ae60', width=4)
        self.animation_items.append(shield)
        
        text = self.canvas.create_text(x, y, text=config['text'],
                                     fill='white', font=('Arial', 12, 'bold'),
                                     justify=tk.CENTER)
        self.animation_items.append(text)
        
        self.animate_blocking(x, y)

    def animate_blocking(self, x, y):
        """Анимация блокировки атаки - ИСПРАВЛЕННАЯ ВЕРСИЯ"""
        for i in range(3):
            barrier = self.canvas.create_rectangle(x-80-i*8, y-60-i*8, x+80+i*8, y+60+i*8,
                                                 outline='#2ecc71', width=3, dash=(2, 2))
            self.animation_items.append(barrier)
            
        self.animate_reflection()

    def animate_reflection(self):
        """Анимация отражения атаки - ИСПРАВЛЕННАЯ ВЕРСИЯ"""
        # Удаляем только линии атаки, оставляем защиту
        for item in self.animation_items[:]:
            if self.canvas.type(item) == 'line':
                self.canvas.delete(item)
                self.animation_items.remove(item)
    
        # Сообщение об успешной защите
        msg = self.canvas.create_text(400, 50, text="✅ Атака отражена! Защита сработала успешно",
                                    fill='#27ae60', font=('Arial', 16, 'bold'))
        self.animation_items.append(msg)
        
        # Автоматическая очистка через 3 секунды
        self.root.after(3000, self.clear_animations)

    def clear_animations(self):
        """Очистка всех анимационных элементов - ИСПРАВЛЕННАЯ ВЕРСИЯ"""
        for item in self.animation_items:
            self.canvas.delete(item)
        self.animation_items.clear()
        self.current_threat = None
        self.protection_active = False
        self.protection_btn.config(state='disabled')
        
        # Перерисовываем схему после очистки анимаций
        self.resize_image_fixed()

    def create_tooltip(self, widget, text):
        """Создание всплывающей подсказки"""
        def on_enter(e):
            tooltip = tk.Toplevel(widget)
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{e.x_root+10}+{e.y_root+10}")
            label = tk.Label(tooltip, text=text, background="#ffffe0", relief='solid', borderwidth=1,
                           font=('Arial', 12))
            label.pack()
            widget.tooltip = tooltip
            
        def on_leave(e):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    def add_hover_effect(self, widget, normal_color, hover_color):
        """Добавить эффект при наведении"""
        def on_enter(e):
            widget.configure(bg=hover_color)
            
        def on_leave(e):
            widget.configure(bg=normal_color)
            
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    def load_scheme_image(self):
        """Загрузка изображения схемы"""
        image_path = "voip_scheme.png"
        
        if os.path.exists(image_path):
            try:
                self.original_image = Image.open(image_path)
                self.root.after(100, self.initial_resize)
            except Exception as e:
                self.show_error_message(f"Ошибка загрузки изображения: {str(e)}")
        else:
            self.show_error_message("Файл 'voip_scheme.png' не найден в папке с программой")
            
    def show_error_message(self, message):
        """Показать сообщение об ошибке"""
        self.canvas.create_text(300, 150, text="⚠️ " + message, 
                               font=("Arial", 16, "bold"), fill="#e74c3c")
        self.canvas.create_text(300, 180, text="Поместите файл 'voip_scheme.png' в папку с программой", 
                               font=("Arial", 13), fill="#3498db")
        
    def initial_resize(self):
        """Первоначальное масштабирование изображения"""
        if self.original_image:
            self.resize_image_fixed()

    def create_tasks_tab(self):
        """Вкладка с заданиями - улучшенная версия с адаптивными блоками"""
        container, tasks_frame, canvas = self.create_scrollable_frame(self.notebook)
        self.notebook.add(container, text="📋 Задания кейса")
        
        title = tk.Label(tasks_frame, text="Задания кейса", 
                        font=('Arial', 28, 'bold'),
                        bg='#ecf0f1', fg='#2c3e50')
        title.pack(pady=20)
        
        cards_container = ttk.Frame(tasks_frame, style='Light.TFrame')
        cards_container.pack(fill=tk.BOTH, expand=True, padx=25, pady=15)
        
        tasks_data = [
            ("1", "🎯 ОПРЕДЕЛЕНИЕ ОБЪЕКТОВ ЗАЩИТЫ", "Классификация критических компонентов VoIP сети\nИдентификация точек уязвимости\nАнализ архитектуры безопасности"),
            ("2", "🔍 АНАЛИЗ АКТУАЛЬНЫХ УГРОЗ", "Определение наиболее вероятных угроз безопасности\nПриоритизация по степени воздействия на КИИ\nОценка рисков для каждого компонента"),
            ("3", "🛡️ РАЗРАБОТКА МЕР ЗАЩИТЫ", "Технические меры безопасности\nОрганизационные меры безопасности\nПроцедурные меры и политики"),
            ("4", "⚙️ ВЫБОР ТЕХНИЧЕСКИХ СРЕДСТВ", "Подбор средств защиты для каждой группы мер\nРекомендации по конкретным решениям\nИнтеграция с существующей инфраструктурой"),
            ("5", "📊 ТРЕБОВАНИЯ К ПО И ОБОРУДОВАНИЮ", "Расширенная конфигурация для КИИ 3-й категории\nТребования к отказоустойчивости\nСоответствие нормативным документам")
        ]
        
        for i, (num, title_text, desc) in enumerate(tasks_data):
            row = i // 2
            col = i % 2
            
            task_card = self.create_task_card(cards_container, num, title_text, desc)
            task_card.grid(row=row, column=col, padx=20, pady=20, sticky='nsew')
            
            cards_container.grid_rowconfigure(row, weight=1)
            cards_container.grid_columnconfigure(col, weight=1)
            
    def create_task_card(self, parent, number, title, description):
        """Создание адаптивной карточки задания"""
        card = tk.Frame(parent, bg='#34495e', relief='raised', bd=3, width=880, height=200)
        card.pack_propagate(False)
        
        num_frame = tk.Frame(card, bg='#3498db', width=80, height=80)
        num_frame.pack_propagate(False)
        num_frame.pack(side=tk.LEFT, padx=25, pady=25)
        
        num_label = tk.Label(num_frame, text=number, font=('Arial', 28, 'bold'),
                            bg='#3498db', fg='white')
        num_label.pack(expand=True)
        
        text_frame = tk.Frame(card, bg='#34495e')
        text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=25)
        
        title_label = tk.Label(text_frame, text=title, font=('Arial', 18, 'bold'),
                              bg='#34495e', fg='#3498db', anchor='w')
        title_label.pack(fill=tk.X, pady=(0, 15))
        desc_label = tk.Label(text_frame, text=description, font=('Arial', 15),
                             bg='#34495e', fg='#ecf0f1', anchor='w', justify=tk.LEFT)
        desc_label.pack(fill=tk.BOTH, expand=True)
        
        self.add_hover_effect(card, '#34495e', '#2c3e50')
        
        return card

    def create_threats_tab(self):
        """Вкладка с угрозами - с расширяемыми блоками"""
        container, threats_frame, canvas = self.create_scrollable_frame(self.notebook)
        self.notebook.add(container, text="⚠️ Анализ угроз")
        
        title = tk.Label(threats_frame, text="Анализ угроз безопасности", 
                        font=('Arial', 28, 'bold'),
                        bg='#ecf0f1', fg='#2c3e50')
        title.pack(pady=20)
        
        self.create_expandable_threats_cards(threats_frame)
        
    def create_expandable_threats_cards(self, parent):
        """Создание расширяемых карточек угроз с использованием pack"""
        main_container = ttk.Frame(parent, style='Light.TFrame')
        main_container.pack(fill=tk.BOTH, expand=True, padx=25, pady=15)
        
        # Создаем два столбца
        left_frame = ttk.Frame(main_container, style='Light.TFrame')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8)
        
        right_frame = ttk.Frame(main_container, style='Light.TFrame')
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=8)
        
        # ПОЛНЫЙ СПИСОК УГРОЗ согласно разделу 2 пояснительной записки
        threats_data = [
            {
                "id": "threat_confidentiality",
                "icon": "🔒",
                "title": "Нарушения конфиденциальности",
                "priority": "Высокий",
                "priority_color": "#e74c3c",
                "target": "Голосовой трафик (RTP), сигнальная информация (SIP, WebRTC), базы данных",
                "scenario": "Перехват трафика, несанкционированный доступ к системам управления",
                "protection": "Шифрование SRTP/TLS, MFA аутентификация, контроль доступа",
                "details": [
                    "🎯 Согласно Федеральному закону №187-ФЗ и п. 18 Приказа ФСТЭК №239:",
                    "  • Перехват голосового трафика (медиапотоков RTP) в сегментах сети",
                    "  • Несанкционированный доступ к базам данных системы управления, программного коммутатора и Web-портала",
                    "  • Копирование конфигурационных файлов критических компонентов через уязвимые сервисы",
                    "  • Утечка персональных данных абонентов, правил маршрутизации и биллинговой информации",
                    "",
                    "🛡️ Меры противодействия в соответствии с требованиями:",
                    "  • Внедрение сквозного шифрования SRTP для медиатрафика",
                    "  • Использование TLS для SIP-сигнализации (SIP over TLS)",
                    "  • Многофакторная аутентификация для доступа к системам управления",
                    "  • Сегментация сети и изоляция критичных компонентов",
                    "  • Регулярный аудит доступа и мониторинг подозрительной активности"
                ]
            },
            {
                "id": "threat_integrity", 
                "icon": "⚖️",
                "title": "Нарушения целостности",
                "priority": "Критический",
                "priority_color": "#e74c3c",
                "target": "Сигнальные сообщения, конфигурации оборудования, программное обеспечение",
                "scenario": "Модификация SIP-сообщений, изменение конфигураций, внедрение вредоносного ПО",
                "protection": "SBC валидация, контроль целостности, антивирусная защита",
                "details": [
                    "🎯 Согласно п. 18 Приказа ФСТЭК России №239:",
                    "  • Модификация сигнальных сообщений (SIP) для перенаправления вызовов",
                    "  • Изменение конфигурации сетевого оборудования через уязвимые протоколы",
                    "  • Внедрение вредоносного ПО в операционные системы виртуальных машин",
                    "  • Спуфинг абонентов и маскировка под легитимных пользователей",
                    "",
                    "🛡️ Меры противодействия согласно требованиям регуляторов:",
                    "  • Валидация SIP-сообщений с использованием SBC",
                    "  • Контроль целостности файлов и конфигураций (HIDS)",
                    "  • Регулярное обновление ПО и устранение уязвимостей",
                    "  • Использование защищенных протоколов управления (SSH, SNMPv3)",
                    "  • Мониторинг изменений конфигураций в реальном времени"
                ]
            },
            {
                "id": "threat_availability",
                "icon": "🚨", 
                "title": "Нарушения доступности",
                "priority": "Критический",
                "priority_color": "#e74c3c",
                "target": "Программный коммутатор, SBC, медиашлюзы, каналы связи",
                "scenario": "DDoS атаки, исчерпание ресурсов, блокирование систем управления",
                "protection": "Anti-DDoS системы, резервирование, мониторинг доступности",
                "details": [
                    "🎯 Согласно п. 19 Приказа ФСТЭК России №239:",
                    "  • Распределенные атаки типа 'отказ в обслуживании' на ключевые элементы",
                    "  • Исчерпание ресурсов системы целевыми атаками на VoIP-протоколы",
                    "  • Блокирование работы через компрометацию системы управления",
                    "  • Флуд SIP-INVITE и REGISTER-сообщениями",
                    "",
                    "🛡️ Меры противодействия для обеспечения устойчивости КИИ:",
                    "  • Внедрение специализированных Anti-DDoS систем",
                    "  • Резервирование критичных компонентов (SBC, коммутаторы)",
                    "  • Настройка лимитов и rate limiting для SIP-сообщений",
                    "  • Мониторинг доступности ключевых сервисов в реальном времени",
                    "  • Планирование восстановления после инцидентов"
                ]
            },
            {
                "id": "threat_vulnerabilities",
                "icon": "🕷️",
                "title": "Уязвимости ПО и инфраструктуры", 
                "priority": "Высокий",
                "priority_color": "#e67e22",
                "target": "ОС Linux, системы виртуализации KVM, прикладное ПО",
                "scenario": "Эксплуатация уязвимостей, использование закладок в ПО",
                "protection": "Регулярное обновление, контроль целостности, безопасная настройка",
                "details": [
                    "🎯 На основе 'Банка данных угроз безопасности информации' ФСТЭК:",
                    "  • Эксплуатация уязвимостей в ОС и системах виртуализации KVM",
                    "  • Использование 'закладок' в стороннем прикладном ПО",
                    "  • Несанкционированный доступ к системе управления виртуализацией",
                    "  • Компрометация всей программно-аппаратной платформы",
                    "",
                    "🛡️ Меры противодействия для защиты инфраструктуры:",
                    "  • Регулярное обновление ПО и применение патчей безопасности",
                    "  • Контроль целостности системного и прикладного ПО",
                    "  • Безопасная настройка (hardening) ОС и гипервизоров",
                    "  • Сегментация и изоляция виртуальной инфраструктуры",
                    "  • Мониторинг уязвимостей и управление исправлениями"
                ]
            },
            {
                "id": "threat_authentication",
                "icon": "🔑",
                "title": "Компрометация аутентификации",
                "priority": "Высокий", 
                "priority_color": "#e67e22",
                "target": "Учетные записи, системы аутентификации, Web-порталы",
                "scenario": "Подбор учетных данных, перехват паролей, эксплуатация уязвимостей",
                "protection": "MFA, RBAC, безопасные протоколы, WAF",
                "details": [
                    "🎯 Угрозы аутентификации и несанкционированного доступа:",
                    "  • Взлом веб-портала управления через уязвимости веб-приложений",
                    "  • Подбор учетных данных (Brute-force) к интерфейсам управления",
                    "  • Перехчет паролей при использовании незашифрованных протоколов",
                    "  • Компрометация учетных записей администраторов",
                    "",
                    "🛡️ Меры защиты систем аутентификации:",
                    "  • Внедрение многофакторной аутентификации (MFA)",
                    "  • Использование ролевой модели доступа (RBAC)",
                    "  • Замена небезопасных протоколов на SSH, HTTPS, SNMPv3",
                    "  • Внедрение WAF для защиты веб-интерфейсов",
                    "  • Мониторинг и блокировка подозрительных попыток входа"
                ]
            },
            {
                "id": "threat_social",
                "icon": "🎭",
                "title": "Социальная инженерия",
                "priority": "Средний",
                "priority_color": "#f1c40f",
                "target": "Персонал, пользователи, доверие к системе",
                "scenario": "Vishing-атаки через подмену номера, фишинг",
                "protection": "Обучение пользователей, валидация Caller ID, мониторинг",
                "details": [
                    "🎯 Угрозы целостности и доверия к данным:",
                    "  • Подмена идентификатора вызывающего номера (Caller ID Spoofing)",
                    "  • Vishing-атаки через социальную инженерию",
                    "  • Фишинг атаки на сотрудников и администраторов",
                    "  • Злоупотребление доверием к системе связи",
                    "",
                    "🛡️ Противодействие социальной инженерии:",
                    "  • Обучение и информирование пользователей о угрозах",
                    "  • Валидация Caller ID на уровне SBC и сигнализации",
                    "  • Мониторинг подозрительных вызовов и паттернов",
                    "  • Внедрение систем обнаружения мошеннических вызовов",
                    "  • Создание культуры безопасности в организации"
                ]
            }
        ]
        
        # Распределяем карточки по двум столбцам
        for i, threat in enumerate(threats_data):
            if i % 2 == 0:
                # Четные индексы - левый столбец
                card = self.create_expandable_threat_card(left_frame, threat)
                card.pack(fill=tk.X, pady=10)
            else:
                # Нечетные индексы - правый столбец
                card = self.create_expandable_threat_card(right_frame, threat)
                card.pack(fill=tk.X, pady=10)
    
    def create_expandable_threat_card(self, parent, threat_data):
        """Создание расширяемой карточки угрозы с кнопкой раскрытия в правом нижнем углу"""
        card_container = tk.Frame(parent, bg='#ecf0f1')
        
        # Основная карточка
        card = tk.Frame(card_container, bg='#34495e', relief='raised', bd=2, 
                       height=285, width=900, cursor="arrow")
        card.pack_propagate(False)
        card.pack(fill=tk.X)
        
        # Заголовок карточки
        header_frame = tk.Frame(card, bg='#2c3e50', height=70)
        header_frame.pack_propagate(False)
        header_frame.pack(fill=tk.X, padx=3, pady=3)
        
        # Верхняя часть заголовка
        top_header = tk.Frame(header_frame, bg='#2c3e50')
        top_header.pack(fill=tk.X, padx=15, pady=5)
        
        icon_frame = tk.Frame(top_header, bg='#2c3e50')
        icon_frame.pack(side=tk.LEFT)
        
        icon_label = tk.Label(icon_frame, text=threat_data["icon"], 
                             font=('Arial', 16), bg='#2c3e50', fg='white')
        icon_label.pack(side=tk.LEFT)
        
        title_label = tk.Label(icon_frame, text=threat_data["title"], 
                              font=('Arial', 16, 'bold'), bg='#2c3e50', fg='white')
        title_label.pack(side=tk.LEFT, padx=10)
        
        priority_frame = tk.Frame(top_header, bg=threat_data["priority_color"])
        priority_frame.pack(side=tk.RIGHT)
        
        priority_label = tk.Label(priority_frame, text=threat_data["priority"], 
                                font=('Arial', 12, 'bold'), bg=threat_data["priority_color"],
                                fg='white', padx=12, pady=6)
        priority_label.pack()
        
        # Содержимое карточки
        content_frame = tk.Frame(card, bg='#34495e')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Объект атаки
        target_frame = tk.Frame(content_frame, bg='#34495e')
        target_frame.pack(fill=tk.X, pady=8)
        
        target_title = tk.Label(target_frame, text="🎯 Объект:", 
                               font=('Arial', 14, 'bold'), bg='#34495e', fg='#3498db',
                               anchor='w')
        target_title.pack(side=tk.LEFT)
        
        target_text = tk.Label(target_frame, text=threat_data["target"], 
                              font=('Arial', 14), bg='#34495e', fg='#ecf0f1',
                              anchor='w')
        target_text.pack(side=tk.LEFT, padx=(10, 0), fill=tk.X, expand=True)
        
        # Сценарий атаки
        scenario_frame = tk.Frame(content_frame, bg='#34495e')
        scenario_frame.pack(fill=tk.X, pady=8)
        
        scenario_title = tk.Label(scenario_frame, text="💥 Сценарий:", 
                                font=('Arial', 14, 'bold'), bg='#34495e', fg='#e74c3c',
                                anchor='w')
        scenario_title.pack(side=tk.LEFT)
        
        scenario_text = tk.Label(scenario_frame, text=threat_data["scenario"], 
                               font=('Arial', 14), bg='#34495e', fg='#ecf0f1',
                               anchor='w')
        scenario_text.pack(side=tk.LEFT, padx=(10, 0), fill=tk.X, expand=True)
        
        # Защита
        protection_frame = tk.Frame(content_frame, bg='#34495e')
        protection_frame.pack(fill=tk.X, pady=8)
        
        protection_title = tk.Label(protection_frame, text="🛡️ Защита:", 
                                  font=('Arial', 14, 'bold'), bg='#34495e', fg='#2ecc71',
                                  anchor='w')
        protection_title.pack(side=tk.LEFT)
        
        protection_text = tk.Label(protection_frame, text=threat_data["protection"], 
                                 font=('Arial', 14), bg='#34495e', fg='#ecf0f1',
                                 anchor='w')
        protection_text.pack(side=tk.LEFT, padx=(10, 0), fill=tk.X, expand=True)
        
        # Кнопка раскрытия в правом нижнем углу
        expand_btn_frame = tk.Frame(card, bg='#34495e')
        expand_btn_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        
        expand_btn = tk.Button(expand_btn_frame,
                             text="▼",
                             font=('Arial', 11, 'bold'),
                             bg='#3498db',
                             fg='white',
                             relief='raised',
                             bd=2,
                             padx=15,
                             pady=6,
                             command=lambda tid=threat_data["id"]: self.toggle_threat_card_expansion(tid))
        expand_btn.pack(side=tk.RIGHT)
        
        # Контейнер для подробной информации
        details_container = tk.Frame(card_container, bg='#2c3e50', relief='sunken', bd=1)
        
        # Сохраняем состояние карточки
        self.expanded_threats_cards[threat_data["id"]] = {
            "expanded": False,
            "card_container": card_container,
            "details_container": details_container,
            "data": threat_data,
            "button": expand_btn  # Сохраняем ссылку на кнопку
        }
        
        self.add_hover_effect(card, '#34495e', '#2c3e50')
        
        return card_container

    def toggle_threat_card_expansion(self, card_id):
        """Переключение состояния расширения карточки угрозы - ОБНОВЛЕННАЯ ВЕРСИЯ"""
        card_data = self.expanded_threats_cards[card_id]
        
        if card_data["expanded"]:
            # Скрываем подробности
            card_data["details_container"].pack_forget()
            card_data["button"].config(text="▼")
            card_data["expanded"] = False
        else:
            # Показываем подробности
            self.show_threat_details(card_id)
            card_data["button"].config(text="▲")
            card_data["expanded"] = True
    
    def show_threat_details(self, card_id):
        """Показ подробной информации об угрозе"""
        card_data = self.expanded_threats_cards[card_id]
        details_container = card_data["details_container"]
        
        # Очищаем предыдущее содержимое
        for widget in details_container.winfo_children():
            widget.destroy()
        
        # Создаем содержимое подробной информации
        details_content = tk.Frame(details_container, bg='#2c3e50')
        details_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Добавляем разделитель
        separator = tk.Frame(details_content, bg=card_data["data"].get("priority_color", "#3498db"), height=2)
        separator.pack(fill=tk.X, pady=(0, 20))
        
        # Заголовок подробной информации
        details_title = tk.Label(details_content, 
                               text="🔍 Детальный анализ угрозы и противодействия:",
                               font=('Arial', 16, 'bold'),
                               bg='#2c3e50', fg=card_data["data"].get("priority_color", "#3498db"),
                               anchor='w')
        details_title.pack(fill=tk.X, pady=(0, 15))
        
        # Добавляем подробности
        details = card_data["data"].get("details", [])
        for detail in details:
            if detail.strip() == "":
                # Пустая строка - добавляем отступ
                tk.Frame(details_content, bg='#2c3e50', height=10).pack(fill=tk.X)
            elif detail.startswith("  •"):
                # Подпункт второго уровня
                subpoint_label = tk.Label(details_content, text=detail,
                                        font=('Arial', 13),
                                        bg='#2c3e50', fg='#bdc3c7',
                                        anchor='w', justify=tk.LEFT)
                subpoint_label.pack(fill=tk.X, padx=(50, 0), pady=2)
            elif detail.startswith("    -"):
                # Подпункт третьего уровня
                subsubpoint_label = tk.Label(details_content, text=detail,
                                           font=('Arial', 12),
                                           bg='#2c3e50', fg='#95a5a6',
                                           anchor='w', justify=tk.LEFT)
                subsubpoint_label.pack(fill=tk.X, padx=(70, 0), pady=1)
            elif ":" in detail:
                # Заголовок раздела с эмодзи
                section_label = tk.Label(details_content, text=detail,
                                       font=('Arial', 14, 'bold'),
                                       bg='#2c3e50', fg='#2ecc71',
                                       anchor='w', justify=tk.LEFT)
                section_label.pack(fill=tk.X, pady=(10, 5))
            else:
                # Обычный текст
                text_label = tk.Label(details_content, text=detail,
                                    font=('Arial', 14),
                                    bg='#2c3e50', fg='#ecf0f1',
                                    anchor='w', justify=tk.LEFT)
                text_label.pack(fill=tk.X, pady=2)
        
        # Кнопка закрытия
        close_frame = tk.Frame(details_content, bg='#2c3e50')
        close_frame.pack(fill=tk.X, pady=(20, 0))
        
        close_btn = tk.Button(close_frame, text="✕ Свернуть",
                            font=('Arial', 12, 'bold'),
                            bg='#e74c3c', fg='white',
                            relief='raised', bd=2,
                            padx=15, pady=8,
                            command=lambda: self.toggle_threat_card_expansion(card_id))
        close_btn.pack(side=tk.RIGHT)
        
        # Отображаем контейнер с подробностями ПОД основной карточкой
        details_container.pack(fill=tk.X, pady=(5, 0))

    def create_measures_tab(self):
        """Вкладка с мерами защиты с расширяемыми блоками"""
        container, measures_frame, canvas = self.create_scrollable_frame(self.notebook)
        self.notebook.add(container, text="🛡️ Меры защиты")
        
        title = tk.Label(measures_frame, text="Система мер защиты", 
                        font=('Arial', 28, 'bold'),
                        bg='#ecf0f1', fg='#2c3e50')
        title.pack(pady=20)
        
        self.create_expandable_measures_cards(measures_frame)
        
    def create_expandable_measures_cards(self, parent):
        """Создание расширяемых карточек мер защиты - ПРАВИЛЬНАЯ СТРУКТУРА"""
        main_container = ttk.Frame(parent, style='Light.TFrame')
        main_container.pack(fill=tk.BOTH, expand=True, padx=25, pady=15)
        
        left_frame = ttk.Frame(main_container, style='Light.TFrame')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8)
        
        right_frame = ttk.Frame(main_container, style='Light.TFrame')
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=8)
        
        # ОРГАНИЗАЦИОННЫЕ МЕРЫ (Раздел 3.1 пояснительной записки)
        org_title = tk.Label(left_frame, text="📝 ОРГАНИЗАЦИОННЫЕ МЕРЫ", 
                            font=('Arial', 20, 'bold'),
                            bg='#ecf0f1', fg='#2c3e50')
        org_title.pack(pady=(0, 20))
        
        # 1. Разработка организационно-распорядительной документации
        org_docs_data = {
            "id": "org_docs",
            "title": "📋 ОРГАНИЗАЦИОННО-РАСПОРЯДИТЕЛЬНАЯ ДОКУМЕНТАЦИЯ",
            "color": "#2ecc71",
            "measures": [
                "• Политика информационной безопасности объекта КИИ",
                "• Регламенты по безопасной настройке компонентов", 
                "• Правила разграничения доступа",
                "• План мероприятий по обеспечению безопасности"
            ],
            "details": [
                "📄 Политика информационной безопасности (п. 6 Приказа №239):",
                "  - Основополагающий документ, определяющий подходы и принципы защиты",
                "  - Утверждается руководством организации",
                "  - Определяет цели, задачи и ответственность за безопасность",
                "  - Регулярно пересматривается и актуализируется",
                "",
                "⚙️ Регламенты и инструкции:",
                "  - Регламенты по безопасной настройке всех компонентов сети",
                "  - Инструкции по администрированию ПО коммутатора, SBC, ОС Linux",
                "  - Процедуры настройки гипервизора KVM и сетевого оборудования",
                "  - Документация по безопасной эксплуатации систем",
                "",
                "🔐 Правила разграничения доступа:",
                "  - Основаны на принципе минимальных привилегий",
                "  - Определяют права доступа к информационным ресурсам",
                "  - Регламентируют доступ к системам управления",
                "  - Устанавливают процедуры предоставления и отзыва прав",
                "",
                "📅 План мероприятий по безопасности (п. 10 Приказа №239):",
                "  - Комплексный план обеспечения безопасности информации",
                "  - Включает сроки, ответственных и ресурсы",
                "  - Регулярно актуализируется на основе оценки рисков",
                "  - Содержит мероприятия по всем направлениям защиты"
            ]
        }
        
        org_docs_card = self.create_expandable_measures_card(left_frame, org_docs_data, height=300)
        org_docs_card.pack(fill=tk.X, pady=10)
        
        # 2. Управление персоналом и доступом
        org_personnel_data = {
            "id": "org_personnel",
            "title": "👥 УПРАВЛЕНИЕ ПЕРСОНАЛОМ И ДОСТУПОМ",
            "color": "#3498db", 
            "measures": [
                "• Регулярные проверки сотрудников",
                "• Обучение и информирование персонала",
                "• Оформление обязательств о неразглашении",
                "• Контроль доступа к объекту КИИ"
            ],
            "details": [
                "🔍 Проверки сотрудников (п. 11 Приказа №239):",
                "  - Регулярное проведение проверок сотрудников, допущенных к управлению КИИ",
                "  - Проверка в соответствии с законодательством РФ",
                "  - Установление требований к гражданам, допускаемым к работам",
                "  - Контроль соответствия персонала установленным требованиям",
                "",
                "🎓 Обучение и информирование:",
                "  - Регулярное обучение персонала политике безопасности",
                "  - Информирование о актуальных киберугрозах",
                "  - Тренинги по реагированию на инциденты",
                "  - Повышение осведомленности в области ИБ",
                "",
                "📝 Обязательства о неразглашении:",
                "  - Оформление юридически значимых документов",
                "  - Определение ответственности за разглашение информации",
                "  - Регулярное подтверждение обязательств",
                "  - Контроль соблюдения конфиденциальности",
                "",
                "🚪 Управление доступом:",
                "  - Контроль физического доступа к объекту КИИ",
                "  - Учет посещений критичных зон",
                "  - Система пропусков и идентификации",
                "  - Мониторинг действий персонала"
            ]
        }
        
        org_personnel_card = self.create_expandable_measures_card(left_frame, org_personnel_data, height=300)
        org_personnel_card.pack(fill=tk.X, pady=10)
        
        # 3. Реагирование на инциденты
        org_incidents_data = {
            "id": "org_incidents",
            "title": "🚨 РЕАГИРОВАНИЕ НА ИНЦИДЕНТЫ",
            "color": "#e74c3c",
            "measures": [
                "• Создание группы CERT/SOC",
                "• Разработка регламента по реагированию",
                "• Ведение журналов инцидентов", 
                "• Пост-инцидентный анализ"
            ],
            "details": [
                "👥 Группа реагирования (п. 26 Приказа №239):",
                "  - Создание группы реагирования на компьютерные инциденты (CERT/SOC)",
                "  - Определение состава и полномочий группы",
                "  - Обеспечение необходимыми ресурсами и инструментами",
                "  - Круглосуточная готовность к реагированию",
                "",
                "📋 Регламент по реагированию:",
                "  - Разработка и регулярное обновление регламента",
                "  - Определение порядка действий при обнаружении атак",
                "  - Процедуры эскалации инцидентов",
                "  - Взаимодействие с внешними организациями",
                "",
                "📊 Ведение журналов инцидентов:",
                "  - Систематический учет всех инцидентов безопасности",
                "  - Фиксация времени, характера и последствий инцидентов",
                "  - Документирование предпринятых мер",
                "  - Формирование статистики и отчетности",
                "",
                "🔍 Пост-инцидентный анализ:",
                "  - Анализ причин и последствий инцидентов",
                "  - Выработка рекомендаций по предотвращению",
                "  - Обновление мер защиты на основе анализа",
                "  - Информирование руководства о результатах"
            ]
        }
        
        org_incidents_card = self.create_expandable_measures_card(left_frame, org_incidents_data, height=300)
        org_incidents_card.pack(fill=tk.X, pady=10)
        
        # 4. Обеспечение надежности и восстановления
        org_recovery_data = {
            "id": "org_recovery", 
            "title": "🔄 НАДЕЖНОСТЬ И ВОССТАНОВЛЕНИЕ",
            "color": "#f39c12",
            "measures": [
                "• Резервное копирование критичных данных",
                "• Проверка целостности бэкапов",
                "• План восстановления функционирования",
                "• Тестирование процедур восстановления"
            ],
            "details": [
                "💾 Резервное копирование:",
                "  - Регулярное резервное копирование критичных данных",
                "  - Копирование конфигураций, баз данных абонентов, биллинга",
                "  - Хранение бэкапов в защищенном месте",
                "  - Автоматизация процессов резервного копирования",
                "",
                "🔍 Проверка целостности:",
                "  - Регулярная проверка целостности резервных копий",
                "  - Тестирование возможности восстановления данных",
                "  - Верификация корректности процедур бэкапа",
                "  - Контроль актуальности резервных копий",
                "",
                "📈 План восстановления:",
                "  - Разработка плана восстановления функционирования объекта КИИ",
                "  - Определение процедур восстановления после сбоев",
                "  - Установление сроков восстановления (RTO, RPO)",
                "  - Распределение ролей и ответственности",
                "",
                "🧪 Тестирование восстановления:",
                "  - Регулярное тестирование плана восстановления",
                "  - Проведение учебных тренировок по восстановлению",
                "  - Анализ результатов тестирования",
                "  - Корректировка плана на основе тестов"
            ]
        }
        
        org_recovery_card = self.create_expandable_measures_card(left_frame, org_recovery_data, height=300)
        org_recovery_card.pack(fill=tk.X, pady=10)
        
        # ТЕХНИЧЕСКИЕ МЕРЫ (Раздел 3.2 пояснительной записки)
        tech_title = tk.Label(right_frame, text="🔧 ТЕХНИЧЕСКИЕ МЕРЫ", 
                             font=('Arial', 20, 'bold'),
                             bg='#ecf0f1', fg='#2c3e50')
        tech_title.pack(pady=(0, 20))
        
        # 1. Меры по управлению доступом и аутентификации
        tech_access_data = {
            "id": "tech_access",
            "title": "🔐 УПРАВЛЕНИЕ ДОСТУПОМ И АУТЕНТИФИКАЦИЯ",
            "color": "#9b59b6",
            "measures": [
                "• Многофакторная аутентификация (МФА)",
                "• Ролевая модель доступа (RBAC)",
                "• Блокировка учетных записей",
                "• Контроль сессий администраторов"
            ],
            "details": [
                "🔑 Многофакторная аутентификация (п. 14 Приказа №239):",
                "  - Строгая аутентификация для доступа к системам управления",
                "  - Использование МФА для SSH, Web-порталов, сетевых устройств",
                "  - Комбинация паролей, токенов, биометрических данных",
                "  - Интеграция с корпоративными системами аутентификации",
                "",
                "👤 Ролевая модель доступа RBAC:",
                "  - Разграничение прав доступа на основе ролей администраторов",
                "  - Принцип минимальных привилегий для всех пользователей",
                "  - Разделение обязанностей для критичных операций",
                "  - Регулярный пересмотр и аудит прав доступа",
                "",
                "🚫 Блокировка учетных записей:",
                "  - Автоматическая блокировка при превышении числа неудачных попыток входа",
                "  - Временная блокировка при подозрительной активности",
                "  - Уведомления администраторов о блокировках",
                "  - Процедуры разблокировки учетных записей",
                "",
                "⏰ Контроль сессий:",
                "  - Ограничение времени сессий администраторов",
                "  - Принудительное завершение неактивных сессий",
                "  - Контроль одновременных сессий пользователей",
                "  - Мониторинг активности сессий в реальном времени"
            ]
        }
        
        tech_access_card = self.create_expandable_measures_card(right_frame, tech_access_data, height=300)
        tech_access_card.pack(fill=tk.X, pady=10)
        
        # 2. Меры по защите от НСД и вторжений
        tech_nsd_data = {
            "id": "tech_nsd",
            "title": "🛡️ ЗАЩИТА ОТ НСД И ВТОРЖЕНИЙ", 
            "color": "#e67e22",
            "measures": [
                "• Сегментация сети (VLAN/VXLAN)",
                "• Межсетевые экраны следующего поколения (NGFW)",
                "• Системы обнаружения/предотвращения вторжений (IDS/IPS)",
                "• Защита систем виртуализации"
            ],
            "details": [
                "🌐 Сегментация сети (п. 15 Приказа №239):",
                "  - Выделение отдельных VLAN для голосового трафика, сигнализации, управления",
                "  - Изоляция критичных систем в защищенный сегмент",
                "  - Микросегментация для ограничения lateral movement",
                "  - Контроль трафика между сегментами сети",
                "",
                "🔥 Межсетевые экраны NGFW:",
                "  - Глубокий анализ трафика на прикладном уровне (Layer 7)",
                "  - Идентификация VoIP-протоколов независимо от портов",
                "  - Блокировка прямого доступа из Интернета к критичным компонентам",
                "  - SSL-инспекция для анализа зашифрованного трафика",
                "",
                "🎯 Системы IDS/IPS:",
                "  - Анализ VoIP-трафика (SIP, RTP) на аномальную активность",
                "  - Обнаружение и блокирование сетевых атак целевого уровня",
                "  - Сигнатурный и поведенческий анализ угроз",
                "  - Интеграция с SIEM для корреляции событий",
                "",
                "🖥️ Защита виртуализации:",
                "  - Настройка безопасной конфигурации гипервизора KVM",
                "  - Разграничение прав доступа к панели управления виртуализацией",
                "  - Изоляция виртуальных машин друг от друга",
                "  - Мониторинг активности на уровне гипервизора"
            ]
        }
        
        tech_nsd_card = self.create_expandable_measures_card(right_frame, tech_nsd_data, height=300)
        tech_nsd_card.pack(fill=tk.X, pady=10)
        
        # 3. Меры по обеспечению целостности и доступности
        tech_integrity_data = {
            "id": "tech_integrity",
            "title": "⚡ ЦЕЛОСТНОСТЬ И ДОСТУПНОСТЬ",
            "color": "#2ecc71",
            "measures": [
                "• Защита от DDoS-атак",
                "• Шифрование критичной информации", 
                "• Контроль целостности ПО и конфигураций",
                "• Резервирование критичных компонентов"
            ],
            "details": [
                "🛡️ Защита от DDoS-атак (п. 19 Приказа №239):",
                "  - Использование специализированных систем DDoS Mitigation",
                "  - Очистка трафика на периметре сети",
                "  - Защита от объемных и целевых атак на уровне приложений",
                "  - Мониторинг аномалий трафика в реальном времени",
                "",
                "🔒 Шифрование информации (п. 16 Приказа №239):",
                "  - TLS для защиты сигнальной информации (SIP over TLS)",
                "  - SRTP для шифрования голосового трафика",
                "  - Криптографическая защита управляющих каналов",
                "  - Использование стойких алгоритмов шифрования",
                "",
                "📊 Контроль целостности (п. 18 Приказа №239):",
                "  - Системы контроля целостности файлов (HIDS)",
                "  - Мониторинг изменений конфигураций и ПО",
                "  - Обнаружение несанкционированных модификаций",
                "  - Аудит изменений в критичных компонентах системы",
                "",
                "🔄 Резервирование компонентов:",
                "  - Резервирование критичных компонентов (SBC, коммутаторы, каналы связи)",
                "  - Обеспечение отказоустойчивости системы",
                "  - Автоматическое переключение на резервные компоненты",
                "  - Мониторинг состояния резервных систем"
            ]
        }
        
        tech_integrity_card = self.create_expandable_measures_card(right_frame, tech_integrity_data, height=300)
        tech_integrity_card.pack(fill=tk.X, pady=10)
        
        # 4. Меры по регистрации и мониторингу
        tech_monitoring_data = {
            "id": "tech_monitoring", 
            "title": "📊 РЕГИСТРАЦИЯ И МОНИТОРИНГ",
            "color": "#3498db",
            "measures": [
                "• Централизованный сбор логов (SIEM)",
                "• Корреляция событий безопасности",
                "• Мониторинг доступности сервисов", 
                "• Аудит действий пользователей"
            ],
            "details": [
                "📈 Система SIEM (п. 24 Приказа №239):",
                "  - Централизованный сбор событий безопасности со всех компонентов",
                "  - Агрегация логов ОС, МЭ, VoIP-компонентов, СХД",
                "  - Корреляция событий для выявления сложных атак",
                "  - Автоматическое оповещение о критичных инцидентах",
                "",
                "🔗 Корреляция событий:",
                "  - Настройка правил корреляции в системе SIEM",
                "  - Выявление сложных многокомпонентных атак",
                "  - Обнаружение координированных действий злоумышленников",
                "  - Автоматизация реагирования на инциденты",
                "",
                "👁️ Мониторинг доступности:",
                "  - Организация мониторинга доступности ключевых сервисов",
                "  - Контроль качества голосовой связи (QoS)",
                "  - Мониторинг загрузки ресурсов критичных компонентов",
                "  - Автоматическое обнаружение сбоев и деградации сервиса",
                "",
                "📝 Аудит действий:",
                "  - Подробное логирование всех административных действий",
                "  - Аудит изменений конфигураций и правил безопасности",
                "  - Мониторинг действий пользователей и администраторов",
                "  - Сохранение доказательной базы для расследований"
            ]
        }
        
        tech_monitoring_card = self.create_expandable_measures_card(right_frame, tech_monitoring_data, height=300)
        tech_monitoring_card.pack(fill=tk.X, pady=10)
        
    def create_expandable_measures_card(self, parent, data, height=240):
        """Создание расширяемой карточки мер защиты с кнопкой раскрытия"""
        card_container = tk.Frame(parent, bg='#ecf0f1')
        
        # Основная карточка
        card = tk.Frame(card_container, bg='#34495e', relief='raised', bd=2, 
                       height=315, width=900, cursor="arrow")
        card.pack_propagate(False)
        card.pack(fill=tk.X)
        
        # Заголовок карточки
        header_frame = tk.Frame(card, bg=data["color"], height=60)
        header_frame.pack_propagate(False)
        header_frame.pack(fill=tk.X, padx=3, pady=3)
        
        header_content = tk.Frame(header_frame, bg=data["color"])
        header_content.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        title_label = tk.Label(header_content, text=data["title"], 
                              font=('Arial', 16, 'bold'), bg=data["color"], fg='white')
        title_label.pack(side=tk.LEFT)
        
        # Содержимое карточки
        content_frame = tk.Frame(card, bg='#34495e')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=18)
        
        # Основные меры
        for measure in data["measures"]:
            measure_label = tk.Label(content_frame, text=measure, 
                                   font=('Arial', 15), bg='#34495e', fg='#ecf0f1',
                                   anchor='w')
            measure_label.pack(fill=tk.X, pady=6)
    
        # Кнопка раскрытия в правом нижнем углу
        expand_btn_frame = tk.Frame(card, bg='#34495e')
        expand_btn_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        
        expand_btn = tk.Button(expand_btn_frame,
                             text="▼",
                             font=('Arial', 11, 'bold'),
                             bg=data["color"],
                             fg='white',
                             relief='raised',
                             bd=2,
                             padx=15,
                             pady=6,
                             command=lambda cid=data["id"]: self.toggle_measures_card_expansion(cid))
        expand_btn.pack(side=tk.RIGHT)
        
        # Контейнер для подробной информации
        details_container = tk.Frame(card_container, bg='#2c3e50', relief='sunken', bd=1)
        
        # Сохраняем состояние карточки
        self.expanded_measures_cards[data["id"]] = {
            "expanded": False,
            "card": card,
            "details_container": details_container,
            "data": data,
            "button": expand_btn
        }
        
        self.add_hover_effect(card, '#34495e', '#2c3e50')
        
        return card_container
    
    def toggle_measures_card_expansion(self, card_id):
        """Переключение состояния расширения карточки мер защиты"""
        card_data = self.expanded_measures_cards[card_id]
        
        if card_data["expanded"]:
            card_data["details_container"].pack_forget()
            card_data["button"].config(text="▼")
            card_data["expanded"] = False
        else:
            self.show_measures_details(card_id)
            card_data["button"].config(text="▲")
            card_data["expanded"] = True
    
    def show_measures_details(self, card_id):
        """Показ подробной информации карточки мер защиты"""
        card_data = self.expanded_measures_cards[card_id]
        details_container = card_data["details_container"]
        
        # Очищаем предыдущее содержимое
        for widget in details_container.winfo_children():
            widget.destroy()
        
        # Создаем содержимое подробной информации
        details_content = tk.Frame(details_container, bg='#2c3e50')
        details_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Добавляем разделитель
        separator = tk.Frame(details_content, bg=card_data["data"].get("color", "#3498db"), height=2)
        separator.pack(fill=tk.X, pady=(0, 20))
        
        # Заголовок подробной информации
        details_title = tk.Label(details_content, 
                               text="📋 Подробная информация о мерах защиты:",
                               font=('Arial', 16, 'bold'),
                               bg='#2c3e50', fg=card_data["data"].get("color", "#3498db"),
                               anchor='w')
        details_title.pack(fill=tk.X, pady=(0, 15))
        
        # Добавляем подробности
        for detail in card_data["data"]["details"]:
            if detail.strip() == "":
                # Пустая строка - добавляем отступ
                tk.Frame(details_content, bg='#2c3e50', height=10).pack(fill=tk.X)
            elif detail.startswith("  -"):
                # Подпункт
                subpoint_label = tk.Label(details_content, text=detail,
                                        font=('Arial', 13),
                                        bg='#2c3e50', fg='#bdc3c7',
                                        anchor='w', justify=tk.LEFT)
                subpoint_label.pack(fill=tk.X, padx=(30, 0), pady=2)
            elif ":" in detail:
                # Заголовок раздела с эмодзи
                section_label = tk.Label(details_content, text=detail,
                                       font=('Arial', 14, 'bold'),
                                       bg='#2c3e50', fg='#2ecc71',
                                       anchor='w', justify=tk.LEFT)
                section_label.pack(fill=tk.X, pady=(10, 5))
            else:
                # Обычный текст
                text_label = tk.Label(details_content, text=detail,
                                    font=('Arial', 14),
                                    bg='#2c3e50', fg='#ecf0f1',
                                    anchor='w', justify=tk.LEFT)
                text_label.pack(fill=tk.X, pady=2)
        
        # Кнопка закрытия
        close_frame = tk.Frame(details_content, bg='#2c3e50')
        close_frame.pack(fill=tk.X, pady=(20, 0))
        
        close_btn = tk.Button(close_frame, text="✕ Свернуть",
                            font=('Arial', 12, 'bold'),
                            bg='#e74c3c', fg='white',
                            relief='raised', bd=2,
                            padx=15, pady=8,
                            command=lambda: self.toggle_measures_card_expansion(card_id))
        close_btn.pack(side=tk.RIGHT)
        
        # Отображаем контейнер с подробностями
        details_container.pack(fill=tk.X, pady=(5, 0))

    def create_technical_tab(self):
        """Вкладка с техническими средствами - с расширяемыми блоками"""
        container, tech_frame, canvas = self.create_scrollable_frame(self.notebook)
        self.notebook.add(container, text="⚙️ Технические средства")
        
        title = tk.Label(tech_frame, text="Технические средства защиты", 
                        font=('Arial', 28, 'bold'),
                        bg='#ecf0f1', fg='#2c3e50')
        title.pack(pady=20)
        
        self.create_expandable_technical_cards(tech_frame)
        
    def create_expandable_technical_cards(self, parent):
        """Создание расширяемых карточек технических средств с использованием pack"""
        main_container = ttk.Frame(parent, style='Light.TFrame')
        main_container.pack(fill=tk.BOTH, expand=True, padx=25, pady=15)
        
        # Создаем два столбца как во вкладке "Меры защиты"
        left_frame = ttk.Frame(main_container, style='Light.TFrame')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8)
        
        right_frame = ttk.Frame(main_container, style='Light.TFrame')
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=8)
        
        technical_data = [
            {
                "id": "tech_mfa",
                "group": "🔐 МНОГОФАКТОРНАЯ АУТЕНТИФИКАЦИЯ",
                "main": "Secret Double Octopus, Рутокен ПАК, Cisco Duo",
                "alt": "VASCO Digipass, YubiKey, Google Authenticator",
                "details": [
                    "🎯 Назначение: Управление доступом и аутентификация (п. 14 Приказа №239)",
                    "  - Контроль доступа ко всем критически важным компонентам инфраструктуры",
                    "  - Строгая аутентификация для систем управления (SSH, Web-порталы)",
                    "  - Защита от компрометации учетных записей и хищения учетных данных",
                    "",
                    "⚙️ Принцип работы:",
                    "  - Требование предоставления не менее двух независимых факторов",
                    "  - Первый фактор: постоянный пароль (знание)",
                    "  - Второй фактор: одноразовый код, SMS, аппаратный токен (владение)",
                    "  - Третий фактор: биометрия (отпечаток, радужная оболочка)",
                    "",
                    "🛡️ Эффективность:",
                    "  - Противостояние угрозам компрометации учетных записей",
                    "  - Защита даже при перехвате или подборе пароля",
                    "  - Соответствие требованиям надежной аутентификации для КИИ",
                    "  - Интеграция с корпоративными системами управления доступом"
                ]
            },
            {
                "id": "tech_ngfw",
                "group": "🔥 МЕЖСЕТЕВЫЕ ЭКРАНЫ NGFW", 
                "main": "Palo Alto PA-Series, Fortinet FortiGate",
                "alt": "Check Point Quantum, Cisco Firepower NGFW",
                "details": [
                    "🎯 Назначение: Защита от НСД и контроль трафика (п. 15 Приказа №239)",
                    "  - Развертывание на границах сетевых сегментов и периметре сети",
                    "  - Контроль соединений в информационной системе и между системами",
                    "  - Защита на стыке с внешними сетями (Интернет, ТфОП)",
                    "",
                    "⚙️ Функциональность:",
                    "  - Глубокий анализ трафика на прикладном уровне (Layer 7)",
                    "  - Идентификация VoIP-протоколов (SIP, RTP, WebRTC) независимо от портов",
                    "  - Создание детализированных политик безопасности для VoIP-трафика",
                    "  - SSL-инспекция для анализа зашифрованного трафика",
                    "  - Проверка на наличие известных уязвимостей",
                    "",
                    "🛡️ Эффективность:",
                    "  - Противодействие несанкционированному доступу к компонентам VoIP",
                    "  - Блокирование сканирования сети и lateral movement",
                    "  - Предотвращение эксплуатации уязвимостей в сетевых протоколах",
                    "  - Контроль доступа из Интернета к критичным компонентам"
                ]
            },
            {
                "id": "tech_ids_ips",
                "group": "🎯 СИСТЕМЫ ОБНАРУЖЕНИЯ/ПРЕДОТВРАЩЕНИЯ ВТОРЖЕНИЙ",
                "main": "Cisco Firepower IPS, Suricata",
                "alt": "Darktrace, Positive Technologies MaxPatrol",
                "details": [
                    "🎯 Назначение: Обнаружение и предотвращение вторжений (п. 19 Приказа №239)",
                    "  - Обнаружение вторжений в информационную систему и реагирование на них",
                    "  - Анализ VoIP-трафика и выявление аномальной активности",
                    "  - Блокирование целевых атак на уровне телефонии",
                    "",
                    "⚙️ Функциональность:",
                    "  - Непрерывный анализ всего сетевого трафика включая VoIP-протоколы",
                    "  - Комбинация сигнатурного и поведенческого анализа",
                    "  - Выявление известных атак (SIP-флуд, сканирование уязвимостей)",
                    "  - Обнаружение аномалий (необычно высокое количество REGISTER/INVITE)",
                    "  - Автоматическое блокирование подозрительного трафика",
                    "",
                    "🛡️ Эффективность:",
                    "  - Противодействие целевым атакам на VoIP-протоколы",
                    "  - Защита от DDoS-атак на уровне приложений",
                    "  - Предотвращение эксплуатации уязвимостей в компонентах телефонии",
                    "  - Обнаружение попыток перехвата вызовов и несанкционированного использования"
                ]
            },
            {
                "id": "tech_ddos",
                "group": "🛡️ ЗАЩИТА ОТ DDoS-АТАК",
                "main": "Radware DefensePro, Arbor Networks APS", 
                "alt": "Qrator Labs, Wallarm, Cloudflare",
                "details": [
                    "🎯 Назначение: Обеспечение доступности (п. 19 Приказа №239)",
                    "  - Обеспечение устойчивости информационной системы к отказам в обслуживании",
                    "  - Защита публичных сервисов (Web-портал, SBC) от объемных атак",
                    "  - Обеспечение доступности услуг телефонии в условиях атак",
                    "",
                    "⚙️ Функциональность:",
                    "  - Многоуровневый подход к фильтрации трафика",
                    "  - Бихевиоральный анализ и формирование профиля нормального VoIP-трафика",
                    "  - Непрерывный мониторинг на предмет аномалий трафика",
                    "  - Автоматическое перенаправление трафика через скрабер-центры",
                    "  - Тщательная фильтрация и возврат очищенного трафика",
                    "",
                    "🛡️ Эффективность:",
                    "  - Обеспечение доступности услуг связи при интенсивных атаках",
                    "  - Защита от исчерпания ресурсов процессора, памяти, пропускной способности",
                    "  - Противодействие как объемным, так и целевым атакам на приложения",
                    "  - Соответствие требованиям по обеспечению устойчивости объекта КИИ"
                ]
            },
            {
                "id": "tech_crypto",
                "group": "🔒 ШИФРОВАНИЕ ИНФОРМАЦИИ",
                "main": "TLS/SRTP в ПО (Asterisk, FreeSWITCH)",
                "alt": "Аппаратные SBC (Ribbon, Oracle ACME Packet)",
                "details": [
                    "🎯 Назначение: Криптографическая защита информации (п. 16 Приказа №239)",
                    "  - Защита информации от уничтожения, блокирования, модификации и копирования",
                    "  - Обеспечение конфиденциальности и целостности передаваемой информации",
                    "  - Защита сигнальной информации и голосового трафика",
                    "",
                    "⚙️ Реализация:",
                    "  - SIP over TLS для шифрования сигнальных сообщений",
                    "  - SRTP (Secure Real-time Transport Protocol) для медиапотоков",
                    "  - Аутентификация сторон и защита от подмены",
                    "  - Аппаратные средства криптографической защиты для ответственных сегментов",
                    "  - Создание защищенных виртуальных каналов между узлами связи",
                    "",
                    "🛡️ Эффективность:",
                    "  - Противодействие перехвату голосового трафика и сигнальной информации",
                    "  - Защита от прослушивания переговоров и спуфинга",
                    "  - Предотвращение модификации вызовов и подмены абонентов",
                    "  - Соответствие требованиям по криптографической защите информации КИИ"
                ]
            },
            {
                "id": "tech_hids",
                "group": "📊 КОНТРОЛЬ ЦЕЛОСТНОСТИ",
                "main": "Wazuh, OSSEC, AIDE", 
                "alt": "Tripwire, Osquery, Falco",
                "details": [
                    "🎯 Назначение: Контроль целостности ПО и конфигураций (п. 18 Приказа №239)",
                    "  - Контроль целостности программной среды и информации в информационной системе",
                    "  - Обнаружение несанкционированных изменений в критичных компонентах",
                    "  - Мониторинг файловых систем серверов VoIP-инфраструктуры",
                    "",
                    "⚙️ Функциональность:",
                    "  - Периодическое вычисление криптографических хэш-сумм (SHA-256, SHA-512)",
                    "  - Сравнение с эталонными значениями в защищенной базе данных",
                    "  - Мониторинг исполняемых файлов, конфигураций, системных библиотек",
                    "  - Немедленное оповещение при обнаружении неавторизованных изменений",
                    "  - Интеграция с SIEM-системой для централизованного управления",
                    "",
                    "🛡️ Эффективность:",
                    "  - Выявление несанкционированных изменений ПО и конфигураций",
                    "  - Обнаружение внедрения закладок, руткитов и вредоносного кода",
                    "  - Контроль действий инсайдеров по модификации параметров системы",
                    "  - Раннее обнаружение компрометации на стадии изменения файлов"
                ]
            },
            {
                "id": "tech_siem",
                "group": "📈 СИСТЕМЫ SIEM",
                "main": "Splunk Enterprise Security, IBM QRadar",
                "alt": "Micro Focus ArcSight, MAXPATROL SIEM",
                "details": [
                    "🎯 Назначение: Регистрация и мониторинг событий (п. 24 Приказа №239)",
                    "  - Регистрация событий безопасности в информационной системе",
                    "  - Обеспечение возможности анализа событий безопасности",
                    "  - Централизованный сбор и корреляция данных безопасности",
                    "",
                    "⚙️ Функциональность:",
                    "  - Централизованный сбор, нормализация, корреляция и анализ событий",
                    "  - Агрегация данных с VoIP-компонентов, ОС, МЭ, IPS, HIDS",
                    "  - Настройка сложных правил корреляции для выявления многозвенных атак",
                    "  - Автоматическое присвоение приоритетов и уведомление группы реагирования",
                    "  - Запуск автоматизированных сценариев реагирования на инциденты",
                    "",
                    "🛡️ Эффективность:",
                    "  - Своевременное обнаружение сложных многозвенных атак",
                    "  - Координация действий по реагированию на инциденты",
                    "  - Накопление доказательной базы для расследований",
                    "  - Обеспечение ситуационной осведомленности о состоянии безопасности"
                ]
            },
            {
                "id": "tech_sbc",
                "group": "📞 SESSION BORDER CONTROLLER",
                "main": "AudioCodes Mediant, Ribbon SBC SWe", 
                "alt": "Cisco CUBE, Oracle ACME Packet",
                "details": [
                    "🎯 Назначение: Защита инфраструктуры VoIP на границе сессий",
                    "  - Ключевой элемент безопасности VoIP-инфраструктуры",
                    "  - Защита от атак на уровне сигнализации и медиатрафика",
                    "  - Обеспечение безопасного взаимодействия с внешними сетями",
                    "",
                    "⚙️ Функциональность:",
                    "  - Нормализация и проверка SIP-сообщений",
                    "  - Защита от флуда, сканирования и атак с подделкой (SPIT)",
                    "  - Топология hiding - сокрытие внутренней структуры сети",
                    "  - Принудительное использование SRTP для шифрования медиатрафика",
                    "  - Аутентификация и авторизация всех SIP-запросов",
                    "",
                    "🛡️ Эффективность:",
                    "  - Защита от целевых атак на VoIP-протоколы",
                    "  - Предотвращение несанкционированного доступа к услугам связи",
                    "  - Обеспечение конфиденциальности коммуникаций",
                    "  - Соответствие требованиям по защите периметра VoIP-инфраструктуры"
                ]
            }
        ]
        
        # Распределяем карточки по двум столбцам
        for i, tech in enumerate(technical_data):
            if i % 2 == 0:
                card = self.create_expandable_tech_card(left_frame, tech)
                card.pack(fill=tk.X, pady=10)
            else:
                card = self.create_expandable_tech_card(right_frame, tech)
                card.pack(fill=tk.X, pady=10)
            
    def create_expandable_tech_card(self, parent, tech_data):
        """Создание расширяемой карточки технических средств с кнопкой раскрытия"""
        card_container = tk.Frame(parent, bg='#ecf0f1')
        
        # Основная карточка
        card = tk.Frame(card_container, bg='#34495e', relief='raised', bd=3, 
                       height=250, width=900, cursor="arrow")
        card.pack_propagate(False)
        card.pack(fill=tk.X)
        
        # Заголовок карточки
        group_frame = tk.Frame(card, bg='#3498db', height=60)
        group_frame.pack_propagate(False)
        group_frame.pack(fill=tk.X, padx=4, pady=4)
        
        group_content = tk.Frame(group_frame, bg='#3498db')
        group_content.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        group_label = tk.Label(group_content, text=tech_data["group"], 
                              font=('Arial', 18, 'bold'),
                              bg='#3498db', fg='white')
        group_label.pack(side=tk.LEFT)
        
        # Содержимое карточки
        content_frame = tk.Frame(card, bg='#34495e')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=20)
        
        main_label = tk.Label(content_frame, text=f"🎯 Основное: {tech_data['main']}", 
                             font=('Arial', 15, 'bold'),
                             bg='#34495e', fg='#2ecc71', anchor='w')
        main_label.pack(fill=tk.X, pady=(0, 12))
        
        alt_label = tk.Label(content_frame, text=f"📋 Альтернативы:\n{tech_data['alt']}", 
                            font=('Arial', 14),
                            bg='#34495e', fg='#bdc3c7', anchor='w', 
                            justify=tk.LEFT)
        alt_label.pack(fill=tk.BOTH, expand=True)
        
        # Кнопка раскрытия в правом нижнем углу
        expand_btn_frame = tk.Frame(card, bg='#34495e')
        expand_btn_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        
        expand_btn = tk.Button(expand_btn_frame,
                             text="▼",
                             font=('Arial', 11, 'bold'),
                             bg='#3498db',
                             fg='white',
                             relief='raised',
                             bd=2,
                             padx=15,
                             pady=6,
                             command=lambda tid=tech_data["id"]: self.toggle_technical_card_expansion(tid))
        expand_btn.pack(side=tk.RIGHT)
        
        # Контейнер для подробной информации
        details_container = tk.Frame(card_container, bg='#2c3e50', relief='sunken', bd=1)
        
        # Сохраняем состояние карточки
        self.expanded_technical_cards[tech_data["id"]] = {
            "expanded": False,
            "card_container": card_container,
            "details_container": details_container,
            "data": tech_data,
            "button": expand_btn
        }
        
        self.add_hover_effect(card, '#34495e', '#2c3e50')
        
        return card_container

    def toggle_technical_card_expansion(self, card_id):
        """Переключение состояния расширения карточки технических средств"""
        card_data = self.expanded_technical_cards[card_id]
        
        if card_data["expanded"]:
            card_data["details_container"].pack_forget()
            card_data["button"].config(text="▼")
            card_data["expanded"] = False
        else:
            self.show_technical_details(card_id)
            card_data["button"].config(text="▲")
            card_data["expanded"] = True
    
    def show_technical_details(self, card_id):
        """Показ подробной информации технического средства"""
        card_data = self.expanded_technical_cards[card_id]
        details_container = card_data["details_container"]
        
        # Очищаем предыдущее содержимое
        for widget in details_container.winfo_children():
            widget.destroy()
        
        # Создаем содержимое подробной информации
        details_content = tk.Frame(details_container, bg='#2c3e50')
        details_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Добавляем разделитель
        separator = tk.Frame(details_content, bg='#3498db', height=2)
        separator.pack(fill=tk.X, pady=(0, 20))
        
        # Заголовок подробной информации
        details_title = tk.Label(details_content, 
                               text="📋 Подробная информация и спецификации:",
                               font=('Arial', 16, 'bold'),
                               bg='#2c3e50', fg='#3498db',
                               anchor='w')
        details_title.pack(fill=tk.X, pady=(0, 15))
        
        # Добавляем подробности
        details = card_data["data"].get("details", [])
        for detail in details:
            if detail.strip() == "":
                # Пустая строка - добавляем отступ
                tk.Frame(details_content, bg='#2c3e50', height=10).pack(fill=tk.X)
            elif detail.startswith("  -"):
                # Подпункт
                subpoint_label = tk.Label(details_content, text=detail,
                                        font=('Arial', 13),
                                        bg='#2c3e50', fg='#bdc3c7',
                                        anchor='w', justify=tk.LEFT)
                subpoint_label.pack(fill=tk.X, padx=(30, 0), pady=2)
            elif ":" in detail:
                # Заголовок раздела с эмодзи
                section_label = tk.Label(details_content, text=detail,
                                       font=('Arial', 14, 'bold'),
                                       bg='#2c3e50', fg='#2ecc71',
                                       anchor='w', justify=tk.LEFT)
                section_label.pack(fill=tk.X, pady=(10, 5))
            else:
                # Обычный текст
                text_label = tk.Label(details_content, text=detail,
                                    font=('Arial', 14),
                                    bg='#2c3e50', fg='#ecf0f1',
                                    anchor='w', justify=tk.LEFT)
                text_label.pack(fill=tk.X, pady=2)
        
        # Кнопка закрытия
        close_frame = tk.Frame(details_content, bg='#2c3e50')
        close_frame.pack(fill=tk.X, pady=(20, 0))
        
        close_btn = tk.Button(close_frame, text="✕ Свернуть",
                            font=('Arial', 12, 'bold'),
                            bg='#e74c3c', fg='white',
                            relief='raised', bd=2,
                            padx=15, pady=8,
                            command=lambda: self.toggle_technical_card_expansion(card_id))
        close_btn.pack(side=tk.RIGHT)
        
        # Отображаем контейнер с подробностями ПОД основной карточкой
        details_container.pack(fill=tk.X, pady=(5, 0))

    def create_requirements_tab(self):
        """Вкладка с требованиями для КИИ с расширяемыми блоками"""
        container, req_frame, canvas = self.create_scrollable_frame(self.notebook)
        self.notebook.add(container, text="📊 Требования для КИИ")
        
        title = tk.Label(req_frame, text="Требования для КИИ 3-й категории", 
                        font=('Arial', 28, 'bold'),
                        bg='#ecf0f1', fg='#2c3e50')
        title.pack(pady=20)
        
        self.create_expandable_requirements_cards(req_frame)
        
    def create_expandable_requirements_cards(self, parent):
        """Создание расширяемых карточек требований с использованием pack"""
        main_container = ttk.Frame(parent, style='Light.TFrame')
        main_container.pack(fill=tk.BOTH, expand=True, padx=25, pady=15)
        
        # Создаем два столбца
        left_frame = ttk.Frame(main_container, style='Light.TFrame')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8)
        
        right_frame = ttk.Frame(main_container, style='Light.TFrame')
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=8)
        
        requirements_data = [
            {
                "id": "req_app_software",
                "icon": "🔐",
                "category": "ПРИКЛАДНОЕ ПО",
                "color": "#3498db",
                "requirements": [
                    "Безопасная разработка и поставка (п. 18 Приказа №239)",
                    "Учет и управление доступом (RBAC, MFA)",
                    "Защита информации (TLS, SRTP)",
                    "Устойчивость к VoIP-атакам"
                ],
                "details": [
                    "📦 Безопасная разработка и поставка (п. 18 Приказа №239):",
                    "  - Поставка ПО только через защищенные каналы связи",
                    "  - Проверка целостности и подлинности дистрибутивов",
                    "  - Требование соблюдения практик Secure SDLC от вендоров",
                    "  - Соответствие Приказу ФСТЭК №41 от 14.03.2022",
                    "  - Предоставление документации по безопасной настройке",
                    "",
                    "🔑 Учет и управление доступом (п. 14 Приказа №239):",
                    "  - Поддержка разграничения прав доступа на основе RBAC",
                    "  - Стойкая аутентификация с интеграцией МФА",
                    "  - Протоколирование всех критичных действий",
                    "  - Контроль сессий и времени доступа",
                    "  - Блокировка при превышении попыток входа",
                    "",
                    "🛡️ Защита информации:",
                    "  - Поддержка TLS для SIP-сигнализации (SIP over TLS)",
                    "  - Использование SRTP для шифрования медиатрафика",
                    "  - Соответствие Приказу ФСТЭК №21 от 10.02.2022",
                    "  - Защищенное хранение паролей и ключей шифрования",
                    "  - Реализация Perfect Forward Secrecy",
                    "",
                    "⚡ Устойчивость к атакам:",
                    "  - Устойчивость к типовым VoIP-атакам (SIP-флуд, спуфинг)",
                    "  - Тестирование на проникновение (Penetration Testing)",
                    "  - Защита от сканирования и reconnaissance-атак",
                    "  - Обработка некорректных и malformed-пакетов"
                ]
            },
            {
                "id": "req_system_software",
                "icon": "💻", 
                "category": "СИСТЕМНОЕ ПО (LINUX)",
                "color": "#2ecc71",
                "requirements": [
                    "Защищенная настройка (hardening)",
                    "Минимизация функциональности",
                    "Регулярное обновление ПО",
                    "Контроль целостности (HIDS)"
                ],
                "details": [
                    "🔒 Защищенная настройка (hardening):",
                    "  - Использование актуальных поддерживаемых дистрибутивов",
                    "  - Реализация защищенной настройки по руководствам ФСТЭК",
                    "  - Настройка SELinux/AppArmor в режиме Enforcing",
                    "  - Применение кастомных политик для VoIP-ПО",
                    "  - Бездисковые (stateless) системы с RO корневой ФС",
                    "",
                    "🎯 Минимизация функциональности (п. 17 Приказа №239):",
                    "  - Отключение неиспользуемых сетевых служб и портов",
                    "  - Удаление ненужного ПО и демонов",
                    "  - Ограничение прав процессов и пользователей",
                    "  - Настройка firewall на уровне ОС",
                    "  - Конфигурация минимально необходимых прав доступа",
                    "",
                    "🔄 Регулярное обновление (п. 18 Приказа №239):",
                    "  - Регулярное обновление для устранения известных уязвимостей",
                    "  - Автоматическое применение security-патчей",
                    "  - Тестирование обновлений в тестовой среде",
                    "  - Мониторинг уязвимостей CVE для используемого ПО",
                    "  - План отката при проблемах с обновлениями",
                    "",
                    "📊 Контроль целостности:",
                    "  - Установка и настройка HIDS (Wazuh, OSSEC, AIDE)",
                    "  - Мониторинг критичных файлов конфигураций",
                    "  - Контроль исполняемых файлов и системных библиотек",
                    "  - Обнаружение несанкционированных изменений в реальном времени"
                ]
            },
            {
                "id": "req_virtualization",
                "icon": "🖥️",
                "category": "СИСТЕМА ВИРТУАЛИЗАЦИИ (KVM)", 
                "color": "#e67e22",
                "requirements": [
                    "Изоляция виртуальных машин",
                    "Разграничение прав доступа",
                    "Защита образов ВМ",
                    "Сетевые меры безопасности"
                ],
                "details": [
                    "🔒 Изоляция виртуальных машин:",
                    "  - Обеспечение изоляции ВМ друг от друга и от хостовой системы",
                    "  - Использование 'Укрепленного гипервизора' на минимальном дистрибутиве",
                    "  - Защита от VM escape-атак и меж-VM атак",
                    "  - Настройка лимитов ресурсов для каждой ВМ",
                    "  - Автоматическое анти-аффинити для критичных сервисов",
                    "",
                    "👤 Разграничение прав доступа:",
                    "  - Разграничение прав доступа администраторов к панели управления",
                    "  - RBAC для управления виртуальной инфраструктурой",
                    "  - Аудит всех действий с гипервизором и ВМ",
                    "  - Многофакторная аутентификация для доступа к управлению",
                    "  - Принцип минимальных привилегий для администраторов",
                    "",
                    "💾 Защита образов ВМ:",
                    "  - Защита образов виртуальных машин от несанкционированного доступа",
                    "  - Шифрование конфигураций ВМ и снапшотов",
                    "  - Контроль целостности образов ВМ",
                    "  - Защита от копирования и несанкционированного распространения",
                    "  - Регулярное обновление базовых образов (golden images)",
                    "",
                    "🌐 Сетевые меры безопасности:",
                    "  - Использование выделенных изолированных сетей для управления",
                    "  - Строгая изоляция на уровне vSwitch с VLAN и MAC-фильтрацией",
                    "  - Сегментация виртуальной сети по функциональному назначению",
                    "  - Контроль меж-VM трафика и предотвращение lateral movement"
                ]
            },
            {
                "id": "req_server_hardware",
                "icon": "🔩",
                "category": "СЕРВЕРНОЕ ОБОРУДОВАНИЕ",
                "color": "#9b59b6",
                "requirements": [
                    "Аппаратное доверие (PFR, Secure Boot)",
                    "Аппаратное шифрование (SED)",
                    "Удаленное управление (iDRAC, iLO)",
                    "Мониторинг состояния"
                ],
                "details": [
                    "🛡️ Аппаратное доверие:",
                    "  - Поддержка аппаратного доверия по цепочке загрузки",
                    "  - Intel PFR (Platform Firmware Resilience) или AMD Secure Boot",
                    "  - TPM 2.0 для проверки целостности при загрузке",
                    "  - UEFI Secure Boot с подписанными образами",
                    "  - Защита от атак на прошивку UEFI/BIOS",
                    "",
                    "🔐 Аппаратное шифрование:",
                    "  - Self-Encrypting Drives (SED) с автоматическим шифрованием",
                    "  - Управление ключами через HSM или специализированные системы",
                    "  - Crypto-erase при изъятии дисков из системы",
                    "  - Прозрачное шифрование 'на лету' без нагрузки на CPU",
                    "  - Поддержка стандартов шифрования FIPS 140-2/3",
                    "",
                    "🎛️ Удаленное управление:",
                    "  - Поддержка безопасного удаленного управления (iDRAC, iLO)",
                    "  - Обязательное использование шифрования для управления",
                    "  - Строгая аутентификация для доступа к системам управления",
                    "  - Аудит всех действий удаленного управления",
                    "  - Изоляция интерфейсов управления в отдельной сети",
                    "",
                    "📈 Мониторинг состояния:",
                    "  - Аппаратный мониторинг состояния компонентов",
                    "  - Контроль температуры, состояния дисков, памяти, вентиляторов",
                    "  - Предупреждения о предотказном состоянии компонентов",
                    "  - Интеграция с системами мониторинга инфраструктуры",
                    "  - Прогнозирование отказов и планирование замены оборудования"
                ]
            },
            {
                "id": "req_network_equipment",
                "icon": "📡",
                "category": "СЕТЕВОЕ ОБОРУДОВАНИЕ", 
                "color": "#e74c3c",
                "requirements": [
                    "Обновление микропрограмм",
                    "Безопасные протоколы управления",
                    "Защита консоли управления",
                    "Поддержка стандартов"
                ],
                "details": [
                    "🔄 Обновление микропрограмм:",
                    "  - Возможность обновления микропрограммного обеспечения",
                    "  - Регулярное применение обновлений безопасности",
                    "  - Тестирование обновлений в тестовой среде",
                    "  - План отката при проблемах с обновлениями",
                    "  - Мониторинг уязвимостей для сетевого оборудования",
                    "",
                    "🔐 Безопасные протоколы управления:",
                    "  - Поддержка безопасных протоколов управления (SSH, SNMPv3)",
                    "  - Полный отказ от небезопасных протоколов (Telnet, FTP, SNMPv1/v2c)",
                    "  - Использование TLS для веб-интерфейсов управления",
                    "  - Аутентификация на основе сертификатов для административного доступа",
                    "  - Шифрование всего трафика управления",
                    "",
                    "🚪 Защита консоли управления:",
                    "  - Наличие средств защиты от несанкционированного доступа к консоли",
                    "  - Аутентификация для доступа к физическим интерфейсам",
                    "  - Блокировка при превышении попыток входа",
                    "  - Аудит всех действий через консоль управления",
                    "  - Физическая защита сетевого оборудования",
                    "",
                    "📋 Поддержка стандартов:",
                    "  - Для медиашлюзов - поддержка SRTP и TLS",
                    "  - Поддержка современных стандартов шифрования",
                    "  - Соответствие отраслевым стандартам связи",
                    "  - Сертификация оборудования для использования в КИИ",
                    "  - Поддержка функций безопасности (MACsec, 802.1X)"
                ]
            },
            {
                "id": "req_general",
                "icon": "🎯",
                "category": "ОБЩИЕ ТРЕБОВАНИЯ",
                "color": "#f1c40f",
                "requirements": [
                    "Жизненный цикл и сопровождение",
                    "Документирование и регламентация", 
                    "Резервирование и отказоустойчивость",
                    "Соответствие нормативным актам"
                ],
                "details": [
                    "📅 Жизненный цикл и сопровождение:",
                    "  - Все компоненты должны находиться на активной стадии жизненного цикла",
                    "  - Регулярное получение обновлений безопасности от производителя",
                    "  - Техническая поддержка для всех компонентов инфраструктуры",
                    "  - Запрет использования неподдерживаемого ПО и оборудования",
                    "  - План миграции при окончании поддержки компонентов",
                    "",
                    "📋 Документирование и регламентация (п. 6, 10 Приказа №239):",
                    "  - Разработка регламентов по безопасной настройке всех компонентов",
                    "  - Инструкции по администрированию и обновлению",
                    "  - Документация по архитектуре и конфигурациям безопасности",
                    "  - Процедуры реагирования на инциденты для каждого компонента",
                    "  - Регулярный пересмотр и актуализация документации",
                    "",
                    "🔄 Резервирование и отказоустойчивость (п. 19 Приказа №239):",
                    "  - Резервирование всех критичных компонентов (серверы, каналы, SBC)",
                    "  - Обеспечение требуемой доступности услуги связи",
                    "  - Автоматическое переключение на резервные компоненты",
                    "  - Географическое распределение критичной инфраструктуры",
                    "  - Регулярное тестирование отказоустойчивости системы",
                    "",
                    "⚖️ Соответствие нормативным актам:",
                    "  - Полное соответствие требованиям ФСТЭК России №239",
                    "  - Соответствие смежным НПА (№187-ФЗ, №152-ФЗ, №126-ФЗ)",
                    "  - Сертификация средств защиты информации при необходимости",
                    "  - Регулярные аудиты и проверки соответствия",
                    "  - Документирование выполнения всех требований регуляторов"
                ]
            }
        ]
        
        # Распределяем карточки по двум столбцам
        for i, requirement in enumerate(requirements_data):
            if i % 2 == 0:
                card = self.create_expandable_requirement_card(left_frame, requirement)
                card.pack(fill=tk.X, pady=10)
            else:
                card = self.create_expandable_requirement_card(right_frame, requirement)
                card.pack(fill=tk.X, pady=10)
    
    def create_expandable_requirement_card(self, parent, requirement_data):
        """Создание расширяемой карточки требований с кнопкой раскрытия"""
        card_container = tk.Frame(parent, bg='#ecf0f1')
        
        # Основная карточка
        card = tk.Frame(card_container, bg='#34495e', relief='raised', bd=2, 
                       height=320, width=900, cursor="arrow")
        card.pack_propagate(False)
        card.pack(fill=tk.X)
        
        # Заголовок карточки
        header_frame = tk.Frame(card, bg=requirement_data["color"], height=70)
        header_frame.pack_propagate(False)
        header_frame.pack(fill=tk.X, padx=3, pady=3)
        
        header_content = tk.Frame(header_frame, bg=requirement_data["color"])
        header_content.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        icon_frame = tk.Frame(header_content, bg=requirement_data["color"])
        icon_frame.pack(side=tk.LEFT)
        
        icon_label = tk.Label(icon_frame, text=requirement_data["icon"], 
                             font=('Arial', 22), bg=requirement_data["color"], fg='white')
        icon_label.pack(side=tk.LEFT)
        
        title_label = tk.Label(icon_frame, text=requirement_data["category"], 
                              font=('Arial', 18, 'bold'), bg=requirement_data["color"], fg='white')
        title_label.pack(side=tk.LEFT, padx=12)
        
        # Содержимое карточки
        content_frame = tk.Frame(card, bg='#34495e')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=18)
        
        for i, requirement in enumerate(requirement_data["requirements"]):
            req_frame = tk.Frame(content_frame, bg='#34495e')
            req_frame.pack(fill=tk.X, pady=6)
            
            number_label = tk.Label(req_frame, text=f"{i+1}.", font=('Arial', 14, 'bold'),
                                  bg='#34495e', fg=requirement_data["color"])
            number_label.pack(side=tk.LEFT)
            
            req_text = tk.Label(req_frame, text=requirement, 
                              font=('Arial', 14), bg='#34495e', fg='#ecf0f1',
                              anchor='w', justify=tk.LEFT)
            req_text.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        # Кнопка раскрытия в правом нижнем углу
        expand_btn_frame = tk.Frame(card, bg='#34495e')
        expand_btn_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        
        expand_btn = tk.Button(expand_btn_frame,
                             text="▼",
                             font=('Arial', 11, 'bold'),
                             bg=requirement_data["color"],
                             fg='white',
                             relief='raised',
                             bd=2,
                             padx=15,
                             pady=6,
                             command=lambda rid=requirement_data["id"]: self.toggle_requirements_card_expansion(rid))
        expand_btn.pack(side=tk.RIGHT)
        
        # Контейнер для подробной информации
        details_container = tk.Frame(card_container, bg='#2c3e50', relief='sunken', bd=1)
        
        # Сохраняем состояние карточки
        self.expanded_requirements_cards[requirement_data["id"]] = {
            "expanded": False,
            "card_container": card_container,
            "details_container": details_container,
            "data": requirement_data,
            "button": expand_btn
        }
        
        self.add_hover_effect(card, '#34495e', '#2c3e50')
        
        return card_container

    def toggle_requirements_card_expansion(self, card_id):
        """Переключение состояния расширения карточки требований"""
        card_data = self.expanded_requirements_cards[card_id]
        
        if card_data["expanded"]:
            card_data["details_container"].pack_forget()
            card_data["button"].config(text="▼")
            card_data["expanded"] = False
        else:
            self.show_requirements_details(card_id)
            card_data["button"].config(text="▲")
            card_data["expanded"] = True
    
    def show_requirements_details(self, card_id):
        """Показ подробной информации требований"""
        card_data = self.expanded_requirements_cards[card_id]
        details_container = card_data["details_container"]
        
        # Очищаем предыдущее содержимое
        for widget in details_container.winfo_children():
            widget.destroy()
        
        # Создаем содержимое подробной информации
        details_content = tk.Frame(details_container, bg='#2c3e50')
        details_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Добавляем разделитель
        separator = tk.Frame(details_content, bg=card_data["data"].get("color", "#3498db"), height=2)
        separator.pack(fill=tk.X, pady=(0, 20))
        
        # Заголовок подробной информации
        details_title = tk.Label(details_content, 
                               text="📋 Подробная информация и спецификации:",
                               font=('Arial', 16, 'bold'),
                               bg='#2c3e50', fg=card_data["data"].get("color", "#3498db"),
                               anchor='w')
        details_title.pack(fill=tk.X, pady=(0, 15))
        
        # Добавляем подробности
        details = card_data["data"].get("details", [])
        for detail in details:
            if detail.strip() == "":
                # Пустая строка - добавляем отступ
                tk.Frame(details_content, bg='#2c3e50', height=10).pack(fill=tk.X)
            elif detail.startswith("  -"):
                # Подпункт
                subpoint_label = tk.Label(details_content, text=detail,
                                        font=('Arial', 13),
                                        bg='#2c3e50', fg='#bdc3c7',
                                        anchor='w', justify=tk.LEFT)
                subpoint_label.pack(fill=tk.X, padx=(30, 0), pady=2)
            elif ":" in detail:
                # Заголовок раздела с эмодзи
                section_label = tk.Label(details_content, text=detail,
                                       font=('Arial', 14, 'bold'),
                                       bg='#2c3e50', fg='#2ecc71',
                                       anchor='w', justify=tk.LEFT)
                section_label.pack(fill=tk.X, pady=(10, 5))
            else:
                # Обычный текст
                text_label = tk.Label(details_content, text=detail,
                                    font=('Arial', 14),
                                    bg='#2c3e50', fg='#ecf0f1',
                                    anchor='w', justify=tk.LEFT)
                text_label.pack(fill=tk.X, pady=2)
        
        # Кнопка закрытия
        close_frame = tk.Frame(details_content, bg='#2c3e50')
        close_frame.pack(fill=tk.X, pady=(20, 0))
        
        close_btn = tk.Button(close_frame, text="✕ Свернуть",
                            font=('Arial', 12, 'bold'),
                            bg='#e74c3c', fg='white',
                            relief='raised', bd=2,
                            padx=15, pady=8,
                            command=lambda: self.toggle_requirements_card_expansion(card_id))
        close_btn.pack(side=tk.RIGHT)
        
        # Отображаем контейнер с подробностями ПОД основной карточкой
        details_container.pack(fill=tk.X, pady=(5, 0))

    def create_regulations_tab(self):
        """Вкладка с нормативно-правовыми актами"""
        container, reg_frame, canvas = self.create_scrollable_frame(self.notebook)
        self.notebook.add(container, text="📚 НПА КИИ")
        
        title = tk.Label(reg_frame, text="Нормативно-Правовые Акты для КИИ", 
                        font=('Arial', 24, 'bold'),
                        bg='#ecf0f1', fg='#2c3e50')
        title.pack(pady=15)
        
        self.create_regulations_cards(reg_frame)
        
    def create_regulations_cards(self, parent):
        """Создание карточек нормативно-правовых актов"""
        cards_container = ttk.Frame(parent, style='Light.TFrame')
        cards_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        regulations_data = [
            {
                "icon": "⚖️",
                "title": "Федеральный закон от 26.07.2017 № 187-ФЗ",
                "type": "🔑 Ключевой НПА",
                "type_color": "#e74c3c",
                "adopted_by": "Госдума, Совет Федерации",
                "date": "26.07.2017",
                "content": "Определяет основные понятия (КИИ, значимый объект, инцидент), субъектов КИИ, принципы обеспечения безопасности, полномочия госорганов (ФСТЭК, ФСБ). Устанавливает обязанность по обеспечению безопасности и категорированию объектов."
            },
            {
                "icon": "📋",
                "title": "Указ Президента РФ от 16.08.2004 № 1085",
                "type": "🔑 Ключевой НПА", 
                "type_color": "#e74c3c",
                "adopted_by": "Президент РФ",
                "date": "16.08.2004",
                "content": "Наделяет ФСТЭК России полномочиями по разработке и принятию нормативных актов в области безопасности КИИ, а также по контролю и надзору."
            },
            {
                "icon": "🛡️",
                "title": "Приказ ФСТЭК России от 25.12.2017 № 239",
                "type": "🔑 Ключевой НПА",
                "type_color": "#e74c3c",
                "adopted_by": "ФСТЭК России",
                "date": "25.12.2017", 
                "content": "Устанавливает конкретные детальные требования по 6-ти мерам безопасности: 1. Организация защиты; 2. Инцидентный менеджмент; 3. Управление доступом; 4. Защита среды; 5. Защита ТС/СВТ; 6. Защита ПАК."
            },
            {
                "icon": "🔍",
                "title": "Приказ ФСТЭК России от 21.12.2017 № 235",
                "type": "📖 Сопутствующий НПА",
                "type_color": "#3498db",
                "adopted_by": "ФСТЭК России",
                "date": "21.12.2017",
                "content": "Регламентирует процедуру проведения проверок ФСТЭК соблюдения требований безопасности. Знание этого документа важно для подготовки к аудиту."
            },
            {
                "icon": "📊",
                "title": "Приказ ФСТЭК России от 25.12.2017 № 240", 
                "type": "📖 Сопутствующий НПА",
                "type_color": "#3498db",
                "adopted_by": "ФСТЭК России",
                "date": "25.12.2017",
                "content": "Детально описывает методику присвоения категории значимому объекту КИИ (в нашем случае - 3-я категория). Объясняет, по каким критериям производится оценка."
            },
            {
                "icon": "🔄",
                "title": "Приказ ФСТЭК России от 08.11.2021 № 239",
                "type": "📖 Сопутствующий НПА",
                "type_color": "#3498db",
                "adopted_by": "ФСТЭК России", 
                "date": "08.11.2021",
                "content": "Более современный и детализированный документ, развивающий требования Приказа №239. Содержит 68 конкретных мероприятий по защите. Крайне важен для проектирования современной СЗИ."
            },
            {
                "icon": "💾",
                "title": "Приказ ФСТЭК России от 11.02.2013 № 17",
                "type": "📖 Сопутствующий НПА",
                "type_color": "#3498db",
                "adopted_by": "ФСТЭК России",
                "date": "11.02.2013",
                "content": "Хотя напрямую не про КИИ, его требования к средствам защиты информации (СЗИ) часто используются на практике. Регламентирует использование межсетевых экранов, СОВ, антивирусов."
            },
            {
                "icon": "👤",
                "title": "Федеральный закон от 27.07.2006 № 152-ФЗ",
                "type": "📖 Сопутствующий НПА",
                "type_color": "#3498db", 
                "adopted_by": "Госдума РФ",
                "date": "27.07.2006",
                "content": "Поскольку в VoIP-системе обрабатываются данные абонентов (номера, история звонков), необходимо соблюдать требования по защите персональных данных. Требует их шифрования, регламентирования обработки и т.д."
            },
            {
                "icon": "📝",
                "title": "Приказ ФСТЭК России от 18.02.2013 № 21",
                "type": "📖 Сопутствующий НПА",
                "type_color": "#3498db",
                "adopted_by": "ФСТЭК России",
                "date": "18.02.2013",
                "content": "Устанавливает конкретные меры для выполнения Закона №152-ФЗ. Требует, среди прочего, автоматической регистрации событий в системе (что пересекается с требованиями по аудиту для КИИ)."
            },
            {
                "icon": "📡",
                "title": "Федеральный закон от 07.07.2003 № 126-ФЗ",
                "type": "🏭 Отраслевой НПА", 
                "type_color": "#2ecc71",
                "adopted_by": "Госдума РФ",
                "date": "07.07.2003",
                "content": "Определяет общие принципы работы сетей связи на территории РФ. Устанавливает обязанность операторов связи обеспечивать устойчивость и безопасность сетей связи."
            },
            {
                "icon": "📋",
                "title": "Постановление Правительства РФ от 16.03.2021 № 396",
                "type": "🏭 Отраслевой НПА",
                "type_color": "#2ecc71",
                "adopted_by": "Правительство РФ",
                "date": "16.03.2021",
                "content": "Может требовать проведения обязательной сертификации некоторых технических средств связи, используемых в инфраструктуре."
            }
        ]
        
        for i, regulation in enumerate(regulations_data):
            row = i // 2
            col = i % 2
            
            card = self.create_regulation_card(cards_container, regulation)
            card.grid(row=row, column=col, padx=15, pady=15, sticky='nsew')
            
            cards_container.grid_rowconfigure(row, weight=1)
            cards_container.grid_columnconfigure(col, weight=1)
    
    def create_regulation_card(self, parent, regulation_data):
        """Создание карточки нормативно-правового акта"""
        card = tk.Frame(parent, bg='#34495e', relief='raised', bd=2, 
                       width=890, height=300)
        card.pack_propagate(False)
        
        header_frame = tk.Frame(card, bg='#2c3e50', height=55)
        header_frame.pack_propagate(False)
        header_frame.pack(fill=tk.X, padx=2, pady=2)
        
        icon_frame = tk.Frame(header_frame, bg='#2c3e50')
        icon_frame.pack(side=tk.LEFT, padx=12, pady=8)
        
        icon_label = tk.Label(icon_frame, text=regulation_data["icon"], 
                             font=('Arial', 14), bg='#2c3e50', fg='white')
        icon_label.pack(side=tk.LEFT)
        
        title_label = tk.Label(icon_frame, text=regulation_data["title"], 
                              font=('Arial', 12, 'bold'), bg='#2c3e50', fg='white',
                              wraplength=600, justify=tk.LEFT)
        title_label.pack(side=tk.LEFT, padx=6)
        
        type_frame = tk.Frame(header_frame, bg=regulation_data["type_color"])
        type_frame.pack(side=tk.RIGHT, padx=12, pady=8)
        
        type_label = tk.Label(type_frame, text=regulation_data["type"], 
                             font=('Arial', 12, 'bold'), bg=regulation_data["type_color"],
                             fg='white', padx=6, pady=3)
        type_label.pack()
        
        content_frame = tk.Frame(card, bg='#34495e')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=12)
        
        adoption_frame = tk.Frame(content_frame, bg='#34495e')
        adoption_frame.pack(fill=tk.X, pady=4)
        
        adopted_title = tk.Label(adoption_frame, text="👤 Принят:", 
                               font=('Arial', 14, 'bold'), bg='#34495e', fg='#3498db',
                               anchor='w')
        adopted_title.pack(side=tk.LEFT)
        
        adopted_text = tk.Label(adoption_frame, text=regulation_data["adopted_by"], 
                              font=('Arial', 14), bg='#34495e', fg='#ecf0f1',
                              anchor='w')
        adopted_text.pack(side=tk.LEFT, padx=(6, 0))
        
        date_frame = tk.Frame(content_frame, bg='#34495e')
        date_frame.pack(fill=tk.X, pady=4)
        
        date_title = tk.Label(date_frame, text="📅 Дата:", 
                            font=('Arial', 14, 'bold'), bg='#34495e', fg='#3498db',
                            anchor='w')
        date_title.pack(side=tk.LEFT)
        
        date_text = tk.Label(date_frame, text=regulation_data["date"], 
                           font=('Arial', 14), bg='#34495e', fg='#ecf0f1',
                           anchor='w')
        date_text.pack(side=tk.LEFT, padx=(6, 0))
        
        content_title_frame = tk.Frame(content_frame, bg='#34495e')
        content_title_frame.pack(fill=tk.X, pady=(10, 4))
        
        content_title = tk.Label(content_title_frame, text="📋 Содержание:", 
                               font=('Arial', 14, 'bold'), bg='#34495e', fg='#e74c3c',
                               anchor='w')
        content_title.pack(side=tk.LEFT)
        
        content_text_frame = tk.Frame(content_frame, bg='#34495e')
        content_text_frame.pack(fill=tk.BOTH, expand=True)
        
        content_text = tk.Label(content_text_frame, text=regulation_data["content"], 
                              font=('Arial', 14), bg='#34495e', fg='#ecf0f1',
                              anchor='w', justify=tk.LEFT, wraplength=820)
        content_text.pack(fill=tk.BOTH, expand=True)
        
        self.add_hover_effect(card, '#34495e', '#2c3e50')
        
        return card
        
    def create_footer(self):
        """Создание футера с подсказками управления"""
        footer_frame = ttk.Frame(self.main_frame, style='Dark.TFrame')
        footer_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Основной текст футера
        footer_text = "🔒 Защита VoIP инфраструктуры • 🎯 КИИ 3-я категория • ⚡ Отказоустойчивость"
        footer_label = tk.Label(footer_frame, text=footer_text,
                               font=('Arial', 16),
                               bg='#2c3e50', fg='#bdc3c7')
        footer_label.pack(pady=10)
        
        # Подсказки управления
        controls_text = "💡 Управление: F11 - переключение полноэкранного режима • ESC - выход из полноэкранного режима • Колесо мыши - прокрутка вкладок • Shift+колесо - горизонтальная прокрутка"
        controls_label = tk.Label(footer_frame, text=controls_text,
                                font=('Arial', 12),
                                bg='#2c3e50', fg='#95a5a6')
        controls_label.pack(pady=6)

def main():
    root = tk.Tk()
    app = VoIPSecurityGuide(root)
    root.mainloop()

if __name__ == "__main__":
    main()
import tkinter as tk
import random
import math

class BallAnimation:
    def __init__(self, root):
        self.root = root
        self.root.title("Ball Animation")
        self.root.geometry("800x600")
        
        # Top boyutları (yarıçap)
        self.ball_sizes = {
            'small': 15,
            'medium': 25,
            'large': 35
        }
        
        # Renk seçenekleri
        self.colors = ['red', 'blue', 'yellow']
        
        # Seçili boyut ve renk
        self.selected_size = 'medium'
        self.selected_color = 'red'
        self.size_canvases = {}  # Boyut canvas'larını saklamak için
        
        # Toplar listesi: her top (x, y, vx, vy, radius, color, id)
        self.balls = []
        
        # Animasyon durumu
        self.is_animating = False
        self.animation_id = None
        
        # Hız çarpanı
        self.speed_multiplier = 1.0
        self.speed_label = None  # Hız göstergesi için label
        self.color_buttons = {}  # Renk butonlarını saklamak için
        
        # Canvas oluştur
        self.canvas = tk.Canvas(root, bg='lightgray', width=800, height=400)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas'ı güncelle (boyutların doğru alınması için)
        self.root.update_idletasks()
        
        # Canvas'a tıklama ile top ekleme
        self.canvas.bind('<Button-1>', self.add_ball_on_click)
        self.canvas.focus_set()  # Canvas'a odak ver
        
        # Kontrol paneli
        self.create_control_panel()
        
    def create_control_panel(self):
        """Kontrol panelini oluşturur"""
        control_frame = tk.Frame(self.root, bg='gray', height=150)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Boyut seçimi
        size_frame = tk.Frame(control_frame, bg='gray')
        size_frame.pack(side=tk.LEFT, padx=20, pady=10)
        
        tk.Label(size_frame, text="Top Boyutu:", bg='gray', fg='white', 
                font=('Arial', 10, 'bold')).pack()
        
        size_buttons_frame = tk.Frame(size_frame, bg='gray')
        size_buttons_frame.pack(pady=5)
        
        # Boyut seçim butonları (görsel daireler)
        for size_name, size_label in [('small', 'Küçük'), ('medium', 'Orta'), ('large', 'Büyük')]:
            btn_frame = tk.Frame(size_buttons_frame, bg='gray')
            btn_frame.pack(side=tk.LEFT, padx=12)
            
            # Daha büyük ve belirgin görsel daire
            circle = tk.Canvas(btn_frame, width=70, height=70, bg='white', 
                             highlightthickness=3, highlightbackground='darkgray',
                             relief=tk.RAISED, borderwidth=2, cursor='hand2')
            circle.pack()
            
            # Tıklama event'i ekle
            circle.bind('<Button-1>', lambda e, s=size_name: self.select_size(s))
            
            # Merkez noktası
            center_x, center_y = 35, 35
            radius = self.ball_sizes[size_name]
            
            # Daha belirgin renkli daire çiz (mavi tonları)
            color_map = {'small': '#4A90E2', 'medium': '#5BA3F5', 'large': '#6BB6FF'}
            circle.create_oval(center_x-radius, center_y-radius, 
                             center_x+radius, center_y+radius, 
                             fill=color_map[size_name], 
                             outline='#2C5F8D', width=3)
            
            # İç gölge efekti için ikinci daire
            circle.create_oval(center_x-radius+2, center_y-radius+2, 
                             center_x+radius-2, center_y+radius-2, 
                             fill='', outline='#7FC8FF', width=1)
            
            self.size_canvases[size_name] = circle
            
            # Daha güzel buton
            btn = tk.Button(btn_frame, text=size_label, 
                          command=lambda s=size_name: self.select_size(s),
                          width=10, height=2, font=('Arial', 9, 'bold'),
                          bg='white', fg='#2C5F8D', cursor='hand2',
                          activebackground='#E8F4FD', activeforeground='#1A4A7A',
                          relief=tk.RAISED, borderwidth=2)
            btn.pack(pady=5)
        
        # Renk ve kontrol butonları
        control_buttons_frame = tk.Frame(control_frame, bg='gray')
        control_buttons_frame.pack(side=tk.LEFT, padx=30, pady=10)
        
        # START butonu
        tk.Button(control_buttons_frame, text="BAŞLAT", command=self.start_animation, 
                 bg='lightgray', fg='black', width=10, height=2, font=('Arial', 9, 'bold'),
                 activebackground='gray', cursor='hand2', relief=tk.RAISED, 
                 borderwidth=2).pack(side=tk.LEFT, padx=10)
        
        # STOP butonu
        tk.Button(control_buttons_frame, text="DURDUR", command=self.stop_animation,
                 bg='lightgray', fg='black', width=10, height=2, font=('Arial', 9, 'bold'),
                 activebackground='gray', cursor='hand2', relief=tk.RAISED,
                 borderwidth=2).pack(side=tk.LEFT, padx=10)
        
        # RESET butonu
        tk.Button(control_buttons_frame, text="SİL", command=self.reset_animation,
                 bg='lightgray', fg='black', width=10, height=2, font=('Arial', 9, 'bold'),
                 activebackground='gray', cursor='hand2', relief=tk.RAISED,
                 borderwidth=2).pack(side=tk.LEFT, padx=10)
        
        # SPEED UP butonu
        speed_frame = tk.Frame(control_buttons_frame, bg='gray')
        speed_frame.pack(side=tk.LEFT, padx=10)
        tk.Button(speed_frame, text="Speed Up", command=self.speed_up,
                 bg='lightgreen', width=10, height=2, font=('Arial', 9, 'bold'),
                 activebackground='green', cursor='hand2').pack(pady=2)
        # Hız göstergesi
        self.speed_label = tk.Label(speed_frame, text="Hız: 1.0x", bg='gray', 
                                    fg='white', font=('Arial', 10, 'bold'),
                                    relief=tk.RAISED, borderwidth=2)
        self.speed_label.pack(pady=2)
        
        # Renk seçimi
        color_frame = tk.Frame(control_frame, bg='gray')
        color_frame.pack(side=tk.RIGHT, padx=20, pady=10)
        
        tk.Label(color_frame, text="Renk Seçimi:", bg='gray', fg='white', 
                font=('Arial', 10, 'bold')).pack()
        
        color_buttons_frame = tk.Frame(color_frame, bg='gray')
        color_buttons_frame.pack(pady=5)
        
        for color in self.colors:
            # Canvas ile renkli kare çiz (daha büyük ve belirgin)
            color_canvas = tk.Canvas(color_buttons_frame, width=60, height=60, 
                                   bg='gray', highlightthickness=2, 
                                   highlightbackground='white', cursor='hand2')
            color_canvas.pack(side=tk.LEFT, padx=10)
            
            # Renkli kare çiz (canvas'ın ortasında)
            color_canvas.create_rectangle(8, 8, 52, 52, fill=color, 
                                         outline='black', width=3)
            
            # Tıklama event'i ekle
            color_canvas.bind('<Button-1>', lambda e, c=color: self.select_color(c))
            
            self.color_buttons[color] = {'canvas': color_canvas}
        
        # İlk seçili rengi vurgula
        self.update_color_selection()
        # İlk seçili boyutu vurgula
        self.update_size_selection()
    
    def update_size_selection(self):
        """Seçili boyutu vurgular"""
        for size_name, canvas in self.size_canvases.items():
            if size_name == self.selected_size:
                # Seçili boyut için sarı vurgu
                canvas.config(highlightbackground='yellow', highlightthickness=4)
            else:
                # Seçili olmayan boyut için gri kenarlık
                canvas.config(highlightbackground='darkgray', highlightthickness=3)
    
    def select_size(self, size):
        """Top boyutu seçilir"""
        self.selected_size = size
        self.update_size_selection()
        print(f"Seçilen boyut: {size}")
    
    def update_color_selection(self):
        """Seçili rengi vurgular"""
        for color, color_widgets in self.color_buttons.items():
            canvas = color_widgets['canvas']
            if color == self.selected_color:
                # Seçili renk için sarı vurgu
                canvas.config(highlightbackground='yellow', highlightthickness=4)
            else:
                # Seçili olmayan renk için beyaz kenarlık
                canvas.config(highlightbackground='white', highlightthickness=2)
    
    def select_color(self, color):
        """Renk seçilir"""
        self.selected_color = color
        self.update_color_selection()
        print(f"Seçilen renk: {color}")
    
    def add_ball_on_click(self, event):
        """Canvas'a tıklandığında top ekler"""
        x = event.x
        y = event.y
        print(f"Canvas'a tıklandı: x={x}, y={y}")
        self.add_ball(x, y)
    
    def add_ball(self, x=None, y=None):
        """Yeni top ekler"""
        radius = self.ball_sizes[self.selected_size]
        color = self.selected_color
        
        if x is None or y is None:
            # Random konum
            self.root.update_idletasks()
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            if canvas_width <= 1 or canvas_height <= 1:
                canvas_width = 800
                canvas_height = 400
            
            x = random.randint(radius + 5, max(radius + 5, canvas_width - radius - 5))
            y = random.randint(radius + 5, max(radius + 5, canvas_height - radius - 5))
        
        # Random hız (başlangıçta duruyor, Start ile hareket başlayacak)
        vx = 0
        vy = 0
        
        # Top çiz
        ball_id = self.canvas.create_oval(
            x - radius, y - radius,
            x + radius, y + radius,
            fill=color, outline='black', width=2
        )
        
        # Top bilgilerini kaydet
        self.balls.append({
            'id': ball_id,
            'x': float(x),
            'y': float(y),
            'vx': vx,
            'vy': vy,
            'radius': radius,
            'color': color
        })
        
        print(f"Top eklendi: x={x}, y={y}, boyut={self.selected_size}, renk={color}")
    
    def start_animation(self):
        """Animasyonu başlatır"""
        if not self.is_animating:
            if len(self.balls) == 0:
                print("Uyarı: Ekranda top yok! Önce canvas'a tıklayarak top ekleyin.")
                return
            
            # Duran toplara random hız ver
            for ball in self.balls:
                if ball['vx'] == 0 and ball['vy'] == 0:
                    # Random yön ve hız
                    angle = random.uniform(0, 2 * math.pi)
                    speed = random.uniform(2, 5) * self.speed_multiplier
                    ball['vx'] = speed * math.cos(angle)
                    ball['vy'] = speed * math.sin(angle)
            
            self.is_animating = True
            print(f"Animasyon başlatıldı. {len(self.balls)} top hareket ediyor.")
            self.animate()
    
    def stop_animation(self):
        """Animasyonu durdurur"""
        self.is_animating = False
        if self.animation_id:
            self.root.after_cancel(self.animation_id)
            self.animation_id = None
    
    def reset_animation(self):
        """Tüm topları siler ve ekranı temizler"""
        self.stop_animation()
        for ball in self.balls:
            self.canvas.delete(ball['id'])
        self.balls = []
        self.speed_multiplier = 1.0
        if self.speed_label:
            self.speed_label.config(text="Hız: 1.0x")
    
    def speed_up(self):
        """Hızı artırır"""
        self.speed_multiplier += 0.5
        # Hız göstergesini güncelle
        if self.speed_label:
            self.speed_label.config(text=f"Hız: {self.speed_multiplier:.1f}x")
        
        # Mevcut topların hızını artır
        for ball in self.balls:
            if ball['vx'] != 0 or ball['vy'] != 0:
                current_speed = math.sqrt(ball['vx']**2 + ball['vy']**2)
                if current_speed > 0:
                    angle = math.atan2(ball['vy'], ball['vx'])
                    new_speed = current_speed * (self.speed_multiplier / (self.speed_multiplier - 0.5))
                    ball['vx'] = new_speed * math.cos(angle)
                    ball['vy'] = new_speed * math.sin(angle)
        
        print(f"Hız artırıldı: {self.speed_multiplier:.1f}x")
    
    def animate(self):
        """Animasyon döngüsü"""
        if not self.is_animating:
            return
        
        # Canvas boyutunu al
        self.root.update_idletasks()
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Canvas boyutu kontrolü
        if canvas_width <= 1 or canvas_height <= 1:
            canvas_width = 800
            canvas_height = 400
        
        for ball in self.balls:
            # Yeni pozisyon
            new_x = ball['x'] + ball['vx']
            new_y = ball['y'] + ball['vy']
            
            # Kenar çarpışma kontrolü
            if new_x - ball['radius'] <= 0:
                ball['vx'] = abs(ball['vx'])  # Sağa git
                new_x = ball['radius']
            elif new_x + ball['radius'] >= canvas_width:
                ball['vx'] = -abs(ball['vx'])  # Sola git
                new_x = canvas_width - ball['radius']
            
            if new_y - ball['radius'] <= 0:
                ball['vy'] = abs(ball['vy'])  # Aşağı git
                new_y = ball['radius']
            elif new_y + ball['radius'] >= canvas_height:
                ball['vy'] = -abs(ball['vy'])  # Yukarı git
                new_y = canvas_height - ball['radius']
            
            # Pozisyonu güncelle
            ball['x'] = new_x
            ball['y'] = new_y
            
            # Canvas'ta topu hareket ettir
            self.canvas.coords(
                ball['id'],
                ball['x'] - ball['radius'],
                ball['y'] - ball['radius'],
                ball['x'] + ball['radius'],
                ball['y'] + ball['radius']
            )
        
        # Bir sonraki frame için zamanlayıcı
        self.animation_id = self.root.after(16, self.animate)  # ~60 FPS

def main():
    root = tk.Tk()
    app = BallAnimation(root)
    root.mainloop()

if __name__ == "__main__":
    main()


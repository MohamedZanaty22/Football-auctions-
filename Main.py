import sqlite3
import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

# Set background color to dark theme
Window.clearcolor = (0.07, 0.07, 0.09, 1)

# ==========================================
# 1. DATABASE SETUP
# ==========================================
def init_db():
    conn = sqlite3.connect('football_auction.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            position TEXT NOT NULL,
            rating INTEGER NOT NULL,
            status TEXT NOT NULL,
            base_price INTEGER NOT NULL
        )
    ''')
    
    cursor.execute("SELECT COUNT(*) FROM players")
    if cursor.fetchone()[0] == 0:
        players_data = [
            # Strikers (ST / FW)
            ("Pele", "ST", 98, "Retired", 40),
            ("C. Ronaldo", "ST", 92, "Current", 30),
            ("E. Haaland", "ST", 91, "Current", 28),
            ("K. Mbappe", "ST", 92, "Current", 30),
            ("Ronaldo Nazario", "ST", 96, "Retired", 35),
            ("M. Salah", "ST", 90, "Current", 25),
            ("L. Messi", "ST", 93, "Current", 32),
            ("H. Kane", "ST", 89, "Current", 20),
            ("R. Lewandowski", "ST", 88, "Current", 18),
            ("W. Weghorst", "ST", 77, "Current", 5),
            ("G. Agbonlahor", "ST", 74, "Retired", 3),

            # Midfielders (MID)
            ("Z. Zidane", "MID", 96, "Retired", 35),
            ("K. De Bruyne", "MID", 91, "Current", 25),
            ("J. Bellingham", "MID", 90, "Current", 25),
            ("L. Modric", "MID", 88, "Current", 15),
            ("D. Maradona", "MID", 97, "Retired", 38),
            ("Ronaldinho", "MID", 94, "Retired", 32),
            ("Xavi", "MID", 93, "Retired", 28),
            ("Iniesta", "MID", 93, "Retired", 28),
            ("Pedri", "MID", 86, "Current", 12),
            ("Fred", "MID", 78, "Current", 5),
            ("Bakayoko", "MID", 75, "Current", 4),

            # Defenders (DEF)
            ("P. Maldini", "DEF", 96, "Retired", 32),
            ("V. van Dijk", "DEF", 89, "Current", 20),
            ("S. Ramos", "DEF", 87, "Current", 15),
            ("Cafu", "DEF", 92, "Retired", 25),
            ("R. Carlos", "DEF", 91, "Retired", 24),
            ("F. Cannavaro", "DEF", 93, "Retired", 26),
            ("A. Hakimi", "DEF", 85, "Current", 12),
            ("T. Hernandez", "DEF", 86, "Current", 14),
            ("H. Maguire", "DEF", 79, "Current", 6),
            ("Mustafi", "DEF", 75, "Retired", 3),

            # Goalkeepers (GK)
            ("L. Yashin", "GK", 95, "Retired", 28),
            ("M. Neuer", "GK", 89, "Current", 18),
            ("G. Buffon", "GK", 91, "Retired", 22),
            ("T. Courtois", "GK", 90, "Current", 20),
            ("Alisson", "GK", 89, "Current", 18),
            ("L. Karius", "GK", 72, "Current", 2),
            ("R. Jimenez", "GK", 70, "Retired", 1)
        ]
        cursor.executemany('''
            INSERT INTO players (name, position, rating, status, base_price) 
            VALUES (?, ?, ?, ?, ?)
        ''', players_data)
        conn.commit()
    conn.close()


# ==========================================
# 2. MAIN APPLICATION
# ==========================================
class FootballAuctionLeagueApp(App):
    def build(self):
        init_db()
        self.root = BoxLayout(orientation='vertical', padding=15, spacing=10)
        self.show_name_setup_screen()
        return self.root

    # ------------------------------------------
    # SCREEN 1: Setup Player Names (Modern UI)
    # ------------------------------------------
    def show_name_setup_screen(self):
        self.root.clear_widgets()
        
        title = Label(
            text="⚽ FOOTBALL DRAFT MANAGER ⚽", 
            font_size='22sp', 
            bold=True, 
            color=(0.2, 0.8, 1, 1),
            size_hint=(1, 0.15)
        )
        self.root.add_widget(title)
        
        self.name_inputs = []
        inputs_box = BoxLayout(orientation='vertical', spacing=10, size_hint=(1, 0.65))
        
        for i in range(4):
            inp = TextInput(
                text=f"Manager {i+1}", 
                multiline=False, 
                font_size='16sp',
                background_color=(0.15, 0.15, 0.2, 1),
                foreground_color=(1, 1, 1, 1),
                padding_y=[12, 12],
                cursor_color=(0.2, 0.8, 1, 1)
            )
            self.name_inputs.append(inp)
            inputs_box.add_widget(inp)
            
        self.root.add_widget(inputs_box)
        
        start_game_btn = Button(
            text="START DRAFT AUCTION ($400M)", 
            font_size='16sp', 
            bold=True,
            background_color=(0.1, 0.7, 0.3, 1),
            size_hint=(1, 0.15), 
            on_press=self.start_auction_game
        )
        self.root.add_widget(start_game_btn)

    # ------------------------------------------
    # SCREEN 2: Auction Phase ($400M Budget & Multiple Bids)
    # ------------------------------------------
    def start_auction_game(self, instance):
        self.players = {
            i: {
                "name": self.name_inputs[i].text.strip() or f"Manager {i+1}", 
                "budget": 400,  # 💰 Updated Budget to $400M
                "squad": [], 
                "pts": 0, "w": 0, "d": 0, "l": 0, "gf": 0, "ga": 0
            } for i in range(4)
        }
        
        self.active_bidders = [0, 1, 2, 3]
        self.current_turn_idx = 0
        self.used_player_ids = set()
        self.current_player = None
        self.hidden_player = None
        self.current_bid = 0
        self.highest_bidder = None

        self.root.clear_widgets()
        
        # Info bar
        self.info_label = Label(
            text="Press 'Start Round' to begin!", 
            font_size='15sp', 
            bold=True, 
            color=(0.2, 0.8, 1, 1),
            size_hint=(1, 0.1)
        )
        self.root.add_widget(self.info_label)
        
        # Card display panel
        self.card_label = Label(
            text="Build your 11-Player Squad!\nStarting Budget: $400M", 
            font_size='15sp', 
            halign='center', 
            valign='middle',
            color=(1, 1, 1, 1),
            size_hint=(1, 0.25)
        )
        self.card_label.bind(size=self._update_text_size)
        self.root.add_widget(self.card_label)
        
        # Logs
        self.log_label = Label(
            text="", 
            font_size='13sp', 
            halign='left', 
            valign='top', 
            color=(0.8, 0.8, 0.8, 1),
            size_hint_y=None
        )
        self.log_label.bind(texture_size=self.log_label.setter('size'))
        
        scroll = ScrollView(size_hint=(1, 0.35))
        scroll.add_widget(self.log_label)
        self.root.add_widget(scroll)
        
        # Action Buttons Layout
        actions_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.3), spacing=6)
        
        # Grid of bidding buttons (+1M, +5M, +10M, +15M)
        bid_grid = GridLayout(cols=4, spacing=5, size_hint=(1, 0.5))
        
        self.bid_btns = []
        bid_amounts = [1, 5, 10, 15]
        for amt in bid_amounts:
            btn = Button(
                text=f"+${amt}M", 
                font_size='13sp', 
                bold=True,
                background_color=(0.1, 0.6, 0.8, 1),
                disabled=True,
                on_press=lambda inst, a=amt: self.place_bid(a)
            )
            self.bid_btns.append(btn)
            bid_grid.add_widget(btn)
            
        actions_layout.add_widget(bid_grid)
        
        # Pass and Start Buttons
        sub_layout = BoxLayout(orientation='horizontal', spacing=8, size_hint=(1, 0.5))
        self.pass_btn = Button(
            text="Pass / Fold", 
            font_size='13sp', 
            bold=True,
            background_color=(0.8, 0.2, 0.2, 1),
            disabled=True, 
            on_press=self.pass_auction
        )
        self.start_btn = Button(
            text="Start Round", 
            font_size='13sp', 
            bold=True,
            background_color=(0.2, 0.7, 0.3, 1),
            on_press=self.next_round
        )
        
        sub_layout.add_widget(self.pass_btn)
        sub_layout.add_widget(self.start_btn)
        actions_layout.add_widget(sub_layout)
        
        self.root.add_widget(actions_layout)

    def _update_text_size(self, instance, value):
        instance.text_size = value

    def get_random_player(self, position=None):
        conn = sqlite3.connect('football_auction.db')
        cursor = conn.cursor()
        query = "SELECT * FROM players WHERE id NOT IN ({})".format(
            ','.join('?' for _ in self.used_player_ids)
        ) if self.used_player_ids else "SELECT * FROM players WHERE 1=1"
        
        params = list(self.used_player_ids)
        if position:
            query += " AND position = ?"
            params.append(position)
            
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        if not rows: return None
        selected = random.choice(rows)
        self.used_player_ids.add(selected[0])
        return {"id": selected[0], "name": selected[1], "pos": selected[2], "rating": selected[3], "status": selected[4], "base": selected[5]}

    def set_bid_buttons_state(self, disabled):
        for btn in self.bid_btns:
            btn.disabled = disabled

    def next_round(self, instance):
        if all(len(p["squad"]) >= 11 for p in self.players.values()):
            self.start_league_matches()
            return

        self.current_player = self.get_random_player()
        if not self.current_player:
            self.card_label.text = "Database Empty! Moving to League..."
            self.start_league_matches()
            return

        self.hidden_player = self.get_random_player(position=self.current_player['pos'])
        self.current_bid = self.current_player['base']
        self.highest_bidder = None
        
        self.active_bidders = [i for i, p in self.players.items() if len(p["squad"]) < 11]
        self.current_turn_idx = 0
        
        self.card_label.text = (
            f"🔥 OPEN PLAYER: {self.current_player['name']}\n"
            f"Pos: {self.current_player['pos']}  |  OVR: {self.current_player['rating']}\n"
            f"Status: {self.current_player['status']}\n"
            f"Base Price: ${self.current_bid}M"
        )
        self.log_label.text = "--- Round Started! ---\n"
        self.update_turn_ui()
        
        self.set_bid_buttons_state(False)
        self.pass_btn.disabled = False
        self.start_btn.disabled = True

    def current_player_id(self):
        return self.active_bidders[self.current_turn_idx]

    def update_turn_ui(self):
        pid = self.current_player_id()
        p = self.players[pid]
        self.info_label.text = f"TURN: {p['name']}  |  Budget: ${p['budget']}M  |  Squad: {len(p['squad'])}/11"

    def advance_turn(self):
        if len(self.active_bidders) <= 1 and self.highest_bidder is not None:
            self.end_round()
            return
        elif len(self.active_bidders) == 0:
            self.end_round()
            return

        self.current_turn_idx = (self.current_turn_idx + 1) % len(self.active_bidders)
        self.update_turn_ui()

    def place_bid(self, amount):
        pid = self.current_player_id()
        p = self.players[pid]
        
        new_bid = self.current_bid + amount
        if p['budget'] < new_bid:
            self.log_label.text += f"⚠️ {p['name']}: Not enough budget for +${amount}M!\n"
            return
            
        self.current_bid = new_bid
        self.highest_bidder = pid
        self.log_label.text += f"⚡ {p['name']} raised bid by +${amount}M (Total: ${self.current_bid}M)\n"
        self.advance_turn()

    def pass_auction(self, instance):
        pid = self.current_player_id()
        p_name = self.players[pid]['name']
        self.log_label.text += f"❌ {p_name} folded.\n"
        self.active_bidders.remove(pid)
        if self.current_turn_idx >= len(self.active_bidders):
            self.current_turn_idx = 0
        self.advance_turn()

    def end_round(self):
        self.set_bid_buttons_state(True)
        self.pass_btn.disabled = True
        
        hidden_text = f"\n\n❓ Hidden Player: {self.hidden_player['name']} (OVR {self.hidden_player['rating']})" if self.hidden_player else ""

        if self.highest_bidder is not None:
            winner = self.players[self.highest_bidder]
            winner['budget'] -= self.current_bid
            winner['squad'].append(self.current_player)
            self.card_label.text = f"🎉 WON! {winner['name']} bought {self.current_player['name']} for ${self.current_bid}M!" + hidden_text
        else:
            self.card_label.text = "🚫 No Bids! Player unsigned." + hidden_text

        if all(len(p["squad"]) >= 11 for p in self.players.values()):
            self.start_btn.text = "START LEAGUE MATCHES!"
        else:
            self.start_btn.text = "Next Round"
        self.start_btn.disabled = False

    # ------------------------------------------
    # SCREEN 3: League Simulation & Matches
    # ------------------------------------------
    def start_league_matches(self):
        self.root.clear_widgets()
        
        self.info_label = Label(
            text="🏆 FOOTBALL LEAGUE MATCHES 🏆", 
            font_size='18sp', 
            bold=True, 
            color=(1, 0.8, 0.2, 1),
            size_hint=(1, 0.12)
        )
        self.root.add_widget(self.info_label)
        
        self.card_label = Label(
            text="Simulating League Season...", 
            font_size='15sp', 
            halign='center', 
            valign='middle', 
            color=(1, 1, 1, 1),
            size_hint=(1, 0.18)
        )
        self.card_label.bind(size=self._update_text_size)
        self.root.add_widget(self.card_label)
        
        self.log_label = Label(
            text="", 
            font_size='13sp', 
            halign='left', 
            valign='top', 
            color=(0.9, 0.9, 0.9, 1),
            size_hint_y=None
        )
        self.log_label.bind(texture_size=self.log_label.setter('size'))
        
        scroll = ScrollView(size_hint=(1, 0.7))
        scroll.add_widget(self.log_label)
        self.root.add_widget(scroll)
        
        self.simulate_league()

    def simulate_league(self):
        match_logs = "=== MATCH RESULTS ===\n\n"
        
        team_ratings = {}
        for pid, p in self.players.items():
            avg_ovr = sum(pl['rating'] for pl in p['squad']) / max(len(p['squad']), 1)
            team_ratings[pid] = avg_ovr

        for i in range(4):
            for j in range(i + 1, 4):
                p1, p2 = self.players[i], self.players[j]
                
                score1 = max(0, int((team_ratings[i] - 70) / 5 + random.randint(-1, 3)))
                score2 = max(0, int((team_ratings[j] - 70) / 5 + random.randint(-1, 3)))
                
                p1['gf'] += score1; p1['ga'] += score2
                p2['gf'] += score2; p2['ga'] += score1
                
                if score1 > score2:
                    p1['pts'] += 3; p1['w'] += 1; p2['l'] += 1
                elif score2 > score1:
                    p2['pts'] += 3; p2['w'] += 1; p1['l'] += 1
                else:
                    p1['pts'] += 1; p2['pts'] += 1
                    p1['d'] += 1; p2['d'] += 1
                    
                match_logs += f"⚽ {p1['name']}  {score1} - {score2}  {p2['name']}\n"

        match_logs += "\n=========================\n"
        match_logs += "🏆 FINAL LEAGUE TABLE 🏆\n"
        match_logs += "=========================\n"
        match_logs += "Pos | Team | Pts | W-D-L | GD\n"
        match_logs += "---------------------------------\n"
        
        sorted_league = sorted(
            self.players.values(), 
            key=lambda x: (x['pts'], x['gf'] - x['ga'], x['gf']), 
            reverse=True
        )
        
        for rank, p in enumerate(sorted_league, 1):
            gd = p['gf'] - p['ga']
            match_logs += f"#{rank} | {p['name']} | {p['pts']}pts | {p['w']}-{p['d']}-{p['l']} | GD: {gd:+d}\n"

        winner = sorted_league[0]
        self.info_label.text = f"LEAGUE CHAMPION: {winner['name']} 🏆"
        self.card_label.text = f"Congratulations {winner['name']}!\nWon the League with {winner['pts']} Points!"
        self.log_label.text = match_logs


if __name__ == '__main__':
    FootballAuctionLeagueApp().run()

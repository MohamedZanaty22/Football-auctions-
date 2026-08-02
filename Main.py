import sqlite3
import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

Window.clearcolor = (0.07, 0.07, 0.09, 1)

POSITIONS = ["GK", "DEF", "MID", "ST"]

POS_REQUIREMENTS = {
    "GK": 1,   # 1 حارس
    "DEF": 4,  # 4 مدافعين
    "MID": 3,  # 3 وسط
    "ST": 3    # 3 مهاجمين
}

def init_db():
    conn = sqlite3.connect('football_auction.db')
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS players')
    cursor.execute('''
        CREATE TABLE players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            position TEXT NOT NULL,
            rating INTEGER NOT NULL,
            status TEXT NOT NULL,
            base_price INTEGER NOT NULL
        )
    ''')
    
    players_data = []

    # 1. GOALKEEPERS (GK)
    gks = [
        ("L. Yashin", 95, "Retired", 28), ("I. Casillas", 92, "Retired", 24), ("G. Buffon", 91, "Retired", 22),
        ("O. Kahn", 91, "Retired", 22), ("P. Schmeichel", 90, "Retired", 20), ("E. van der Sar", 89, "Retired", 18),
        ("T. Courtois", 90, "Current", 20), ("M. Neuer", 89, "Current", 18), ("Alisson", 89, "Current", 18),
        ("E. Martinez", 87, "Current", 14), ("J. Oblak", 88, "Current", 16), ("M. El-Shenawy", 82, "Current", 8),
        ("D. de Gea", 84, "Current", 10), ("Y. Bounou", 85, "Current", 12), ("E. Mendy", 81, "Current", 7),
        ("G. Donnarumma", 87, "Current", 15), ("M. Maignan", 86, "Current", 14), ("D. Raya", 84, "Current", 10),
        ("Unai Simón", 83, "Current", 9), ("A. Ramsdale", 80, "Current", 6), ("W. Szczęsny", 84, "Current", 9),
        ("K. Navas", 83, "Retired", 8), ("J. Dudek", 80, "Retired", 5), ("V. Valdés", 84, "Retired", 9)
    ]
    for item in gks: players_data.append((item[0], "GK", item[1], item[2], item[3]))

    # 2. DEFENDERS (DEF)
    defs = [
        ("P. Maldini", 96, "Retired", 32), ("F. Beckenbauer", 95, "Retired", 30), ("F. Cannavaro", 93, "Retired", 26),
        ("Cafu", 92, "Retired", 25), ("R. Carlos", 91, "Retired", 24), ("C. Puyol", 91, "Retired", 22),
        ("V. van Dijk", 89, "Current", 20), ("S. Ramos", 88, "Current", 16), ("A. Hakimi", 85, "Current", 12),
        ("T. Hernandez", 86, "Current", 14), ("R. Dias", 88, "Current", 18), ("A. Rüdiger", 86, "Current", 13),
        ("Wael Gomaa", 85, "Retired", 12), ("Ahmed Hegazi", 80, "Current", 6), ("Mohamed Abdelmonem", 82, "Current", 8),
        ("Ali Maaloul", 81, "Current", 7), ("Shkodran Mustafi", 75, "Current", 3), ("Harry Maguire", 79, "Current", 5),
        ("J. Stones", 85, "Current", 12), ("K. Walker", 84, "Current", 10), ("D. Alaba", 85, "Current", 11),
        ("M. de Ligt", 84, "Current", 10), ("J. Koundé", 85, "Current", 11), ("W. Saliba", 87, "Current", 15),
        ("G. Chiellini", 87, "Retired", 14), ("L. Bonucci", 86, "Retired", 13), ("J. Zanetti", 90, "Retired", 20),
        ("L. Thuram", 89, "Retired", 18), ("N. Vidic", 88, "Retired", 16), ("R. Ferdinand", 88, "Retired", 16),
        ("J. Terry", 87, "Retired", 15), ("A. Nesta", 91, "Retired", 22), ("D. Godín", 84, "Retired", 9),
        ("Gabriel Magalhães", 85, "Current", 12), ("E. Militao", 85, "Current", 12), ("C. Romero", 84, "Current", 10),
        ("S. Botman", 82, "Current", 8), ("A. Robertson", 85, "Current", 11), ("D. Carvajal", 86, "Current", 13),
        ("J. Frimpong", 84, "Current", 11), ("M. Akanji", 83, "Current", 9), ("Lisandro Martínez", 83, "Current", 9)
    ]
    for item in defs: players_data.append((item[0], "DEF", item[1], item[2], item[3]))

    # 3. MIDFIELDERS (MID)
    mids = [
        ("D. Maradona", 97, "Retired", 38), ("Z. Zidane", 96, "Retired", 35), ("Ronaldinho", 94, "Retired", 32),
        ("Xavi", 93, "Retired", 28), ("A. Iniesta", 93, "Retired", 28), ("A. Pirlo", 91, "Retired", 24),
        ("K. De Bruyne", 91, "Current", 25), ("J. Bellingham", 90, "Current", 25), ("L. Modric", 88, "Current", 15),
        ("Rodri", 91, "Current", 26), ("M. Aboutrika", 88, "Retired", 18), ("Emam Ashour", 82, "Current", 8),
        ("Fred", 78, "Current", 4), ("Bakayoko", 75, "Current", 3), ("Charlie Adam", 73, "Retired", 2),
        ("B. Fernandes", 88, "Current", 18), ("F. Valverde", 88, "Current", 19), ("N. Kanté", 86, "Current", 12),
        ("P. Pogba", 82, "Current", 8), ("T. Kroos", 88, "Retired", 16), ("S. Busquets", 85, "Current", 10),
        ("P. Vieira", 90, "Retired", 22), ("R. Gullit", 92, "Retired", 26), ("L. Matthäus", 91, "Retired", 24),
        ("C. Seedorf", 88, "Retired", 16), ("M. Ballack", 87, "Retired", 14), ("Kaka", 90, "Retired", 22),
        ("Pedri", 86, "Current", 14), ("Gavi", 83, "Current", 9), ("M. Ødegaard", 88, "Current", 18),
        ("A. Tchouaméni", 85, "Current", 12), ("E. Camavinga", 84, "Current", 11), ("J. Musiala", 87, "Current", 16),
        ("Alexis Mac Allister", 84, "Current", 10), ("Dominik Szoboszlai", 83, "Current", 9)
    ]
    for item in mids: players_data.append((item[0], "MID", item[1], item[2], item[3]))

    # 4. STRIKERS (ST)
    sts = [
        ("L. Messi", 93, "Current", 32), ("Pele", 98, "Retired", 40), ("Ronaldo Nazario", 96, "Retired", 35),
        ("C. Ronaldo", 92, "Current", 30), ("K. Mbappe", 92, "Current", 30), ("E. Haaland", 91, "Current", 28),
        ("Thierry Henry", 93, "Retired", 30), ("M. Salah", 91, "Current", 28), ("Mahmoud El-Khatib", 89, "Retired", 20),
        ("Wout Weghorst", 77, "Current", 3), ("Gabriel Agbonlahor", 74, "Retired", 2), ("Jackson Martínez", 76, "Retired", 3),
        ("R. Lewandowski", 90, "Current", 22), ("H. Kane", 90, "Current", 24), ("V. Osimhen", 87, "Current", 16),
        ("L. Martínez", 88, "Current", 18), ("Z. Ibrahimovic", 88, "Retired", 18), ("G. Batistuta", 89, "Retired", 20),
        ("M. van Basten", 92, "Retired", 25), ("R. van Nistelrooy", 88, "Retired", 16), ("D. Drogba", 89, "Retired", 19),
        ("S. Eto'o", 89, "Retired", 19), ("Wayne Rooney", 88, "Retired", 17), ("Sergio Agüero", 88, "Retired", 17),
        ("L. Suárez", 87, "Current", 15), ("Vinicius Jr.", 90, "Current", 25), ("Rodrygo", 85, "Current", 12),
        ("Bukayo Saka", 87, "Current", 16), ("K. Benzema", 89, "Current", 20), ("A. Griezmann", 87, "Current", 15),
        ("Julian Alvarez", 85, "Current", 13), ("Son Heung-min", 87, "Current", 16), ("Rafael Leão", 85, "Current", 12)
    ]
    for item in sts: players_data.append((item[0], "ST", item[1], item[2], item[3]))

    cursor.executemany('''
        INSERT INTO players (name, position, rating, status, base_price) 
        VALUES (?, ?, ?, ?, ?)
    ''', players_data)
    conn.commit()
    conn.close()


class FootballAuctionLeagueApp(App):
    def build(self):
        init_db()
        self.num_players = 3
        self.root = BoxLayout(orientation='vertical', padding=15, spacing=10)
        self.show_name_setup_screen()
        return self.root

    def show_name_setup_screen(self):
        self.root.clear_widgets()
        
        title = Label(
            text="⚽ 4-3-3 MULTI-MANAGER DRAFT ⚽", 
            font_size='20sp', bold=True, color=(0.2, 0.8, 1, 1), size_hint=(1, 0.1)
        )
        self.root.add_widget(title)
        
        select_box = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=10)
        select_label = Label(text="Select Number of Managers:", font_size='14sp', color=(1, 1, 1, 1))
        
        self.spinner = Spinner(
            text=str(self.num_players), values=('2', '3', '4', '5'),
            size_hint=(0.4, 1), background_color=(0.2, 0.6, 0.9, 1)
        )
        self.spinner.bind(text=self.on_player_count_change)
        select_box.add_widget(select_label)
        select_box.add_widget(self.spinner)
        self.root.add_widget(select_box)

        self.inputs_box = BoxLayout(orientation='vertical', spacing=8, size_hint=(1, 0.65))
        self.render_name_inputs()
        self.root.add_widget(self.inputs_box)
        
        start_game_btn = Button(
            text="START DRAFT FOR ALL MANAGERS", 
            font_size='15sp', bold=True, background_color=(0.1, 0.7, 0.3, 1),
            size_hint=(1, 0.15), on_press=self.start_auction_game
        )
        self.root.add_widget(start_game_btn)

    def on_player_count_change(self, spinner, text):
        self.num_players = int(text)
        self.render_name_inputs()

    def render_name_inputs(self):
        self.inputs_box.clear_widgets()
        self.name_inputs = []
        for i in range(self.num_players):
            inp = TextInput(
                text=f"Manager {i+1}", multiline=False, font_size='15sp',
                background_color=(0.15, 0.15, 0.2, 1), foreground_color=(1, 1, 1, 1)
            )
            self.name_inputs.append(inp)
            self.inputs_box.add_widget(inp)

    def start_auction_game(self, instance):
        self.players = {
            i: {
                "name": self.name_inputs[i].text.strip() or f"Manager {i+1}", 
                "budget": 400, "squad": [], 
                "pts": 0, "w": 0, "d": 0, "l": 0, "gf": 0, "ga": 0,
                "yellow_cards": 0, "red_cards": 0
            } for i in range(self.num_players)
        }
        self.used_player_ids = set()
        self.current_stage_idx = 0
        self.setup_auction_ui()

    def setup_auction_ui(self):
        self.root.clear_widgets()
        curr_pos = POSITIONS[self.current_stage_idx]
        needed_count = POS_REQUIREMENTS[curr_pos]
        
        self.info_label = Label(
            text=f"🔥 PHASE: {curr_pos} (Each Manager needs {needed_count} player(s))", 
            font_size='14sp', bold=True, color=(0.2, 0.8, 1, 1), size_hint=(1, 0.1)
        )
        self.root.add_widget(self.info_label)
        
        self.card_label = Label(
            text=f"Current Stage: {curr_pos}\nPress 'Start Round' to begin bidding.", 
            font_size='14sp', halign='center', valign='middle', color=(1, 1, 1, 1), size_hint=(1, 0.25)
        )
        self.card_label.bind(size=self._update_text_size)
        self.root.add_widget(self.card_label)
        
        self.log_label = Label(text="", font_size='13sp', halign='left', valign='top', color=(0.8, 0.8, 0.8, 1), size_hint_y=None)
        self.log_label.bind(texture_size=self.log_label.setter('size'))
        
        scroll = ScrollView(size_hint=(1, 0.35))
        scroll.add_widget(self.log_label)
        self.root.add_widget(scroll)
        
        actions_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.3), spacing=6)
        bid_grid = GridLayout(cols=4, spacing=5, size_hint=(1, 0.5))
        self.bid_btns = []
        for amt in [1, 5, 10, 15]:
            btn = Button(
                text=f"+${amt}M", font_size='13sp', bold=True, background_color=(0.1, 0.6, 0.8, 1),
                disabled=True, on_press=lambda inst, a=amt: self.place_bid(a)
            )
            self.bid_btns.append(btn)
            bid_grid.add_widget(btn)
            
        actions_layout.add_widget(bid_grid)
        
        sub_layout = BoxLayout(orientation='horizontal', spacing=8, size_hint=(1, 0.5))
        self.pass_btn = Button(text="Pass / Fold", font_size='13sp', bold=True, background_color=(0.8, 0.2, 0.2, 1), disabled=True, on_press=self.pass_auction)
        self.start_btn = Button(text="Start Round", font_size='13sp', bold=True, background_color=(0.2, 0.7, 0.3, 1), on_press=self.next_round)
        
        sub_layout.add_widget(self.pass_btn)
        sub_layout.add_widget(self.start_btn)
        actions_layout.add_widget(sub_layout)
        
        self.root.add_widget(actions_layout)

    def _update_text_size(self, instance, value):
        instance.text_size = value

    def get_random_player_by_pos(self, pos):
        conn = sqlite3.connect('football_auction.db')
        cursor = conn.cursor()
        query = f"SELECT * FROM players WHERE position = '{pos}'"
        if self.used_player_ids:
            query += " AND id NOT IN ({})".format(','.join('?' for _ in self.used_player_ids))
            cursor.execute(query, list(self.used_player_ids))
        else:
            cursor.execute(query)
            
        rows = cursor.fetchall()
        conn.close()
        
        if rows:
            selected = random.choice(rows)
            self.used_player_ids.add(selected[0])
            return {"id": selected[0], "name": selected[1], "pos": selected[2], "rating": selected[3], "status": selected[4], "base": selected[5]}
        return None

    def set_bid_buttons_state(self, disabled):
        for btn in self.bid_btns:
            btn.disabled = disabled

    def count_players_in_pos(self, squad, pos):
        return sum(1 for p in squad if p['pos'] == pos)

    def is_stage_complete(self):
        curr_pos = POSITIONS[self.current_stage_idx]
        needed = POS_REQUIREMENTS[curr_pos]
        return all(self.count_players_in_pos(p["squad"], curr_pos) >= needed for p in self.players.values())

    def auto_fill_stage_if_needed(self, pos=None):
        target_pos = pos if pos else POSITIONS[self.current_stage_idx]
        needed = POS_REQUIREMENTS[target_pos]
        
        for pid, p in self.players.items():
            current_count = self.count_players_in_pos(p['squad'], target_pos)
            missing = needed - current_count
            for _ in range(missing):
                filler_player = self.get_random_player_by_pos(target_pos)
                if filler_player:
                    p['budget'] -= filler_player['base']
                    p['squad'].append(filler_player)

    def next_round(self, instance):
        curr_pos = POSITIONS[self.current_stage_idx]
        needed = POS_REQUIREMENTS[curr_pos]
        
        if self.is_stage_complete():
            self.show_stage_summary_screen()
            return

        self.active_bidders = [i for i, p in self.players.items() if self.count_players_in_pos(p['squad'], curr_pos) < needed]
        
        self.current_player = self.get_random_player_by_pos(curr_pos)
        if not self.current_player:
            self.show_stage_summary_screen()
            return

        self.current_bid = self.current_player['base']
        self.highest_bidder = None
        self.current_turn_idx = 0
        
        self.card_label.text = (
            f"🔥 OPEN PLAYER ({curr_pos}): {self.current_player['name']}\n"
            f"OVR: {self.current_player['rating']}  |  Status: {self.current_player['status']}\n"
            f"Base Price: ${self.current_bid}M"
        )
        self.log_label.text = f"--- New Auction Round for {curr_pos} Started! ---\n"
        self.update_turn_ui()
        
        self.set_bid_buttons_state(False)
        self.pass_btn.disabled = False
        self.start_btn.disabled = True

    def current_player_id(self):
        return self.active_bidders[self.current_turn_idx]

    def update_turn_ui(self):
        pid = self.current_player_id()
        p = self.players[pid]
        curr_pos = POSITIONS[self.current_stage_idx]
        needed = POS_REQUIREMENTS[curr_pos]
        
        # فحص ما إذا كان المدير الفني لا يملك رصيداً كافياً للحد الأدنى للمزايدة (+1M على الأقل)
        min_required_bid = self.current_bid + 1
        if p['budget'] < min_required_bid:
            self.log_label.text += f"⚠️ {p['name']} has insufficient budget (${p['budget']}M) to bid. Auto-folding to Hidden Player option!\n"
            self.active_bidders.pop(self.current_turn_idx)
            
            if len(self.active_bidders) == 0 or (len(self.active_bidders) == 1 and self.highest_bidder is not None):
                self.end_round()
                return
                
            if self.current_turn_idx >= len(self.active_bidders):
                self.current_turn_idx = 0
            
            self.update_turn_ui()
            return

        self.info_label.text = f"TURN: {p['name']} | Budget: ${p['budget']}M | {curr_pos}: {self.count_players_in_pos(p['squad'], curr_pos)}/{needed}"

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
            self.log_label.text += f"⚠️ {p['name']}: Not enough budget!\n"
            return
            
        self.current_bid = new_bid
        self.highest_bidder = pid
        self.log_label.text += f"⚡ {p['name']} raised bid to ${self.current_bid}M\n"
        self.advance_turn()

    def pass_auction(self, instance):
        pid = self.current_player_id()
        p_name = self.players[pid]['name']
        self.log_label.text += f"❌ {p_name} folded.\n"
        
        self.active_bidders.pop(self.current_turn_idx)
        
        if len(self.active_bidders) == 0 or (len(self.active_bidders) == 1 and self.highest_bidder is not None):
            self.end_round()
            return
            
        if self.current_turn_idx >= len(self.active_bidders):
            self.current_turn_idx = 0
            
        self.update_turn_ui()

    def end_round(self):
        self.set_bid_buttons_state(True)
        self.pass_btn.disabled = True
        curr_pos = POSITIONS[self.current_stage_idx]
        needed = POS_REQUIREMENTS[curr_pos]

        if self.highest_bidder is not None:
            winner = self.players[self.highest_bidder]
            winner['budget'] -= self.current_bid
            winner['squad'].append(self.current_player)
            self.log_label.text += f"\n🎉 WON: {winner['name']} bought {self.current_player['name']} (${self.current_bid}M)!\n"
        else:
            self.log_label.text += f"\n🚫 No Bids for {self.current_player['name']}.\n"

        self.log_label.text += f"🎁 Assigning Hidden Players ({curr_pos}) to managers who folded or lack budget:\n"
        for pid, p in self.players.items():
            if pid != self.highest_bidder and self.count_players_in_pos(p['squad'], curr_pos) < needed:
                hidden_p = self.get_random_player_by_pos(curr_pos)
                if hidden_p:
                    p['budget'] -= hidden_p['base']
                    p['squad'].append(hidden_p)
                    self.log_label.text += f"   ➡️ {p['name']} received hidden player: {hidden_p['name']} (${hidden_p['base']}M)\n"

        if self.is_stage_complete():
            self.start_btn.text = f"VIEW {curr_pos} STAGE SUMMARY 📋"
        else:
            self.start_btn.text = "Next Round"
        self.start_btn.disabled = False

    def show_stage_summary_screen(self):
        self.auto_fill_stage_if_needed()
        self.root.clear_widgets()
        curr_pos = POSITIONS[self.current_stage_idx]

        title_label = Label(
            text=f"📋 STAGE SUMMARY: {curr_pos} PLAYERS 📋", 
            font_size='14sp', bold=True, color=(0.2, 0.8, 1, 1), size_hint=(1, 0.1)
        )
        self.root.add_widget(title_label)
        
        summary_text = ""
        for pid, p in self.players.items():
            pos_players = [pl for pl in p['squad'] if pl['pos'] == curr_pos]
            summary_text += f"=========================================\n"
            summary_text += f"👤 MANAGER: {p['name']} | Remaining Budget: ${p['budget']}M\n"
            summary_text += f"   [{curr_pos} Lineup - Total {len(pos_players)}/{POS_REQUIREMENTS[curr_pos]}]:\n"
            summary_text += f"-----------------------------------------\n"
            for idx, pl in enumerate(pos_players, 1):
                summary_text += f"   {idx}. {pl['name']} | OVR: {pl['rating']} | Status: {pl['status']}\n"
            summary_text += "\n"

        summary_label = Label(
            text=summary_text, font_size='13sp', halign='left', valign='top', color=(0.9, 0.9, 0.9, 1), size_hint_y=None
        )
        summary_label.bind(texture_size=summary_label.setter('size'))
        
        scroll = ScrollView(size_hint=(1, 0.75))
        scroll.add_widget(summary_label)
        self.root.add_widget(scroll)
        
        if self.current_stage_idx + 1 < len(POSITIONS):
            next_stage_name = POSITIONS[self.current_stage_idx + 1]
            btn_text = f"PROCEED TO NEXT STAGE ({next_stage_name}) ➡️"
            on_click = self.advance_to_next_stage
        else:
            btn_text = "VIEW FULL 4-3-3 SQUADS & START LEAGUE 🏆"
            on_click = lambda x: self.show_squads_screen()

        action_btn = Button(
            text=btn_text, font_size='14sp', bold=True, background_color=(0.1, 0.7, 0.3, 1), size_hint=(1, 0.15), on_press=on_click
        )
        self.root.add_widget(action_btn)

    def advance_to_next_stage(self, instance):
        self.current_stage_idx += 1
        self.setup_auction_ui()

    def show_squads_screen(self):
        self.root.clear_widgets()
        for pos in POSITIONS:
            self.auto_fill_stage_if_needed(pos)

        title_label = Label(
            text="📋 FINAL 4-3-3 SQUADS OVERVIEW 📋", 
            font_size='16sp', bold=True, color=(0.2, 0.8, 1, 1), size_hint=(1, 0.1)
        )
        self.root.add_widget(title_label)
        
        squads_text = ""
        for pid, p in self.players.items():
            avg_ovr = sum(pl['rating'] for pl in p['squad']) / max(len(p['squad']), 1)
            squads_text += f"=========================================\n"
            squads_text += f"MANAGER: {p['name']} | Budget Left: ${p['budget']}M | Avg OVR: {avg_ovr:.1f}\n"
            squads_text += f"-----------------------------------------\n"
            
            for pos in POSITIONS:
                pos_list = [pl for pl in p['squad'] if pl['pos'] == pos]
                squads_text += f"[{len(pos_list)}/{POS_REQUIREMENTS[pos]}]: " + ", ".join([f"{pl['name']} ({pl['rating']})" for pl in pos_list]) + "\n"
            squads_text += "\n"

        squads_label = Label(
            text=squads_text, font_size='13sp', halign='left', valign='top', color=(0.9, 0.9, 0.9, 1), size_hint_y=None
        )
        squads_label.bind(texture_size=squads_label.setter('size'))
        
        scroll = ScrollView(size_hint=(1, 0.75))
        scroll.add_widget(squads_label)
        self.root.add_widget(scroll)
        
        action_btn = Button(
            text="PROCEED TO LEAGUE MATCHES (FIRST HALF) 🏆", font_size='14sp', bold=True, background_color=(0.1, 0.7, 0.3, 1), size_hint=(1, 0.15), on_press=lambda x: self.start_league_matches()
        )
        self.root.add_widget(action_btn)

    def start_league_matches(self):
        self.player_stats = {}
        for pid, p in self.players.items():
            for pl in p['squad']:
                self.player_stats[pl['name']] = {
                    "player": pl,
                    "manager_name": p['name'],
                    "goals": 0,
                    "assists": 0
                }
        self.first_half_logs = ""
        self.transfer_reports = {}
        self.play_first_half_matches()

    def distribute_match_stats(self, team_id, goals_scored):
        squad = self.players[team_id]['squad']
        if goals_scored > 0 and squad:
            attackers = [pl for pl in squad if pl['pos'] in ['ST', 'MID']] or squad
            midfielders = [pl for pl in squad if pl['pos'] in ['MID', 'DEF']] or squad

            for _ in range(goals_scored):
                scorer = random.choice(attackers)
                self.player_stats[scorer['name']]['goals'] += 1
                
                if random.random() < 0.7:
                    assister = random.choice(midfielders)
                    if assister['name'] != scorer['name']:
                        self.player_stats[assister['name']]['assists'] += 1

        yellows = random.choices([0, 1, 2, 3], weights=[40, 35, 15, 10])[0]
        reds = random.choices([0, 1], weights=[90, 10])[0]
        
        self.players[team_id]['yellow_cards'] += yellows
        self.players[team_id]['red_cards'] += reds

    def play_single_match(self, home_id, away_id, leg_label):
        home_team = self.players[home_id]
        away_team = self.players[away_id]
        
        team_ratings = {pid: sum(pl['rating'] for pl in p['squad']) / max(len(p['squad']), 1) for pid, p in self.players.items()}
        home_rating = team_ratings[home_id] + 2
        away_rating = team_ratings[away_id]
        
        score_home = max(0, int((home_rating - 70) / 5 + random.randint(-1, 3)))
        score_away = max(0, int((away_rating - 70) / 5 + random.randint(-1, 3)))
        
        home_team['gf'] += score_home
        home_team['ga'] += score_away
        away_team['gf'] += score_away
        away_team['ga'] += score_home
        
        self.distribute_match_stats(home_id, score_home)
        self.distribute_match_stats(away_id, score_away)

        if score_home > score_away:
            home_team['pts'] += 3
            home_team['w'] += 1
            away_team['l'] += 1
        elif score_away > score_home:
            away_team['pts'] += 3
            away_team['w'] += 1
            home_team['l'] += 1
        else:
            home_team['pts'] += 1
            away_team['pts'] += 1
            home_team['d'] += 1
            away_team['d'] += 1
            
        return f"[{leg_label}] 🏠 {home_team['name']}  {score_home} - {score_away}  {away_team['name']} ✈️\n"

    def play_first_half_matches(self):
        self.first_half_logs = "=== FIRST HALF MATCH RESULTS (LEG 1) ===\n\n"
        for i in range(self.num_players):
            for j in range(i + 1, self.num_players):
                self.first_half_logs += self.play_single_match(i, j, "LEG 1")
        
        self.current_transfer_manager_idx = 0
        self.show_mid_season_transfer_screen()

    def show_mid_season_transfer_screen(self):
        self.root.clear_widgets()
        
        if self.current_transfer_manager_idx >= self.num_players:
            self.show_transfer_summary_screen()
            return

        p = self.players[self.current_transfer_manager_idx]
        
        title = Label(
            text=f"🔄 WINTER TRANSFER WINDOW (Manager {self.current_transfer_manager_idx + 1}/{self.num_players})", 
            font_size='16sp', bold=True, color=(1, 0.8, 0.2, 1), size_hint=(1, 0.08)
        )
        self.root.add_widget(title)

        info = Label(
            text=f"Manager: {p['name']}\nSelect up to 3 players to replace (Optional):", 
            font_size='13sp', halign='center', color=(1, 1, 1, 1), size_hint=(1, 0.08)
        )
        self.root.add_widget(info)

        scroll = ScrollView(size_hint=(1, 0.7))
        grid = GridLayout(cols=1, spacing=5, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        self.selected_players_to_swap = []

        for pl in p['squad']:
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=10)
            lbl = Label(text=f"{pl['name']} ({pl['pos']}) - OVR: {pl['rating']}", font_size='13sp', color=(0.9, 0.9, 0.9, 1), size_hint_x=0.7)
            
            btn = Button(text="Keep", font_size='12sp', background_color=(0.2, 0.6, 0.3, 1), size_hint_x=0.3)
            btn.bind(on_press=lambda inst, pl_ref=pl, b=btn: self.toggle_player_swap(pl_ref, b))
            
            box.add_widget(lbl)
            box.add_widget(btn)
            grid.add_widget(box)

        scroll.add_widget(grid)
        self.root.add_widget(scroll)

        confirm_btn = Button(
            text="CONFIRM TRANSFERS & NEXT ➡️", 
            font_size='14sp', bold=True, background_color=(0.1, 0.7, 0.3, 1), size_hint=(1, 0.14),
            on_press=self.confirm_manager_transfers
        )
        self.root.add_widget(confirm_btn)

    def toggle_player_swap(self, player, btn_instance):
        if player in self.selected_players_to_swap:
            self.selected_players_to_swap.remove(player)
            btn_instance.text = "Keep"
            btn_instance.background_color = (0.2, 0.6, 0.3, 1)
        else:
            if len(self.selected_players_to_swap) >= 3:
                return
            self.selected_players_to_swap.append(player)
            btn_instance.text = "SWAP ❌"
            btn_instance.background_color = (0.8, 0.2, 0.2, 1)

    def confirm_manager_transfers(self, instance):
        pid = self.current_transfer_manager_idx
        p = self.players[pid]
        manager_swaps = []

        for old_player in self.selected_players_to_swap:
            p['squad'].remove(old_player)
            if old_player['name'] in self.player_stats:
                del self.player_stats[old_player['name']]
            
            new_player = self.get_random_player_by_pos(old_player['pos'])
            if new_player:
                p['squad'].append(new_player)
                self.player_stats[new_player['name']] = {
                    "player": new_player,
                    "manager_name": p['name'],
                    "goals": 0,
                    "assists": 0
                }
                manager_swaps.append((old_player, new_player))

        self.transfer_reports[pid] = manager_swaps
        self.current_transfer_manager_idx += 1
        self.show_mid_season_transfer_screen()

    def show_transfer_summary_screen(self):
        self.root.clear_widgets()
        
        title = Label(
            text="📋 WINTER TRANSFER WINDOW SUMMARY 📋", 
            font_size='16sp', bold=True, color=(1, 0.8, 0.2, 1), size_hint=(1, 0.1)
        )
        self.root.add_widget(title)

        summary_text = "Here are the changes made by each manager:\n\n"
        for pid, p in self.players.items():
            swaps = self.transfer_reports.get(pid, [])
            summary_text += f"👤 MANAGER: {p['name']}\n"
            if not swaps:
                summary_text += "   - No changes made (Kept the original squad).\n"
            else:
                for old_p, new_p in swaps:
                    summary_text += f"   ❌ Out: {old_p['name']} ({old_p['pos']}, OVR: {old_p['rating']})\n"
                    summary_text += f"   ✨ In:  {new_p['name']} ({new_p['pos']}, OVR: {new_p['rating']})\n"
            summary_text += "-----------------------------------------\n"

        summary_label = Label(
            text=summary_text, font_size='13sp', halign='left', valign='top', color=(0.9, 0.9, 0.9, 1), size_hint_y=None
        )
        summary_label.bind(texture_size=summary_label.setter('size'))

        scroll = ScrollView(size_hint=(1, 0.75))
        scroll.add_widget(summary_label)
        self.root.add_widget(scroll)

        btn = Button(
            text="PROCEED TO SECOND HALF MATCHES 🏆", font_size='14sp', bold=True, background_color=(0.1, 0.7, 0.3, 1), size_hint=(1, 0.15),
            on_press=lambda x: self.play_second_half_and_finish()
        )
        self.root.add_widget(btn)

    def play_second_half_and_finish(self):
        self.root.clear_widgets()
        self.info_label = Label(text="🏆 HOME & AWAY LEAGUE FINAL RESULTS 🏆", font_size='18sp', bold=True, color=(1, 0.8, 0.2, 1), size_hint=(1, 0.12))
        self.root.add_widget(self.info_label)
        
        self.card_label = Label(text="Second Half Completed Successfully!", font_size='14sp', halign='center', color=(1, 1, 1, 1), size_hint=(1, 0.1))
        self.root.add_widget(self.card_label)
        
        self.log_label = Label(text="", font_size='13sp', halign='left', valign='top', color=(0.9, 0.9, 0.9, 1), size_hint_y=None)
        self.log_label.bind(texture_size=self.log_label.setter('size'))
        
        scroll = ScrollView(size_hint=(1, 0.78))
        scroll.add_widget(self.log_label)
        self.root.add_widget(scroll)

        match_logs = self.first_half_logs + "\n=== SECOND HALF MATCH RESULTS (LEG 2) ===\n\n"
        for i in range(self.num_players):
            for j in range(i + 1, self.num_players):
                match_logs += self.play_single_match(j, i, "LEG 2")

        match_logs += "\n=========================\n🏆 FINAL LEAGUE STANDINGS 🏆\n=========================\n"
        sorted_league = sorted(self.players.values(), key=lambda x: (x['pts'], x['gf'] - x['ga'], x['gf']), reverse=True)
        
        for rank, p in enumerate(sorted_league, 1):
            gd = p['gf'] - p['ga']
            total_played = p['w'] + p['d'] + p['l']
            match_logs += f"#{rank} | {p['name']} | Pld: {total_played} | Pts: {p['pts']} | {p['w']}W-{p['d']}D-{p['l']}L | GF: {p['gf']} GA: {p['ga']} (GD: {gd:+d})\n"

        top_scorer = max(self.player_stats.values(), key=lambda x: (x['goals'], x['player']['rating']))
        top_assister = max(self.player_stats.values(), key=lambda x: (x['assists'], x['player']['rating']))
        best_player = max(self.player_stats.values(), key=lambda x: (x['goals'] * 2 + x['assists'] * 1.5 + x['player']['rating']))
        
        most_yellows_team = max(self.players.values(), key=lambda x: x['yellow_cards'])
        most_reds_team = max(self.players.values(), key=lambda x: x['red_cards'])

        match_logs += "\n=========================\n🌟 END OF SEASON AWARDS 🌟\n=========================\n"
        match_logs += f"🥇 TOP SCORER (الهداف): {top_scorer['player']['name']} ({top_scorer['goals']} Goals) - {top_scorer['manager_name']}\n"
        match_logs += f"🅰️ TOP ASSIST (الأكثر صناعة): {top_assister['player']['name']} ({top_assister['assists']} Assists) - {top_assister['manager_name']}\n"
        match_logs += f"⭐ BEST PLAYER (أفضل لاعب): {best_player['player']['name']} (OVR: {best_player['player']['rating']}) - {best_player['manager_name']}\n"
        match_logs += "-----------------------------------------\n"
        match_logs += f"🟨 MOST YELLOW CARDS: {most_yellows_team['name']} ({most_yellows_team['yellow_cards']} Yellow Cards)\n"
        match_logs += f"🟥 MOST RED CARDS: {most_reds_team['name']} ({most_reds_team['red_cards']} Red Cards)\n"

        winner = sorted_league[0]
        self.info_label.text = f"LEAGUE CHAMPION: {winner['name']} 🏆"
        self.card_label.text = f"Congratulations {winner['name']}!\nWon the League with {winner['pts']} Points!"
        self.log_label.text = match_logs

if __name__ == '__main__':
    FootballAuctionLeagueApp().run()

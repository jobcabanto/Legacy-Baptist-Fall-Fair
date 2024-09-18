
from lbcleaderboard.scripts.authenticate import Token
import pandas as pd
import os

class RawData:

    def __init__(self):
        self.spreadsheet_id = "1srLoO1qtrXkLo5T3R2OVcmAxcnNRcb8Qfby3mwcKLwc"
        self.range_count = "Registration!G3"
        self.file_path = r"C:\Users\JC\OneDrive\Documents\ProgrammingProjects\LegacyFallFair2024\lbcproject\lbcleaderboard\templates"
        self.raw_scoreboard_data, self.raw_adult_leader_data, self.adult_leaders, self.raw_child_leader_data, self.child_leaders = None, None, None, None, None

    def PullData(self):

        if Token().access_api()[0]:
            sheet = Token().access_api()[1].spreadsheets()
            result = (
                sheet.values()
                .get(spreadsheetId=self.spreadsheet_id, range=self.range_count)
                .execute()
                )
        else:
            return Token().access_api()
        player_count = result.get("values", [])[0][0]
        scoreboard_range = "B3:" + "P" + str(int(player_count) + 3)
        result = (
            sheet.values()
            .get(spreadsheetId = self.spreadsheet_id, range = scoreboard_range)
            .execute()
            )
        player_records = result.get("values", [])
        if not player_records:
            print("No data found.")
            return
        self.raw_scoreboard_data = pd.DataFrame(player_records[1:], columns=player_records[0])
        self.raw_scoreboard_data = self.raw_scoreboard_data.drop(labels = "Player ID", axis=1)

        leading_adults, leading_children = [], []

        self.raw_adult_leader_data = self.raw_scoreboard_data[self.raw_scoreboard_data['Youth'] == 'N']
        numeric_columns = self.raw_adult_leader_data.columns[-11:]

        self.raw_adult_leader_data.loc[:, numeric_columns] = self.raw_adult_leader_data.loc[:, numeric_columns].apply(pd.to_numeric, errors='coerce')

        for game in self.raw_adult_leader_data.columns[3:-1]:
            max_points = self.raw_adult_leader_data[game].max()
            leaders_for_game = self.raw_adult_leader_data[self.raw_adult_leader_data[game] == max_points][['Name', game]]
            for _, row in leaders_for_game.iterrows():
                leading_adults.append({'Point Leader (Adult)': row['Name'], 'Game': game, 'Points': row[game]})

        self.adult_leaders = pd.DataFrame(leading_adults).sort_values(['Points']).drop_duplicates(subset = ['Game']).sort_values(['Game'])
    
        self.raw_child_leader_data = self.raw_scoreboard_data[self.raw_scoreboard_data['Youth'] == 'Y']
        numeric_columns = self.raw_child_leader_data.columns[-11:]

        self.raw_child_leader_data.loc[:, numeric_columns] = self.raw_child_leader_data.loc[:, numeric_columns].apply(pd.to_numeric, errors='coerce')
        
        for game in self.raw_child_leader_data.columns[3:-1]:
            max_points = self.raw_child_leader_data[game].max()
            leaders_for_game = self.raw_child_leader_data[self.raw_child_leader_data[game] == max_points][['Name', game]]
            for _, row in leaders_for_game.iterrows():
                leading_children.append({'Point Leader (Youth)': row['Name'], 'Game': game, 'Points': row[game]})
 
        self.child_leaders = pd.DataFrame(leading_children).sort_values(['Points']).drop_duplicates(subset = ['Game']).sort_values(['Game'])

        self.raw_scoreboard_data = self.raw_scoreboard_data.drop(labels = "Youth", axis=1)

        return self.raw_scoreboard_data, self.adult_leaders, self.child_leaders

    def StyleData(self):

        try:
            self.raw_scoreboard_data = self.raw_scoreboard_data.style.set_table_styles(
                                        [{
                                            'selector': 'th',
                                            'props': [('background-color', '#ae4b0d'), ("color", "white")]
                                        }])
            self.raw_scoreboard_data = self.raw_scoreboard_data.hide(axis="index")
        except:
            pass

        try:
            self.adult_leaders = self.adult_leaders.style.set_table_styles(
                                        [{
                                            'selector': 'th',
                                            'props': [('background-color', '#ae4b0d'), ("color", "white")]
                                        }])
            self.adult_leaders = self.adult_leaders.hide(axis="index")
        except:
            pass

        try:
            self.child_leaders = self.child_leaders.style.set_table_styles(
                                        [{
                                            'selector': 'th',
                                            'props': [('background-color', '#ae4b0d'), ("color", "white")]
                                        }])
            self.child_leaders = self.child_leaders.hide(axis="index")
        except:
            pass

        return self.raw_scoreboard_data, self.adult_leaders, self.child_leaders
    
    def DataToWeb(self):
        index_file = os.path.join(self.file_path, "index.html") 
        html_string = '''
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">       
                <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1,user-scalable=no">
                <link rel="icon" href="static/logo3.png">
                <link rel="stylesheet" href="static/df_style.css">
                <link rel="preconnect" href="https://fonts.googleapis.com">
                <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
                <link href="https://fonts.googleapis.com/css2?family=Archivo:ital,wght@0,100..900;1,100..900&family=Radio+Canada+Big:ital,wght@0,400..700;1,400..700&display=swap" rel="stylesheet">
                <script src="https://unpkg.com/htmx.org@1.9.12" integrity="sha384-ujb1lZYygJmzgSwoxRggbCHcjc0rB2XoQrxeTUQyRjrOnlCoYta87iKBWq3EsdM2" crossorigin="anonymous"></script>
                <title>LBC Fall Fair 2024</title>
            </head>
            <body class="center top-bottom" hx-get="" hx-trigger="every 3s">
                <div style="background-color: #ae4b0d">
                    <a href="https://www.legacybaptist.church" target="_blank">
                        <img src="static/logo.png" width="362.25" height="115" class="center">
                    </a>
                </div>
                <div>
                    <img src="static/leaderboard.png" height="150" width="200" class="center">
                </div>
                <div class="container">
                    <div class="table-responsive">
                        <table class="leaderboard">
                            {leaderboard}
                        </table>
                    </div>
                </div><br>
                <div class="container">
                    <div class="table-responsive">
                        <div class="table-wrapper">
                            <table>
                                {adult_leaders}
                            </table>
                            <br>
                            <table>
                                {child_leaders}
                            </table>
                        </div>
                    </div>
                </div>
                <div>
                    <img src="static/archive.png" height="150" width="200" class="center">
                </div>
                <div class="container">
                    <center>
                        <a href="https://www.instagram.com/p/Cy0h1ULuiCN/?img_index=1" target="_blank">
                            <img src="static/placeholder.png" width="800" height="800" class="big-image">
                        </a>
                    </center>
                </div><br>
                <div class="center" style="background-color: #ae4b0d"> 
                    <a href="https://www.legacybaptist.church" target="_blank">
                        <img src="static/logo4.png" height="115" width="100" class="center">
                    </a>
                    <h5>Service Times: Sundays @ 9AM and 11AM</h5>
                    <h5>Legacy Baptist Church</h5>
                    <h5>3415 Etude Drive</h5>
                    <h5>Mississauga, ON | L4T 1T5</h5>
                    <h5>info@legacybaptist.church | 905-821-6302</h5><br>
                    <h5></h5>
                </div>
            </body>
        </html> 
        '''
        
        with open(index_file, 'w') as f:
            try:
                f.write(html_string.format(leaderboard=self.raw_scoreboard_data.to_html(), adult_leaders=self.adult_leaders.to_html(), child_leaders=self.child_leaders.to_html()))
            except:
                pass
import json


class Analize:

    @staticmethod
    def show_champions():
        with open(f'C:\\Users\\Kyo\\PycharmProjects\\DiscordBot\\lolchamps\\champions.json', 'r') as f:
            data = json.loads(f.readlines()[0])
            return data

    def choose_champ(self, *choose: str):
        data = self.show_champions()
        champ_name = [champ for champ in data if champ['name'][0].lower() == choose[0].lower()]
        return champ_name

    def pretify(self, name_champ):
        champ = self.choose_champ(name_champ)
        beauty = ''
        values = ''
        for k, v in champ[0].items():
            beauty += f'{k:<15}'
            for value in v:
                values += f'{value} | '
            beauty += f'{values}\n'
            values = ''
        return beauty

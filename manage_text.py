class ManagerText:

    def __init__(self):
        pass

    def change_name_district(self, name: str):
        result = name.lower().replace(' ', '_')
        return result

    def get_start_text(self) -> str:
        text = '''*Привіт*
Я ваш робот помічник для пошуку квартир в цьому місті 
Для більш детальної інформації напишіть команду /help
        '''

        return text

    def get_help_text(self) -> str:
        text = '''Я маю такі команди
/start - починає роботу бота 
/help - надає інформацію про команди 
/add - додає лінк для пошуку 
/week - надає список квартир за останні 7 днів
/district - надає список районів

Більш детально про `/add`
Приклад його написання 
`/add 44 квартал , https://example.com/`
спочатку пишемо `/add` потім назву району `44 квартал` після, 
*через кому* посилання на олх по цьому району `https://example.com/`
        '''

        return text

    def change_cmd_add(self, text: str) -> tuple:

        correct_text = '''Все чудово
Посилання додано, наступного разу ви побачите квартири з нього 
        '''

        text_err = f'''*Невірно введена команда*
        `{text}`
Пеевірте її та порівняйте з прикладом 
`/add 44 квартал, https://example.com/`
        '''

        if ', ' in text:
            name_district, url = text[4:].split(', ')

            name_district = self.change_name_district(name=name_district)
        else:
            return (False, ('', ''), text_err)

        return (True, (name_district, url), correct_text)

    def change_week_text(self, data: list) -> str:
        text = 'За цей тиждень у нас такі варавнти\n'

        count = 1

        for i in data:
            url = i[2]

            text += f'{count}. {url} \n'

            count += 1

        return text

    def change_ofer_text(self, urls: list) -> str:

        flag = len(urls)

        null_ofer_text = 'Сьогодні нічого нового, пропоную подивитись що булло за цей тиждень /week'

        text = 'За сьогодні у нвс тaкі пропозиції\n'

        count = 1

        for i in urls:
            text += f'{count}. {i} \n'

            count += 1

        return text if flag else null_ofer_text


    def get_district_text(self, txt: str) -> str:

        text = 'У нас є такі райони\n'

        count = 1

        for i in txt.split(', '):
            text += f'{count}. {i} \n'

        return text

    def get_start_bot_text(self):
        text = '''Привіт! Я зараз почнаю працювати. Буду працювати ≈ 2 годинии 
        '''

        return text
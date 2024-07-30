import random
# достаем refer_id из команды /start
import re
import string

from app.db.requests import (get_ref_market, get_ref_price, get_today_refs, get_week_refs, get_month_refs,
                             check_ref_code, get_ref_unique, get_all_ref_starts, check_user_subs)
from app.db.requests_op import get_op_data, check_bot_channel_admin, get_actual_op_full, \
    switch_status_op_by_username

from app.filters.main_filter import ADMINS as admins

def get_refer_id(command_args):
    try:
        return str(command_args)
    except (TypeError, ValueError):
        return None

def gen_res():
    # Генерируем случайные балансы для каждого аспекта
    percent = random.randint(0, 100)
    economics_balance = random.randint(0, 100)
    workflow_balance = random.randint(0, 100)
    health_balance = random.randint(0, 100)
    children_count = random.randint(0, 5)

    # Генерируем списки основных аспектов и аспектов для улучшения
    keys_to_future = ['Вдохновение', 'Мотивация', 'Творчество', 'Счастливые моменты', 'Успех', 'Достижения',
                      'Самореализация', 'Уверенность', 'Жизненная сила', 'Энергия', 'Любовь к жизни', 'Радость',
                      'Гармония', 'Внутренний мир', 'Процветание', 'Смысл жизни', 'Вера в себя', 'Дружба',
                      'Семейное счастье', 'Здоровье', 'Эмоциональный подъем', 'Стремление к лучшему', 'Открытие нового',
                      'Самопознание', 'Признание', 'Вдохновляющие люди', 'Красота вокруг', 'Благодарность',
                      'Удивительные открытия', 'Мечты и цели', 'Доброта', 'Взаимопомощь', 'Спокойствие', 'Свобода',
                      'Светлые воспоминания', 'Теплота отношений', 'Романтика', 'Приключения', 'Удивление',
                      'Чувство гордости', 'Целеустремленность', 'Эмпатия', 'Сострадание', 'Терпимость', 'Смелость',
                      'Новаторство', 'Умиротворение', 'Взаимопонимание', 'Чувство удовлетворения', 'Желание учиться',
                      'Созидание', 'Проницательность', 'Ценность момента', 'Благополучие', 'Жизнерадостность',
                      'Душевное тепло', 'Интуиция', 'Самодисциплина', 'Умение прощать', 'Честность',
                      'Радость от работы', 'Талант', 'Настойчивость', 'Познание мира', 'Ценность семьи', 'Эстетика',
                      'Любознательность', 'Оригинальность', 'Продуктивность']

    need_to_work = ['Коммуникация и умение слышать друг друга', 'Доверие', 'Уважение', 'Эмпатия', 'Терпимость',
                    'Взаимопонимание', 'Совместные цели', 'Слушание', 'Поддержка', 'Честность', 'Прощение',
                    'Умение идти на компромисс', 'Эмоциональная близость', 'Финансовое планирование',
                    'Баланс времени вместе и порознь', 'Взаимные интересы', 'Совместное принятие решений',
                    'Открытость к изменениям', 'Разрешение конфликтов', 'Уважение личного пространства',
                    'Развитие интимности', 'Признание и похвала', 'Работа над недостатками', 'Взаимная мотивация',
                    'Понимание ожиданий друг друга', 'Сохранение романтики', 'Позитивное отношение',
                    'Планирование будущего', 'Сохранение независимости', 'Духовное развитие',
                    'Поддержка в трудные времена'
        , 'Совместное обучение и рост', 'Забота о здоровье', 'Взаимное вдохновение', 'Разделение обязанностей',
                    'Принятие различий', 'Взаимное уважение границ', 'Развитие общей культуры',
                    'Уважение к друзьям и родственникам партнера', 'Умение делиться радостью',
                    'Позитивное влияние друг на друга', 'Работа над преодолением стресса', 'Сохранение гармонии',
                    'Понимание ролей в отношениях', 'Совместное решение проблем', 'Поддержка личных достижений',
                    'Проявление благодарности', 'Уважение к прошлому партнера', 'Умение радоваться мелочам',
                    'Совместные увлечения', 'Время для себя', 'Осознанность в отношениях',
                    'Регулярные откровенные разговоры', 'Эмоциональная поддержка', 'Физическая забота',
                    'Социальная поддержка', 'Согласованность в воспитании детей', 'Сексуальная гармония',
                    'Гибкость в отношениях', 'Позитивное восприятие изменений', 'Согласование ожиданий',
                    'Принятие слабостей друг друга']

    # Рандомные значения для баланса и количества детей
    economics_balance = random.randint(0, 100)
    workflow_balance = random.randint(0, 100)
    health_balance = random.randint(0, 100)
    children_count = random.randint(0, 5)

    # Случайный выбор ключевых аспектов для перспективы
    keys_to_future_choices = random.sample(keys_to_future, k=random.randint(2, 3))
    need_to_work_choices = random.sample(need_to_work, k=random.randint(2, 3))

    # Формирование текста сообщения
    message = (
        f"🔮 *Прогноз для ваших отношений* 🔮\n\n"
        f"👩‍❤️‍👨 *Совместимость*: {percent}%\n"
        f"🌟 *Экономический баланс*: {economics_balance}%\n"
        f"📊 *Баланс рабочей нагрузки*: {workflow_balance}%\n"
        f"❤️ *Здоровье*: {health_balance}%\n"
        f"👶 *Возможное количество детей*: {children_count}\n\n"
        "🌠 *Основные аспекты для будущего*:\n"
    )

    # Добавление выбранных ключевых аспектов для будущего
    for key in keys_to_future_choices:
        message += f"🔸 {key}\n"

    message += "\n🔧 *Что нужно улучшить*:\n"

    # Добавление выбранных аспектов, над которыми нужно работать
    for work in need_to_work_choices:
        message += f"🔹 {work}\n"

    return message


def gen_unique():
    text = [random.choice(string.ascii_lowercase + string.digits if i != 5 else string.ascii_uppercase) for i in
            range(20)]
    print(f'genned: {text}')
    text = ''.join(text)
    return text


def escape_markdown_v2(text):
    escape_chars = r'\_*[]()~`>#+-=|{}.!'
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)

async def get_ref_info(ref_name):
    if await check_ref_code(ref_name)!= 0:
        refs_all = await get_ref_market(ref_name) # Можно все это заменить на 1 функцию, которая получает все эти данные
        all_refs_starts = await get_all_ref_starts(ref_name)
        refs_unique = await get_ref_unique(ref_name)
        code_price = await get_ref_price(ref_name)
        refs_today = await get_today_refs(ref_name)
        refs_week = await get_week_refs(ref_name)
        refs_month = await get_month_refs(ref_name)
        print(f'refs_all: {refs_all} code_price: {code_price}')
        if int(code_price) !=0:
            if all_refs_starts!=0:
                ref_price = int(code_price) / int(all_refs_starts)
            else:
                ref_price = 'Не измеримо'
            if refs_unique!=0:
                ref_unique_price = int(code_price) / int(refs_unique)
            else:
                ref_unique_price = 'Не измеримо'
        else:
            ref_price = '0'
            ref_unique_price = '0'
        link = 'https://t.me/astrostar_bot?start='+str(ref_name)
        link = escape_markdown_v2(link)
        ref_price = escape_markdown_v2(str(ref_price))
        ref_unique_price = escape_markdown_v2(str(ref_unique_price))
        code_price = escape_markdown_v2(code_price)
        answer = (f'*Название ссылки* {ref_name}\n\n'
                             f'📊 *Статистика*: \n\n'
                             f'• Всего перешли \- {all_refs_starts}\n'
                             f'• Из них уникальны \- {refs_unique}\n'
                             f'• Из них живы \- {refs_all}\n'
                             f'• Подписались на ОП \- 0\n\n'
                             f'⌛️ *Статистика по времени*\n\n'
                             f'• Сегодня \- {refs_today}\n'
                             f'• За последние 7 дней \- {refs_week}\n'
                             f'• За последние 30 дней \- {refs_month}\n\n'
                             f'*Цены*\n\n'
                             f'• Цена ссылки \- {code_price}\n'
                             f'• Цена за переход \- {ref_price}\n'
                             f'• Цена за уникального \- {ref_unique_price}\n'
                             f'• Цена за подписчика \(ОП\) \- 0\n\n'
                             f'Ссылка: {link}')
        #answer = escape_markdown_v2(answer)
        return answer
    else:
        answer = f'Ссылки {ref_name} не существует, создайте ее для просмотра статистики'
        return answer

async def get_op_info(op_name):
    name = op_name
    data = await get_op_data(str(op_name))
    print(data)
    print(f'link: {data.op_link}')
    count = 0
    answer = (f'Название ОП кнопки: {name}\nНик: {data.op_username}\nСсылка: {data.op_link}\nКол-во подписок: {data.op_count}\nСтатус: {data.op_status}')
    answer = escape_markdown_v2(answer)
    return answer


async def check_admin_channels(bot):
    bad_lst = await check_bot_channel_admin(bot)
    if not bad_lst:
        answer = 'Бот админ во всех подключенных каналах для ОП. Бот функционирует правильно'
    else:
        answer = f'Список каналов, в которых бот не админ: {bad_lst}' # Предложить отключить их
        for bad in bad_lst:
            #bad = bad.replace('@', 't.me/')
            await switch_status_op_by_username(bad)
        answer += '\nОтключили от работы эти каналы, так как они нарушают работу бота'
        for admin in admins:
            await bot.send_message(admin,f'Список каналов, в которых бот не админ: {bad_lst}\nОтключили от работы эти каналы, так как они нарушают работу бота')

async def check_user_subs_util(user, bot):
    actual_ops = await get_actual_op_full()

    need_to_sub = []
    for op in actual_ops:
        #link = str(op.op_link).replace('t.me/', '@')
        link = str(op.op_username)
        print(f'link: {link}')
        channel = await check_user_subs(user, bot, link)
        if channel:
            need_to_sub.append(channel)

    return need_to_sub
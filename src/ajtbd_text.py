"""Texts for the SmartFlow AJTBD case (ajtbd.src.html). Every value is (Russian, English).

Training case for the product-management course: R1 is the author's self-interview as a practising expert,
R2–R5 are composite personas built from her chats with students, clients and marketers — hypotheses to validate.
Structured data (interviews, job graph, tables) is turned into HTML here; build.py only fills {{key}} placeholders.
"""
import html


def e(s):
    return html.escape(s, quote=False)


T = {
    "title": ("AJTBD-исследование SmartFlow · Томирис (Гулсара) Жайлаубеккызы",
              "SmartFlow AJTBD research · Tomiris (Gulsara) Zhailaubekkyzy"),
    "desc": ("Учебный кейс: 5 AJTBD-интервью, граф работ, боли, изменения в продукте и приоритизация ICE для SmartFlow.",
             "Training case: 5 AJTBD interviews, a job graph, pains, product changes and ICE prioritisation for SmartFlow."),
    "nav_label": ("Разделы кейса", "Case sections"),
    "nav_back": ("← Портфолио", "← Portfolio"),
    "nav_summary": ("Итог", "Summary"),
    "nav_method": ("Метод", "Method"),
    "nav_int": ("Интервью", "Interviews"),
    "nav_graph": ("Граф работ", "Job graph"),
    "nav_alt": ("Альтернативы", "Alternatives"),
    "nav_pain": ("Боли", "Pains"),
    "nav_changes": ("Изменения", "Changes"),
    "nav_ice": ("Приоритеты", "Priorities"),
    "nav_seg": ("Сегменты", "Segments"),
    "eyebrow": ("Учебный кейс · Advanced JTBD · уровень 3", "Training case · Advanced JTBD · level 3"),
    "h1": ("SmartFlow: <span>деньги теряются между шагами</span>",
           "SmartFlow: <span>money is lost between the steps</span>"),
    "lead": ("Провела 5 AJTBD-интервью с экспертами, малым бизнесом и маркетологами, построила граф работ для трёх типов работы и превратила боли в 7 изменений продукта с приоритетами ICE. Главный вывод: клиенты нанимают SmartFlow не ради «бота», а ради стабильного дохода без жизни в переписке, а деньги теряются не на первом ответе, а на статусах и дожиме.",
             "I ran 5 AJTBD interviews with experts, small businesses and marketers, built a job graph for three job types and turned the pains into 7 product changes prioritised with ICE. The key finding: customers hire SmartFlow not for a “bot” but for steady income without living in chats, and money is lost not on the first reply but on statuses and follow-ups."),
    "note": ("R1 — самоинтервью автора как эксперта; R2–R5 — собирательные персоны, выводы — гипотезы для проверки",
             "R1 is the author’s self-interview as an expert; R2–R5 are composite personas, findings are hypotheses to validate"),
    "k1_e": ("Интервью", "Interviews"), "k1_v": ("5", "5"), "k1_d": ("3 сегмента: эксперты, малый бизнес, маркетологи", "3 segments: experts, small business, marketers"),
    "k2_e": ("Граф работ", "Job graph"), "k2_v": ("21 шаг", "21 steps"), "k2_d": ("3 типа работы, 9 шагов с болью", "3 job types, 9 steps with pain"),
    "k3_e": ("Оценка текущих решений", "Current solutions score"), "k3_v": ("4,6 / 10", "4.6 / 10"), "k3_d": ("средняя по 5 респондентам", "average across 5 respondents"),
    "k4_e": ("Приоритет №1", "Priority #1"), "k4_v": ("ICE 512", "ICE 512"), "k4_d": ("статусы клиентов в Office", "customer statuses in Office"),
    "con_h": ("Что нашла", "What I found"),
    "con1_t": ("Нанимают «время + деньги». ", "They hire “time + money”. "),
    "con1": ("У всех пятерых одна работа выше: стабильный доход и свободное время. Позиционирование — «продаёт, пока вы живёте», а не «AI-чат-бот».",
             "All five share one higher job: steady income and free time. Positioning: “sells while you live”, not “an AI chatbot”."),
    "con2_t": ("Потери — между шагами. ", "Losses happen between steps. "),
    "con2": ("Ответить — полдела: главные потери на шагах «статус клиента» и «дожать не купивших».",
             "Replying is half the job: the main losses are at “see the customer’s status” and “follow up non-buyers”."),
    "con3_t": ("Новый сегмент — офлайн-услуги. ", "New segment: offline services. "),
    "con3": ("Салонам и студиям в WhatsApp нужна запись, а не прогрев: короткий сценарий, ценность видна в первый день.",
             "Salons and studios on WhatsApp need booking, not nurturing: a short script with value visible on day one."),
    "do_h": ("Что предлагаю", "What I propose"),
    "do1_t": ("Статусы в Office (ICE 512). ", "Statuses in Office (ICE 512). "),
    "do1": ("5 статусов клиента и пуш «кого дожать сегодня».", "5 customer statuses and a “who to follow up today” push."),
    "do2_t": ("Запуск из шаблона за 10 минут (504). ", "Launch from a template in 10 minutes (504). "),
    "do2": ("Smart консультант по шаблону ниши отвечает 24/7.", "A Smart consultant from a niche template replies 24/7."),
    "do3_t": ("AI-генерация этапов воронки (294). ", "AI-generated funnel stages (294). "),
    "do3": ("Маркетолог пишет бриф, AI собирает этапы, он правит.", "The marketer writes a brief, AI drafts the stages, the marketer edits."),
    "m_e": ("Метод", "Method"),
    "m_h": ("5 интервью по одному шаблону AJTBD", "5 interviews with one AJTBD template"),
    "m_i": ("Вопросы — о последнем реальном случае, а не о мнениях. Критерий отбора: за последние 3 месяца человек сам решал задачу продаж в мессенджере. Из-за сроков R1 — самоинтервью автора (3 года онлайн-школы TMR Academy, продажи через мессенджеры), R2–R5 — собирательные персоны по перепискам с ученицами, клиентами и коллегами за 2023–2026 годы.",
            "Questions are about the last real case, not opinions. Screening: in the last 3 months the person handled messenger sales themselves. Because of the deadline, R1 is the author’s self-interview (3 years running the TMR Academy online school, selling via messengers), and R2–R5 are composite personas built from chats with students, clients and colleagues in 2023–2026."),
    "t_num": ("#", "#"), "t_seg": ("Сегмент", "Segment"), "t_type": ("Тип работы", "Job type"), "t_src": ("Источник", "Source"),
    "q_h": ("Вопросы интервью", "Interview questions"),
    "i_e": ("Интервью", "Interviews"),
    "i_h": ("Что рассказали респонденты", "What respondents told me"),
    "i_i": ("Каждое интервью заканчивается формулировкой работы «Когда…, хочу…, чтобы…». Нажмите на карточку, чтобы раскрыть все поля.",
            "Each interview ends with a job statement “When…, I want…, so that…”. Tap a card to open all fields."),
    "g_e": ("Граф работ", "Job graph"),
    "g_h": ("Три уровня: работа выше → основная работа → шаги", "Three levels: higher job → core job → steps"),
    "g_i": ("Красным отмечены шаги, где респонденты назвали боль. Типы A и B связаны: воронка маркетолога становится инструментом эксперта на шагах A2–A8.",
            "Steps where respondents named a pain are marked red. Types A and B are linked: the marketer’s funnel becomes the expert’s tool at steps A2–A8."),
    "g_higher": ("Работа выше", "Higher job"), "g_core": ("Основная работа", "Core job"),
    "a_e": ("Альтернативы", "Alternatives"),
    "a_h": ("С чем конкурирует SmartFlow", "What SmartFlow competes with"),
    "t_alt": ("Альтернатива", "Alternative"), "t_who": ("Кто", "Who"), "t_bad": ("Чем плоха", "Why it fails"),
    "p_e": ("Боли и возможности", "Pains and opportunities"),
    "p_h": ("Где теряются деньги и время", "Where money and time are lost"),
    "t_step": ("Шаг", "Step"), "t_pain": ("Боль", "Pain"), "t_force": ("Сила", "Severity"), "t_opp": ("Возможность", "Opportunity"),
    "ch_e": ("Изменения в продукте", "Product changes"),
    "ch_h": ("От цитаты к решению", "From quote to solution"),
    "ch_i": ("Каждое изменение выросло из конкретной цитаты и закрывает шаг графа. Ранг — из приоритизации ниже.",
             "Each change comes from a specific quote and closes a step of the graph. Rank comes from the prioritisation below."),
    "t_rank": ("Ранг", "Rank"), "t_insight": ("Инсайт из интервью", "Interview insight"), "t_change": ("Изменение", "Change"),
    "ice_e": ("Приоритизация", "Prioritisation"),
    "ice_h": ("ICE = Impact × Confidence × Ease", "ICE = Impact × Confidence × Ease"),
    "t_sol": ("Решение", "Solution"), "t_metric": ("Метрика успеха", "Success metric"),
    "ice_i1_t": ("Impact ", "Impact "),
    "ice_i1": ("выше у решений, которые прямо возвращают потерянные продажи.", "is higher for solutions that directly win back lost sales."),
    "ice_i2_t": ("Confidence ", "Confidence "),
    "ice_i2": ("выше, когда боль повторили несколько респондентов; у подбора эксперта она низкая — конечных клиентов среди респондентов не было.",
               "is higher when several respondents repeated the pain; it is low for expert matching — no end customers were interviewed."),
    "ice_i3_t": ("Ease ", "Ease "),
    "ice_i3": ("выше у того, что уже заложено в архитектуре (статусы, шаблоны); % автору требует выплат на 3+ роли.",
               "is higher for what the architecture already supports (statuses, templates); author payouts need a 3+ role split."),
    "s_e": ("Новые сегменты", "New segments"),
    "s_h": ("Где ещё расти", "Where else to grow"),
    "t_job": ("Работа", "Job"), "t_why": ("Почему перспективен", "Why it is promising"),
    "next_t": ("Следующий шаг: ", "Next step: "),
    "next": ("провести 5 реальных интервью (2 эксперта, 1 офлайн-бизнес, 2 маркетолога), заменить персоны R2–R5 и пересчитать Confidence.",
             "run 5 real interviews (2 experts, 1 offline business, 2 marketers), replace personas R2–R5 and recalculate Confidence."),
    "foot": ("Учебный кейс курса по продакт-менеджменту. R2–R5 — собирательные персоны, не реальные клиенты SmartFlow. Томирис (Гулсара) Жайлаубеккызы, 2026.",
             "Training case from a product-management course. R2–R5 are composite personas, not real SmartFlow customers. Tomiris (Gulsara) Zhailaubekkyzy, 2026."),
}

QUESTIONS = [
    ("Контекст: чем занимаетесь, как сейчас приходят клиенты?", "Context: what do you do, how do customers reach you now?"),
    ("Последний случай: вспомните последнюю заявку или продажу в мессенджере. Что произошло?", "Last case: recall your latest lead or sale in a messenger. What happened?"),
    ("Триггер: что заставило искать решение?", "Trigger: what made you look for a solution?"),
    ("Ожидаемый результат: что должно было измениться?", "Expected outcome: what should have changed?"),
    ("Шаги: что делали по порядку, от заявки до оплаты?", "Steps: what did you do, from lead to payment?"),
    ("Сложности и эмоции: где застряли, что бесило?", "Struggles and emotions: where did you get stuck, what annoyed you?"),
    ("Текущее решение: чем пользуетесь сейчас, почему не ушли?", "Current solution: what do you use now, why haven’t you switched?"),
    ("Работа выше: зачем вам больше продаж? (2–3 раза «зачем»)", "Higher job: why do you want more sales? (ask “why” 2–3 times)"),
    ("Критерии: что было бы идеально? За что заплатили бы?", "Criteria: what would be ideal? What would you pay for?"),
    ("Оценка: насколько довольны текущим результатом, от 1 до 10?", "Score: how satisfied are you with the current result, 1 to 10?"),
]

RESP = [
    ("R1", ("Онлайн-эксперт, школа маркетинга", "Online expert, marketing school"), "A", ("Автор, самоинтервью", "Author, self-interview")),
    ("R2", ("Эксперт-нутрициолог с ассистентом", "Nutrition expert with an assistant"), "A", ("Собирательная персона", "Composite persona")),
    ("R3", ("Салон красоты, Тараз", "Beauty salon, Taraz"), "A", ("Собирательная персона", "Composite persona")),
    ("R4", ("Маркетолог-продюсер", "Marketer and producer"), "B", ("Собирательная персона", "Composite persona")),
    ("R5", ("Техспециалист GetCourse / чат-боты", "GetCourse / chatbot tech specialist"), "B", ("Собирательная персона", "Composite persona")),
]

FIELDS = [("Контекст", "Context"), ("Последний случай", "Last case"), ("Триггер", "Trigger"), ("Ожидаемый результат", "Expected outcome"),
          ("Шаги", "Steps"), ("Сложности и эмоции", "Struggles and emotions"), ("Текущее решение", "Current solution"),
          ("Работа выше", "Higher job"), ("Критерии", "Criteria"), ("Оценка", "Score")]
JOB_LABEL = ("Формулировка работы", "Job statement")

INTERVIEWS = [
    ("R1", ("Онлайн-эксперт, школа маркетинга (автор)", "Online expert, marketing school (author)"), [
        ("«Я 3 года вела онлайн-школу маркетинга. Клиенты приходили из Instagram и Telegram, а дальше вся продажа шла в личке».", "“I ran an online marketing school for 3 years. Customers came from Instagram and Telegram, and the whole sale then happened in DMs.”"),
        ("«Запустила рекламу, за выходные пришло около 80 заявок. Отвечала сама до ночи. Половине ответила только на следующий день, и они уже остыли».", "“I ran ads and got about 80 leads over a weekend. I replied myself until late at night. Half only got an answer the next day, and they had gone cold.”"),
        ("«Я поняла, что продаю не я, а моя усталость. Чем больше трафика, тем хуже конверсия».", "“I realised it wasn’t me selling, it was my tiredness. The more traffic, the worse the conversion.”"),
        ("Каждый лид получает ответ сразу, а она подключается только к готовым платить.", "Every lead gets an instant reply, and she steps in only for those ready to pay."),
        ("Заявка → ответ в личке → вопросы о программе → цена → возражения → ссылка на оплату → напоминания вручную.", "Lead → DM reply → questions about the programme → price → objections → payment link → manual reminders."),
        ("Выгорание, чувство вины перед детьми, злость на себя за потерянных лидов.", "Burnout, guilt towards her children, anger at herself for lost leads."),
        ("Бот на конструкторе: «люди писали вопрос текстом, и бот ломался. Менеджер дорого, и его надо обучать моему подходу».", "A builder bot: “people typed questions and the bot broke. A manager is expensive and has to learn my approach.”"),
        ("«Мне нужно не больше переписок, а стабильный доход и вечера с детьми».", "“I don’t need more chats, I need steady income and evenings with my kids.”"),
        ("«Продавец, который знает мой продукт как я, отвечает сразу и зовёт меня, только когда человек готов платить».", "“A seller who knows my product like I do, replies instantly and calls me only when the person is ready to pay.”"),
        ("4/10", "4/10")],
     ("Когда за выходные приходит 80 заявок, а я одна, хочу, чтобы каждый получил ответ сразу, а меня звали только к готовым платить, чтобы иметь стабильный доход и вечера с детьми.",
      "When 80 leads arrive over a weekend and I’m alone, I want each to get an instant reply and to be called only for those ready to pay, so that I have steady income and evenings with my kids.")),
    ("R2", ("Эксперт-нутрициолог с ассистентом (персона)", "Nutrition expert with an assistant (persona)"), [
        ("«Веду марафоны питания. У меня ассистентка, она отвечает в WhatsApp».", "“I run nutrition challenges. My assistant answers on WhatsApp.”"),
        ("«Ассистентка ушла в отпуск, и за 2 недели продажи упали почти вдвое. Всё было у неё в голове».", "“My assistant went on holiday and sales nearly halved in 2 weeks. Everything was in her head.”"),
        ("Падение продаж из-за отпуска одного человека.", "Sales dropped because one person went on holiday."),
        ("Видеть каждого клиента и его этап, не спрашивая ассистента.", "See every customer and their stage without asking the assistant."),
        ("Заявка → ассистент отвечает → созвон с экспертом → оплата → таблица в Excel.", "Lead → assistant replies → call with the expert → payment → Excel sheet."),
        ("Тревога и потеря контроля: «я не знаю, кто купил, кто думает, а кто пропал».", "Anxiety and loss of control: “I don’t know who bought, who is thinking, and who vanished.”"),
        ("Ассистент + Excel: «таблица вечно устаревшая».", "Assistant + Excel: “the sheet is always out of date.”"),
        ("«Хочу масштабироваться и не зависеть от одного человека».", "“I want to scale and not depend on one person.”"),
        ("«Мне не нужна CRM на 100 кнопок, мне нужно видеть, кого дожать сегодня».", "“I don’t need a CRM with 100 buttons, I need to see who to follow up today.”"),
        ("5/10", "5/10")],
     ("Когда ассистент недоступен, хочу видеть статус каждого клиента и кого дожать сегодня, чтобы расти без зависимости от одного человека.",
      "When my assistant is unavailable, I want to see every customer’s status and who to follow up today, so that I can grow without depending on one person.")),
    ("R3", ("Салон красоты, Тараз (персона)", "Beauty salon, Taraz (persona)"), [
        ("«Запись идёт через WhatsApp и Instagram, отвечаю я или администратор».", "“Bookings come through WhatsApp and Instagram; I or the administrator reply.”"),
        ("«Клиентка вечером спросила цену на окрашивание, а ответили утром. Она уже записалась в другой салон».", "“A client asked the price of colouring in the evening and got a reply in the morning. She had already booked another salon.”"),
        ("Потерянная запись из-за вечернего сообщения.", "A booking lost because of an evening message."),
        ("Клиент сразу узнаёт цену и записывается на свободное время без администратора.", "The client gets the price at once and books a free slot without the administrator."),
        ("Вопрос о цене → ответ → подбор времени → запись в тетрадь → напоминание накануне.", "Price question → reply → pick a time → write it in a notebook → reminder the day before."),
        ("Раздражение от одинаковых вопросов, усталость: «пишут в 11 вечера».", "Irritation at repeated questions, tiredness: “they write at 11 pm.”"),
        ("Автоответ WhatsApp Business: «он просто говорит „ответим позже“, это не помогает».", "WhatsApp Business auto-reply: “it just says ‘we’ll reply later’, that doesn’t help.”"),
        ("«Чтобы мастера были загружены, а я не сидела в телефоне».", "“So my stylists are fully booked and I’m not glued to my phone.”"),
        ("«Если бот сам скажет цену и запишет на время, я заплачу».", "“If a bot tells the price and books the time itself, I’ll pay.”"),
        ("3/10", "3/10")],
     ("Когда клиент вечером спрашивает цену, хочу, чтобы ему сразу ответили и записали, чтобы мастера были загружены.",
      "When a client asks the price in the evening, I want them answered and booked at once, so that my stylists are fully booked.")),
    ("R4", ("Маркетолог-продюсер (персона)", "Marketer and producer (persona)"), [
        ("«Делаю запуски экспертам: воронки, прогревы, чат-боты».", "“I run launches for experts: funnels, nurturing, chatbots.”"),
        ("«Собрала воронку для психолога за 3 недели. Для следующего клиента, коуча, пришлось почти всё переделывать с нуля».", "“I built a funnel for a psychologist in 3 weeks. For the next client, a coach, I had to redo almost everything from scratch.”"),
        ("Эксперт не доплатил, потому что «воронка не сработала», хотя лидов было много.", "An expert didn’t pay the rest because “the funnel didn’t work”, although there were plenty of leads."),
        ("Собирать воронку за дни, а не недели, и доказывать результат цифрами.", "Build a funnel in days, not weeks, and prove the result with numbers."),
        ("Поиск клиента → бриф → сценарий → тексты и видео → настройка через техспеца → запуск → отчёт.", "Find a client → brief → script → copy and video → setup via a tech specialist → launch → report."),
        ("Обида и бессилие: «эксперт плохо продаёт на созвонах, а виноватой выходит воронка».", "Resentment and helplessness: “the expert sells badly on calls, and the funnel gets the blame.”"),
        ("Фикс за проект, свои заготовки в Google Docs, бот через техспеца.", "A fixed fee per project, her own drafts in Google Docs, a bot via a tech specialist."),
        ("«Хочу зарабатывать на своих наработках, а не продавать часы».", "“I want to earn from my assets, not sell hours.”"),
        ("«Если бы мои воронки продавались как шаблон и я получала процент с продаж, я бы делала их без остановки».", "“If my funnels sold as templates and I got a share of sales, I’d make them non-stop.”"),
        ("5/10", "5/10")],
     ("Когда беру клиента из новой ниши, хочу собрать воронку из готовой основы и получать % с продаж, чтобы зарабатывать на наработках, а не на часах.",
      "When I take a client from a new niche, I want to build the funnel from a ready base and earn a share of sales, so that I earn from my assets, not my hours.")),
    ("R5", ("Техспециалист GetCourse / чат-боты (персона)", "GetCourse / chatbot tech specialist (persona)"), [
        ("«Настраиваю GetCourse, Salebot, оплаты».", "“I set up GetCourse, Salebot, payments.”"),
        ("«Клиент попросил, чтобы бот отвечал на любые вопросы. На Salebot это сотни веток».", "“A client asked for a bot that answers any question. On Salebot that’s hundreds of branches.”"),
        ("Клиенты всё чаще просят «умного» бота, как ChatGPT.", "Clients increasingly ask for a “smart” bot like ChatGPT."),
        ("Бот понимает свободный текст, а правки занимают минуты.", "The bot understands free text and edits take minutes."),
        ("ТЗ от маркетолога → схема веток → сборка в конструкторе → подключение оплаты → тесты → бесконечные правки.", "Brief from the marketer → branch map → build in the builder → connect payments → tests → endless edits."),
        ("Рутина и выгорание: «любая правка стоит денег и времени».", "Routine and burnout: “every edit costs money and time.”"),
        ("Salebot и GetCourse, потому что «клиенты там уже сидят».", "Salebot and GetCourse, because “clients are already there.”"),
        ("«Хочу брать больше клиентов без выгорания на рутинной настройке».", "“I want to take more clients without burning out on routine setup.”"),
        ("«Мне нужен инструмент, где я ставлю логику и цели, а тексты AI пишет сам».", "“I need a tool where I set the logic and goals, and AI writes the texts.”"),
        ("6/10", "6/10")],
     ("Когда клиент просит «умного» бота, хочу задать логику и цели, а не писать сотни веток, чтобы брать больше клиентов без выгорания.",
      "When a client asks for a “smart” bot, I want to set logic and goals instead of writing hundreds of branches, so that I can take more clients without burning out.")),
]

# job graph: (label, higher, core, [(step, pain or None)])
GRAPH = [
    (("Тип A. Эксперт и малый бизнес (R1, R2, R3)", "Type A. Expert and small business (R1, R2, R3)"),
     ("Стабильный доход и свободное время", "Steady income and free time"),
     ("Превращать сообщения в оплаты без ручной переписки", "Turn messages into payments without manual chatting"),
     [(("Получить заявку", "Get a lead"), None),
      (("Ответить сразу", "Reply at once"), ("лид остывает за ночь · R1, R3", "lead goes cold overnight · R1, R3")),
      (("Понять запрос", "Understand the request"), None),
      (("Прогреть: кейсы, видео", "Nurture: cases, video"), None),
      (("Снять возражения, цена", "Handle objections, price"), None),
      (("Запись или оплата", "Booking or payment"), ("нет записи без админа · R3", "no booking without an admin · R3")),
      (("Видеть статус клиента", "See the customer’s status"), ("всё в голове ассистента · R2", "it’s all in the assistant’s head · R2")),
      (("Дожать не купивших", "Follow up non-buyers"), ("никто не ведёт · R1, R2", "nobody follows up · R1, R2")),
      (("Повторная продажа", "Repeat sale"), None)]),
    (("Тип B. Маркетолог и техспециалист (R4, R5)", "Type B. Marketer and tech specialist (R4, R5)"),
     ("Зарабатывать на наработках, а не на часах", "Earn from assets, not hours"),
     ("Быстро запускать работающие воронки для разных ниш", "Quickly launch working funnels for different niches"),
     [(("Найти клиента", "Find a client"), None),
      (("Бриф: ЦА, продукт, цель", "Brief: audience, product, goal"), None),
      (("Написать сценарий", "Write the script"), ("каждая ниша с нуля · R4", "every niche from scratch · R4")),
      (("Настроить технику", "Set up the tech"), ("сотни веток, правки · R5", "hundreds of branches, edits · R5")),
      (("Показать результат", "Show the result"), None),
      (("Получить оплату или %", "Get paid or a share"), ("фикс без связи с итогом · R4", "fixed fee unrelated to results · R4")),
      (("Продать шаблон снова", "Sell the template again"), None)]),
    (("Тип C. Конечный клиент (новый сегмент, гипотеза)", "Type C. End customer (new segment, hypothesis)"),
     ("Получить результат (навык, доход, здоровье) без лишних трат", "Get a result (skill, income, health) without wasted spend"),
     ("Выбрать подходящего эксперта и не купить лишний курс", "Choose the right expert and not buy a useless course"),
     [(("Найти эксперта", "Find an expert"), None),
      (("Задать вопросы", "Ask questions"), None),
      (("Сравнить варианты", "Compare options"), None),
      (("Решиться на покупку", "Decide to buy"), ("страх купить не то · R1, R4", "fear of buying the wrong thing · R1, R4")),
      (("Дойти до результата", "Reach the result"), ("бросает обучение · R1, R4", "drops out of learning · R1, R4"))]),
]

ALTS = [
    (("Отвечать самой", "Replying herself"), "R1, R3", ("Не успевает, лиды остывают", "Can’t keep up, leads go cold")),
    (("Ассистент / администратор", "Assistant / administrator"), "R2, R3", ("Зависимость, знания в голове одного человека", "Dependency, knowledge in one person’s head")),
    (("Автоответ WhatsApp Business", "WhatsApp Business auto-reply"), "R3", ("«Ответим позже» не продаёт", "“We’ll reply later” doesn’t sell")),
    (("Salebot / кнопочные боты", "Salebot / button bots"), "R1, R5", ("Ломаются на свободном тексте, дорогие правки", "Break on free text, costly edits")),
    (("Excel-таблица", "Excel sheet"), "R2", ("Всегда устаревшая", "Always out of date")),
    (("Фикс за проект + Google Docs", "Fixed fee + Google Docs"), "R4", ("Нет связи с результатом, каждая ниша с нуля", "No link to results, every niche from scratch")),
]

HIGH, MID = ("Высокая", "High"), ("Средняя", "Medium")
PAINS = [
    ("A2", ("Лид остывает за ночь", "Lead goes cold overnight"), "R1, R3", HIGH, ("Smart консультант 24/7", "24/7 Smart consultant")),
    ("A7", ("Всё в голове ассистента", "It’s all in the assistant’s head"), "R2", HIGH, ("Воронка статусов в Office", "Status funnel in Office")),
    ("A8", ("Не купивших никто не ведёт", "Nobody follows up non-buyers"), "R1, R2", HIGH, ("Авто-касания по статусу", "Automatic touches by status")),
    ("B3", ("Каждая ниша с нуля, 3 недели", "Every niche from scratch, 3 weeks"), "R4", HIGH, ("AI-генерация этапов по брифу", "AI-generated stages from a brief")),
    ("B4", ("Сотни веток, дорогие правки", "Hundreds of branches, costly edits"), "R5", MID, ("Логика и цели вместо веток", "Logic and goals instead of branches")),
    ("A6", ("Нет записи без человека", "No booking without a person"), "R3", MID, ("Запись в календарь из чата", "Calendar booking from the chat")),
    ("B6", ("Фикс без связи с результатом", "Fixed fee unrelated to results"), "R4", MID, ("% с продаж + маркетплейс шаблонов", "Share of sales + template marketplace")),
    ("C", ("Страх купить не то", "Fear of buying the wrong thing"), "R1, R4", MID, ("AI-подбор эксперта", "AI expert matching")),
]

CHANGES = [
    (1, ("R2: «видеть, кого дожать сегодня»", "R2: “see who to follow up today”"), "A7",
     ("<b>Статусы в Office:</b> 5 статусов (не договорили / не купил / ждёт человека / купил / отказ) + пуш «кого дожать сегодня»",
      "<b>Statuses in Office:</b> 5 statuses (unfinished / didn’t buy / waiting for a human / bought / declined) + a “who to follow up today” push")),
    (2, ("R1, R3: лид остывает за ночь", "R1, R3: lead goes cold overnight"), "A2, A5",
     ("<b>Запуск Smart консультанта за 10 минут</b> из шаблона ниши", "<b>Launch a Smart consultant in 10 minutes</b> from a niche template")),
    (3, ("R4, R5: каждый раз с нуля, сотни веток", "R4, R5: from scratch every time, hundreds of branches"), "B3, B4",
     ("<b>AI-генерация этапов воронки</b> по брифу, маркетолог правит", "<b>AI-generated funnel stages</b> from a brief, edited by the marketer")),
    (4, ("R1, R2: не купивших никто не ведёт", "R1, R2: nobody follows up non-buyers"), "A8",
     ("<b>Авто-дожим по статусу:</b> напоминания, кейсы, видео", "<b>Automatic follow-ups by status:</b> reminders, cases, video")),
    (5, ("R3: «запишет на время — заплачу»", "R3: “books the time — I’ll pay”"), "A6",
     ("<b>Запись в календарь из чата</b> для сервисного бизнеса", "<b>Calendar booking from the chat</b> for service businesses")),
    (6, ("R4: «процент — делала бы без остановки»", "R4: “a share — I’d make them non-stop”"), "B6, B7",
     ("<b>Маркетплейс шаблонов с % автору</b> и еженедельными выплатами", "<b>Template marketplace with an author share</b> and weekly payouts")),
    (7, ("R1, R4: неподходящие ученики не учатся", "R1, R4: unsuitable students don’t study"), "C",
     ("<b>AI-подбор эксперта</b> для конечного клиента", "<b>AI expert matching</b> for the end customer")),
]

ICE = [
    (("Статусы в Office", "Statuses in Office"), 8, 8, 8, ("Доля лидов со статусом, заходы эксперта в Office в неделю", "Share of leads with a status, expert visits to Office per week")),
    (("Запуск из шаблона", "Launch from a template"), 9, 8, 7, ("Время до первого ответа, доля ответов быстрее минуты", "Time to first reply, share of replies under a minute")),
    (("AI-генерация этапов", "AI-generated stages"), 7, 6, 7, ("Время создания воронки (сейчас 3 недели у R4)", "Time to build a funnel (now 3 weeks for R4)")),
    (("Авто-дожим", "Automatic follow-ups"), 8, 6, 6, ("Конверсия «не купил» → «купил»", "Conversion “didn’t buy” → “bought”")),
    (("Запись из чата", "Booking from the chat"), 7, 5, 6, ("Доля записей без участия человека", "Share of bookings with no human involved")),
    (("% автору шаблона", "Template author share"), 8, 5, 4, ("Опубликованные шаблоны, продажи через шаблоны", "Published templates, sales via templates")),
    (("AI-подбор эксперта", "AI expert matching"), 6, 4, 4, ("Доля клиентов, выбравших через подбор и дошедших до конца", "Share of customers who chose via matching and finished")),
]

SEGMENTS = [
    (("Офлайн-услуги в WhatsApp (салоны, клиники, студии)", "Offline services on WhatsApp (salons, clinics, studios)"),
     ("«Цена → запись» без администратора", "“Price → booking” without an administrator"),
     ("Короткий сценарий, ценность видна в первый день, есть в каждом городе", "Short script, value visible on day one, in every city")),
    (("Маркетологи как авторы шаблонов", "Marketers as template authors"),
     ("Зарабатывать на наработках", "Earn from their assets"),
     ("Сторона предложения маркетплейса, мотивированы процентом", "The marketplace’s supply side, motivated by a share")),
    (("Конечные клиенты, выбирающие эксперта", "End customers choosing an expert"),
     ("Не купить лишний курс", "Not buy a useless course"),
     ("Основа удержания на платформе, пока гипотеза", "The basis of platform retention, still a hypothesis")),
]


def build(i):
    """Return {key: html} for language index i (0 = ru, 1 = en)."""
    out = {}
    out["questions"] = "".join(f"<li>{e(q[i])}</li>" for q in QUESTIONS)
    out["rows_resp"] = "".join(f"<tr><td>{r}</td><td>{e(s[i])}</td><td>{t}</td><td>{e(src[i])}</td></tr>" for r, s, t, src in RESP)
    cards = []
    for n, (rid, name, vals, job) in enumerate(INTERVIEWS):
        dl = "".join(f"<dt>{e(FIELDS[k][i])}</dt><dd>{e(v[i])}</dd>" for k, v in enumerate(vals))
        cards.append(f'<details class="int"{" open" if n == 0 else ""}><summary><span class="rid">{rid}</span><span class="nm">{e(name[i])}</span>'
                     f'<span class="sc num">{e(vals[-1][i])}</span></summary><dl>{dl}</dl>'
                     f'<p class="job"><b>{e(JOB_LABEL[i])}:</b> {e(job[i])}</p></details>')
    out["interviews"] = "".join(cards)
    g = []
    for label, higher, core, steps in GRAPH:
        st = []
        for k, (name, pain) in enumerate(steps, 1):
            p = f'<span class="pn">{e(pain[i])}</span>' if pain else ""
            st.append(f'<li class="st{" pain" if pain else ""}"><span class="sn num">{k}</span><span><b>{e(name[i])}</b>{p}</span></li>')
        g.append(f'<article class="jg"><h3>{e(label[i])}</h3>'
                 f'<div class="lvl hi"><span class="eyebrow">{e(T["g_higher"][i])}</span>{e(higher[i])}</div><span class="arr" aria-hidden="true">↓</span>'
                 f'<div class="lvl core"><span class="eyebrow">{e(T["g_core"][i])}</span>{e(core[i])}</div><span class="arr" aria-hidden="true">↓</span>'
                 f'<ol class="steps">{"".join(st)}</ol></article>')
    out["graph"] = "".join(g)
    out["rows_alt"] = "".join(f"<tr><td>{e(a[i])}</td><td>{w}</td><td>{e(b[i])}</td></tr>" for a, w, b in ALTS)
    out["rows_pain"] = "".join(f'<tr><td>{s}</td><td>{e(p[i])}</td><td>{w}</td><td class="{"bad" if f is HIGH else ""}">{e(f[i])}</td><td>{e(o[i])}</td></tr>'
                               for s, p, w, f, o in PAINS)
    out["rows_change"] = "".join(f'<tr><td class="num">{r}</td><td>{e(q[i])}</td><td>{s}</td><td>{c[i]}</td></tr>' for r, q, s, c in CHANGES)
    rows = []
    for k, (name, a, b, c, m) in enumerate(ICE, 1):
        rows.append(f'<tr><td class="num">{k}</td><td>{e(name[i])}</td><td class="num">{a}</td><td class="num">{b}</td><td class="num">{c}</td>'
                    f'<td class="num{" good" if k <= 2 else ""}">{a * b * c}</td><td>{e(m[i])}</td></tr>')
    out["rows_ice"] = "".join(rows)
    out["rows_seg"] = "".join(f"<tr><td>{e(s[i])}</td><td>{e(j[i])}</td><td>{e(w[i])}</td></tr>" for s, j, w in SEGMENTS)
    return out

# Texts for the FinanceApp retention case (financeapp.src.html -> financeapp-retention.html + en/financeapp-retention.html).
# Each key is used in financeapp.src.html as {{key}}. Value: (Russian, English).
# Table rows are generated below from the brief's figures, so numbers stay consistent in both languages.
# Edit the text here, then run: python3 src/build.py


def _n(x, d=0, lang=0):
    """Number in RU (1 000 / 15,7) or EN (1,000 / 15.7) format."""
    s = f"{x:,.{d}f}"
    return s.replace(",", " ").replace(".", ",") if lang == 0 else s


def _both(f):
    return (f(0), f(1))


# ---------- figures from the brief ----------
COHORTS = [("Q1 2022", 180000, 86400), ("Q2 2022", 210000, 94500), ("Q3 2022", 240000, 100800),
           ("Q4 2022", 270000, 102600), ("Q1 2023", 300000, 105000)]
COUNTRIES = [("A", 8, 4.5, 40), ("B", 12, 6.0, 25), ("C", 15, 7.5, 15), ("D", 18, 9.0, 12), ("E", 25, 13.5, 8)]
FEATURES = [(("Только учёт", "Accounting only"), 60, 25),
            (("Учёт + инвестиции", "Accounting + investing"), 15, 58),
            (("Учёт + кредиты", "Accounting + loans"), 10, 32),
            (("Все три (Ultra)", "All three (Ultra)"), 15, 72)]

RET = [r / n * 100 for _, n, r in COHORTS]
CHURN = 100 - sum(RET) / len(RET)          # 58.4% per 6 months
MULT = 100 / CHURN                          # periods a user lives
REV_TOTAL = sum(a * s for _, _, a, s in COUNTRIES)


def _cohort_rows(lang):
    out = []
    for (q, n, r), ret in zip(COHORTS, RET):
        out.append(f"<tr><td>{q}</td><td class='num'>{_n(n, 0, lang)}</td><td class='num'>{_n(r, 0, lang)}</td>"
                   f"<td class='num'><b>{_n(ret, 0, lang)}%</b></td></tr>")
    return "".join(out)


def _ltv_rows(lang):
    out = []
    for c, cac, arpu, _ in COUNTRIES:
        ltv = arpu * MULT
        out.append(f"<tr><td>{c}</td><td class='num'>${cac}</td><td class='num'>${_n(arpu, 1, lang)}</td>"
                   f"<td class='num'>${_n(ltv, 1, lang)}</td><td class='num bad'>{_n(ltv / cac, 2, lang)}</td>"
                   f"<td class='num good'>{_n(ltv * 6 / cac, 1, lang)}</td></tr>")
    return "".join(out)


def _country_rows(lang):
    out = []
    for c, cac, arpu, share in COUNTRIES:
        rev = arpu * share / REV_TOTAL * 100
        out.append(f"<tr><td>{c}</td><td class='num'>{share}%</td><td class='num'><b>{_n(rev, 0, lang)}%</b></td>"
                   f"<td class='num'>{_n(arpu * MULT / cac, 2, lang)}</td></tr>")
    return "".join(out)


def _feature_rows(lang):
    out = []
    base = FEATURES[0][2]
    for name, share, ret in FEATURES:
        lift = "—" if ret == base else f"+{ret - base} {('п.п.', 'pp')[lang]}"
        x = _n(ret / base, 1, lang) + "×"
        out.append(f"<tr><td>{name[lang]}</td><td class='num'>{share}%</td><td class='num'><b>{ret}%</b></td>"
                   f"<td class='num'>{lift}</td><td class='num'>{x}</td></tr>")
    return "".join(out)


def _data_country_rows(lang):
    return "".join(f"<tr><td>{c}</td><td class='num'>${cac}</td><td class='num'>${_n(a, 1, lang)}</td><td class='num'>{s}%</td></tr>"
                   for c, cac, a, s in COUNTRIES)


def _data_feature_rows(lang):
    price = [("$1 500", "$1,500"), ("+$1 200 ", "+$1,200 "), ("+$1 000 ", "+$1,000 "), ("$3 000", "$3,000")]
    note = ["", ("за инвестиции", "for investing"), ("за кредиты", "for loans"), ""]
    out = []
    for (name, share, ret), p, nt in zip(FEATURES, price, note):
        out.append(f"<tr><td>{name[lang]}</td><td class='num'>{share}%</td><td class='num'>{ret}%</td>"
                   f"<td class='num'>{p[lang].replace(' ', chr(160), 1) if lang == 0 else p[lang]}{nt[lang] if nt else ''}</td></tr>")
    return "".join(out)


T = {
# ---------- meta & nav ----------
"title": ("Retention FinanceApp", "FinanceApp Retention"),
"desc": ("Продуктовый кейс: почему 6-месячное удержание финтех-приложения падает с 48% до 35%, LTV по странам, сегменты и стратегия из трёх фокусов.",
         "Product case: why 6-month retention of a fintech app fell from 48% to 35%, LTV by country, segments and a three-focus strategy."),
"nav_label": ("Разделы", "Sections"),
"nav_back": ("← Все проекты", "← All projects"),
"nav_summary": ("Итог", "Summary"),
"nav_data": ("Данные", "Data"),
"nav_assume": ("Допущения", "Assumptions"),
"nav_cohorts": ("1 · Когорты", "1 · Cohorts"),
"nav_ltv": ("2 · LTV", "2 · LTV"),
"nav_seg": ("3 · Сегменты", "3 · Segments"),
"nav_feat": ("4 · Функции", "4 · Features"),
"nav_strat": ("5 · Стратегия", "5 · Strategy"),
"nav_test": ("Проверка", "Validation"),

# ---------- hero ----------
"eyebrow": ("Продуктовый кейс · Retention и монетизация", "Product case · Retention & monetization"),
"h1": ("Retention <span>FinanceApp</span>", "Retention <span>FinanceApp</span>"),
"lead": ("FinanceApp — финтех-приложение: учёт финансов, инвестиции и кредиты, 1,2 млн активных пользователей в 5 странах. Привлечение растёт каждый квартал, а 6-месячное удержание падает с 48% до 35%. Я нашла главный рычаг — переход пользователя во вторую функцию — и собрала стратегию из трёх фокусов.",
         "FinanceApp is a fintech app for budgeting, investing and loans, with 1.2M active users in 5 countries. Acquisition grows every quarter, while 6-month retention falls from 48% to 35%. I found the main lever — moving users into a second feature — and built a three-focus strategy."),
"note": ("Учебный кейс курса по продукт-менеджменту: данные из условия задачи, не реального продукта",
         "A training case from a product management course: the data come from the brief, not a real product"),
"k1_e": ("Retention 6 мес.", "6-month retention"),
"k1_v": ("48% → 35%", "48% → 35%"),
"k1_d": ("когорты Q1 2022 и Q1 2023", "Q1 2022 vs Q1 2023 cohort"),
"k2_e": ("Удержано из прироста", "Retained from growth"),
"k2_v": ("15,5%", "15.5%"),
"k2_d": ("из 120 тыс. дополнительных новых пользователей за год", "of 120K extra new users year over year"),
"k3_e": ("«Только учёт»", "Accounting only"),
"k3_v": ("60% · 25%", "60% · 25%"),
"k3_d": ("доля базы и её удержание: самый массовый и самый «дырявый» сегмент", "share of the base and its retention: the largest and leakiest segment"),
"k4_e": ("Страны C, D, E", "Countries C, D, E"),
"k4_v": ("≈ 50%", "≈ 50%"),
"k4_d": ("выручки при 35% пользователей", "of revenue from 35% of users"),

# ---------- summary ----------
"con_h": ("Что я нашла", "What I found"),
"con1_t": ("Рост держится на объёме, а не на качестве. ", "Growth runs on volume, not quality. "),
"con1": ("За год новых пользователей стало на 67% больше, удержанных — только на 22%. Каждая новая когорта держится хуже предыдущей.",
         "New users grew 67% in a year, retained users only 22%. Each new cohort retains worse than the one before."),
"con2_t": ("Главный рычаг — вторая функция, а не страна. ", "The main lever is a second feature, not a country. "),
"con2": ("Инвестиции поднимают удержание с 25% до 58%, все три функции — до 72%. Страны по LTV/CAC отличаются всего на ±6%.",
         "Investing lifts retention from 25% to 58%, all three features to 72%. Countries differ by only ±6% on LTV/CAC."),
"con3_t": ("Кредиты зарабатывают, но не удерживают. ", "Loans earn, but don’t retain. "),
"con3": ("32% против 25% у базы: кредит выплачен — повода возвращаться нет.",
         "32% vs 25% for the base: once the loan is repaid, there is no reason to come back."),
"do_h": ("Что я делаю", "What I do"),
"do0_t": ("Не наращиваю привлечение, пока retention падает. ", "No more acquisition spend while retention falls. "),
"do0": ("Иначе мы платим CAC за пользователей, которые уходят.", "Otherwise we pay CAC for users who leave."),
"f1_t": ("«Только учёт» → инвестиции. ", "Accounting only → investing. "),
"f1": ("Перевод 10% базы даёт около +3,3 п.п. общего удержания.", "Moving 10% of the base adds about +3.3 pp of overall retention."),
"f2_t": ("Кредит как мост. ", "Loans as a bridge. "),
"f2": ("Кредит → бюджет на выплату → оффер «откладывай себе» в момент последнего платежа.",
       "Loan → repayment budget → a “now save for yourself” offer at the last payment."),
"f3_t": ("C, D, E → Ultra. ", "C, D, E → Ultra. "),
"f3": ("Половина выручки при самом дорогом CAC: удерживаем этих пользователей в пакете с retention 72%.",
       "Half the revenue at the highest CAC: keep these users in the plan with 72% retention."),

# ---------- data ----------
"data_e": ("Исходные данные", "Input data"),
"data_h": ("Что дано в условии", "What the brief gives"),
"t_cohort": ("Когорта", "Cohort"),
"t_new": ("Новые", "New users"),
"t_active6": ("Активны через 6 мес.", "Active after 6 mo."),
"t_ret": ("Retention", "Retention"),
"t_country": ("Страна", "Country"),
"t_share": ("Доля пользователей", "Share of users"),
"t_set": ("Набор функций", "Feature set"),
"t_share_active": ("Доля активных", "Share of active"),
"t_ret6": ("Retention 6 мес.", "6-mo retention"),
"t_price": ("Подписка", "Subscription"),
"t_ltv": ("LTV по формуле", "LTV, brief formula"),
"t_ratio": ("LTV/CAC", "LTV/CAC"),
"t_ratio6": ("LTV/CAC, ARPU в месяц", "LTV/CAC, monthly ARPU"),
"t_rev": ("Доля выручки", "Share of revenue"),
"t_lift": ("Прирост к базе", "Lift vs base"),
"t_x": ("Во сколько раз", "Multiple"),
"cap_cohort": ("Когорты", "Cohorts"),
"cap_country": ("Страны", "Countries"),
"cap_feat": ("Функции", "Features"),
"rows_data_cohort": _both(lambda l: "".join(f"<tr><td>{q}</td><td class='num'>{_n(n, 0, l)}</td><td class='num'>{_n(r, 0, l)}</td></tr>" for q, n, r in COHORTS)),
"rows_data_country": _both(_data_country_rows),
"rows_data_feat": _both(_data_feature_rows),

# ---------- assumptions ----------
"as_e": ("Прежде чем считать", "Before calculating"),
"as_h": ("Допущения и проверка данных", "Assumptions and data checks"),
"as1_t": ("ARPU — месячный, churn — за 6 месяцев. ", "ARPU is monthly, churn is per 6 months. "),
"as1": ("Поэтому LTV показываю дважды: по формуле задания и с поправкой ×6. Ранжирование стран не меняется, меняется вывод об окупаемости.",
        "So I show LTV twice: with the brief’s formula and adjusted ×6. The country ranking stays the same; the payback conclusion changes."),
"as2_t": ("Цены подписки несопоставимы с ARPU. ", "Subscription prices don’t match ARPU. "),
"as2": ("$1 500–3 000 против ARPU $4,5–13,5 — вероятно, другие единицы или валюта. В расчётах их не использую.",
        "$1,500–3,000 vs ARPU of $4.5–13.5 — likely different units or currency. I leave them out of the calculations."),
"as3_t": ("Retention по функциям — связь, а не причина. ", "Retention by feature is correlation, not cause. "),
"as3": ("Функции могут подключать уже лояльные пользователи. Причину проверяю A/B-тестом.",
        "Loyal users may simply add more features. I test causality with an A/B test."),
"as4_t": ("Retention по странам не дан. ", "Retention by country isn’t given. "),
"as4": ("Выводы о странах опираются на экономику пользователя, а не на удержание. Это ограничение анализа.",
        "Country conclusions rest on unit economics, not retention. This is a limitation of the analysis."),
"as5_t": ("Данные согласованы. ", "The data are consistent. "),
"as5": ("Средневзвешенный retention по функциям — 37,7%, по когортам — 41,6%: порядок совпадает.",
        "Weighted retention by feature is 37.7%, by cohort 41.6%: the same order of magnitude."),

# ---------- 1 cohorts ----------
"c_e": ("Задача 1", "Task 1"),
"c_h": ("6-месячный retention по когортам", "6-month retention by cohort"),
"c_f": ("Retention = активные через 6 мес. ÷ новые пользователи", "Retention = active after 6 months ÷ new users"),
"rows_cohort": _both(_cohort_rows),
"c_i": ("Retention падает каждый квартал на 3–4 п.п. Число удержанных при этом растёт — это vanity metric: она растёт, даже когда продукт работает хуже. Если бы удержание держалось на 48%, за четыре квартала осталось бы примерно на 87 тыс. пользователей больше.",
        "Retention drops 3–4 pp every quarter. The number of retained users still grows — a vanity metric that rises even when the product gets worse. Had retention held at 48%, about 87K more users would have stayed over four quarters."),

# ---------- 2 LTV ----------
"l_e": ("Задача 2", "Task 2"),
"l_h": ("LTV по странам", "LTV by country"),
"l_f": ("Средний churn = 100% − 41,6% = 58,4% за 6 мес. · LTV = ARPU × 1 ÷ 0,584", "Average churn = 100% − 41.6% = 58.4% per 6 months · LTV = ARPU × 1 ÷ 0.584"),
"rows_ltv": _both(_ltv_rows),
"l_i": ("По формуле задания LTV/CAC меньше 1 во всех странах: привлечение убыточно. Но churn 6-месячный, а ARPU, скорее всего, месячный. С поправкой ×6 LTV/CAC = 5,1–5,8, бизнес здоров. Один расчёт даёт противоположные выводы, поэтому допущение — часть ответа. Ранжирование одинаковое: A и E впереди, B, C и D равны.",
        "With the brief’s formula LTV/CAC is below 1 in every country: acquisition loses money. But churn is per 6 months, while ARPU is most likely monthly. Adjusted ×6, LTV/CAC is 5.1–5.8 — a healthy business. The same calculation gives opposite conclusions, so the assumption is part of the answer. The ranking is identical: A and E lead, B, C and D are equal."),

# ---------- 3 segments ----------
"s_e": ("Задача 3", "Task 3"),
"s_h": ("Самые выгодные сегменты", "The most valuable segments"),
"s_f": ("Доля выручки = доля пользователей × ARPU ÷ сумма по всем странам", "Revenue share = user share × ARPU ÷ total across countries"),
"rows_country": _both(_country_rows),
"s1_t": ("По странам. ", "By country. "),
"s1": ("A — объём и лучшая окупаемость. E — самый ценный пользователь: 16% выручки при 8% людей. C, D и E вместе — около половины выручки при трети пользователей.",
       "A brings volume and the best payback. E has the most valuable user: 16% of revenue from 8% of people. C, D and E together bring about half the revenue from a third of users."),
"s2_t": ("По функциям. ", "By feature. "),
"s2": ("Лучший сегмент — все три функции (72%), за ним учёт + инвестиции (58%). Худший — «только учёт», и в нём 60% базы.",
       "The best segment is all three features (72%), then accounting + investing (58%). The worst is accounting only — and it holds 60% of the base."),
"s3_t": ("Вывод. ", "Takeaway. "),
"s3": ("Между странами разница ±6%, между наборами функций — почти втрое. Основной фокус — функции, страны — второстепенный.",
       "Countries differ by ±6%, feature sets by almost 3×. Features are the main focus; countries come second."),

# ---------- 4 features ----------
"fe_e": ("Задача 4", "Task 4"),
"fe_h": ("Влияние нескольких функций на удержание", "How multiple features affect retention"),
"rows_feat": _both(_feature_rows),
"fe1_t": ("Инвестиции — привычка, кредит — разовая потребность. ", "Investing is a habit, a loan is a one-off need. "),
"fe1": ("Портфель проверяют часто, а кредит берут, выплачивают и уходят. Поэтому инвестиции добавляют +33 п.п., кредиты — только +7.",
        "People check a portfolio often; a loan gets taken, repaid and forgotten. So investing adds +33 pp, loans only +7."),
"fe2_t": ("Корреляция ≠ причина. ", "Correlation ≠ causation. "),
"fe2": ("Возможно, это лояльные пользователи сами подключают больше функций. Тогда насильно предложенные инвестиции удержание не поднимут — это нужно проверить до масштабирования.",
        "Loyal users may simply add more features on their own. Then pushing investing on everyone won’t raise retention — this has to be tested before scaling."),

# ---------- 5 strategy ----------
"st_e": ("Задача 5", "Task 5"),
"st_h": ("Стратегия: три фокуса", "Strategy: three focuses"),
"st_lead": ("Принцип: сначала остановить падение retention, потом наращивать привлечение. Все три фокуса — про перевод пользователей в сегменты, которые остаются.",
            "Principle: stop the retention decline first, then grow acquisition. All three focuses move users into segments that stay."),
"why": ("Почему", "Why"),
"how": ("Как", "How"),
"metric": ("Метрика", "Metric"),
"sf1_h": ("«Только учёт» → инвестиции", "Accounting only → investing"),
"sf1_w": ("60% базы с retention 25%. Инвестиции поднимают его до 58%. Перевод 10% базы ≈ +3,3 п.п. общего удержания.",
          "60% of the base at 25% retention. Investing lifts it to 58%. Moving 10% of the base ≈ +3.3 pp overall retention."),
"sf1_h2": ("Кастдев о барьерах (страх, непонимание, мало денег), затем A/B-тест оффера: первая инвестиция с маленькой суммой прямо из бюджета.",
           "Customer interviews on barriers (fear, confusion, small budgets), then an A/B test of the offer: a first small investment straight from the budget."),
"sf1_m": ("Доля пользователей с 2+ функциями; retention 6 мес. группы теста.", "Share of users with 2+ features; 6-month retention of the test group."),
"sf2_h": ("Кредит как мост, а не тупик", "Loans as a bridge, not a dead end"),
"sf2_w": ("Кредиты почти не удерживают (32%), зато приводят людей с сильным намерением. Сейчас момент последнего платежа — точка оттока.",
          "Loans barely retain (32%) but bring users with strong intent. Today the last payment is the churn point."),
"sf2_h2": ("Кредит → бюджет, чтобы спокойно выплатить (снижает и риск просрочек) → в момент последнего платежа оффер: «эту сумму теперь откладывай себе».",
           "Loan → a budget to repay calmly (also cuts delinquency risk) → at the last payment an offer: “now put this amount aside for yourself”."),
"sf2_m": ("Retention через 3 мес. после закрытия кредита; доля перешедших в инвестиции.", "Retention 3 months after loan payoff; share moving into investing."),
"sf3_h": ("C, D, E → Ultra", "C, D, E → Ultra"),
"sf3_w": ("Треть пользователей, половина выручки, самый дорогой CAC: каждый ушедший — большая потеря. Ultra удерживает 72%.",
          "A third of users, half the revenue, the highest CAC: every loss hurts. Ultra retains 72%."),
"sf3_h2": ("Пробный период Ultra для активных пользователей двух функций, локальные сценарии использования, приоритетная поддержка.",
           "An Ultra trial for active two-feature users, local use cases, priority support."),
"sf3_m": ("Доля Ultra и LTV/CAC по странам C, D, E.", "Ultra share and LTV/CAC in C, D and E."),
"not_t": ("Чего не делаю: ", "What I don’t do: "),
"not": ("не перераспределяю бюджет между странами (разница ±6%) и не запускаю новые функции, пока существующие не удерживают.",
        "reshuffle budget between countries (only ±6% difference) or launch new features while the current ones don’t retain."),

# ---------- validation ----------
"v_e": ("Как проверяю", "How I validate"),
"v_h": ("Прежде чем масштабировать", "Before scaling"),
"v1_t": ("Кастдев. ", "Customer interviews. "),
"v1": ("Не «нравятся ли инвестиции», а «что мешает начать». От ответа зависит оффер.", "Not “do you like investing” but “what stops you from starting”. The answer shapes the offer."),
"v2_t": ("A/B-тест. ", "A/B test. "),
"v2": ("Случайно делим пользователей «только учёта» с похожим стажем: одной группе — оффер инвестиций, другой — нет. Случайность убирает эффект «лояльные сами подключают».",
       "Randomly split accounting-only users with similar tenure: one group gets the investing offer, the other doesn’t. Randomization removes the “loyal users add features anyway” effect."),
"v3_t": ("Ранняя метрика. ", "Early metric. "),
"v3": ("Ждать 6 месяцев долго: смотрю активность на 30-й день, заранее проверив на старых данных её связь с 6-месячным retention.",
       "Six months is too long to wait: I track day-30 activity, first checking on past data that it predicts 6-month retention."),
"v4_t": ("Guardrails. ", "Guardrails. "),
"v4": ("Просрочки по кредитам, отписки от уведомлений, обращения в поддержку.", "Loan delinquencies, notification opt-outs, support tickets."),

"foot": ("Retention FinanceApp · учебный продуктовый кейс · 2026", "FinanceApp Retention · training product case · 2026"),
}

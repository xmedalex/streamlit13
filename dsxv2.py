import io

import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

from text_msg import InputTextRus


ftes_salary_conditions = {
    'MedRep': {
        'salary': 100000,
        'tax_index': 0,
        'fullname': 'Medical Representative',
        'fullname_rus': 'Медицинский представитель',
        'shortname': 'mr',
        'bonus_quarter': 20,
        'bonus_year': 30,
        'compensation': 25000,
    },
    'ProdMan': {
        'salary': 150000,
        'tax_index': 0,
        'fullname': 'Product Manager',
        'fullname_rus': 'Продакт Менеджер',
        'shortname': 'pm',
        'bonus_quarter': 15,
        'bonus_year': 20,
        'compensation': 15000,
    },
    'ComDir': {
        'salary': 200000,
        'tax_index': 1,
        'fullname': 'Commercial Director',
        'fullname_rus': 'Коммерческий директор',
        'shortname': 'cd',
        'bonus_quarter': 1,
        'bonus_year': 1,
        'compensation': 10000,
    },
}

tax_condition = {
    'ФизЛицо': 15,
    'ЮрЛицо': 0,
}

months_num = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
month_name = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

tm = InputTextRus()

st.set_page_config(layout="wide")

# контейнер с блоком ввода переменных
container_with_input = st.container()
drug_section, fte_section, customer_section = container_with_input.columns([1, 2, 2])

# drug section
with drug_section:
    st.header('Упаковка')

    pharmacy_price = 5000
    if 'pack_price_pharmacy' in st.session_state:
        pharmacy_price = (1 + st.session_state.pack_price_pharmacy_change / 100) * pharmacy_price
    st.number_input(label=tm.pack_price_pharmacy_label,
                    value=int(pharmacy_price),
                    min_value=1, step=100, format='%d',
                    help=tm.pack_price_pharmacy_help,
                    key='pack_price_pharmacy')

    own_to_pharm_price = 3750
    if 'pack_price_owner' in st.session_state:
        own_to_pharm_price = (1 + st.session_state.pack_price_pharmacy_change / 100) * own_to_pharm_price
    st.number_input(label=tm.pack_price_owner_label,
                    value=int(own_to_pharm_price),
                    min_value=1, step=100, format='%d',
                    help=tm.pack_price_owner_help,
                    key='pack_price_owner')

    man_to_own_price = 1500
    st.number_input(label=tm.pack_price_manufacturer_label,
                    value=man_to_own_price,
                    min_value=1, step=100, format='%d',
                    help=tm.pack_price_manufacturer_help,
                    key='pack_price_manufacturer')

    st.slider(label=tm.pack_price_change_label,
              value=0,
              min_value=-30, max_value=30, step=5, format='%d%%',
              help=tm.pack_price_change_help,
              key='pack_price_pharmacy_change')

# FTE section
with fte_section:
    def create_fte_card(fte_data: dict):
        with st.expander(fte_data['fullname_rus']):
            with st.container():
                col_salary, col_compensation = st.columns(2)
                with col_salary:
                    st.number_input(label=tm.salary_label,
                                    value=fte_data['salary'], format='%d',
                                    min_value=1, step=5000,
                                    help=tm.salary_help,
                                    key=f"{fte_data['shortname']}_salary_gross")
                with col_compensation:
                    st.number_input(label=tm.compensation_label,
                                    value=fte_data['compensation'], format='%d',
                                    min_value=1, step=1000,
                                    help=tm.compensation_help,
                                    key=f"{fte_data['shortname']}_compensation")
            with st.container():
                quarter_bonus_col, year_bonus_col, taxation_type_col = st.columns(3)
                with quarter_bonus_col:
                    st.number_input(label=tm.quarter_bonus_label,
                                    value=fte_data['bonus_quarter'], format='%d',
                                    min_value=1, step=5,
                                    help=tm.quarter_bonus_help,
                                    key=f"{fte_data['shortname']}_quarter_bonus")
                with year_bonus_col:
                    st.number_input(label=tm.year_bonus_label,
                                    value=fte_data['bonus_year'], format='%d',
                                    min_value=1, step=5,
                                    help=tm.year_bonus_help,
                                    key=f"{fte_data['shortname']}_year_bonus")
                with taxation_type_col:
                    st.selectbox(label=tm.tax_type_label,
                                 options=(i for i in tax_condition),
                                 index=fte_data['tax_index'],
                                 key=f"{fte_data['shortname']}_tax_type",
                                 help=tm.tax_type_help)


    st.header('FTE')
    with st.expander(label='Выберите ставки', expanded=False):
        options = (i for i in ftes_salary_conditions)
        ftes = st.multiselect(label='Выбрано',
                              options=(i for i in ftes_salary_conditions),
                              default=(i for i in ftes_salary_conditions if i != 'ProdMan'),
                              key='chosen_fte')
    for num, i in enumerate(st.session_state.chosen_fte):
        create_fte_card(ftes_salary_conditions[i])
    with st.container():
        col_a, col_b, col_c = st.columns([1, 10, 1])
        with col_b:
            st.slider("Кол-во медицинских представителей", 1, 9, 1, 1,
                      key='medreps_number',
                      help='Выберите количество медицинских представителей в штате')

# customer section
with customer_section:
    columns = ['districts', 'accounts_number']
    districts_data = [
        ['ВАО', 14],
        ['ЗАО', 14],
        ['САО', 11],
        ['СВАО', 14],
        ['СЗАО', 6],
        ['ЦАО', 10],
        ['ЮВАО', 24],
        ['ЮЗАО', 16],
        ['ЮАО', 20]
    ]


    @st.cache_data
    def load_districts_data() -> pd.DataFrame:
        return pd.DataFrame(districts_data, columns=columns)


    districts = load_districts_data()

    st.header('B2B-клиенты')
    with st.expander('**Округи Москвы:**'):
        st.multiselect(label=f'**Выберите:**',
                       options=districts['districts'].tolist(),
                       default=districts['districts'].tolist(),
                       key='selected_districts')

        col1, col2, col3 = st.columns([1, 8, 1])
        with col2:
            counts_sum = districts.loc[
                districts['districts'].isin(st.session_state.selected_districts), 'accounts_number'].sum()
            st.slider("Активных учреждений в промоции", 1, int(counts_sum), int((counts_sum * 0.1)),
                      key='active_accounts_number',
                      help='Выберите из общего количества учреждений те, которые будут находиться в активной работе')

            accounts_number = st.session_state.active_accounts_number
            accounts_fte = accounts_number / st.session_state.medreps_number
            physicians_fte = accounts_fte * 6
    with st.expander('**OPEX на одно учреждение**'):
        with st.container():
            col_initiation, col_support = st.columns([1, 1])
            with col_initiation:
                st.number_input(label='Инициация', min_value=1, value=150000, step=10000,
                                key='initial_event',
                                help='ОПЕКС начального мероприятия, руб. с НДС. В первом квартале, один раз')
            with col_support:
                st.number_input(label='Поддержание', min_value=1, value=30000, step=1000,
                                key='supporting_OPEX',
                                help='OPEX поддерживающих активностей, руб. с НДС. Каждый квартал Q2-Q4, 3 в год')
    with st.expander('**Комиссия агентства**'):
        with st.container():
            col1, col2, col3 = st.columns([1, 8, 1])
            with col2:
                st.slider(label='Комиссия, %', min_value=1, max_value=30, value=10, step=1,
                          format='%d%%', key='agency_fee')
    # sliders with pack per account and pack growth
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.slider(label="Упак. в нед. в одном ЛПУ",
                      min_value=1, value=4, step=1, max_value=24,
                      key='patients_per_one_account_per_week',
                      help='В одном ЛПУ 8 врачей в две смены (4 по 2), часть из них работает в обе смены.'
                           'Среднее количество врачей для расчета - 6.')
        with col2:
            st.slider("Прирост упак. (мес-к-мес)", min_value=0, value=20, max_value=50,
                      key='pack_growth',
                      help='Расчетный прирост продаж со второго квартала, каждый последующий месяц',
                      format='%d%%')
    # calculation of packs per month
    packs_per_month = st.session_state.active_accounts_number * st.session_state.patients_per_one_account_per_week * 4
    packs_jan_to_apr = [int(packs_per_month / 4), int(packs_per_month / 2),
                        int(packs_per_month / 4 * 3), int(packs_per_month)]
    packs_apr_to_dec = [
        int(packs_per_month * (1 + st.session_state.pack_growth / 100) ** i) for i in range(4, 12)
    ]
    packs = packs_jan_to_apr + packs_apr_to_dec

    with st.container():
        packs_sum = sum(packs)
        sum_a = f"{packs_sum:,}".replace(',', ' ')
        st.write(f"Всего упаковок за год: {sum_a}")

# calculation of packs per month
packs_per_month = st.session_state.active_accounts_number * st.session_state.patients_per_one_account_per_week * 4
packs_jan_to_apr = [int(packs_per_month / 4), int(packs_per_month / 2),
                    int(packs_per_month / 4 * 3), int(packs_per_month)]
packs_apr_to_dec = [
    int(packs_per_month * (1 + st.session_state.pack_growth / 100) ** i) for i in range(4, 12)
]
packs = packs_jan_to_apr + packs_apr_to_dec

# make dictionary with FTE salary, bonuses and compensations
ftes_salary_final = {}
for fte_role in st.session_state.chosen_fte:
    fte_shortname = ftes_salary_conditions[fte_role]['shortname']
    fte_salary_monthly = st.session_state.get(f"{fte_shortname}_salary_gross")
    fte_tax_type = st.session_state.get(f"{fte_shortname}_tax_type")
    fte_tax = tax_condition.get(fte_tax_type)

    ftes = 1 if fte_shortname != 'mr' else st.session_state.medreps_number
    ftes_salary_final[fte_role] = {}

    # salary calculation
    salary = [fte_salary_monthly / (1 - fte_tax / 100) for i in range(12)]
    if fte_shortname == 'mr':
        salary = [i * ftes for i in salary]
    ftes_salary_final[fte_role]['salary'] = salary

    # compensation calculation
    compensation_monthly = st.session_state.get(f"{fte_shortname}_compensation") / (1 - fte_tax / 100)
    compensation = [compensation_monthly * ftes for i in range(12)]
    ftes_salary_final[fte_role]['compensation'] = compensation

    # quarter bonus calculation
    quarter_bonus = st.session_state.get(f"{fte_shortname}_quarter_bonus")
    bonus_quarter = fte_salary_monthly * 3 * (quarter_bonus / 100) / (1 - fte_tax / 100)
    bonus_quarter_total = []
    for i in range(12):
        if i == 2 or i == 5 or i == 8 or i == 11:
            bonus_quarter_total.append(bonus_quarter * ftes)
        else:
            bonus_quarter_total.append(0)
    ftes_salary_final[fte_role]['bonus_quarter'] = bonus_quarter_total

    # year bonus calculation
    year_bonus = st.session_state.get(f"{fte_shortname}_year_bonus")
    bonus_year = fte_salary_monthly * 12 * (year_bonus / 100) / (1 - fte_tax / 100)
    bonus_year_total = []
    for i in range(12):
        if i == 11:
            bonus_year_total.append(bonus_year * ftes)
        else:
            bonus_year_total.append(0)
    ftes_salary_final[fte_role]['bonus_year'] = bonus_year_total

salary_arr = np.array([0.0])
compensation_arr = np.array([0] * 12)
bonus_quarter_arr = np.array([0] * 12)
bonus_year_arr = np.array([0] * 12)

for i in ftes_salary_final:
    salary_arr = salary_arr + np.array(ftes_salary_final[i]['salary'])
    compensation_arr = compensation_arr + np.array(ftes_salary_final[i]['compensation'])
    bonus_quarter_arr = bonus_quarter_arr + np.array(ftes_salary_final[i]['bonus_quarter'])
    bonus_year_arr = bonus_year_arr + np.array(ftes_salary_final[i]['bonus_year'])

# calculation of drug cost
price_cor_coef = (1 + st.session_state.pack_price_pharmacy_change / 100)

revenue_without_VAT_list = [i * st.session_state.pack_price_owner * price_cor_coef for i in packs]
cogs_without_VAT_list = [i * st.session_state.pack_price_manufacturer for i in packs]

# Customers OPEX
agency_fee_list = [st.session_state.pack_price_pharmacy * price_cor_coef * i * st.session_state.agency_fee / 100 for i
                   in packs]

initial_event_total = st.session_state.initial_event * st.session_state.active_accounts_number
initial_per_month = initial_event_total / 3
initial_event_OPEX_list = [int(initial_per_month) for i in range(3)] + [0 for i in range(3, 12)]

supporting_OPEX_total = st.session_state.supporting_OPEX * st.session_state.active_accounts_number
supporting_OPEX_monthly = supporting_OPEX_total / 9
supporting_OPEX_list = [0 for i in range(3)] + [int(supporting_OPEX_monthly) for i in range(3, 12)]


def transform_list(a: list, reverse_sign: bool = True, kilo_view: bool = True) -> list:
    divider = 1000 if kilo_view else 1
    return [-int(i / divider) for i in a] if reverse_sign else [int(i / divider) for i in a]


df = pd.DataFrame({'date': pd.date_range(start='1/1/2024', freq='M', periods=12),
                   'packs': transform_list(packs, reverse_sign=False, kilo_view=False),
                   'revenue': transform_list(revenue_without_VAT_list, reverse_sign=False),
                   'COGS': transform_list(cogs_without_VAT_list),
                   'salary': transform_list(salary_arr),
                   'compensation': transform_list(compensation_arr),
                   'bonus_quarter': transform_list(bonus_quarter_arr),
                   'bonus_year': transform_list(bonus_year_arr),
                   'agency_fee': transform_list(agency_fee_list),
                   'initial_event': transform_list(initial_event_OPEX_list),
                   'supporting_opex': transform_list(supporting_OPEX_list)}
                  )

df['date'] = df['date'].dt.date
df['expenses'] = df['COGS'] + df['salary'] + df['compensation'] + df['bonus_quarter'] \
                 + df['bonus_year'] + df['initial_event'] + df['agency_fee'] + df['supporting_opex']
df['profit'] = df['revenue'] + df['expenses']
df['rolling_profit'] = df['profit'].cumsum()

packs_sum = df['packs'].sum()
revenue_sum = df['revenue'].sum()
COGS_sum = df['COGS'].sum()
salary_sum = df['salary'].sum()
compensation_sum = df['compensation'].sum()
bonus_quarter_sum = df['bonus_quarter'].sum()
bonus_year_sum = df['bonus_year'].sum()
agency_fee_sum = df['agency_fee'].sum()
initial_event_sum = df['initial_event'].sum()
supporting_opex_sum = df['supporting_opex'].sum()
profit_sum = df['profit'].sum()

st.write('---')
with st.container():
    col1, col2 = st.columns([2, 1])
    with col1:
        fig = go.Figure(go.Waterfall(
            name="20", orientation="v",
            measure=["absolute",
                     "relative", "relative", "relative", "relative",
                     "relative", "relative", "relative", "relative",
                     "total",
                     ],
            x=['revenue',
               'COGS', 'salary', 'compensation', 'bonus_quarter', 'bonus_year',
               'agency_fee', 'initial_event', 'supporting_opex', 'profit'],
            textposition="outside",
            text=[revenue_sum, COGS_sum, salary_sum, compensation_sum, bonus_quarter_sum, bonus_year_sum,
                  agency_fee_sum, initial_event_sum, supporting_opex_sum, profit_sum],
            y=[revenue_sum, COGS_sum, salary_sum, compensation_sum, bonus_quarter_sum, bonus_year_sum,
               agency_fee_sum, initial_event_sum, supporting_opex_sum, profit_sum],
            # decreasing={"marker": {"color": "Maroon"}},
            # increasing={"marker": {"color": "Teal"}},
            # totals = {"marker":{"color":"red"}} if profit_sum < 0 else {"marker":{"color":"green"}},
            connector={"line": {"color": "rgb(63, 63, 63)"}},
        ))

        title_dir = "Общая прибыль" if profit_sum > 0 else "Общий убыток"
        sum_a = f"{profit_sum:,}".replace(',', ' ')
        title = f"{title_dir}:   {sum_a} тыс. руб"
        st.subheader(title)
        min_b = -10000 if profit_sum > 0 else profit_sum * 1.8
        max_b = revenue_sum * 1.2
        fig.update_layout(
            title="Profit and loss statement 2024",
            yaxis_range=[min_b, max_b],
            showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        profit_list = df['profit'].tolist()
        st.subheader("Выручка/прибыль по месяцам")
        x = month_name

        fig = go.Figure(go.Bar(x=x, y=profit_list, name='Profit'))
        fig.add_trace(go.Bar(x=x, y=transform_list(revenue_without_VAT_list, reverse_sign=False), name='Revenue'))

        markers, line = fig.data
        fig.data = line, markers

        min_a = min(profit_list) * 1, 5
        max_a = max(revenue_without_VAT_list) * 1, 5

        # fig.update_layout(barmode='stack')
        fig.update_layout(
            title="тыс. руб. без НДС",
            yaxis_range=[min_a, max_a],
            showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

st.write('---')
st.header('Исходные данные. Суммы указаны в тыс. рублей')

# df.loc['Column_Total']= df.sum(numeric_only=True, axis=0)


df.loc[df.shape[0]] = [np.nan for col_num in range(1,df.shape[1]+1)]
df.iloc[df.shape[0]-1,[1,2,3,4,5,6,7,8,9,10,11,12]] = df.iloc[:,[1,2,3,4,5,6,7,8,9,10,11,12]].sum(axis=0)
# df.at[12, 'rolling_profit'] = profit_sum

st.write(df)

buffer = io.BytesIO()

with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    # Write each dataframe to a different worksheet.
    df.to_excel(writer, sheet_name='Sheet1')

    # Close the Pandas Excel writer and output the Excel file to the buffer
    writer.close()

    st.download_button(
        label="Download Excel worksheets",
        data=buffer,
        file_name="Model.xlsx",
        mime="application/vnd.ms-excel"
    )

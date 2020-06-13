import pandas as pd
from math import isnan

def create_subdf(df, begin, end):
    subdf = df.iloc[begin, end]
    new_header = subdf.iloc[0]
    subdf = subdf[1:]
    subdf.columns = new_header
    subdf.reset_index()
    return subdf

def goToNextNan(df, i):
    val = df.iloc[i, 1]
    while type(val) == str or isnan(val) == False:
        i += 1
        val = df.iloc[i, 1]
    return i

def create_df(folder, file):
    # summary sheet
    df_summary = pd.read_excel('%s/%s' % (folder, file))
    current_day = df_summary.iloc[0, 0].split()[0]

    # sales summary
    ss_df1 = create_subdf(df_summary, slice(2,4), slice(1, 8))
    ss_df2 = create_subdf(df_summary, slice(5,7), slice(1, 5))

    # Payment summary
    p_df1 = create_subdf(df_summary, slice(9, 14), slice(1, 8)) # payment types

    start_idx, cur_idx = 16, 16
    cur_idx = goToNextNan(df_summary, cur_idx)
    p_df2 = df_summary.iloc[start_idx: cur_idx, 1:8] # credit types ***

    # Sales categories
    cur_idx += 3
    start_idx, cur_idx = cur_idx, cur_idx + 6
    s_df = create_subdf(df_summary, slice(start_idx, cur_idx), slice(1, 8))

    # Revenue Centers
    cur_idx += 1
    start_idx, cur_idx = cur_idx, cur_idx + 4
    r_df = create_subdf(df_summary, slice(start_idx, cur_idx), slice(1, 8))

    # Dining Options ***
    cur_idx += 1
    start_idx = cur_idx
    cur_idx = goToNextNan(df_summary, cur_idx)
    d_df = create_subdf(df_summary, slice(start_idx, cur_idx), slice(1, 4))

    # Taxes ***
    cur_idx += 2
    start_idx = cur_idx
    cur_idx = goToNextNan(df_summary, cur_idx)
    t_df = create_subdf(df_summary, slice(start_idx, cur_idx), slice(1,5))

    # Service Charges ***
    cur_idx += 1
    start_idx = cur_idx
    cur_idx = goToNextNan(df_summary, cur_idx)
    sc_df = create_subdf(df_summary, slice(start_idx, cur_idx), slice(1,4))

    # Menu Item Discounts ***
    cur_idx += 2
    start_idx = cur_idx
    cur_idx = goToNextNan(df_summary, cur_idx)
    m_df = create_subdf(df_summary, slice(start_idx, cur_idx), slice(1, 4))

    # Check Discounts ***
    cur_idx += 2
    start_idx = cur_idx
    cur_idx = goToNextNan(df_summary, cur_idx)
    cd_df = create_subdf(df_summary, slice(start_idx, cur_idx), slice(1, 4))

    # Sales by Service
    cur_idx += 2
    start_idx, cur_idx = cur_idx, cur_idx + 4
    sbs_df = create_subdf(df_summary, slice(start_idx, cur_idx), slice(1, 4))

    # Voids
    cur_idx += 2
    start_idx, cur_idx = cur_idx, cur_idx + 2
    v_df = create_subdf(df_summary, slice(start_idx, cur_idx), slice(1, 5))

    # Cash Summary
    cur_idx += 3
    total_cash_payments = df_summary.iloc[cur_idx, 3]
    cash_adjustments = df_summary.iloc[cur_idx + 1, 3]
    cash_before_tipouts = df_summary.iloc[cur_idx + 2, 3]
    cash_gratuity = df_summary.iloc[cur_idx + 3, 3]
    credit_non_cash_gratuity = df_summary.iloc[cur_idx + 4, 3]
    credit_non_cash_tips = df_summary.iloc[cur_idx + 5, 3]
    total_cash = df_summary.iloc[cur_idx + 6, 3]

    #hourly sheet
    df_hourly = pd.read_excel('%s/%s' % (folder, file), sheet_name = 'Hourly Breakdown')

    return (current_day, ss_df1, ss_df2, p_df1,p_df2, s_df, r_df,d_df, t_df, sc_df, m_df, cd_df, sbs_df, v_df,
            total_cash_payments, cash_adjustments,cash_before_tipouts,cash_gratuity, credit_non_cash_gratuity,
            credit_non_cash_tips,total_cash, df_hourly)
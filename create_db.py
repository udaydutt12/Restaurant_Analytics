import pymongo
from settings import DB_USERNAME, DB_PASSWORD, DB_ROOT
from process_data import create_df
from os import listdir
from math import isnan

def addSalesSummary(ss_df1, ss_df2, document):
    document['SalesSummary'] = {
        'NetSales': ss_df1.iloc[0, 0],
        'Tax': ss_df1.iloc[0, 1],
        'Gratuity': ss_df1.iloc[0, 2],
        'Tips': ss_df1.iloc[0, 2],
        'Refunds': ss_df1.iloc[0, 3],
        'Deferred': ss_df1.iloc[0, 4],
        'Total': ss_df1.iloc[0, 5],
        'GuestCount': ss_df2.iloc[0, 0],
        'OrderCount': ss_df2.iloc[0, 1],
        'Discounts': ss_df2.iloc[0, 2],
        'TipsWithheld': ss_df2.iloc[0, 3]
    }

def addPaymentSummary(p_df1, p_df2, document):
    payment_type = {}
    for i in range(len(p_df1)):
        current_type = p_df1.iloc[i, 0]
        payment_type[current_type] = {
            'Count': 0 if isnan(p_df1.iloc[i, 1]) else p_df1.iloc[i, 1],
            'Amount': 0 if isnan(p_df1.iloc[i, 2]) else p_df1.iloc[i, 2],
            'Tips': 0 if isnan(p_df1.iloc[i, 3]) else p_df1.iloc[i, 3],
            'TipGratPercent': 0 if isnan(p_df1.iloc[i, 4]) else p_df1.iloc[i, 4],
            'Total': 0 if isnan(p_df1.iloc[i, 5]) else p_df1.iloc[i, 5]
        }
    if not len(p_df2):
        document['PaymentSummary'] = {
            'PaymentType': payment_type
        }
        return
    credit_type = {}
    for i in range(len(p_df2)):
        current_type = p_df2.iloc[i, 0]
        credit_type[current_type] = {
            'Count': 0 if isnan(p_df2.iloc[i, 1]) else p_df2.iloc[i, 1],
            'Amount': 0 if isnan(p_df2.iloc[i, 2]) else p_df2.iloc[i, 2],
            'Tips': 0 if isnan(p_df2.iloc[i, 3]) else p_df2.iloc[i, 3],
            'TipGratPercent': 0 if isnan(p_df2.iloc[i, 4]) else p_df2.iloc[i, 4],
            'Total': 0 if isnan(p_df2.iloc[i, 5]) else p_df2.iloc[i, 5]
        }      
    document['PaymentSummary'] = {
        'PaymentType': payment_type,
        'CreditType': credit_type
    }

def addSalesCategories(s_df, document):
    document['SalesCategories'] = {}
    sales_categories = document['SalesCategories']
    for i in range(len(s_df) - 1):
        if i == 3:
            continue
        sales_categories[s_df.iloc[i, 0]] = {
            'OrderCount': 0 if isnan(s_df.iloc[i, 1]) else s_df.iloc[i, 1],
            'ItemCount': 0 if isnan(s_df.iloc[i, 2]) else s_df.iloc[i, 2],
            'GrossAmt': 0 if isnan(s_df.iloc[i, 3]) else s_df.iloc[i, 3],
            'Discounts': 0 if isnan(s_df.iloc[i, 4]) else s_df.iloc[i, 4]
        }

    sales_categories['None'] = {
            'OrderCount': 0 if isnan(s_df.iloc[3, 1]) else s_df.iloc[3, 1],
            'ItemCount': 0 if isnan(s_df.iloc[3, 2]) else s_df.iloc[3, 2],
            'GrossAmt': 0 if isnan(s_df.iloc[3, 3]) else s_df.iloc[3, 3],
            'Discounts': 0 if isnan(s_df.iloc[3, 4]) else s_df.iloc[3, 4]
    }

def addRevenueCenter(r_df, document):
    document['RevenueCenter'] = {
        'Patio': {
            'OrderCount': 0 if isnan(r_df.iloc[0, 1]) else r_df.iloc[0,1],
            'ItemCount': 0 if isnan(r_df.iloc[0, 2]) else r_df.iloc[0,2],
            'GrossAmt': 0 if isnan(r_df.iloc[0,3]) else r_df.iloc[0,3],
            'Discounts': 0 if isnan(r_df.iloc[0,4]) else r_df.iloc[0,4],
            'Net': 0 if isnan(r_df.iloc[0,5]) else r_df.iloc[0,5],
            'Tax': 0 if isnan(r_df.iloc[0,6]) else r_df.iloc[0,6]
        },
        'MainDiningRoom': {
            'OrderCount': 0 if isnan(r_df.iloc[1, 1]) else r_df.iloc[1,1],
            'ItemCount': 0 if isnan(r_df.iloc[1, 2]) else r_df.iloc[1,2],
            'GrossAmt': 0 if isnan(r_df.iloc[1,3]) else r_df.iloc[1,3],
            'Discounts': 0 if isnan(r_df.iloc[1,4]) else r_df.iloc[1,4],
            'Net': 0 if isnan(r_df.iloc[1,5]) else r_df.iloc[1,5],
            'Tax': 0 if isnan(r_df.iloc[1,6]) else r_df.iloc[1,6]
        },
        'NoRevenueCenter': {
            'OrderCount': 0 if isnan(r_df.iloc[2, 1]) else r_df.iloc[2,1],
            'ItemCount': 0 if isnan(r_df.iloc[2, 2]) else r_df.iloc[2,2],
            'GrossAmt': 0 if isnan(r_df.iloc[2,3]) else r_df.iloc[2,3],
            'Discounts': 0 if isnan(r_df.iloc[2,4]) else r_df.iloc[2,4],
            'Net': 0 if isnan(r_df.iloc[2,5]) else r_df.iloc[2,5],
            'Tax': 0 if isnan(r_df.iloc[2,6]) else r_df.iloc[2,6]
        }
    }


def addDiningOptions(d_df, document):
    if not len(d_df):
        return
    dining_options = {}
    for i in range(len(d_df)):
        option = ''.join(d_df.iloc[i, 0].split())
        dining_options[option] = {
            'OrderCount': 0 if isnan(d_df.iloc[i, 1]) else d_df.iloc[i, 1],
            'NetSales': 0 if isnan(d_df.iloc[i, 2]) else d_df.iloc[i, 2]
        }
    document['DiningOptions'] = dining_options

def addTaxes(t_df, document):
    if not len(t_df):
        return
    taxes = {}
    for i in range(len(t_df)):
        tax_type = ''.join(t_df.iloc[i, 0].split())
        taxes[tax_type] = {
            'OrderCount': 0 if isnan(t_df.iloc[i, 1]) else t_df.iloc[i, 1],
            'TaxAmount': 0 if isnan(t_df.iloc[i, 2]) else t_df.iloc[i, 2],
            'NetSales': 0 if isnan(t_df.iloc[i, 3]) else t_df.iloc[i, 3]
        }
    document['Taxes'] = taxes

def addServiceCharges(sc_df, document):
    if not len(sc_df):
        return
    service_charges = {}
    for i in range(len(sc_df)):
        service_type = ''.join(sc_df.iloc[i, 0].split())
        service_charges[service_type] = {
            'Count': 0 if isnan(sc_df.iloc[i, 1]) else sc_df.iloc[i, 1],
            'Amount': 0 if isnan(sc_df.iloc[i, 2]) else sc_df.iloc[i, 2]
        }
    document['ServiceCharges'] = service_charges

def addMenuItemDiscount(m_df, document):
    if not len(m_df): 
        return
    menu_item_discount = {}
    for i in range(len(m_df)):
        current_discount = ''.join(m_df.iloc[i, 0].split())
        menu_item_discount[current_discount] = {
            'Count': 0 if isnan(m_df.iloc[i, 1]) else m_df.iloc[i, 1],
            'Amount': 0 if isnan(m_df.iloc[i, 2]) else m_df.iloc[i, 2]
        }
    document['MenuItemDiscount'] = menu_item_discount

def addCheckDiscounts(cd_df, document):
    if not len(cd_df):
        return
    check_discounts = {}
    for i in range(len(cd_df)):
        key = ''.join(cd_df.iloc[i, 0].split())
        check_discounts[key] = {
            'Count': 0 if isnan(cd_df.iloc[i, 1]) else cd_df.iloc[i, 1],
            'Amount': 0 if isnan(cd_df.iloc[i, 2]) else cd_df.iloc[i, 2]
        }
    document['CheckDiscounts'] = check_discounts

def addSalesByService(sbs_df, document):
    document['SalesByService'] = {
        'Lunch': {
            'Orders': sbs_df.iloc[0, 1],
            'NetSales': sbs_df.iloc[0, 2]
        },
        'Dinner': {
            'Orders': sbs_df.iloc[1, 1],
            'NetSales': sbs_df.iloc[1, 2]
        },
        'NoService': {
            'Orders': sbs_df.iloc[2, 1],
            'NetSales': sbs_df.iloc[2, 2]
        }
    }

def addVoids(v_df, document):
    document['Voids'] = {
        'Amount': v_df.iloc[0,0],
        'OrderCount': v_df.iloc[0,1],
        'ItemCount': v_df.iloc[0,2],
        'Percent': v_df.iloc[0,3] 
    }

def addHourly(df_hourly, document):
    hourly = {}
    for i in range(len(df_hourly)):
        hourly[str(df_hourly.iloc[i, 0])] = {
            'NetSales': df_hourly.iloc[i, 1],
            'OrderCount': df_hourly.iloc[i, 2].item(),
            'GuestCount': df_hourly.iloc[i, 3].item()
        }
    document['HourlyBreakdown'] = hourly

def verifyDocument(document):
    for key in document:
        print(key, type(document[key]))
        if type(document[key]) == dict:
            verifyDocument(document[key])

if __name__ == '__main__':
    client = pymongo.MongoClient(
                'mongodb+srv://%s:%s@restaurant-data-xxxqf.mongodb.net/%s?retryWrites=true&w=majority' %
                (DB_USERNAME, DB_PASSWORD, DB_ROOT)
            )
    db = client.restaurant_data
    folder_names = ['Del_Mar', 'McPherson', 'Loop_20', 'Saunders']
    i = 0
    for folder in folder_names:
        for file in listdir(folder):
            (current_day, ss_df1, ss_df2, p_df1,p_df2, s_df, r_df,d_df, t_df, sc_df, m_df, cd_df, sbs_df, v_df,
            total_cash_payments, cash_adjustments,cash_before_tipouts,cash_gratuity, credit_non_cash_gratuity,
            credit_non_cash_tips,total_cash, df_hourly) = create_df(folder, file) 
            month, day, year = tuple(current_day.split('/'))
            if len(month) == 1:
                month = '0' + month
            if len(day) == 1:
                day = '0' + day
            year = '20' + year
            current_collection = db.get_collection(year)
            current_id = month + day + year + folder[0]
            document = {'_id': current_id}
            addSalesSummary(ss_df1, ss_df2, document)
            addPaymentSummary(p_df1, p_df2, document)
            addSalesCategories(s_df, document)
            addRevenueCenter(r_df, document)
            addDiningOptions(d_df, document)
            addTaxes(t_df, document)
            addServiceCharges(sc_df, document)
            addMenuItemDiscount(m_df, document)
            addCheckDiscounts(cd_df, document)
            addSalesByService(sbs_df, document)
            addVoids(v_df, document)
            document['CashSummary'] = {
                'TotalCashPayments': total_cash_payments,
                'CashAdjustments': cash_adjustments,
                'CashBeforeTipouts': cash_before_tipouts,
                'CashGratuity': cash_gratuity,
                'CreditNonCashGratuity': credit_non_cash_gratuity,
                'CreditNonCashTips': credit_non_cash_tips,
                'TotalCash': total_cash
            }
            addHourly(df_hourly, document)
            current_collection.insert_one(document)
            i += 1
            if i == 100:
                break
        break
 
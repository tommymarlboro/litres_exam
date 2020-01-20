import sys
import re
import os
import csv
from datetime import datetime

# hardcode file name
filename = '\Orders.csv'

# path to csv file
path_to_file = sys.stdin.read() #(!)this is path without file name
if re.findall('\n', path_to_file):
    path_to_file = re.sub('\n', '', path_to_file)



def file_cheker(path):
    '''
    Check exist file. Return True if file exist, else - False
    '''
    check = os.path.exists(path)
    return check



def csv_to_data(path):

    data = {}
    n = 0
    try:
        with open(path, newline='') as f:
            rowrider = csv.reader(f, delimiter=';', quotechar='|')
            for row in rowrider:
                try:
                    data[n] = {
                        'Row ID' : row[0],
                        'Order ID' : row[1],
                        'Order Date' : row[2],
                        'Ship Date' : row[3],
                        'Ship Mode' : row[4],
                        'Customer ID' : row[5],
                        'Customer Name' : row[6],
                        'Segment' : row[7],
                        'Country' : row[8],
                        'City' : row[9],
                        'State' : row[10],
                        'Postal Code' : row[11],
                        'Region' : row[12],
                        'Product ID' : row[13],
                        'Category' : row[14],
                        'Sub-Category' : row[15],
                        'Product Name' : row[16],
                        'Sales' : row[17],
                        'Quantity' : row[18],
                        'Discount' : row[19],
                        'Profit' : row[20]
                    }
                    n += 1
                except Exception as e:
                    print(e)
    except Exception as e:
        print(e)
    return data



def set_data_type(data):

    data.pop(0)
    # replace ',' on '.' and set data type
    for k, v in data.items():
        if re.search(',', v['Row ID']):
            v['Row ID'] = re.sub(',', '.', v['Row ID'])

        if re.search(',', v['Postal Code']):
            v['Postal Code'] = re.sub(',', '.', v['Postal Code'])

        if re.search(',', v['Row ID']):
            v['Row ID'] = re.sub(',', '.', v['Row ID'])

        if re.search(',', v['Sales']):
            v['Sales'] = re.sub(',', '.', v['Sales'])

        if re.search(',', v['Quantity']):
            v['Quantity'] = re.sub(',', '.', v['Quantity'])

        if re.search(',', v['Discount']):
            v['Discount'] = re.sub(',', '.', v['Discount'])

        if re.search(',', v['Profit']):
            v['Profit'] = re.sub(',', '.', v['Profit'])

        # if re.search('*\d(2)/', v['Order Date']):
        #     print(v['Order Date'])
        #     # v['Order Date'] = re.sub(',', '.', v['Order Date'])

        
        try:
            v['Row ID'] =  int(v['Row ID'])
        except Exception as e:
            print(e)
        try:
            v['Order Date'] =  datetime.strptime(v['Order Date'], '%m/%d/%y')
        except Exception as e:
            print(e)
        try:
            v['Ship Date'] =  datetime.strptime(v['Ship Date'], '%m/%d/%y')
        except Exception as e:
            print(e)
        try:
            v['Postal Code'] = int(v['Postal Code'])
        except Exception as e:
            print(e)
        try:
            v['Sales'] = float(v['Sales'])
        except Exception as e:
            v['Sales'] = 0.00
            print(e)
            print('Replace on 0.00')
        try:
            v['Quantity'] = float(v['Quantity'])
        except Exception as e:
            print(e)
        try:
            v['Discount'] = float(v['Discount'])
        except Exception as e:
            print(e)
        try:
            v['Profit'] = float(v['Profit'])
        except Exception as e:
            print(e)        
            
    
    return data

    
def get_profit(data):
    profit = []
    
    for k, v in data.items():
        profit.append(v['Profit'])

    clear_profit = sum(profit)
    return round(clear_profit, 2)



def best_sellers(data):

    # sorting data by profit
    sorted_profit = sorted(data.values(), key=lambda x: x['Profit'])
    
    # get best and worst data by profit
    bestseller_profit = sorted_profit[-1:]
    bestseller_profit ="Best seller order by profit - " + bestseller_profit[0]['Product Name']
    worst_profit = "Worst seller order by profit - " + sorted_profit[0]['Product Name']

    # sorting data by sales
    sorted_sale = sorted(sorted_profit, key=lambda x: x['Sales'])

    # get best and worst data by sales
    bestseller_sale = sorted_sale[-1:]
    bestseller_sale ="Best seller order by sale - " + bestseller_sale[0]['Product Name']
    worst_sale ="Worst seller order by sale - " + sorted_sale[0]['Product Name']
       
    return bestseller_profit, bestseller_sale, worst_profit, worst_sale


def get_date(data):
    shipping_dt = []
    shipping_int = []

    # get days of shipping
    for k,v in data.items(): 
        shipping_dt.append(v['Ship Date'] - v['Order Date'])

    # from date to integer
    for i in shipping_dt:
        shipping_int.append(i.days)

    # get average days of shipping
    average_shipping = sum(shipping_int) / len(shipping_int)

    # get deviation from average days of shipping
    for i in shipping_int:
        i = (i - average_shipping) ** 2
    deviation_from_average = sum(shipping_int) / (len(shipping_int) - 1)
    return average_shipping, deviation_from_average


def get_info_prod(data):

    #get all product name
    prod_name = []
    for k, v in data.items():
        prod_name.append(v['Product Name'])

    #get unique product name
    prod_name = list(set(prod_name))

    product_info = {}
    prft = []
    sale = []

    #get sum profit and sales for unique product name
    for name in prod_name:
        for k, v in data.items():
            if v['Product Name'] == name:
                prft.append(v['Profit'])
                sale.append(v['Sales'])
        product_info[name] = {
            'Profit' : sum(prft),
            'Sales' : sum(sale)
        }
        prft.clear()
        sale.clear()

    return product_info


def write_to_csv(data):
    
    filename = 'result.csv'
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Product name', 'Total profit', 'Total sales'])
        for k, v in data.items():
            writer.writerow([k, v['Profit'], v['Sales']])
    return




def main():

    path = path_to_file + filename

    check = file_cheker(path)
    if not check:
        print('file does not exist')
        return
    
    data = csv_to_data(path)
    
    data = set_data_type(data)

    profit = get_profit(data) #Profit
    sys.stdout.write('Total profit: ' + str(profit) + '\n')

    #best and worst sellers
    bestseller = best_sellers(data)
    sys.stdout.write(bestseller[0] + '\n')
    sys.stdout.write(bestseller[1] + '\n')
    sys.stdout.write(bestseller[2] + '\n')
    sys.stdout.write(bestseller[3] + '\n')

    #get days of shiping
    date = get_date(data)
    sys.stdout.write('Average shipping days: ' + str(date[0]) + '\n')
    sys.stdout.write('Deviation from average days of shipping: ' + str(date[1]) + '\n')

    #get sum profit and sales by product name
    sum_products = get_info_prod(data)
    # write data to csv file
    write = write_to_csv(sum_products)
    sys.stdout.write('Other data writed in result.csv. Please check it')
    
    return

if __name__ == '__main__':
    main()
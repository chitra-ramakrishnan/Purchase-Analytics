import sys
import csv

def process_input_file(order,product):

    with open(product, 'r') as f1:
        f1.readline()
        r1 = csv.reader(f1)
        productData = {}
        for row in r1:
            row[-1] = int(row[-1])
            if row[-1] not in productData:
                productData[row[-1]] = [row[:-1]]
            else:
                productData[row[-1]].append(row[:-1])
    f1.close()

    with open(order, 'r') as f:
        f.readline()
        r = csv.reader(f)
        orderData = {}
        for row in r:
            if row[1] not in orderData:
                orderData[row[1]] = [row]
            else:
                orderData[row[1]].append(row)
    return(productData, orderData)


def createCartData(productData, orderData):
    for  key, values in productData.items():
        for records in values:
            productid = records[0]
            records[0] = {}
            if productid in orderData:
                    records[0][productid] = orderData[productid]
    return productData

def first_time_orders(orders,first_time):
    for orderrecord in orders:
        if orderrecord[-1] == '0':
            first_time += 1
    return first_time


def number_of_orders(cartData):
    department = sorted(cartData.keys())
    result = []
    for dept in department:
        first_time = 0
        order_list = cartData[dept]
        dept_orders = 0
        for products in order_list:
            for pdtid,orders in products[0].items():
                #print(orders, len(orders))
                dept_orders += len(orders)
                first_time = first_time_orders(orders,first_time)
                percent_new = round(first_time/dept_orders, 2)
        if dept_orders > 0:
            result.append([dept,dept_orders, first_time,percent_new])
    return result

def generateOutput(result,output_filepath):
    with open(output_filepath, 'w') as writefile:
        output_report = csv.writer(writefile)
        output_report.writerow(['department_id','number_of_orders','number_of_first_orders','percentage'])
        output_report.writerows(result)
    writefile.close()



#def first_time_orders(result):

def main():
    orders_filepath = sys.argv[1]
    products_filepath = sys.argv[2]
    output_filepath = sys.argv[3]
    productData, orderData = process_input_file(orders_filepath, products_filepath)
    cartData = createCartData(productData, orderData)
    print(cartData)
    result = number_of_orders(cartData)
    print(result)
    generateOutput(result, output_filepath)


if __name__ == "__main__":
    main()

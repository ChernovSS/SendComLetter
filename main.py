import json

from Modules.Gmail import Gmail


def read_data():
    with open('test.json') as file_json:
        data = json.load(file_json)
    return data


def main():
    input_data = read_data()
    recipients = input_data['recipients']
    product_lists = input_data['productLists']
    sender = input_data['sender']

    for recipient in recipients:
        print(f'{recipient["id"]} - {recipient["fullName"]} - with email {recipient["email"]}')
        print('---------------------------------------------')
        # if product_lists['reciepientId'] == recipient['id']
        # products = [list(product.values())[0] for product in
        #             [products['products'] for products in product_lists if products['reciepientId'] == recipient['id']]]
        # print(products)

        products_name = get_products(product_lists,  recipient)
        print(products_name)
        if len(products_name) > 0:
            body = send_mail(products_name, recipient, sender)

            print(body)
        print('=======================================')
        print()


def send_mail(products_name, recipient, sender):
    send_to = recipient['email']
    send_from = sender['email']
    subject = f'Commercial Proposal'
    body_header = f'Dear {recipient["fullName"]}!\r\n' \
                  f'' \
                  f'We want to offer you the following product:\r\n\r\n'
    body_footer = f'\r\n\r\n' \
                  f'Best regards, \r\n' \
                  f'{sender["name"]} \r\n' \
                  f'email: {sender["email"]}'
    body_product_list = ',\r\n'.join(products_name)
    body = body_header + body_product_list + body_footer;

    gmail = Gmail()
    gmail.send_gmail(send_to,subject,body)
    return body


def get_products(product_lists, recipient):
    result = []
    for products in product_lists:
        if products['reciepientId'] == recipient['id']:
            for product in products['products']:
                result.append(product['name'])
    return result

if __name__ == "__main__":
    main()

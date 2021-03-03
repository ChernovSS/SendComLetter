from collections import namedtuple

Contact = namedtuple("Contact", "id fullname email")
Products = namedtuple("Products", "contactid name")

KEY_RECIPIENTS = 'recipients'
KEY_PRODUCT_LISTS = 'productLists'
KEY_PRODUCTS = 'products'
KEY_SENDER = 'sender'

email_header = lambda recipient: f'Dear {recipient.fullname}!\r\n' \
                                 f'We want to offer you the following product:\r\n\r\n'

email_footer = lambda sender: f'Best regards, \r\n' \
                              f'{sender.fullname} \r\n' \
                              f'email: {sender.email}'

email_product_list = lambda products: ',\r\n'.join(products)

email_body = lambda recipient, sender, products: email_header(recipient) \
                                                 + email_product_list(products) \
                                                 + email_footer(sender)

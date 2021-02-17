import json
from typing import Dict, List
import Modules.Types as Type
from Modules.Gmail import Gmail


class Processed:

    def __init__(self, filename: str = None,
                 sender: Type.Contact = None,
                 products: List[Type.Products] = None,
                 recipients: List[Type.Contact] = None):
        self.filename = filename
        self.sender = sender
        self.products = products
        self.recipients = recipients
        self.has_error = False
        self.err_message = ''

        if filename is not None:
            self.parse_file(filename)
        # elif all (sender, products, recipients) is not None:
        #     self.manual_processed(sender, products, recipients)
        # else:
        #     self.raiseError("Not Full Parameters")

        if not self.has_error:
            self.send_mails()

    def parse_file(self, filename):
        file_extension = filename.split('.')[-1]
        if file_extension.lower() == 'json':
            self.parse_json(filename)
        else:
            self.raiseError("undestrand")

    def manual_processed(self, sender, products, recipients):
        pass

    def raiseError(self, param: str = None) -> None:
        self.has_error = True
        self.err_message = param

    def parse_json(self, filename):
        data = self.read_json(filename)

        if self.has_error:
            return False
        try:
            self.recipients = []
            for data_one in data[Type.KEY_RECIPIENTS]:
                recipient = Type.Contact(id=data_one['id'],
                                         fullname=data_one['fullName'],
                                         email=data_one['email'])
                self.recipients.append(recipient)

            self.products = []
            for data_one in data[Type.KEY_PRODUCT_LISTS]:
                contact_id = data_one['reciepientId']
                for prod in data_one[Type.KEY_PRODUCTS]:
                    product_name = prod['name']
                    product = Type.Products(contactid=contact_id,
                                            name=product_name)
                    self.products.append(product)

            self.sender = Type.Contact(id=data[Type.KEY_SENDER]['id'],
                                       fullname=data[Type.KEY_SENDER]['fullName'],
                                       email=data[Type.KEY_SENDER]['email'])
        except Exception as e:
            self.raiseError(f"Something wrong: \r\n {e}")

    def read_json(self, filename):
        data = None
        try:
            with open(filename) as file_json:
                data = json.load(file_json)
        except Exception as e:
            self.raiseError(f"Can't read file - {filename}")

        if not ((Type.KEY_RECIPIENTS or Type.KEY_SENDER or Type.KEY_PRODUCT_LISTS) in data):
            self.raiseError("Json not have all keys")

        return data

    def send_mails(self):
        for recepient in self.recipients:
            self.send_mail(recepient)

    # noinspection PyTypeChecker
    def send_mail(self, recepient):
        products = [product['name'] for product in self.products if product['contactid'] == recepient['id'] or 0]
        if len(products) <= 0:
            self.raiseError("Not Products. Email can't sending")

        send_to = recepient['email']
        subject = f'Commercial Proposal'
        email_body = Type.email_body(recepient, self.sender, products)
        try:
            gmail = Gmail()
            gmail.send_gmail(send_to,subject,email_body)
        except Exception as e:
            self.raiseError(f"Something wrong when send email to {send_to} : \r\n {e}")


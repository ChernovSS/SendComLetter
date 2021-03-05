import csv
import json
from typing import List

import Modules.Types as Type
from Modules.Gmail import Gmail

"""
Processed class for mailings
"""
class Processed:


    def __init__(self, filename: str = None,
                 sender: Type.Contact = None,
                 products: List[Type.Products] = None,
                 recipients: List[Type.Contact] = None):
        """
        Init class by next params

        :param filename: input file (.json/.csv) having inputs data
        :param sender: Types.Contaсts
        :param products: list Types.Products
        :param recipients: list Types.Contacts
        """
        self.filename = filename
        self.sender = sender
        self.products = products
        self.recipients = recipients
        self.has_error = False
        self.err_message = ''

        if filename is not None:
            self.parse_file(filename)
        elif sender is not None and products is not None and recipients is not None:
            self.send_mails()
        else:
            self.raiseError("Not Full Parameters")

    def parse_file(self, filename):
        """
        determinate method for parsing file
        :param filename:  str filename
        :return: raise error for class if file extension not in .json or .csv
        """
        file_extension = filename.split('.')[-1]
        if file_extension.lower() == 'json':
            self.parse_json(filename)
        elif file_extension.lower() == 'csv':
            self.parse_csv(filename)
        else:
            self.raiseError("undestrand")

    def raiseError(self, param: str = None) -> None:
        """
        set error message and error flag is true
        :param param:
        """
        self.has_error = True
        self.err_message = param

    def parse_json(self, filename):
        """
        parsing json file to main parameters recipients, products, sender
        and if class not have error sending mails
        :param filename: str
        """
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

        self.send_mails()

    def read_json(self, filename):
        """
        reading json files to data[]
        :param filename: str
        :return: list data or None if raise error
        """
        data = None
        try:
            with open(filename) as file_json:
                data = json.load(file_json)
        except Exception as e:
            self.raiseError(f"Can't read file - {filename}")

        if not ((Type.KEY_RECIPIENTS or Type.KEY_SENDER or Type.KEY_PRODUCT_LISTS) in data):
            self.raiseError("Json not have all keys")

        return data

    # noinspection PyBroadException
    def read_csv(self, filename):
        """
        reading csv files and sending mails if not error
        :param filename: str
        """
        try:
            with open(filename, newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                next(reader, None)
                index = 1
                for row in reader:
                    print(row)
                    self.recipients = []
                    self.products = []

                    new_recipient = Type.Contact(index, row[0], row[1])
                    self.recipients.append(new_recipient)
                    products_list = row[2].split(';')
                    for product in products_list:
                        new_product = Type.Products(index, product.strip())
                        self.products.append(new_product)
                    new_sender = Type.Contact(index, row[3], row[4])
                    self.sender = new_sender
                    self.send_mails()
            exit()
        except Exception as e:
            self.raiseError(f"Can't read file - {filename}")

    def send_mails(self):
        """
        sending all email into loop by in list
        """
        for recepient in self.recipients:
            self.send_mail(recepient)

    # noinspection PyTypeChecker
    def send_mail(self, recepient):
        """
        send one email to one recipient
        :param recepient: Types.Contacts
        """
        products = [product.name for product in self.products if product.contactid == recepient.id or 0]
        if len(products) <= 0:
            self.raiseError(f"Not Products. Email can't sending to {recepient.email}")

        send_to = recepient.email
        subject = f'Commercial Proposal'
        email_body = Type.email_body(recepient, self.sender, products)
        try:
            gmail = Gmail()
            gmail.send_gmail(send_to, subject, email_body)
        except Exception as e:
            self.raiseError(f"Something wrong when send email to {send_to} : \r\n {e}")

    def parse_csv(self, filename):
        data = self.read_csv(filename)
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

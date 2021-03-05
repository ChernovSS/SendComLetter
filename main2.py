from Modules import Types
from processed import Processed


def main():
    # #send from json
    # filename = 'test.json'
    # proc = Processed(filename=filename)
    #
    # if proc.has_error:
    #     print(proc.err_message)
    #
    # # send from csv
    # filename = 'test.csv'
    # proc = Processed(filename=filename)
    #
    # if proc.has_error:
    #     print(proc.err_message)

    # send from data
    recipients = [
        Types.Contact(id=1, fullname='Test1', email='test1@test.com'),
        Types.Contact(id=2, fullname='Test2', email='test2@test.com'),
        Types.Contact(id=3, fullname='Test3', email='test3@test.com')
    ]

    products = [
        Types.Products(contactid=1, name='product1'),
        Types.Products(contactid=1, name='product2'),
        Types.Products(contactid=1, name='product3'),
        Types.Products(contactid=1, name='product4'),
        Types.Products(contactid=2, name='product5'),
        Types.Products(contactid=3, name='product6'),
    ]

    sender = Types.Contact(id=1, fullname='Sender Letter', email='sender1@test.com')
    proc = Processed(recipients=recipients, products=products, sender=sender)


if __name__ == "__main__":
    main()

from processed import Processed


def main():
    filename = 'test.csv'
    proc = Processed(filename=filename)

    if proc.has_error:
        print(proc.err_message)

    # products = []
    # product = Type.Products("test1")
    # products.append(product)
    # product2 = Type.Products("test2")
    # products.append(product2)
    # proc2 = Processed(products=products)
    # print("Products: \r\n")
    # for product in products:
    #     print(f'{product[0]}')


if __name__ == "__main__":
    main()

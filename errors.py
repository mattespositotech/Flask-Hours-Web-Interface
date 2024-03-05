def handle_error(error):
    match error:
        case 0:
            return
        case 1555:
            print("Already inputed data for today")
        case _:
            print('Unkown error: code ' + str(error))
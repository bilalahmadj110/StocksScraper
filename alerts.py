def log(num, detail, level=0, send_email=False):
    print(f"LOG[{level}] - {num}: {detail}")


def success(num, details):
    print(f'SUCCESS {num}: {details}')

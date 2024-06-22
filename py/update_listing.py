from misc import timestamp, exists
import os

def update_listing():
    ts = timestamp()
    cmd = ' '.join(['aws',  # read data from aws
                    's3api',
                    'list-objects',
                    '--no-sign-request',
                    '--bucket sentinel-products-ca-mirror'])
    print(cmd)
    data = os.popen(cmd).read()

    if not exists(my_path + 'listing'):  # json backup for analysis
        os.mkdir(my_path + 'listing')

    df = my_path + 'listing' + sep + ts + '_objects.txt'  # file to write
    open(df, 'wb').write(data.encode())  # record json to file

if __name__ == '__main__':
    update_listing()

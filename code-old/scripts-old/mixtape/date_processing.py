import datetime


def parse_datetime(line):
    print(f'Original line -> {line}')
    line = line[1:].split()
    line = line[:-1]+line[-1].split('.')
    line = list(map(int,line))
    line[-1] = line[-1]*10
    print(f'Spilt line -> {line}')
    epoch = datetime.datetime(line[0], line[1], line[2], line[3], line[4], line[5])
    print(f'Epoch -> {epoch}')

def main():
    parse_datetime('*  2001  8  8  0  0  0.00000000')
    parse_datetime('*  2018 10  7  8  15  12.14562981')

if __name__ == '__main__':
    main()

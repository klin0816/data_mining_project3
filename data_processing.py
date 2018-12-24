import pickle
import sys

if __name__ == '__main__':
    file = sys.argv[1]
    big_list = []
    with open(file, "r") as f:
        temp = []
        start = 1
        sstring = ''
        for line in f:
            s = line.rsplit()
            sstring += str(s[1]) + ',' + str(s[2]) + '\n'

    with open("hw3dataset/graph_7.txt", "w") as fp:
        fp.write(str(sstring))

    print("Proceed!")

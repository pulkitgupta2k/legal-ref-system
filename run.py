from helper import *

if __name__ == "__main__":
    file1 = open("input.txt")
    keywords = file1.read().split('\n')
    to_addr = "sam@forkast.news"
    day_driver(keywords, to_addr)
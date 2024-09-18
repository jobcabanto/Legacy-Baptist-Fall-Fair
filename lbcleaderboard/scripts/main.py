
from lbcleaderboard.scripts.data import RawData

def main(client = RawData()):

    client.PullData()
    client.StyleData()
    client.DataToWeb()

if __name__ == "__main__":
    main()
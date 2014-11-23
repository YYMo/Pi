import csv
class DBconnector():
    def __init__(self):
        self.cmd = 1
        self.readCSV()
    def readCSV(self):
        self.info_dict = {'adult':{}, 
                        'elderly':{},
                        'midage':{},
                        'students':{},
                        'youth':{}}
        csv_file = file('health_data/data.csv', 'rb')
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            #print line
            self.info_dict[line[1]][line[0]] = (line[2], line[3], line[4])
            #print self.info_dict[line[1]][line[0]]
        csv_file.close()
    def getInfo(self, age_range, time):
        return self.info_dict[age_range][time];

def main():
    db = DBconnector()
    #db.readCSV()

if __name__ == '__main__':
    main()


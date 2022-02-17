class engine():
    
    def __init__(self,mode):
        self.mode=mode
        self.datas = list()
        self.strats = list()
        self.feeds = list()

    def adddata(self,data):
        self.data=data
        self.datas.append(data)

    def addstrategy(self,strategy):
        self.strats.append(strategy)
    
    def run(self):

        if not self.datas:
            print("Nothing can run ! No data present!")
            return []  # nothing can be run

        strat = self.strats[0](self.datas[0])
        strat.execute()

    
    


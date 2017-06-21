## parse ACES streamgauge into CSV

import sys
import pandas as pd
from datetime import datetime


rawfile = open(sys.argv[1], 'r').read()
pieces = rawfile.split(",")

csv_pre = [(datetime.fromtimestamp(float(pieces[x])/1000.0), pieces[x+1]) for x in range(0, len(pieces)-1, 2)]

pd.DataFrame(csv_pre).to_csv(sys.argv[1]+".csv", header=False, index=False)



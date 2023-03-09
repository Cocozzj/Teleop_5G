from utils.context import *
import numpy as np
import pandas as pd
NR_EVENT='Event 5G-NR Events'

l = ['Python', 'C++', 'Java']
#追加元素
l.extend('C')
print(l)
#追加元组，元祖被拆分成多个元素
t = ('JavaScript', 'C#', 'Go')
l.extend(t)
print(l)
#追加列表，列表也被拆分成多个元素

l.extend([NR_EVENT])
print(l)
import random
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

usa_city_population = pd.DataFrame({
    'population': [8398748, 3990456, 2705994, 2325502, 1660272],
}, index = ['New York City', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'])
china_city_population = pd.DataFrame({
    'population': [26917322, 20381745, 15773658, 13552359, 13238590],
}, index = ['Shanghai', 'Beijing', 'Chongqing', 'Tianjin', 'Guangzhou'])
top_city_population = pd.DataFrame({
    'usa': usa_city_population['population'].values,
    'china': china_city_population['population'].values
}, index = ['top1', 'top2', 'top3', 'top4', 'top5'])
print(top_city_population)

axs = top_city_population.plot.bar(rot = 0)
plt.show()
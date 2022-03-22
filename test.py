import pandas as pd


data = [['tapiwa', 27], ['wadza', 24]]

dt = pd.DataFrame(data, columns = ['Name', 'Age'])

print(dt)
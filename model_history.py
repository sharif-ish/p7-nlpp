import matplotlib.pyplot as plt

filename = '2020-04-21 20:12:42 model history.txt'

data = eval(open(f'trained model/{filename}', 'r').read())

iter = list()
loss = list()
for d in data:
    iter.append(d['Iteration'])
    loss.append(d['Loss']['ner'])

plt.plot(iter, loss, c='red')
plt.xlabel("Iteration")
plt.ylabel("Loss")
plt.show()
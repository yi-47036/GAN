#time: 20211109 
#author: wangjunyi
#基于GAN生成1010格式的数字

import torch
import torch.nn as nn


import pandas
import random
import matplotlib.pyplot as plt

def generate_real():
    real_data = torch.FloatTensor(
        [random.uniform(0.8, 1.0),
         random.uniform(0, 0.2),
         random.uniform(0.8, 1.0),
         random.uniform(0, 0.2),
        ]
    )
    return real_data

def generate_random(size):
    random_data = torch.rand(size)
    return random_data

class Generator(nn.Module):
    def __init__(self):
        super().__init__()

        self.model = nn.Sequential(
            nn.Linear(1, 3),
            nn.Sigmoid(),
            nn.Linear(3, 4),
            nn.Sigmoid()
        )

        self.optimiser = torch.optim.SGD(self.parameters(), lr = 0.01)

        self.counter = 0
        self.progress = []
        pass
    
    def forward(self, inputs):
        return self.model(inputs)

    def train(self, D, inputs, targets):
        g_output = self.forward(inputs)
        d_output = D.forward(g_output)

        loss = D.loss_function(d_output, targets)

        self.optimiser.zero_grad()
        loss.backward()
        self.optimiser.step()

        self.counter += 1
        if(self.counter % 10 == 0):
            self.progress.append(loss.item())


class Discriminator(nn.Module):
    def __init__(self):
        super().__init__()

        self.model = nn.Sequential(
            nn.Linear(4, 3),
            nn.Sigmoid(),
            nn.Linear(3, 1),
            nn.Sigmoid()
        )

        self.loss_function = nn.MSELoss()
        self.optimiser = torch.optim.SGD(self.parameters(), lr = 0.01)

        self.counter = 0
        self.progress = []

        pass

    def forward(self, inputs):
            return self.model(inputs)

    def train(self, inputs, targets):
        outputs = self.forward(inputs)

        loss = self.loss_function(outputs, targets)

        self.optimiser.zero_grad()
        loss.backward()
        self.optimiser.step()

        self.counter += 1
        if(self.counter % 10 == 0):
            self.progress.append(loss.item())
        if(self.counter % 10000 == 0):
            print("counter = ", self.counter)
    
    def plot_progress(self):
        print("plot : ")
        df = pandas.DataFrame(self.progress, columns=['loss'])
        # df.plot(ylim=(0, 1.0), figsize = (16,8), alpha=0.1,
        # marker='.', grid=True, yticks=(0, 0.25, 0.5))
        df.plot

if __name__ == '__main__':
    D = Discriminator()
    G = Generator()

    for i in range(30000):
        #用真实样本训练判别器
        D.train(generate_real(), torch.FloatTensor([1.0]))
        #用生成的样本训练判别器
        #用detach来截断判别器训练事对于生成器的梯度传播
        D.train(G.forward(torch.FloatTensor([0.5])).detach(), torch.FloatTensor([0.0]))
        #训练生成器
        G.train(D, torch.FloatTensor([0.5]), torch.FloatTensor([1.0]))

    print(G.forward(torch.FloatTensor([0.5])))
    x1 = len(D.progress)
    plt.scatter(range(x1), D.progress, color = 'blue', s = 10 ,label = 'loss')
    plt.show()
    x2 = len(G.progress)
    plt.scatter(range(x2), G.progress, color = 'blue', s = 10 ,label = 'loss')
    plt.show()
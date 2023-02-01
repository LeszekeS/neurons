import random as r
import matplotlib.pyplot as plt


class Train_data:
    ekstensja = list()

    def __init__(self, item):
        self.result = item[len(item) - 1]
        self.data = list()
        for e in range(len(item) - 1):
            self.data.append(int(item[e]))
        Train_data.ekstensja.append(self)

    def __str__(self):
        return f'data: {self.data}; expected result: {self.result}'

    def get_element(self):
        tmp = []
        for e in self.data:
            tmp.append(e)
        tmp.append(1)
        return tmp

    def get_expected_result(self):
        return self.result


class Neuron:
    ekstensja = list()

    def __init__(self, ntype, dot, ilosc_wsadowych):
        self.ntype = ntype
        self.dot = dot
        self.n = .1
        self.weights = []
        for i in range(ilosc_wsadowych):
            self.weights.append(r.randint(-1, 1))
        Neuron.ekstensja.append(self)

    def load_train_data(self, train_data):
        self.train_data = train_data

    def count_net(self):
        net_result = 0
        for i in range(len(self.weights)):
            net_result += self.train_data.get_element()[i] * self.weights[i]
        return net_result

    def decision(self):
        net = self.count_net()

        r = 0

        if net > 0:
            r = 1
        elif net < 0:
            r = 0
        else:
            r = int(self.dot)

        if self.ntype == "bi" and r == 0: r = -1
        return r

    def recount_weights(self, neuron_no):
        counted_decision = self.decision()
        for i in range(len(self.weights)):
            exp_decision = int(result_to_decision[self.train_data.get_expected_result()][neuron_no])
            inp_info = self.train_data.get_element()[i]

            self.weights[i] += self.n * (exp_decision - counted_decision) * inp_info

    def __str__(self):
        return f'Neuron: {Neuron.ekstensja.index(self)}; type: {self.ntype}; dot: {self.dot}; weights: {self.weights}'


def load_file(learn_source):
    file = open(learn_source, 'r')
    data = file.readlines()
    file.close()

    for e in range(len(data)-1):
        Train_data(data[e].strip().split(";"))


result_to_decision = {}


def result_template():
    result_to_decision[Train_data.ekstensja[0].result] = "1"
    for obj in Train_data.ekstensja:
        if obj.result not in result_to_decision:
            for i in result_to_decision:
                result_to_decision[i] = result_to_decision[i] + "0"
            m = len(result_to_decision)
            result_to_decision[obj.result] = "0" * m + "1"


load_file("train_data.txt")

result_template()

print(result_to_decision)

for i in range(len(result_to_decision)):
    Neuron("uni", False, 3)


stillearning = True
while stillearning:
    stillearning = False
    idx = 0
    while idx < len(Neuron.ekstensja):
        jdx = 0
        while jdx < len(Train_data.ekstensja):
            Neuron.ekstensja[idx].load_train_data(Train_data.ekstensja[jdx])

            if Neuron.ekstensja[idx].decision() != int(result_to_decision[Train_data.ekstensja[jdx].get_expected_result()][idx]):
                # print(Neuron.ekstensja[idx].decision())
                # print(int(result_to_decision[Train_data.ekstensja[jdx].get_expected_result()][idx]))
                Neuron.ekstensja[idx].recount_weights(idx)
                stillearning = True
                idx = 0
                jdx = 0
            jdx += 1
        idx += 1


for n in Neuron.ekstensja:
    print(n)


x = []
y = []

for k in result_to_decision.keys():
    for d in Train_data.ekstensja:
        if k == d.result:
            x.append(d.data[0])
            y.append(d.data[1])
    plt.scatter(x, y, color=k.lower())
    x.clear()
    y.clear()
plt.show()


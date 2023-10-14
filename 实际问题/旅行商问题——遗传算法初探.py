import random
import scipy.cluster.hierarchy as sch
import pandas as pd
import scipy
from matplotlib import pyplot as plt
import matplotlib as mpl


class TSP_GA:
    def __init__(self, iteration, cost_mat, pop_size, mutation_rate, elite_rate):
        self.iteration = iteration  # 迭代次数
        self.cost_mat = cost_mat  # 成本矩阵
        self.cities = self.cost_mat.shape[0]  # 城市数量+最终回到起点城市
        self.pop_size = pop_size  # 种群数量
        self.mutation_rate = mutation_rate  # 变异率
        self.elite_rate = elite_rate  # 精英率

    # 种群初始化
    def initial_population(self):
        population = []
        for i in range(self.pop_size):
            cities_list = list(range(self.cities))
            random.shuffle(cities_list)
            population.append(cities_list)
        return population

    # 计算个体适应度
    def fitness(self, individual):
        route_cost = 0
        for i in range(len(individual) - 1):  # 个体长度为城市节点总数量，节点数量-1为路径数量
            start = individual[i]
            end = individual[i + 1]
            route_cost += self.cost_mat[start][end]
        route_cost += self.cost_mat[individual[-1]][individual[0]]
        return route_cost

    @staticmethod
    # 基因遗传
    def __crossover(parent_a, parent_b):  # a对应需要完整保留的优质基因
        child = [None] * len(parent_a)
        start_index, end_index = random.sample(range(len(parent_a)), 2)  # 随机生成索引点，街区基因片段
        if start_index > end_index:
            start_index, end_index = end_index, start_index
        child[start_index: end_index] = parent_a[start_index: end_index]  # 将父代截取出的基因传递给子代对应位置
        remain_genes = [gene for gene in parent_b if gene not in child]  # 从另一个父代基因中按顺序提取剩余基因
        i = 0
        for gene in remain_genes:  # 将另一个父代基因传递给子代
            while child[i] is not None:
                i = i + 1
            child[i] = gene
        return child

    # 精英选择
    def select_elite(self, population, fitnesses):
        num_elites = int(len(population) * self.elite_rate)  # 计算精英数量
        sorted_population = [individual for f, individual in sorted(zip(fitnesses, population))]
        elites = sorted_population[:num_elites]
        return elites

    # 亲代选择
    def selete_parents(self, population, fitnesses):
        total_fitness = sum(fitnesses)
        selection_probability = [fitness / total_fitness for fitness in fitnesses]
        parent_a_index = random.choices(range(len(population)), weights=selection_probability, k=1)[0]
        parent_a = population[parent_a_index]

        population_without_a = population[:parent_a_index] + population[parent_a_index + 1:]
        fitnesses_without_a = fitnesses[:parent_a_index] + fitnesses[parent_a_index + 1:]

        total_fitness = sum(fitnesses_without_a)
        selection_probability = [fitness / total_fitness for fitness in fitnesses_without_a]
        parent_b_index = random.choices(range(len(population_without_a)), weights=selection_probability, k=1)[0]
        parent_b = population_without_a[parent_b_index]

        return parent_a, parent_b

    # 变异
    def displacement_mutation(self, individual):
        i, j = sorted(random.sample(range(len(individual)), 2))
        k = random.randint(0, len(individual) - (j - i + 1))
        genes = individual[i:j + 1]
        del individual[i:j + 1]
        individual[k:k] = genes
        return individual

    def solve(self):
        population = self.initial_population()  # 初始化种群
        best_fitness = []
        for i in range(self.iteration):  # 设定种群代数
            fitnesses = [self.fitness(individual) for individual in population]  # 计算中群内所有个体适应度
            selection_probability = [1 / self.fitness(individual) for individual in population]
            next_population = self.select_elite(population, fitnesses)  # 选择精英进行保留
            while len(next_population) < self.pop_size:  # 补充新的子代直至种群数量达到设定值
                parent_a, parent_b = self.selete_parents(population, selection_probability)  # 选择亲代
                child_a = self.__crossover(parent_a, parent_b)  # 生成子代A
                child_b = self.__crossover(parent_b, parent_a)  # 生成子代B
                if random.random() < self.mutation_rate:  # 子代A按照变异率随机变异
                    child_a = self.displacement_mutation(child_a)
                if random.random() < self.mutation_rate:  # 子代B按照变异率随机变异
                    child_b = self.displacement_mutation(child_b)
                next_population.append(child_a)  # 将子代纳入新种群中
                next_population.append(child_b)
            population = next_population
            fitnesses = [self.fitness(individual) for individual in population]  # 计算中群内所有个体适应度
            best_fitness.append(min(fitnesses))
            print('当前迭代进度{}/{}，最短路线距离为{}'.format(i, self.iteration, min(fitnesses)))
        fitnesses = [self.fitness(individual) for individual in population]  # 计算中群内所有个体适应度
        best_individual = population[fitnesses.index(min(fitnesses))]
        return best_individual, min(fitnesses), best_fitness


# 从坐标中计算欧氏距离
# df = pd.read_csv(r'C:\Users\Administrator\Desktop\geoinfo.csv', header=0, index_col=0)  # 读取坐标文件
# data_dic = list(df.itertuples(name=None))  # 读取坐标信息
# df.values[:, :] = df.values[:, :].astype(float)  # 提取坐标信息
# cosMat = scipy.spatial.distance.squareform(sch.distance.pdist(X=df[['x', 'y']], metric='euclidean'))  # 生成距离矩阵

# 使用已有距离矩阵
df = pd.read_csv(r'C:\Users\Administrator\Desktop\geoinfo.csv', header=0, index_col=0) # 读入坐标文件
cf = pd.read_csv(r'C:\Users\Administrator\Desktop\cost_Matrix.csv', header=0, index_col=0) # 读入对应坐标文件的成本举证
data_dic = list(df.itertuples(name=None))
cosMat = cf.values[:, :].astype(float)

TSP = TSP_GA(iteration=10000, cost_mat=cosMat, pop_size=200, mutation_rate=0.1, elite_rate=0.1)  # 求解问题
TSP_result = TSP.solve()

best_individual = TSP_result[0]  # 提取最佳路线
route = []
for point_index in best_individual:
    route.append(data_dic[point_index])

mpl.rcParams['font.sans-serif'] = ['SimHei']  # 设定中文字体
line_x = []
line_y = []
for point in route:  # 显示散点图
    name, x, y = point
    line_x.append(x)
    line_y.append(y)
    plt.scatter(x, y)
    plt.text(x, y, name, fontdict={"size": 4})
line_x.append(route[0][1])
line_y.append(route[0][2])
plt.plot(line_x, line_y)
plt.axis('equal')

plt.show()

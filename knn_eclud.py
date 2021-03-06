from numpy import *
import matplotlib.pyplot as plt

def loadDataSet(fileName):
    datMat = []
    fp = open(fileName)
    for line in fp.readlines():
        curLine = line.split(' ')
        floatLine = list(map(float,curLine))
        datMat.append(floatLine)
    return datMat

def randCent(dataSet,k):
    ndim = array(dataSet).shape[1]
    # 初始化中心点数组
    centsArray = zeros((k,ndim))
    # 这一步的操作是将初始随机中心点的每个维度的值限定在数据点的维度值域之间，二维的话就是说中心点不会处在
    # 数据点组成的“域”之外
    for i in range(ndim):
        minIDim = min(array(dataSet)[:,i])
        maxIDim = max(array(dataSet)[:,i])
        rangeIDim = maxIDim-minIDim
        centsArray[:,i] = (minIDim + rangeIDim * random.rand(k, 1)).reshape(centsArray[:, i].shape)
    return centsArray

def distEclud(vecA,vecB):
    return sqrt(sum(power(vecA-vecB,2)))

def kMeans(dataSet,k):
    # 数据总量
    num = dataSet.shape[0]
    # 建立一个数组存储每个点的类别和与对应中心点的欧氏距离
    clusterAssignmentArray = zeros((num,2))
    centsArray = randCent(dataSet,k)
    clusterChanged = True
    while clusterChanged:
        clusterChanged = False
        for i in range(num):
            minIndex = -1
            minDist = inf
            for j in range(k):
                diEclud = distEclud(dataSet[i],centsArray[j])
                if diEclud<minDist:
                    minDist = diEclud
                    minIndex = j
            if clusterAssignmentArray[i][0]!=minIndex:
                clusterAssignmentArray[i] = minIndex,minDist
                clusterChanged = True
        # 根据新的分类结果中每一类的数据点，重新计算每一类的中心点
        for centIndex in range(k):
            # 根据minIndex取出每一类的数据点进行计算
            ptrInClust = []
            for j in range(num):
                if clusterAssignmentArray[j][0]==centIndex:
                    ptrInClust.append(dataSet[j])
            centsArray[centIndex, :] = mean(ptrInClust, axis=0)
    return centsArray,clusterAssignmentArray
if __name__ == "__main__":
    k = 4
    datMat = mat(loadDataSet('1.txt'))
    myCentroids, clustAssing = kMeans(datMat, k)

    x = []
    y = []
    x.append(((myCentroids[:, 0]).tolist()))
    y.append((myCentroids[:, 1]).tolist())
    # plt.plot(x[0], y[0], 'b*')
    plt.plot(((myCentroids[:, 0]).tolist()), (myCentroids[:, 1]).tolist(), 'k*')

    colourList = ['bo', 'ro', 'yo', 'co','ko']
    for i in range(k):
        centX = []
        centY = []

        for j in range(19):
            if clustAssing[j].tolist()[0] == i:
                centX.append(datMat[j].tolist()[0][0])
                centY.append(datMat[j].tolist()[0][1])
        plt.plot(centX, centY, colourList[i])

    plt.show()
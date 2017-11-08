# 2017.5.23 zhujian
# Hierarchical Clustering: initial points
# Kmeans: do clustering in [2,(n-1)]
#VRC: choose the best k and cluster based on the CH
import numpy as np
import random

class bicluster:
    def __init__(self,vec,left=None,right=None,distance=0.0,id=None):
        self.left = left
        self.right = right
        self.id = id
        self.vec = vec
        self.distance = distance

def yezi(clust):
    if clust.left == None and clust.right ==None:
        return [clust.id]
    return yezi(clust.left) + yezi(clust.right)

def hcluster(dataSet,n):
    biclusters = [bicluster(vec = dataSet[i],id = i) for i in range(len(dataSet))]
    distances = {}
    flag = None
    currentclusted = -1
    while(len(biclusters) > n):
        min_val = 1000000;
        biclusters_len = len(biclusters)
        #calculate the distance of any two points
        #for i in range(biclusters_len - 1):
        for i in range(biclusters_len-1):
            for j in range(i + 1 , biclusters_len):
                if distances.get((biclusters[i].id,biclusters[j].id)) == None:
                    distances[(biclusters[i].id, biclusters[j].id)] = abs(biclusters[i].vec - biclusters[j].vec)
                #find min distance
                d = distances[(biclusters[i].id,biclusters[j].id)]
                if d < min_val :
                    min_val = d
                    flag = (i,j)
        bic1,bic2 = flag
        newvec = (biclusters[bic1].vec + biclusters[j].vec)/2
        newbic = bicluster(newvec,left=biclusters[bic1], right=biclusters[bic2], distance=min_val, id=currentclusted)
        currentclusted -= 1
        del biclusters[bic2]
        del biclusters[bic1]
        biclusters.append(newbic)
        clusters = [yezi(biclusters[i]) for i in range(len(biclusters))]
    #return biclusters,clusters
    return clusters

def initpoint(dataSet,k):
    initClusters = hcluster(dataSet,k)
    cluster_center = np.zeros(k)
    for i in range(k):
        #clusterPoint = dataSet[np.nonzero(initClusters[i])]
        clusterPoint = dataSet[initClusters[i]]
        cluster_center[i] = np.mean(clusterPoint)
    return cluster_center




#data:numpy.array dataset
#k:the number of cluster
def k_means(dataSet,k):

    #random generate clusteer_center
    sample_num=dataSet.shape[0]
    cluster_cen=initpoint(dataSet,k)
    
    #cluster_cen=np.zeros(k)
    
    #center_index=random.sample(range(sample_num),k)
    #cluster_cen=dataSet[center_index]
    #print "random init cluster_cen:",cluster_cen
    
    is_change=1
    cat=np.zeros(sample_num)
 
    while is_change:
        is_change=0

        for i in range(sample_num):
            min_distance=100000
            min_index=0

            for j in range(k):
                distance=abs(dataSet[i]-cluster_cen[j])

                #print "distance----------",distance
                if distance<min_distance:
                    min_distance=distance
                    min_index=j

            if cat[i]!=min_index:
                is_change=1
                cat[i]=min_index

        for j in range(k):
            pointsInCluster = dataSet[np.nonzero(cat[:] == j)]
            cluster_cen[j]=np.mean(pointsInCluster)

    return cat,cluster_cen

def VRC(dataSet):
    m=np.mean(dataSet)#the centroid of the entire data set
    sample_num=dataSet.shape[0]
    
    vrc = []

    for k in range(2,sample_num):
        cat, cluster_cen = k_means(dataSet,k)
        cat2 = cat.tolist()
        ssb = 0
        ssw = 0
        for i in range(k):
            nk = cat2.count(i)#nk is the number of points in cluster k
            ssb = ssb + nk*(cluster_cen[i]-m)*(cluster_cen[i]-m)

            pointsInCluster = dataSet[np.nonzero(cat[:] == i)]
            ssw = ssw + nk*(np.var(pointsInCluster))
        vrc.append((ssb*(sample_num-k))/(ssw*(k-1)))

    return (vrc.index(max(vrc))+2)

def main():
    comSpeed=open("data_speed.txt")
    data=[]
    n=0
    while 1:
        line=comSpeed.readline()
        line=line.strip('\n')
        try:
            data.append(round(float(line),8))
        except:
            #print "speedData.txt have something wrong in format."
            break
        if not line:
            break
        n=n+1
    #print data
    dataSet=np.array(data)

    k=VRC(dataSet)
    print "--------Best k:",k
    mycat,mycluster_cen=k_means(dataSet,k)

    print "clustering results: ",mycat


if __name__=="__main__":
    main()



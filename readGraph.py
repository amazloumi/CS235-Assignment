import sys
from math import sqrt
import matplotlib.pylab as plt
import numpy
import scipy.sparse.linalg
from scipy import sparse

def main():
    
    #reading all sources and destinations of every edges
    input_graph_file = sys.argv[1]
    graph = open(input_graph_file, 'r')
    lines = graph.read()
    srcs = [int(item.split(",")[0]) for item in lines.split('\n')[0:-1]]
    dsts = [int(item.split(",")[1]) for item in lines.split('\n')[0:-1]]
    
    #specify the number of vertices and the number of edges
    max_s = max(srcs)
    max_d = max(dsts)
    num_vertices = max(max_s, max_d)
    num_edges = len(srcs)

    #create the vertex ids starting from 0
    vertex_ids = []
    for i in range(num_vertices):
        vertex_ids.append(i)

    #declare an empty adjacency array
    adj_array = []
    for i in range(num_vertices):
        adj_array.append([0 for i in range(num_vertices)])

    #declare an empty degree array
    degree_array = [0 for i in range(num_vertices)]

    #fill the undirected adjacency array
    for i in range(num_edges):
        adj_array[srcs[i]-1][dsts[i]-1] = 1
        degree_array[srcs[i]-1]+=1

    #extracting the frequency of unique degrees
    unique_degrees, counts_degrees = numpy.unique(degree_array,return_counts=True)

    #spy plot
    fig = plt.figure() 
    plt.spy(numpy.array(adj_array), markersize=1)

    #annotating the plot
    ax=plt.gca()
    circle_rad = 15  # This is the radius, in points
    ax.plot(725 , 740, 'o',
                    ms=circle_rad * 1.2, mec='b', mfc='none', mew=2)
    
    ax.plot(2720 , 2760, 'o',
                    ms=circle_rad * 3, mec='b', mfc='none', mew=2)
    
    ax.plot(15950 , 16050, 'o',
                    ms=circle_rad * 4, mec='b', mfc='none', mew=2)    
    fig.savefig('adjacency_plot.png')

    #degree distribution plot
    fig = plt.figure() 
    plt.scatter(unique_degrees,counts_degrees)
    plt.xscale('log')
    plt.yscale('log')
    fig.savefig('degree_distribution.png')

    #convert adj_array to sparse matrix
    adj_array_sparse = sparse.csr_matrix(adj_array)
    
    #calculated SVD parameters
    u, s, vt = scipy.sparse.linalg.svds(adj_array_sparse.asfptype(), k=1420, which='LM')

    #claculating the approximate graph to evaluate the accuracy
    singular_array = []
    for i in range(len(s)):
        singular_array.append([0 for i in range(len(s))])
    for i in range(len(s)):
        singular_array[i][i]=s[i]
    approx_array = (u.dot(singular_array)).dot(vt)

    #print the accuracy
    sum_sqr = 0
    sum_diff_sqr = 0
    for i in range(num_vertices):
        for j in range(num_vertices):
            sum_sqr += (adj_array[i][j])**2
            sum_diff_sqr += (adj_array[i][j]-approx_array[i][j])**2
    accuracy = round((1 - sqrt(sum_diff_sqr/sum_sqr))*100, 2)
    print('accuracy: ', accuracy)

    #print 5 top left singular vector in one figure 
    fig = plt.figure()
    plt.plot(u[:,(len(s)-5):len(s)])
    fig.savefig("top5singular.png")
    
    #print 5 induced sub-graph
    for i in range ((len(s)-5),len(s)):
        top_u = []
        top_vt = []
        u1 = u[:][i]
        vt1 = vt[i][:]
        idxs = u1.argsort()
        
        for j in (idxs):
            if int(numpy.where(idxs == j)[0]) < 100:
                top_u.append(u1[j]) 
                top_vt.append(vt1[j])
       
        induced_matrix = (numpy.asmatrix(top_u).T).dot(numpy.asmatrix(s[i])).dot(numpy.asmatrix(top_vt))
        fig = plt.figure()
        plt.spy(induced_matrix,markersize=2)
        fig.savefig('induced_subgraph_%i'%i) 




#Running the MAIN function
if __name__=="__main__":
    main()

import matplotlib.pylab as plt
import numpy

def main():
    
    #reading all sources and destinations of every edges
    graph = open("assignment_graph.txt", 'r')
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
    unique_degrees, counts_degrees = numpy.unique(degree_array,counts=True)

    print(unique_degrees)
    print(counts_degrees)

    plt.scatter(unique_degrees,counts_degrees)
    plt.xscale('log')
    plt.yscale('log')
    plt.show()
'''
    #spy plot
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
    
    plt.show()
'''
#Running the MAIN function
if __name__=="__main__":
    main()

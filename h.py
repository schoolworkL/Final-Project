def sorter(list):
    for i in range(len(list)-1, 0, -1):
        value = 0
        for j in range(1, i+1):
            if list[j] > list[value]:
                value = j
        print(list)
        list[i], list[value] = list[value], list[i]
    print(list)


# main

courses = ['English', 'Economics', 'Fitness and Weight Training', 'Data Management', 'Calculus and Vectors', 'Canadian and World Politics', 'Computer Science']
sorter(courses)
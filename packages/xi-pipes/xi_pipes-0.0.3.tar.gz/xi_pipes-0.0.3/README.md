# Custom pipes

## Description

This pack has some custom pipes to work with the pipe package.

This package is compatible with python 3.

## Pipes

### reduce

    list1 = [1, 2, 3, 4, 5, 6, 7]
    result = list1 | reduce(lambda a, b: a + b)

    list1 = []
    # raises TypeError
    _ = list1 | reduce(lambda a, b: a + b)

    list1 = [1]
    result = list1 | reduce(lambda a, b: a + b)

### fold

    list1 = [1, 2, 3, 4, 5, 6, 7]
    result = list1 | fold(lambda a, b: a + b, 0)

    list1 = [1, 2, 3, 4, 5, 6, 7]
    result = list1 | fold(lambda a, b: f"{a}/{b}" if a else f"{b}", "")

    list1 = []
    _ = list1 | fold(lambda a, b: f"{a}/{b}" if a else f"{b}", "")

### deep_flatten

    list1 = [[1,2], [3,4]]
    # result is [1, 2, 3, 4]
    result = list(list1 | deep_flatten())

    result = list(1 | deep_flatten())
    # result is [1]

    list1 = [1, 2, 3, 4]
    # result is [1, 2, 3, 4]
    result = list(list1 | deep_flatten())

    list1 = [[1,2], [3, [4, 5]]]
    # result is [1, 2, 3, 4, 5]
    result = list(list1 | deep_flatten())

    list1 = [[1,2], [3, [4, [5, 6]]]]
    # result is [1, 2, 3, 4, 5, 6]
    result = list(list1 | deep_flatten())

### deep_flatmap

    list1:list[int] = [1, 2, 3, 4]
    # result is [2, 3, 4, 5]
    result = list(list1 | deep_flatmap(lambda x: x+1))

    list1 = [[1, 2], [3, 4]]
    # result is [2, 3, 4, 5]
    result = list(list1 | deep_flatmap(lambda x: x+1))

    list1 = [[1, 2], [3, [4]]]
    # result is [2, 3, 4, 5]
    result = list(list1 | deep_flatmap(lambda x: x+1))

    result = list(1 | deep_flatmap(lambda x: x))
    # result is [1]

### flatten

    list1 = [[1, 2], [3, 4]]
    # result is [1, 2, 3, 4]
    result = list(list1 | flatten())

    list1 = [1, 2, 3, 4]
    # raises TypeError
    _ = list(list1 | flatten())

    list1 = [[[1, 2]], [[3, 4]]]
    # result is [[1, 2], [3, 4]]
    result = list(list1 | flatten())

### flatmap

    list1:list = [1, 2, 3, 4]
    # raises TypeError
    _ = list(list1 | flatmap(lambda x: x+1))

    list1 = [[1, 2], [3, [4]]]
    # raises TypeError
    _ = list(list1 | flatmap(lambda x: x+1))

    # raises TypeError
    _ = list(1 | flatmap(lambda x: x+1))

    list1:list = [[1, 2], [3, 4]]
    # result is [2, 3, 4, 5]
    result = list(list1 | flatmap(lambda x: x+1))

### as_dict

    data = [(1, 2), (3, 4)]
    # result {1:2, 3:4}
    result = data | as_dict()

### as_list

    data = range(1, 5)
    # result is = [1, 2, 3, 4]
    result = data | as_list()

### as_set

    data = [1, 2, 3, 4]
    # result {1, 2, 3, 4}
    result = data | as_set()

### split

    data = [1, 2, 3, 4]
    # result is ([2, 4], [1, 3])
    result = data | split(lambda x: x%2==0)

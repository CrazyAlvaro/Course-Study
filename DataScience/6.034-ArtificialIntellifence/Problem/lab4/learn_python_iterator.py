
def myzip(*iterables):
    # zip('ABCD', 'xy') --> Ax By
    sentinel = object()
    print iterables
    iterators = [iter(it) for it in iterables]

    while iterators:
        print iterators
        result = []
        for it in iterators:
            elem = next(it, sentinel)
            if elem is sentinel:
                return
            print "elem: ", elem
            result.append(elem)
            print "result: ", result
        yield tuple(result)

a = [1,2,3]
b = [4,5,6]
print zip(a,b)
print myzip(a,b)
print [x for x in myzip(a,b)]

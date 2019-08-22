

def appendsums(sums):
    """
    Repeatedly append the sum of the current last three elements of the end  of the list
    """
    for i in range(25):
        temp = sums[-1] + sums[-2] + sums[-3]
        sums.append(temp)

if __name__ == "__main__":
    sum_three = [0, 1, 2]
    appendsums( sum_three )
    print sum_three[20]

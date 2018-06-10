import matplotlib.pyplot as plt


def generator(input, weight, max_level, result, level=0):
    if level == 1:
        output = input

        result.append(output)
        level += 1
        generator(input=output, weight=weight, level=level, max_level=max_level, result=result)

    elif level <= max_level:
        output = weight * input - weight * pow(input, 2)
        result.append(output)
        level += 1
        generator(input=output, weight=weight, level=level, max_level=max_level, result=result)

    else:
        return result


if __name__ == '__main__':

    max_level = 50

    results_1 = []
    input_1 = 0.5
    weight_1 = 1
    results_1 = generator(input=input_1, weight=weight_1, max_level=max_level, result=results_1)
    plt.plot(results_1)

    results_2 = []
    input_2 = 0.5
    weight_2 = 3
    results_2 = generator(input=input_2, weight=weight_2, max_level=max_level, result=results_2)
    plt.plot(results_2)

    results_3 = []
    input_3 = 0.0001
    weight_3 = 4
    results_3 = generator(input=input_3, weight=weight_3, max_level=max_level, result=results_3)
    plt.plot(results_3)

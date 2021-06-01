def interpret(values, equation):
    operations = ["^", "*", "/", "+", "-"]
    equation = equation.replace(" ", "")
    simplified_equation = ""
    end = -1
    for i in range(len(equation)):
        char0 = equation[i]
        if char0 == "(" and i > end:
            nest = 0
            for j in range(i+1, len(equation)):
                char1 = equation[j]
                if char1 == "(":
                    nest += 1
                elif char1 == ")":
                    if nest > 0:
                        nest -= 1
                    elif nest == 0:
                        ans = interpret(values, equation[i+1:j])

                        simplified_equation += ans
                        end = j
                        break
        elif i > end:
            simplified_equation += char0

    total_operations_left = 0
    for i in simplified_equation:
        total_operations_left += operations.count(i)
    if total_operations_left > 1:
        for operation in operations:
            for d in range(simplified_equation.count(operation)):
                temp_equation = simplified_equation
                simplified_equation = ""
                temp_obj = ""
                ended = False
                for n in range(len(temp_equation)):
                    if ended:
                        break
                    if operations.count(temp_equation[n]) > 0 and temp_equation[n] != operation:
                        temp_obj += temp_equation[n]
                        simplified_equation += temp_obj
                        temp_obj = ""
                    elif temp_equation[n] == operation:
                        temp_obj += operation
                        for h in range(n+1, len(temp_equation)):
                            if operations.count(temp_equation[h]) > 0:
                                simplified_equation += interpret(values, temp_obj)
                                simplified_equation += temp_equation[h:]

                                ended = True
                                break
                            elif h == len(temp_equation)-1:
                                temp_obj += temp_equation[h]
                                simplified_equation += interpret(values, temp_obj)
                                ended = True
                                break
                            else:
                                temp_obj += temp_equation[h]
                    else:
                        temp_obj += temp_equation[n]

    for value in values:
        values[value] = str(values[value])

    if simplified_equation.count("^") > 0:
        temp_equation_list = simplified_equation.split("^")
        for i in values:
            if temp_equation_list[0].lower() == i: temp_equation_list[0] = values[i]
            if temp_equation_list[1].lower() == i: temp_equation_list[1] = values[i]
        answer = float(temp_equation_list[0]) ** float(temp_equation_list[1])
    elif simplified_equation.count("*")>0:
        temp_equation_list = simplified_equation.split("*")
        for i in values:
            if temp_equation_list[0].lower() == i: temp_equation_list[0] = values[i]
            if temp_equation_list[1].lower() == i: temp_equation_list[1] = values[i]
        answer = float(temp_equation_list[0])*float(temp_equation_list[1])
    elif simplified_equation.count("/")>0:
        temp_equation_list = simplified_equation.split("/")
        for i in values:
            if temp_equation_list[0].lower() == i: temp_equation_list[0]=values[i]
            if temp_equation_list[1].lower() == i: temp_equation_list[1] = values[i]
        answer = float(temp_equation_list[0]) / float(temp_equation_list[1])
    elif simplified_equation.count("+")>0:
        temp_equation_list = simplified_equation.split("+")
        for i in values:
            if temp_equation_list[0].lower() == i: temp_equation_list[0]=values[i]
            if temp_equation_list[1].lower() == i: temp_equation_list[1] = values[i]
        answer = float(temp_equation_list[0]) + float(temp_equation_list[1])
    elif simplified_equation.count("-")>0:
        temp_equation_list = simplified_equation.split("-")
        if "" in temp_equation_list:
            answer = -1*float(temp_equation_list[0]+temp_equation_list[1])
        else:
            for i in values:
                if temp_equation_list[0].lower() == i: temp_equation_list[0]=values[i]
                if temp_equation_list[1].lower() == i: temp_equation_list[1] = values[i]
            answer = float(temp_equation_list[0]) - float(temp_equation_list[1])
    else:
        for i in values:
            if simplified_equation == i:
                simplified_equation = values[i]
        answer = simplified_equation
    return str(answer)

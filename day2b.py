from day2a import *

target = 19690720
# target = 5866663

done = False
for noun in range(100):
    if done:
        break
    for verb in range(100):
        # print("Trying {}, {}".format(noun, verb))
        memory_copy = memory.copy()
        memory_copy[1] = noun
        memory_copy[2] = verb
        try:
            result = run_program(memory_copy)[0]
        except:
            # print("Error")
            continue
        # print("Result ", result)
        if result == target:
            print("Target hit with noun {}, verb {}".format(noun, verb))
            print("Answer:", 100*noun + verb)
            done = True
            break
else:
    print("Target not found")

    
        


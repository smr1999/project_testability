from project.controller import Controller

controller = Controller('all_benchs/c7552.bench',None, None)

controller.add_primay_gates()
controller.add_fanout_gates()

for gate, v in controller.gates.items():
    print(v)
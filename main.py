from project.controllers import Controller



if __name__ == '__main__':
    controller = Controller('all_benchs/c432.bench', 'input_file.txt' , None)

    controller.run()

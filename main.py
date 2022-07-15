from my_def import *


min_time_in = datetime.time(0, 5, 0)  # 5 минут


def main():
    conf_load()
    load_groups("groups.csv")
    load_dir('input/','history/')
    #save_groups("groups.csv", epc_db)


if __name__ == '__main__':
    main()

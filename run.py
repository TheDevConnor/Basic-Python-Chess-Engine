import sys, os
from multiprocessing import Process

def chess_server():
    try:
        os.system(sys.executable + " " + "Chess/ChessServer.py")
    except OSError as e:
        print(e)
    except Exception as ex:
        print(ex)

def chess_main():
    try:
        os.system(sys.executable + " " + "Chess/ChessMain.py")
    except OSError as e:
        print(e)
    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    processes = []
    num_processes = 1

    for i in range(num_processes):
        p1 = Process(target=chess_main)
        p2 = Process(target=chess_server)
        processes.append(p1)
        processes.append(p2)

    for process in processes:
        process.start()
    
    for process in processes:
        process.join()
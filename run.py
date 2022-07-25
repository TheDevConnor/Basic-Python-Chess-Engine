import sys, os
from multiprocessing import Process

def chess_server():
    os.system(sys.executable + " " + "Chess/ChessServer.py")

def chess_main():
    os.system(sys.executable + " " + "Chess/ChessMain.py")

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
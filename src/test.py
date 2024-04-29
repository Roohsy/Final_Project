from fifo import FIFO, execute_fifo
from s3fifo import S3_FIFO, execute_s3_fifo
from gen_rand import gen
import matplotlib.pyplot as plt

def test():
    fifo_result = []
    s3fifo_result = []
    for _ in range(10):
        gen()
        s3 = S3_FIFO(100, 0.1)
        execute_s3_fifo(s3)
        s3fifo_result.append(s3.get_miss_ratio())
        fifo = FIFO(100)
        execute_fifo(fifo)
        fifo_result.append(fifo.get_miss_ratio())
        
    # print(fifo_result)
    # print(s3fifo_result)
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(fifo_result) + 1), fifo_result, label='FIFO Result', marker='o')
    plt.plot(range(1, len(s3fifo_result) + 1), s3fifo_result, label='S3FIFO Result', marker='s')

    plt.title('Comparison of FIFO and S3FIFO Results')
    plt.xlabel('Iterations')
    plt.ylabel('Miss Ratio')

    plt.legend()

    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    test()
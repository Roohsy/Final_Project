### Test correctness
To test the correctness of the algorithm, the following command will read the `toy_test.txt` file in the root dictory. 

The instructions in this file have been carefully designed to ensure that all eviction scenarios are tested.     

You can also write your designed test cases into `toy_test.txt` to test the accuracy of the algorithm.

```
# for testing correctness of fifo
python fifo.py
# for testing correctness of s3fifo
python s3fifo.py
```
### Test Performance
To test the performance of the algorithm, the following commands will randomly generate `10000` instructions, calculate the miss ratio for both `FIFO` and `S3FIFO` algorithms, and repeat this process `10` times.

The results will be used to plot a line gragh.
```
python test.py
```
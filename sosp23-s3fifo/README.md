# Final Project:

Members:
Ziwei Quan
Shuhao Yu

## Setup Environment:
Ubuntu 20.04 LTS 16GB RAM 30GB DISK
VMware Workstation Pro
Windows 10

## External Resources:
zstd (Z-standard)
matplotlib
scikit-learn (optional for flash writes)
lru-dict (optional for flash writes)

### Results for Report:
The folder named project_results.、

It is too big to upload to gradescope. Please check this link for github:

git@github.com:Roohsy/Final_Project.git

## Implement of Experiments:
### Miss ratio：
test: 
```bash
for trace in ${trace_dir}; do
    ./libCacheSim/_build/bin/cachesim ${trace} oracleGeneral FIFO,LRU,ARC,LIRS,TinyLFU,2Q,SLRU,S3FIFO 0 --ignore-obj-size 1;
done
```
plot:
```bash
python3 scripts/libCacheSim/plot_miss_ratio.py --datapath=result/cachesim/
```
### Throughput：
test: 
```bash
# generate Zipf request data of 1 million objects 100 million requests
python3 libCacheSim/scripts/data_gen.py -m 100 -n 20000 --alpha 1.0 --bin-output cachelib/mybench/zipf1.0_1_100.oracleGeneral.bin

git clone https://github.com/Thesys-lab/cachelib-sosp23 cachelib;
cd cachelib/mybench/; 

# turnoff turobo boose and change to performance mode, this is very important for getting consistent results
bash turboboost.sh disable
# you can monitor the CPU freq using this 
# watch -n.1 "cat /proc/cpuinfo | grep \"^[c]pu MHz\" | sort -t : -r -nk 2"

# build cachelib, it takes a few minutes up to one hour
bash build.sh
```
plot:
```bash
python3 scripts/plot_throughput.py
```

### Flash-write：(not success)
```bash
# download traces the zstd files can be changed
wget https://ftp.pdl.cmu.edu/pub/datasets/twemcacheWorkload/cacheDatasets/tencentPhoto/tencent_photo1.oracleGeneral.zst -O tencent_photo1.oracleGeneral.bin.zst
wget https://ftp.pdl.cmu.edu/pub/datasets/twemcacheWorkload/cacheDatasets/wiki/wiki_2019t.oracleGeneral.zst -O wiki_2019t.oracleGeneral.bin.zst

# decompress
zstd -d tencent_photo1.oracleGeneral.bin.zst;
zstd -d wiki_2019t.oracleGeneral.bin.zst;

# calculate the miss ratio and write amplification of FIFO 
./libCacheSim/_build/bin/flash /path/to/data oracleGeneral FIFO 0.1 &

for dram_size_ratio in 0.001 0.01 0.1; do
    # calculate the miss ratio and write amplication of probabilistic admission
    ./libCacheSim/_build/bin/flash /path/to/data oracleGeneral flashProb 0.1 -e "ram-size-ratio=${dram_size_ratio},disk-admit-prob=0.2,disk-cache=fifo"
    # calculate the miss ratio and write amplication when using FIFO filters
    ./libCacheSim/_build/bin/flash /path/to/data oracleGeneral qdlp 0.1 -e "fifo-size-ratio=${dram_size_ratio},main-cache=fifo,move-to-main-threshold=2"
done

# calcualte the miss ratio and write amplification of flashield
# note that this will take more than one day to run, add --logging-interval 100000 to have frequent logging
python3 scripts/flashield/flashield.py /path/to/data --ram-size-ratio=0.001 --disk-cache-type=FIFO --use-obj-size true
python3 scripts/flashield/flashield.py /path/to/data --ram-size-ratio=0.01 --disk-cache-type=FIFO --use-obj-size true
python3 scripts/flashield/flashield.py /path/to/data --ram-size-ratio=0.10 --disk-cache-type=FIFO --use-obj-size true
```
### plot:
```bash
python3 scripts/plot_write_amp.py
```



More detailed instructions can check ./doc/AE.md for operations in libCacheSim




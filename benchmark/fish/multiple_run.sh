RUN_DIR=/home/tseng/Works/benchmark/PizDaint/weak_scaling/FMA_O
OUT_FILE=Perf_Avg

python get_ave_performance_gamer.py -i ${RUN_DIR}/rank0016/Record__Performance -o $OUT_FILE -n   16
python get_ave_performance_gamer.py -i ${RUN_DIR}/rank0032/Record__Performance -o $OUT_FILE -n   32
python get_ave_performance_gamer.py -i ${RUN_DIR}/rank0064/Record__Performance -o $OUT_FILE -n   64
python get_ave_performance_gamer.py -i ${RUN_DIR}/rank0128/Record__Performance -o $OUT_FILE -n  128
python get_ave_performance_gamer.py -i ${RUN_DIR}/rank0256/Record__Performance -o $OUT_FILE -n  256
python get_ave_performance_gamer.py -i ${RUN_DIR}/rank0512/Record__Performance -o $OUT_FILE -n  512
python get_ave_performance_gamer.py -i ${RUN_DIR}/rank1024/Record__Performance -o $OUT_FILE -n 1024
python get_ave_performance_gamer.py -i ${RUN_DIR}/rank2048/Record__Performance -o $OUT_FILE -n 2048

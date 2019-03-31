RUN_DIR=../source/gamer/bin/maxlv7
OUT_FILE=table__merger_average_performance_gamer_res16384

python get_ave_performance_gamer.py -i ${RUN_DIR}/run_node0016/Record__Performance -o $OUT_FILE -n   16
python get_ave_performance_gamer.py -i ${RUN_DIR}/run_node0032/Record__Performance -o $OUT_FILE -n   32
python get_ave_performance_gamer.py -i ${RUN_DIR}/run_node0064/Record__Performance -o $OUT_FILE -n   64
python get_ave_performance_gamer.py -i ${RUN_DIR}/run_node0128/Record__Performance -o $OUT_FILE -n  128
python get_ave_performance_gamer.py -i ${RUN_DIR}/run_node0256/Record__Performance -o $OUT_FILE -n  256
python get_ave_performance_gamer.py -i ${RUN_DIR}/run_node0512/Record__Performance -o $OUT_FILE -n  512
python get_ave_performance_gamer.py -i ${RUN_DIR}/run_node1024/Record__Performance -o $OUT_FILE -n 1024
python get_ave_performance_gamer.py -i ${RUN_DIR}/run_node2048/Record__Performance -o $OUT_FILE -n 2048

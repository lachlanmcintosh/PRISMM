# to run the pipeline just write

# sbatch steps.sh path_length where path length is an integer

for i in $(seq 4 10); do
    sbatch steps.sh $i
done


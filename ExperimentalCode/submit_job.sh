#!/bin/bash
#SBATCH --job-name=mifeng_job        # Job name
#SBATCH --nodelist=hkbugpusrv[06]
#SBATCH --ntasks=40               # Total number of tasks
#SBATCH --cpus-per-task=1         # Number of CPUs per task


# Run the tasks
expr_name="optm_from_param"
task_param="fatality"

for ((i=0; i<$SLURM_NTASKS; i++)); do
    srun --ntasks=1 --exclusive --cpus-per-task=$SLURM_CPUS_PER_TASK --nodes=1 python main.py $i $SLURM_NTASKS "$expr_name" "$task_param" &
done

wait
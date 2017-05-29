#@ job_name = vanHove-U1.0-beta200.0_static_execution_tpri0.000
#@ job_type = MPICH
#@ output = /home/vilardi/Prog/Proj/DMF2RG_simple/run/tests/test_fRG/SCAN_VANHOVE_U4t/vanHove-U1.0-beta200.0_static/execution_tpri0.000//log/$(jobid).extra.out
#@ error  = /home/vilardi/Prog/Proj/DMF2RG_simple/run/tests/test_fRG/SCAN_VANHOVE_U4t/vanHove-U1.0-beta200.0_static/execution_tpri0.000//log/$(jobid).extra.err
#@ node = 1
#@ tasks_per_node = 56
#@ environment = COPY_ALL
#@ notification = complete
#@ notify_user = demi.vilardi@gmail.com
#@ class = 28core
#@ queue

LOG_INFO=/home/vilardi/Prog/Proj/DMF2RG_simple/run/tests/test_fRG/SCAN_VANHOVE_U4t/vanHove-U1.0-beta200.0_static/execution_tpri0.000/job_info
echo $LOADL_PROCESSOR_LIST > $LOG_INFO
echo $LOADL_STEP_ID >> $LOG_INFO
echo $LOADL_JOB_NAME >> $LOG_INFO
. /home/vilardi/.bash_intel

##############################################################
# Execute program
##############################################################
export OMP_NUM_THREADS=56
./dmf2rg_scan --frg --starting-filling 1.00000 --tp 0.00000 --U 1.00000 --beta 200.00000 --no-frequencies --isum 200 --no-self-energy-flow --threshold 0.00000 --threshold-vertex 500.00000
echo END >> $LOG_INFO

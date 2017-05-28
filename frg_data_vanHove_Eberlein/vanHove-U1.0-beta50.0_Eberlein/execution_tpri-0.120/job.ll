#@ job_name = ._vanHove-U1.0-beta50.0_Eberlein_execution_tpri-0.120
#@ job_type = MPICH
#@ output = /home/vilardi/Prog/Proj/DMF2RG_simple/run/tests/test_fRG/SCAN_VANHOVE_U4t/vanHove-U1.0-beta50.0_Eberlein/execution_tpri-0.120//log/$(jobid).extra.out
#@ error  = /home/vilardi/Prog/Proj/DMF2RG_simple/run/tests/test_fRG/SCAN_VANHOVE_U4t/vanHove-U1.0-beta50.0_Eberlein/execution_tpri-0.120//log/$(jobid).extra.err
#@ node = 1
#@ tasks_per_node = 56
#@ environment = COPY_ALL
#@ notification = complete
#@ notify_user = demi.vilardi@gmail.com
#@ class = 28core
#@ queue

LOG_INFO=/home/vilardi/Prog/Proj/DMF2RG_simple/run/tests/test_fRG/SCAN_VANHOVE_U4t/vanHove-U1.0-beta50.0_Eberlein/execution_tpri-0.120/job_info
echo $LOADL_PROCESSOR_LIST > $LOG_INFO
echo $LOADL_STEP_ID >> $LOG_INFO
echo $LOADL_JOB_NAME >> $LOG_INFO
. /home/vilardi/.bash_intel

##############################################################
# Execute program
##############################################################
./dmf2rg_scan --frg --starting-filling 0.34452 --tp -0.12000 --U 1.00000 --beta 50.00000  --cutoff Eberlein --ode-end -80.0 --no-self-energy-flow --threshold 0.00000 --threshold-vertex 300.00000
echo END >> $LOG_INFO

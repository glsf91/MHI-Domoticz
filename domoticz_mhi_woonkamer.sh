#! /bin/bash

cd /home/john/WFRAC

#out=$(python3 mhi.py -json 2>&1)
python3 mhi.py --json <ip-address airco>

exit_status=$?
if [ "${exit_status}" -ne 0 ];
then
    exit ${exit_status}
fi

#echo "output"
#echo $out

exit 0

#!/bin/bash

max_execution=48
actual_execution=1
generated_files=7

while [ $actual_execution -le $max_execution ]; do
    num_out_files=$(ls -l /tmp/monitoring-hosts/paralle | grep ^- | wc -l)
    expected=$(($actual_execution*$generated_files))

    #python monitoring/run.py start -dir <dir> -time 1800
    python monitoring/run.py start -dir /local/nfs/workspace/monitoring-hosts/sample/ -time 1800

    while [ $num_out_files -lt $expected ]; do
        echo "new files?"
        let num_out_files=$(ls -l /tmp/monitoring-hosts/paralle | grep ^- | wc -l)
        sleep 5
    done

    #python monitoring/run.py stop -dir <dir>
    python monitoring/run.py stop -dir /local/nfs/workspace/monitoring-hosts/sample/

    let actual_execution=actual_execution+1

    if [ $actual_execution -le $max_execution ]; then
        sleep 1800
    else
        continue
    fi

done

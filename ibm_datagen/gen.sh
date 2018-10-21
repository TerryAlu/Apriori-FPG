#!/bin/bash 

basename="test_"
dir="../data/"

i=1
no=10
step=10000

echo "Output to ${dir}"
echo "Step: ${step}, Times: ${no}"
echo "Start"

while [ $i -le $no ]
do
    ntrans="$(($i * $step))"
    echo "        $ntrans"
    ./gen lit -ntrans $ntrans -tlen 20 -nitems 100 -npats 100 -fname "${dir}${basename}${ntrans}" > /dev/null
    ((i++))
done

echo "Done"



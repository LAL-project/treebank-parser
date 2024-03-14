#!/bin/bash

LOG_FILE=execution_log
MAIN_FILE=../cli/main.py

SMTW="--SplitMultiwordTokens"
RPM="--RemovePunctuationMarks"
RFW="--RemoveFunctionWords"

function run_test {
	
	# ID name of the test
	local ID=$1
	
	# name of the input file
	local input_file=$2
	
	# name of the local output file to compare the result against
	local output_file=$3
	
	shift 3
	
	# the flags to run the treebank parser with
	local flags=("$@")
	
	local result_file=.hv.$ID.out
	
	#~ echo "Parameters:"
	#~ echo "    ID: $ID"
	#~ echo "    input_file: $input_file"
	#~ echo "    output_file: $output_file"
	#~ echo "    result_file: $result_file"
	#~ echo "    flags: $flags"
	
	if [ ! -f $input_file ]; then
		echo -e "\e[1;4;31mError\e[0m Input file $output_file does not exist"
		return
	fi
	if [ ! -f $output_file ]; then
		echo -e "\e[1;4;31mError\e[0m Base output file $output_file does not exist"
		return
	fi
	
	echo -en "\e[1;1;35mRunning test\e[0m $ID"
	
	# run the program
	python3 $MAIN_FILE -i $input_file -o $result_file --lal --quiet ${flags[@]}
	
	# calculate diff between the outputs
	local DIFF=$(diff $result_file $output_file)
	
	if [ ! -z "$DIFF" ]; then
		echo -n ""
		echo -e "    \e[1;4;31mDifferent outputs\e[0m "
		echo "    See result in $result_file"
		# write output in the execution log
		echo "$(date +"%Y/%m/%d.%T")    Error: when executing test $ID -- Output of test differs from ground truth" >> $LOG_FILE
	else
		echo -e "    \e[1;1;32mOk\e[0m"
		rm -f $result_file
	fi
}

run_test "ca-01-01" "CoNLL-U/inputs/ca-01.conllu" "CoNLL-U/outputs/ca-01-01.hv"	"CoNLL-U" $SMTW
run_test "ca-01-02" "CoNLL-U/inputs/ca-01.conllu" "CoNLL-U/outputs/ca-01-02.hv"	"CoNLL-U" $SMTW $RPM
run_test "ca-01-03" "CoNLL-U/inputs/ca-01.conllu" "CoNLL-U/outputs/ca-01-03.hv"	"CoNLL-U" $SMTW $RFW
run_test "ca-01-04" "CoNLL-U/inputs/ca-01.conllu" "CoNLL-U/outputs/ca-01-04.hv"	"CoNLL-U"
run_test "ca-01-05" "CoNLL-U/inputs/ca-01.conllu" "CoNLL-U/outputs/ca-01-05.hv"	"CoNLL-U" $RPM
run_test "ca-01-06" "CoNLL-U/inputs/ca-01.conllu" "CoNLL-U/outputs/ca-01-06.hv"	"CoNLL-U" $RFW

run_test "ca-02-01" "CoNLL-U/inputs/ca-02.conllu" "CoNLL-U/outputs/ca-02-01.hv"	"CoNLL-U" $SMTW
run_test "ca-02-02" "CoNLL-U/inputs/ca-02.conllu" "CoNLL-U/outputs/ca-02-02.hv"	"CoNLL-U" $SMTW $RPM
run_test "ca-02-03" "CoNLL-U/inputs/ca-02.conllu" "CoNLL-U/outputs/ca-02-03.hv"	"CoNLL-U" $SMTW $RFW
run_test "ca-02-04" "CoNLL-U/inputs/ca-02.conllu" "CoNLL-U/outputs/ca-02-04.hv"	"CoNLL-U" $SMTW $RFW $RPM
run_test "ca-02-05" "CoNLL-U/inputs/ca-02.conllu" "CoNLL-U/outputs/ca-02-05.hv"	"CoNLL-U" $SMTW $RPM $RFW
run_test "ca-02-06" "CoNLL-U/inputs/ca-02.conllu" "CoNLL-U/outputs/ca-02-06.hv"	"CoNLL-U"
run_test "ca-02-07" "CoNLL-U/inputs/ca-02.conllu" "CoNLL-U/outputs/ca-02-07.hv"	"CoNLL-U" $RPM
run_test "ca-02-08" "CoNLL-U/inputs/ca-02.conllu" "CoNLL-U/outputs/ca-02-08.hv"	"CoNLL-U" $RFW
run_test "ca-02-09" "CoNLL-U/inputs/ca-02.conllu" "CoNLL-U/outputs/ca-02-09.hv"	"CoNLL-U" $RPM $RFW

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
	
	local result_file=.out.$ID
	
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
		echo "$(date +"%Y/%m/%d.%T")     Error: when executing test $ID -- Output of test differs from ground truth" >> $LOG_FILE
	else
		echo -e "    \e[1;1;32mOk\e[0m"
		rm -f $result_file
	fi
}

function run_tests {
	local FORMAT=$1
	local LANG=$2
	local ID=$3

	if [ "$FORMAT" == "CoNLL-U" ]; then
		if [ "$LANG" == "ca" ]; then
			if [ "$ID" == "01" ]; then
				run_test "ca-01-01" "CoNLL-U/inputs/ca-01.conllu" "CoNLL-U/outputs/ca-01-01.hv"	"CoNLL-U" $SMTW
				run_test "ca-01-02" "CoNLL-U/inputs/ca-01.conllu" "CoNLL-U/outputs/ca-01-02.hv"	"CoNLL-U" $SMTW $RPM
				run_test "ca-01-03" "CoNLL-U/inputs/ca-01.conllu" "CoNLL-U/outputs/ca-01-03.hv"	"CoNLL-U" $SMTW $RFW
				run_test "ca-01-04" "CoNLL-U/inputs/ca-01.conllu" "CoNLL-U/outputs/ca-01-04.hv"	"CoNLL-U"
				run_test "ca-01-05" "CoNLL-U/inputs/ca-01.conllu" "CoNLL-U/outputs/ca-01-05.hv"	"CoNLL-U" $RPM
				run_test "ca-01-06" "CoNLL-U/inputs/ca-01.conllu" "CoNLL-U/outputs/ca-01-06.hv"	"CoNLL-U" $RFW
			fi

			if [ "$ID" == "02" ]; then
				run_test "ca-02-01" "CoNLL-U/inputs/ca-02.conllu" "CoNLL-U/outputs/ca-02-01.hv"	"CoNLL-U" $SMTW
				run_test "ca-02-02" "CoNLL-U/inputs/ca-02.conllu" "CoNLL-U/outputs/ca-02-02.hv"	"CoNLL-U" $SMTW $RPM
				run_test "ca-02-03" "CoNLL-U/inputs/ca-02.conllu" "CoNLL-U/outputs/ca-02-03.hv"	"CoNLL-U" $SMTW $RFW
				run_test "ca-02-04" "CoNLL-U/inputs/ca-02.conllu" "CoNLL-U/outputs/ca-02-04.hv"	"CoNLL-U" $SMTW $RFW $RPM
				run_test "ca-02-05" "CoNLL-U/inputs/ca-02.conllu" "CoNLL-U/outputs/ca-02-05.hv"	"CoNLL-U" $SMTW $RPM $RFW
				run_test "ca-02-06" "CoNLL-U/inputs/ca-02.conllu" "CoNLL-U/outputs/ca-02-06.hv"	"CoNLL-U"
				run_test "ca-02-07" "CoNLL-U/inputs/ca-02.conllu" "CoNLL-U/outputs/ca-02-07.hv"	"CoNLL-U" $RPM
				run_test "ca-02-08" "CoNLL-U/inputs/ca-02.conllu" "CoNLL-U/outputs/ca-02-08.hv"	"CoNLL-U" $RFW
				run_test "ca-02-09" "CoNLL-U/inputs/ca-02.conllu" "CoNLL-U/outputs/ca-02-09.hv"	"CoNLL-U" $RPM $RFW
				run_test "ca-02-10" "CoNLL-U/inputs/ca-02.conllu" "CoNLL-U/outputs/ca-02-10.hv"	"CoNLL-U" $RFW $RPM
			fi
		fi

		if [ "$LANG" == "es" ]; then
			if [ "$ID" == "01" ]; then
				run_test "es-01-01" "CoNLL-U/inputs/es-01.conllu" "CoNLL-U/outputs/es-01-01.hv"	"CoNLL-U" $SMTW
				run_test "es-01-02" "CoNLL-U/inputs/es-01.conllu" "CoNLL-U/outputs/es-01-02.hv"	"CoNLL-U" $SMTW $RPM
				run_test "es-01-03" "CoNLL-U/inputs/es-01.conllu" "CoNLL-U/outputs/es-01-03.hv"	"CoNLL-U" $SMTW $RFW
				run_test "es-01-04" "CoNLL-U/inputs/es-01.conllu" "CoNLL-U/outputs/es-01-04.hv"	"CoNLL-U" $SMTW $RFW $RPM
				run_test "es-01-05" "CoNLL-U/inputs/es-01.conllu" "CoNLL-U/outputs/es-01-05.hv"	"CoNLL-U" $SMTW $RPM $RFW
				run_test "es-01-06" "CoNLL-U/inputs/es-01.conllu" "CoNLL-U/outputs/es-01-06.hv"	"CoNLL-U"
				run_test "es-01-07" "CoNLL-U/inputs/es-01.conllu" "CoNLL-U/outputs/es-01-07.hv"	"CoNLL-U" $RPM
				run_test "es-01-08" "CoNLL-U/inputs/es-01.conllu" "CoNLL-U/outputs/es-01-08.hv"	"CoNLL-U" $RFW
				run_test "es-01-09" "CoNLL-U/inputs/es-01.conllu" "CoNLL-U/outputs/es-01-09.hv"	"CoNLL-U" $RPM $RFW
				run_test "es-01-10" "CoNLL-U/inputs/es-01.conllu" "CoNLL-U/outputs/es-01-10.hv"	"CoNLL-U" $RFW $RPM
			fi
		fi

		if [ "$LANG" == "en" ]; then
			if [ "$ID" == "01" ]; then
				run_test "en-01-01" "CoNLL-U/inputs/en-01.conllu" "CoNLL-U/outputs/en-01-01.hv"	"CoNLL-U" $SMTW
				run_test "en-01-02" "CoNLL-U/inputs/en-01.conllu" "CoNLL-U/outputs/en-01-02.hv"	"CoNLL-U" $SMTW $RPM
				run_test "en-01-03" "CoNLL-U/inputs/en-01.conllu" "CoNLL-U/outputs/en-01-03.hv"	"CoNLL-U" $SMTW $RFW
				run_test "en-01-04" "CoNLL-U/inputs/en-01.conllu" "CoNLL-U/outputs/en-01-04.hv"	"CoNLL-U" $SMTW $RFW $RPM
				run_test "en-01-05" "CoNLL-U/inputs/en-01.conllu" "CoNLL-U/outputs/en-01-05.hv"	"CoNLL-U" $SMTW $RPM $RFW
				run_test "en-01-06" "CoNLL-U/inputs/en-01.conllu" "CoNLL-U/outputs/en-01-06.hv"	"CoNLL-U"
				run_test "en-01-07" "CoNLL-U/inputs/en-01.conllu" "CoNLL-U/outputs/en-01-07.hv"	"CoNLL-U" $RPM
				run_test "en-01-08" "CoNLL-U/inputs/en-01.conllu" "CoNLL-U/outputs/en-01-08.hv"	"CoNLL-U" $RFW
				run_test "en-01-09" "CoNLL-U/inputs/en-01.conllu" "CoNLL-U/outputs/en-01-09.hv"	"CoNLL-U" $RPM $RFW
				run_test "en-01-10" "CoNLL-U/inputs/en-01.conllu" "CoNLL-U/outputs/en-01-10.hv"	"CoNLL-U" $RFW $RPM
			fi
		fi
	fi
}

all=0
usage=0
format=0
lang=0
id=0

for i in "$@"; do
	case $i in
		
		--help|-h)
		usage=1
		shift
		;;

		--all|-a)
		all=1
		shift
		;;

		--format=*|-f=)
		format="${i#*=}"
		shift
		;;

		--lang=*|-l=)
		lang="${i#*=}"
		shift
		;;
		
		--id=*|-i=)
		id="${i#*=}"
		shift
		;;
		
		*)
		echo -e "\e[1;4;31mError:\e[0m Option $i unknown"
		exit
		;;
	esac
done

if [ $all == 0 ]; then
	echo "$(date +"%Y/%m/%d.%T") Run specific tests: $format $lang $id" >> $LOG_FILE
	run_tests $format $lang $id
	echo "$(date +"%Y/%m/%d.%T") Finished running tests" >> $LOG_FILE
else
	echo "$(date +"%Y/%m/%d.%T") Run all tests" >> $LOG_FILE
	for f in "CoNLL-U"; do
		for l in "ca" "es" "en"; do
			for i in "01" "02"; do
				run_tests $f $l $i
			done
		done
	done
	echo "$(date +"%Y/%m/%d.%T") Finished running tests" >> $LOG_FILE
fi
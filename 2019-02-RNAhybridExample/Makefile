SHELL=/bin/bash

runRNAhybrid:
	RNAhybrid -s 3utr_human -t myRNAs.txt -q myASO.txt

noDiffUT:
	diff <(RNAhybrid -s 3utr_human -t myRNA-cDNAs.txt -q myASO.txt) <(RNAhybrid -s 3utr_human -t myRNAs.txt -q myASO.txt)
	diff <(RNAhybrid -s 3utr_human -t myRNA-cDNAs.txt -q myASO-U.txt) <(RNAhybrid -s 3utr_human -t myRNA-cDNAs.txt -q myASO.txt)

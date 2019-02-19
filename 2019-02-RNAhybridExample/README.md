Example to run RNAhybrid
===

Target file should be the transcript sequence (cDNA sequence).

Query file should be RNA sequence.

Replacing U with T, I observed no difference. In fact, the Ts are replaced by Us by the program. Try `make noDiffUT`

-s affects the p value but not the minimum free energy (MFE) calculation.

I compared the results with the output of Vienna RNAup, using the Turner model (1999), and found good consistency though the numbers do not match exactly (-31.5 versus -27.58 kcal/model for the fully matching pair). The RNAup code is

`RNAup -b -d0 --noLP -P rna_turner1999.par -c 'S' < sequences.fa > RNAup.out`

#!/bin/bash

mkdir -p compiled images compiled_test

for i in sources/*.txt; do
	echo "Compiling: $i"
    fstcompile --isymbols=syms.txt --osymbols=syms.txt $i | fstarcsort > compiled/$(basename $i ".txt").fst
done

for i in tests/inverter_horas_test/*.txt; do
	echo "Compiling: $i"
    fstcompile --isymbols=syms.txt --osymbols=syms.txt $i | fstarcsort > compiled_test/$(basename $i ".txt").fst
done

# TODO 

# text2num FIXME: exemplo vinte e quinze minutos | vinte e quarenta e cinco minutos etc ... problema no vinte ele le o "e" e espera uma duas tres

fstconcat compiled/horas.fst compiled/e.fst > compiled/text2num_aux.fst 
fstconcat compiled/text2num_aux.fst compiled/minutos.fst > compiled/text2num.fst 
rm compiled/text2num_aux.fst

# lazy2num FIXME: exemplo vinte e quinze minutos | vinte e quarenta e cinco minutos etc ... problema no vinte ele le o "e" e espera uma duas tres

fstconcat compiled/horas.fst compiled/lazy.fst > compiled/lazy2num.fst

# num2text FIXME: exemplo vinte e quinze minutos | vinte e quarenta e cinco minutos etc ... problema no vinte ele le o "e" e espera uma duas tres
fstinvert compiled/horas.fst > compiled/invert_horas.fst 
fstinvert compiled/minutos.fst > compiled/invert_minutos.fst 
fstinvert compiled/e.fst > compiled/invert_e.fst 
fstconcat compiled/invert_horas.fst compiled/invert_e.fst > compiled/num2text_aux.fst 
fstconcat compiled/num2text_aux.fst compiled/invert_minutos.fst > compiled/num2text.fst 
rm compiled/invert_horas.fst compiled/invert_minutos.fst compiled/invert_e.fst compiled/num2text_aux.fst 

for i in compiled/*.fst; do
	echo "Creating image: images/$(basename $i '.fst').pdf"
    fstdraw --portrait --isymbols=syms.txt --osymbols=syms.txt $i | dot -Tpdf > images/$(basename $i '.fst').pdf
done

for i in compiled_test/*.fst; do
	echo "Testing the transducer compiled_test/$(basename $i '.fst')"
	fstcompose compiled_test/$(basename $i) compiled/num2text.fst  | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
done

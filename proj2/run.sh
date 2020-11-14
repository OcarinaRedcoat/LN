#!/bin/bash

mkdir -p compiled images compiled_test

for i in sources/*.txt; do
	echo "Compiling: $i"
    fstcompile --isymbols=syms.txt --osymbols=syms.txt $i | fstarcsort > compiled/$(basename $i ".txt").fst
done

for i in tests/lazy2num_test/*.txt; do
	echo "Compiling: $i"
    fstcompile --isymbols=syms.txt --osymbols=syms.txt $i | fstarcsort > compiled_test/$(basename $i ".txt").fst
done

# TODO 

# text2num FIXME: exemplo vinte e quinze minutos | vinte e quarenta e cinco minutos etc ... problema no vinte ele le o "e" e espera uma duas tres

fstconcat compiled/horas.fst compiled/e.fst > compiled/text2num_aux.fst 
fstconcat compiled/text2num_aux.fst compiled/minutos.fst > compiled/text2num.fst 
rm compiled/text2num_aux.fst

# lazy2num FIXME: exemplo vinte e quinze minutos | vinte e quarenta e cinco minutos etc ... problema no vinte ele le o "e" e espera uma duas tres

fstconcat compiled/e.fst compiled/minutos.fst > compiled/eminutos.fst
fstunion compiled/eminutos.fst compiled/lazy.fst > compiled/lazy2num_aux.fst
fstconcat compiled/horas.fst compiled/lazy2num_aux.fst > compiled/lazy2num.fst

# rich2text FIXME: os 20

fstconcat compiled/horas.fst compiled/e.fst | fstproject --project_type=input  > compiled/rich2text_aux.fst 
fstunion compiled/quartos.fst compiled/meias.fst > compiled/rich2text_aux2.fst
fstconcat compiled/rich2text_aux.fst compiled/rich2text_aux2.fst > compiled/rich2text.fst
rm compiled/rich2text_aux.fst compiled/rich2text_aux2.fst

# rich2num
fstcompose compiled/meias.fst compiled/minutos.fst > compiled/rich2num_aux1.fst # talvez um project_type=output
fstcompose compiled/quartos.fst compiled/minutos.fst > compiled/rich2num_aux2.fst
fstunion compiled/rich2num_aux1.fst compiled/rich2num_aux2.fst > compiled/rich2num_aux3.fst
fstunion compiled/minutos.fst compiled/rich2num_aux3.fst > compiled/rich2num_aux4.fst
fstconcat compiled/e.fst compiled/rich2num_aux4.fst > compiled/rich2num_aux5.fst
fstunion compiled/rich.fst compiled/rich2num_aux5.fst > compiled/rich2num_aux6.fst
fstconcat compiled/horas.fst compiled/rich2num_aux6.fst > compiled/rich2num.fst 
rm compiled/rich2num_aux1.fst compiled/rich2num_aux2.fst compiled/rich2num_aux3.fst compiled/rich2num_aux4.fst compiled/rich2num_aux5.fst compiled/rich2num_aux6.fst

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
	fstcompose compiled_test/$(basename $i) compiled/lazy2num.fst  | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
done

rm compiled/* compiled_test/*

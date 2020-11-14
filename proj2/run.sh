#!/bin/bash

mkdir -p compiled images compiled_test

for i in sources/*.txt tests/*.txt; do
	echo "Compiling: $i"
    fstcompile --isymbols=syms.txt --osymbols=syms.txt $i | fstarcsort > compiled/$(basename $i ".txt").fst
done

# text2num

fstconcat compiled/horas.fst compiled/e.fst > compiled/text2num_aux.fst 
fstconcat compiled/text2num_aux.fst compiled/minutos.fst > compiled/text2num.fst 
rm compiled/text2num_aux.fst

# lazy2num 

fstconcat compiled/e.fst compiled/minutos.fst > compiled/eminutos.fst
fstunion compiled/eminutos.fst compiled/lazy.fst > compiled/lazy2num_aux.fst
fstconcat compiled/horas.fst compiled/lazy2num_aux.fst > compiled/lazy2num.fst

# rich2text

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

# num2text 
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

fstcompose compiled/wakeupA_87636.fst compiled/rich2num.fst  | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt | fstdraw --portrait --isymbols=syms.txt --osymbols=syms.txt $i | dot -Tpdf > images/wakeupA_87636.pdf
fstcompose compiled/wakeupB_87636.fst compiled/num2text.fst  | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt | fstdraw --portrait --isymbols=syms.txt --osymbols=syms.txt $i | dot -Tpdf > images/wakeupB_87636.pdf
fstcompose compiled/sleepA_87636.fst compiled/rich2num.fst  | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt | fstdraw --portrait --isymbols=syms.txt --osymbols=syms.txt $i | dot -Tpdf > images/sleepA_87636.pdf
fstcompose compiled/sleepB_87636.fst compiled/num2text.fst  | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt | fstdraw --portrait --isymbols=syms.txt --osymbols=syms.txt $i | dot -Tpdf > images/sleepB_87636.pdf

fstcompose compiled/wakeupC_87699.fst compiled/rich2num.fst  | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt | fstdraw --portrait --isymbols=syms.txt --osymbols=syms.txt $i | dot -Tpdf > images/wakeupC_87699.pdf
fstcompose compiled/wakeupD_87699.fst compiled/num2text.fst  | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt | fstdraw --portrait --isymbols=syms.txt --osymbols=syms.txt $i | dot -Tpdf > images/wakeupD_87699.pdf
fstcompose compiled/sleepC_87699.fst compiled/rich2num.fst  | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt | fstdraw --portrait --isymbols=syms.txt --osymbols=syms.txt $i | dot -Tpdf > images/sleepC_87699.pdf
fstcompose compiled/sleepD_87699.fst compiled/num2text.fst  | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt | fstdraw --portrait --isymbols=syms.txt --osymbols=syms.txt $i | dot -Tpdf > images/sleepD_87699.pdf

from Bio.SeqUtils.ProtParam import ProteinAnalysis
import csv

f = open('shuffled_vaccines.txt', 'r')
seqList = f.read().splitlines()
f.close()
result = {}

for seq in seqList:
    instabilityIndex = ProteinAnalysis(seq).instability_index()
    if (instabilityIndex < 40):
        result[seq] = instabilityIndex
    
sortedByStability = sorted(result.items(), key=lambda x:x[1], reverse=False)
print(sortedByStability)

f = open('sortedByProtParamStability.csv', 'w')
writer = csv.writer(f)
writer.writerow(['sequence', 'Instability Index'])
for seq in sortedByStability:
    writer.writerow([seq[0], round(seq[1],2)])

f.close()
print(len(sortedByStability))


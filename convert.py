# read "working/titles.txt" which is tab-separated file with pmid and title, and create dict mapping from pmid to title
import math
file = open("working/titles.txt", "rt")
lines = file.readlines()
file.close()

pmid_title = {}
for line in lines:
    line = line.strip()
    if line:
        try:
            pmid, title = line.split("\t")
        except ValueError:
            print("Error:", line)
            continue
        pmid_title[pmid] = title

# read "abstracts_classfied.sorted.tsv" which is TSV with pmid, pheno_classification, pheno log_prob, org_classification, org log_prob and iterate through it
# building a list which will be output to a JSON file

file = open("working/abstracts_classified.sorted.tsv", "rt")
outputs = []
pmids = set()
for line in file:
    line = line.strip()
    if line:
        pmid, pheno_classification, pheno_log_prob, org_classification, org_log_prob = line.split("\t")
        if pmid in pmid_title:
            print(org_classification)
            if org_classification=="fal":
                org_classification="P. falciparum"
            elif org_classification=="berg":
                org_classification="P. berghei"

            title = pmid_title[pmid]
            # convert pheno log_prob to percentage probability
            pheno_log_prob = float(pheno_log_prob)
            pheno_prob = round(math.exp(pheno_log_prob) * 100, 2)
            # convert org log_prob to percentage probability
            org_log_prob = float(org_log_prob)
            org_prob = round(math.exp(org_log_prob) * 100, 2)
            if pheno_classification == "phenotype" and pmid not in pmids:
                output = {"title": title, "pmid":int(pmid), "pheno_conf": pheno_prob,"organism":org_classification, "org_conf": org_prob}
                outputs.append(output)
                pmids.add(pmid)
file.close()

# write outputs to app/public/output.json
file = open("app/public/output.json", "wt")
import json
# sort outputs by pmid
outputs = sorted(outputs, key=lambda k: k['pmid'])
file.write(json.dumps(outputs))
file.close()
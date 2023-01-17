import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

fec = pd.read_csv('https://github.com/benrolfs/pydata/raw/master/ch09/P00000001-ALL.csv', low_memory=False)

unique_cands = fec['cand_nm'].unique()

parties = {"Bachmann, Michelle": "Republican",
           "Cain, Herman": "Republican",
           "Gingrich, Newt": "Republican",
           "Huntsman, Jon": "Republican",
           "Johnson, Gary Earl": "Republican",
           "McCotter, Thaddeus G": "Republican",
           "Obama, Barack": "Democrat",
           "Paul, Ron": "Republican",
           "Pawlenty, Timothy": "Republican",
           "Perry, Rick": "Republican",
           "Roemer, Charles E. 'Buddy' III": "Republican",
           "Romney, Mitt": "Republican",
           "Santorum, Rick": "Republican"
           }

fec['party'] = fec["cand_nm"].map(parties)

# donazioni per partito
print(fec['party'].value_counts())

# numero rimborsi
print((fec['contb_receipt_amt'] > 0).value_counts())

# filtriamo via i rimborsi direttamente
fec = fec[fec['contb_receipt_amt'] > 0]

# statistiche relative soltanto ad Obama e Romney
fec_main = fec[fec['cand_nm'].isin(['Obama, Barack', 'Romney, Mitt'])]
print(fec_main['cand_nm'].value_counts())
print((fec_main['contb_receipt_amt'] > 0).value_counts())

# statistiche sugli impieghi dei donatori
occ_mapping = {"INFORMATION REQUESTED PER BEST EFFORTS": "NOT PROVIDED",
               "INFORMATION REQUESTED": "NOT PROVIDED",
               "INFORMATION REQUESTED (BEST EFFORTS)": "NOT PROVIDED",
               "C.E.O.": "CEO"
               }


def get_occ(x):
    return occ_mapping.get(x, x)


fec['contbr_occupation'] = fec['contbr_occupation'].map(get_occ)
print(fec["contbr_occupation"].value_counts()[:10])

by_occupation = fec.pivot_table("contb_receipt_amt",
                                index="contbr_occupation",
                                columns="party", aggfunc="sum")

print(by_occupation)

over_2mm = by_occupation[by_occupation.sum(axis="columns") > 2_000_000]

over_2mm.plot(figsize=(12, 4), kind="barh")
plt.show()


def get_top_amounts(group, key, n=5):
    totalss = group.groupby(key)["contb_receipt_amt"].sum()
    return totalss.nlargest(n)


grouped = fec_main.groupby("cand_nm")
print(grouped.apply(get_top_amounts, "contbr_employer", n=7))

bins = np.array([0, 1, 10, 100, 1000, 10000, 100_000, 1_000_000, 10_000_000])

labels = pd.cut(fec_main['contb_receipt_amt'], bins)

grouped = fec_main.groupby(['cand_nm', labels])
print(grouped.size().unstack(level=0))

bucket_sums = grouped['contb_receipt_amt'].sum().unstack(level=0)

normed_sums = bucket_sums.div(bucket_sums.sum(axis='columns'), axis='index')
print(normed_sums)

normed_sums[:-2].plot(kind='barh')
plt.show()

totals = grouped['contb_receipt_amt'].sum().unstack(level=0)
print(totals)
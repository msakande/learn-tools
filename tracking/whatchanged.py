import pandas as pd
import get_changes as a
import os
# git changes summary
# fix truncation
pd.set_option('display.max_colwidth', 500)

# change these as needed
repo_path = "C:/GitPrivate/fabric-docs-pr"
author = 'Sheri Gilley' # leave blank for all; only use for a single month!
since = '09/01/2023'
until = '04/11/2024'

output = a.get_changes(repo_path, author, since, until)
if author == '':
    results = [line for line in output.split('\n') if "machine-learning" in line and line.strip()]
else:
    results = [line for line in output.split('\n') if line.strip()]
changes = pd.DataFrame([line.split() for line in results])
# now only want columns 4 and beyond.  For some reason, sometimes there is a 7th col. 
changes = changes.iloc[:, 4:]
extra_col = False
# name the columns
if changes.shape[1] == 3:
    changes.columns = ['ChangeType', 'Filename', 'Filename2']
    extra_col = True
    print ("Extra columns found")
else:
    changes.columns = ['ChangeType', 'Filename']

if extra_col:
    # some lines had two filenames, split them out and then append them to the unique list
    extra = changes[changes['Filename2'].notnull()][['ChangeType','Filename2']].copy()
    # now drop filename2 from changes
    changes = changes[['ChangeType','Filename']]
    # Rename 'Filename2' to 'Filename' in extra
    extra = extra.rename(columns={'Filename2': 'Filename'})
    # Append extra to changes
    # print(f'changes {type(changes)} extra {type(extra)}')
    # print(f'changes {changes.shape} extra {extra.shape}')
    # changes = pd.concat([changes, extra])

# find the unique filename/type combos
unique = changes.drop_duplicates().copy()
unique['FileType'] = unique['Filename'].apply(lambda x: os.path.splitext(x)[1])

# show counts for unique files
if author == '':
    print(f"*** Changes in {repo_path} from {since} to {until} *** ")
else:
    print(f"*** Changes in {repo_path} by {author} from {since} to {until} ***")

print(pd.crosstab(index=unique['ChangeType'], columns=unique['FileType']))

# show the added files
# print("Added:")
# print(unique[(unique['FileType'] == ".md") & (unique['ChangeType'] == 'A')]['Filename'])

# show the deleted files
# print("Deleted:")
# print(unique[(unique['FileType'] == ".md") & (unique['ChangeType'] == 'D')]['Filename'])


# check out some stats 

# some imports 
from pathlib import Path
from pathlib import PurePath
import pandas as pd
import datetime


# define the file location 
input_path = r'/Users/benmoretti/Development/electric-newspaper-archive/electric_newspaper'

# get a dataframe of file paths
p = Path(input_path)
files_df = pd.DataFrame(p.glob('**/*'))
files_df.rename(columns={0:'Path'}, inplace=True)

# things to find
# 
# categorise based on file extenson - story, index, graphic
# read the date 
# determine the topic based on file path

def get_mod_date(path_string):
    """gets the modified time for the file"""
    p = Path(path_string)
    return(datetime.datetime.fromtimestamp(p.stat().st_mtime))


def get_topic(path_string, index_point):
    """works out the topic of a file based on its file path"""
    try:
        ppath = PurePath(path_string)
        path_elements = ppath.parts
        topic = path_elements[index_point]
        topic = topic.title()
        return(topic)
    except:
        return("Error")

# assign the topic for each 
files_df['Topic'] = files_df.apply(lambda row: get_topic(row['Path'], 6), axis=1)

# see if its a directory
files_df['Is_Dir'] = files_df.apply(lambda row: Path(row['Path']).is_dir(), axis=1)

# see if its a file
files_df['Is_File'] = files_df.apply(lambda row: Path(row['Path']).is_file(), axis=1)

# get the date
files_df['Mod_date'] = files_df.apply(lambda row: get_mod_date(row['Path']), axis=1)

# get the file suffix
files_df['Suffix'] = files_df.apply(lambda row: PurePath(row['Path']).suffix, axis=1)

# get the file stem
files_df['Stem'] = files_df.apply(lambda row: PurePath(row['Path']).stem, axis=1)



# list the non index files with HTM suffix
stories_df = files_df[(files_df['Stem'] != 'INDEX') & (files_df['Is_File'] == True) & (files_df['Suffix'] == '.HTM')]

stories_df.to_csv(path_or_buf="../data/stories.csv", index=False)
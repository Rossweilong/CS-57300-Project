import sys
import pandas as pd
sys.path.append("/Documents/Purdue/CS573/project/youtube_tutorial/")
from youtube_videos import youtube_search,youtube_search_with_stats
import json

video_search_result_file = './video_search_result.json'
# video_dict = {'youID':[], 'title':[], 'pub_date':[],'description':[]}
video_dict = json.load(open(video_search_result_file))
# curr_len = len(video_dict['youID'])
# def grab_videos(keyword, token=None):
# 	print('category is:', keyword)
# 	res = youtube_search(keyword,token = token)
# 	token = res[0]
# 	videos = res[1]
# 	for vid in videos:
# 		video_dict['youID'].append(vid['id']['videoId'])
# 		video_dict['title'].append(vid['snippet']['title'])
# 		video_dict['pub_date'].append(vid['snippet']['publishedAt'])
# 		video_dict['description'].append(vid['snippet']['description'])
# 	print ("added " + str(len(videos)) + " videos to a total of " + str(len(video_dict['youID'])))
# 	return token,len(videos)

# token,v_len = grab_videos('nature')
# # token = 'CJADEAA'
# while token !='last_page':
# 	token,v_len = grab_videos('nature',token = token)
# 	if len(video_dict['youID'])-curr_len>=1000 or v_len ==0:
# 		break
# # print(token)


# with open(video_search_result_file, 'w') as fout:
#     json.dump(video_dict, fout)
# # video_dict = json.load(open(video_search_result_file))
# test = set(video_dict['youID'])
# print(len(test))
# # print(video_dict['youID'][-100:])



test = {}
test['results']=[]
for i in range(0,len(video_dict['youID']),50):
	print(i)
	start = i
	end = min(i+50,len(video_dict['youID']))
	results = youtube_search_with_stats(video_dict['youID'][start:end])
	for result in results:
		test["results"].append(result)

video_stats_file = './video_stats_with_id_more_columns_with_description.json'
with open(video_stats_file, 'w') as fout:
    json.dump(test, fout)

stats = json.load(open(video_stats_file))
stats_data = stats['results']
df_video_dict = pd.DataFrame.from_dict(video_dict,orient = 'columns')
df_stats = pd.DataFrame.from_dict(stats_data,orient = 'columns')

# print(df_video_dict[:10])
# print(df_stats[:10])

df_video_dict = df_video_dict.rename(columns = {"youID":"id"})
# print(df_video_dict[:10])

df_joined = pd.merge(df_video_dict, df_stats, on='id', how='inner')

df_joined.sort_values('id',inplace = True)
df_joined.drop_duplicates(subset = 'id',keep = 'first', inplace = True)


outfile = './youtube_data_newer.csv'
df_joined.to_csv(outfile)

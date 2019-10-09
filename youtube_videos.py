from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

DEVELOPER_KEY = "AIzaSyCFXGoHxKpjCBdJKX2g-0_9SBBCnzkdviQ"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def youtube_search_with_stats(v_ids):
  vid_str = ",".join(v_ids)
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  search_request = youtube.videos().list(
    part = "id, statistics, snippet,contentDetails",
    id = vid_str
    )
  search_response = search_request.execute()
  videos = []
  for search_result in search_response.get("items",[]):
    content = {}
    if 'description' in search_result['snippet']:
      content['video_description'] = search_result['snippet']['description']
    else:
      content['video_description'] = ''
    if 'categoryId' in search_result['snippet']:
      content['categoryId'] = search_result['snippet']['categoryId']
    else:
      content['categoryId'] = ''
    if 'defaultLanguage' in search_result['snippet']:
      content['defaultLanguage'] = search_result['snippet']['defaultLanguage']
    else:
      content['defaultLanguage'] = ''
    if 'viewCount' in search_result['statistics']:
      content['viewCount'] = search_result['statistics']['viewCount']
    else:
      content['viewCount']=0
    if 'likeCount' in search_result['statistics']:  
      content['likeCount'] = search_result['statistics']['likeCount']
    else:
      content['likeCount']=0
    if 'dislikeCount' in search_result['statistics']:  
      content['dislikeCount']=search_result['statistics']['dislikeCount']
    else:
      content['dislikeCount']=0
    if 'commentCount' in search_result['statistics']:
      content['commentCount']=search_result['statistics']['commentCount']
    else:
      content['commentCount']=0
    if 'tags' in search_result['snippet']:
      content['tags'] = search_result['snippet']['tags']
    else:
      content['tags'] = []
    if 'id' in search_result:
      content['id'] = search_result['id']
    else:
      content['id'] = ''
    if 'duration' in search_result['contentDetails']:
      content['duration'] = search_result['contentDetails']['duration']
    else:
      content['duration'] = 0
    if 'dimension' in search_result['contentDetails']:
      content['dimension'] = search_result['contentDetails']['dimension']
    else:
      content['dimension'] = ''
    if 'definition' in search_result['contentDetails']:
      content['definition'] = search_result['contentDetails']['definition']
    else:
      content['definition'] = ''
    if 'caption' in search_result['contentDetails']:
      content['caption'] = search_result['contentDetails']['caption']
    else:
      content['caption'] = ''
    if 'hasCustomThumbnail' in search_result['contentDetails']:
      content['hasCustomThumbnail'] = search_result['contentDetails']['hasCustomThumbnail']
    else:
      content['hasCustomThumbnail'] = ''
    videos.append(content)
  return videos

def youtube_search(q, max_results=50,order="relevance", token=None, location=None, location_radius=None):

  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  search_response = youtube.search().list(
    q=q,
    type="video",
    pageToken=token,
    order = order,
    part="id,snippet",
    maxResults=max_results,
    location=location,
    locationRadius=location_radius

  ).execute()

  print('input token is: ', token)


  videos = []

  for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
      videos.append(search_result)
  try:
      nexttok = search_response["nextPageToken"]
      print('return token: ',nexttok)
      return(nexttok, videos)
  except Exception as e:
      nexttok = "last_page"
      return(nexttok, videos)


def geo_query(video_id):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    video_response = youtube.videos().list(
        id=video_id,
        part='snippet, recordingDetails, statistics'

    ).execute()

    return video_response



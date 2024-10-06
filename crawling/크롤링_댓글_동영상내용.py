import googleapiclient.discovery
import pandas as pd

# YouTube API 설정
api_key = 'YOUR_API_KEY'
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

# 유튜버 구독자 수 가져오기
def get_channel_details(channel_id):
    request = youtube.channels().list(
        part="statistics,snippet",
        id=channel_id
    )
    response = request.execute()
    
    # 구독자 수, 채널 이름 추출
    subscriber_count = response['items'][0]['statistics'].get('subscriberCount', 0)
    channel_name = response['items'][0]['snippet']['title']
    
    return {
        'channel_name': channel_name,
        'subscriber_count': int(subscriber_count)
    }

# 유튜버의 최신 10개 동영상 수집
def get_latest_videos(channel_id, max_videos=10):
    request = youtube.search().list(
        part="id,snippet",
        channelId=channel_id,
        maxResults=max_videos,
        order="date",
        type="video"
    )
    response = request.execute()
    
    video_data = []
    for item in response['items']:
        video_id = item['id']['videoId']
        title = item['snippet']['title']
        description = item['snippet']['description']
        published_date = item['snippet']['publishedAt']
        video_data.append({
            'video_id': video_id,
            'title': title,
            'description': description,
            'published_date': published_date
        })
    
    return video_data

# 각 동영상의 조회수, 좋아요 수, 댓글 최대 100개 수집
def get_video_details(video_id, max_comments=100):
    # 동영상 상세 정보 가져오기 (조회수, 좋아요 수 등)
    video_request = youtube.videos().list(
        part="statistics",
        id=video_id
    )
    video_response = video_request.execute()
    view_count = video_response['items'][0]['statistics'].get('viewCount', 0)
    like_count = video_response['items'][0]['statistics'].get('likeCount', 0)
    
    # 댓글 가져오기
    comments_request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=max_comments,
        order="relevance"
    )
    comments_response = comments_request.execute()
    
    comments = []
    for comment in comments_response['items']:
        comment_text = comment['snippet']['topLevelComment']['snippet']['textDisplay']
        comment_likes = comment['snippet']['topLevelComment']['snippet'].get('likeCount', 0)
        comment_date = comment['snippet']['topLevelComment']['snippet'].get('publishedAt', '')
        comments.append({
            'comment_text': comment_text,
            'comment_likes': comment_likes,
            'comment_date': comment_date
        })
    
    return {
        'view_count': int(view_count),
        'like_count': int(like_count),
        'comments': comments  # 댓글 리스트 저장
    }

# 유튜버의 채널 ID로 최신 10개 동영상 데이터와 댓글 수집
def collect_youtuber_data(channel_id):
    # 채널 세부 정보 (구독자 수 포함)
    channel_info = get_channel_details(channel_id)
    
    # 최신 동영상 수집
    videos = get_latest_videos(channel_id)
    
    all_video_data = []
    
    for video in videos:
        video_id = video['video_id']
        video_details = get_video_details(video_id)
        video.update(video_details)  # 동영상 데이터에 조회수, 좋아요 수 등 추가
        all_video_data.append(video)
    
    return {
        'channel_info': channel_info,
        'videos': all_video_data
    }

# 데이터프레임으로 저장 (유튜버 ID -> 동영상 ID -> 댓글 구조로)
def save_to_dataframe(channel_id, file_name='youtuber_data.csv'):

    # 데이터 수집
    data = collect_youtuber_data(channel_id)
    channel_info = data['channel_info']
    video_data = data['videos']
    
    # 전체 데이터 저장용 리스트
    structured_data = []
    
    # 각 동영상에 대한 댓글을 포함한 데이터 정리
    for video in video_data:
        for comment in video['comments']:
            structured_data.append({
                'channel_name': channel_info['channel_name'],
                'subscriber_count': channel_info['subscriber_count'],
                'video_id': video['video_id'],
                'video_title': video['title'],
                'video_description': video['description'],
                'published_date': video['published_date'],
                'view_count': video['view_count'],
                'like_count': video['like_count'],
                'comment_text': comment['comment_text'],
                'comment_likes': comment['comment_likes'],
                'comment_date': comment['comment_date']
            })
    
    # 데이터프레임으로 변환
    df = pd.DataFrame(structured_data)
    
    # CSV 파일로 저장
    df.to_csv(file_name, index=False, encoding='utf-8-sig')
    print(f"Data saved to {file_name}")

# 예시: 유튜버 채널 ID로 데이터프레임 저장
channel_id = 'YOUR_CHANNEL_ID'  # 유튜버 채널 ID 입력
save_to_dataframe(channel_id, 'youtuber_data.csv')

# 저장된 데이터프레임을 확인하고 싶다면
df = pd.read_csv('youtuber_data.csv')
print(df.head())


# 동영상 내용(자막)도 같이 추출해야 함

#%% 유튜브 댓글 크롤링
import googleapiclient.discovery
import pandas as pd

# YouTube API 설정
api_key = 'AIzaSyDnyKNHP_JAlKdWwWNSaQb7p2Fer1g5mj8'
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

# 유튜버 구독자 수 가져오기
def get_channel_details(channel_id):
    request = youtube.channels().list(
        part="statistics,snippet",
        id=channel_id
    )
    response = request.execute()
    
    # 구독자 수, 채널 이름 추출
    subscriber_count = response['items'][0]['statistics'].get('subscriberCount', 0)
    channel_name = response['items'][0]['snippet']['title']
    
    return {
        'channel_name': channel_name,
        'subscriber_count': int(subscriber_count)
    }

# 유튜버의 최신 10개 동영상 수집
def get_latest_videos(channel_id, max_videos=10):
    request = youtube.search().list(
        part="id,snippet",
        channelId=channel_id,
        maxResults=max_videos,
        order="date",
        type="video"
    )
    response = request.execute()
    
    video_data = []
    for item in response['items']:
        video_id = item['id']['videoId']
        title = item['snippet']['title']
        description = item['snippet']['description']
        published_date = item['snippet']['publishedAt']
        video_data.append({
            'video_id': video_id,
            'title': title,
            'description': description,
            'published_date': published_date
        })
    
    return video_data

# 동영상 자막(캡션) 가져오기
def get_video_subtitles(video_id):
    # 자막 리스트 가져오기
    try:
        captions_request = youtube.captions().list(
            part="snippet",
            videoId=video_id
        )
        captions_response = captions_request.execute()
        
        # 사용할 수 있는 자막 ID 검색
        if 'items' in captions_response and captions_response['items']:
            caption_id = captions_response['items'][0]['id']  # 첫 번째 자막 사용
            # 자막 다운로드
            subtitle_request = youtube.captions().download(
                id=caption_id,
                tfmt="srt"  # SRT 포맷으로 다운로드
            )
            subtitle_response = subtitle_request.execute()
            subtitles = subtitle_response.decode('utf-8')
            return subtitles
        else:
            return None
    except Exception as e:
        print(f"Error fetching subtitles for video {video_id}: {e}")
        return None

# 각 동영상의 조회수, 좋아요 수, 댓글, 자막 수집
def get_video_details(video_id, max_comments=100):
    # 동영상 상세 정보 가져오기 (조회수, 좋아요 수 등)
    video_request = youtube.videos().list(
        part="statistics",
        id=video_id
    )
    video_response = video_request.execute()
    view_count = video_response['items'][0]['statistics'].get('viewCount', 0)
    like_count = video_response['items'][0]['statistics'].get('likeCount', 0)
    
    # 자막 가져오기
    subtitles = get_video_subtitles(video_id)
    
    # 댓글 가져오기
    comments_request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=max_comments,
        order="relevance"
    )
    comments_response = comments_request.execute()
    
    comments = []
    for comment in comments_response['items']:
        comment_text = comment['snippet']['topLevelComment']['snippet']['textDisplay']
        comment_likes = comment['snippet']['topLevelComment']['snippet'].get('likeCount', 0)
        comment_date = comment['snippet']['topLevelComment']['snippet'].get('publishedAt', '')
        comments.append({
            'comment_text': comment_text,
            'comment_likes': comment_likes,
            'comment_date': comment_date
        })
    
    return {
        'view_count': int(view_count),
        'like_count': int(like_count),
        'subtitles': subtitles,  # 자막 추가
        'comments': comments  # 댓글 리스트 저장
    }

# 유튜버의 채널 ID로 최신 10개 동영상 데이터와 댓글 수집
def collect_youtuber_data(channel_id):
    # 채널 세부 정보 (구독자 수 포함)
    channel_info = get_channel_details(channel_id)
    
    # 최신 동영상 수집
    videos = get_latest_videos(channel_id)
    
    all_video_data = []
    
    for video in videos:
        video_id = video['video_id']
        video_details = get_video_details(video_id)
        video.update(video_details)  # 동영상 데이터에 조회수, 좋아요 수 등 추가
        all_video_data.append(video)
    
    return {
        'channel_info': channel_info,
        'videos': all_video_data
    }

# 데이터프레임으로 저장 (유튜버 ID -> 동영상 ID -> 댓글 및 자막 구조로)
def save_to_dataframe(channel_id, file_name='youtuber_data_with_subtitles.csv'):

    # 데이터 수집
    data = collect_youtuber_data(channel_id)
    channel_info = data['channel_info']
    video_data = data['videos']
    
    # 전체 데이터 저장용 리스트
    structured_data = []
    
    # 각 동영상에 대한 댓글 및 자막을 포함한 데이터 정리
    for video in video_data:
        subtitles = video.get('subtitles', None)
        for comment in video['comments']:
            structured_data.append({
                'channel_name': channel_info['channel_name'],
                'subscriber_count': channel_info['subscriber_count'],
                'video_id': video['video_id'],
                'video_title': video['title'],
                'video_description': video['description'],
                'published_date': video['published_date'],
                'view_count': video['view_count'],
                'like_count': video['like_count'],
                'subtitles': subtitles,  # 자막 추가
                'comment_text': comment['comment_text'],
                'comment_likes': comment['comment_likes'],
                'comment_date': comment['comment_date']
            })
    
    # 데이터프레임으로 변환
    df = pd.DataFrame(structured_data)
    
    # CSV 파일로 저장
    df.to_csv(file_name, index=False, encoding='utf-8-sig')
    print(f"Data saved to {file_name}")

# 예시: 유튜버 채널 ID로 데이터프레임 저장
channel_id = 'YOUR_CHANNEL_ID'  # 유튜버 채널 ID 입력
save_to_dataframe(channel_id, 'youtuber_data_with_subtitles.csv')

# 저장된 데이터프레임을 확인하고 싶다면
df = pd.read_csv('youtuber_data_with_subtitles.csv')
print(df.head())

import os
import googleapiclient.discovery
import isodate
from datetime import timedelta


class YoutubeSearch:
    youtube_query = 'https://www.youtube.com/watch?v='
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyDBJ0Eyt_Ve2egl2wTLNO5ABS2NUuY8Res"
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)
    part_string = 'contentDetails, snippet'

    def process_ids(self, n, ids):
        request = self.youtube.videos().list(
            part=self.part_string,
            id=ids,
        )
        response = request.execute()['items'][0]
        id_ = response["id"]
        title = response["snippet"]["title"]
        duration = str(isodate.parse_duration(response["contentDetails"]["duration"]))
        if len(title) > 61:
            title = title[:58] + '...'
        return {"number": n+1, "id": id_, "title": title, "duration": duration}

    def get_id(self, request, only_id=False):
        response = request.execute()
        links = list()
        if only_id:
            item = response.get('items')[0]['id']['videoId']
            links.append(self.youtube_query + item)
        else:
            for n, item in enumerate(response.get('items')):
                links.append(self.process_ids(n, item["id"]["videoId"]))
        return links

    def search(self, search: str):
        request = self.youtube.search().list(
            part="snippet",
            type="video",
            maxResults=5,
            q=search
        )
        return self.get_id(request)

    def get_song(self, name: str):
        request = self.youtube.search().list(
            part='snippet',
            type='video',
            maxResults=1,
            q=name
        )
        link = self.get_id(request, only_id=True)
        return link[0]


# Teste
# too = YoutubeSearch()
# too.get_song('pinto')


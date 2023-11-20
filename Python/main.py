import requests

caption = 'Test image posting'
url = 'https://i1.sndcdn.com/artworks-000177387984-ncd92i-t500x500.jpg'
url2 = 'https://images.unsplash.com/11/berries.jpg?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=1080'

access_token1 = 'secret access token 1'
access_token2 = 'secret access token 2'
access_url = 'FB access url'
client_id = 'client id'
client_secret = 'client secret'

graph_url = 'https://graph.facebook.com/v18.0/'

scope = 'publish_pages,business_management,ads_management,pages_show_list,pages_read_engagement,pages_manage_metadata,pages_read_user_content,pages_manage_ads,pages_manage_posts,pages_manage_engagement,instagram_basic,instagram_content_publish,instagram_manage_insights,instagram_manage_comments',


def post_image(caption='', image_url='', instagram_account_id='', access_token='', page_id=0):
    url = graph_url + instagram_account_id + '/media'
    param = dict()
    param['access_token'] = access_token
    param['caption'] = caption
    param['image_url'] = image_url
    # param['location_id'] = page_id
    response = requests.post(url, params=param)
    response = response.json()
    return response


def publish_container(creation_id='', instagram_account_id='', access_token=''):
    url = graph_url + instagram_account_id + '/media_publish'
    param = dict()
    param['access_token'] = access_token
    param['creation_id'] = creation_id
    response = requests.post(url, params=param)
    response = response.json()
    return response


def post_video(video_url='', caption='', instagram_account_id='', access_token=''):
    url = graph_url + instagram_account_id + '/media'
    param = dict()
    param['access_token'] = access_token
    param['caption'] = caption
    param['video_url'] = video_url
    param['media_type'] = 'VIDEO'
    param['thumb_offset'] = '10'
    response = requests.post(url, params=param)
    response = response.json()
    return response


def post_carousel(caption='', media_url='', instagram_account_id='', access_token=''):
    url = graph_url + instagram_account_id + '/media'
    param = dict()
    param['access_token'] = access_token
    param['is_carousel_item'] = 'true'
    container_id = []
    for i in media_url:
        param['image_url'] = i
        response = requests.post(url, params=param)
        response = response.json()
        container_id.append(response['id'])
    carousel_container_id = make_carousel_container(container_id=container_id, caption=caption,
                                                    access_token=access_token,
                                                    instagram_account_id=instagram_account_id)
    return carousel_container_id


def make_carousel_container(container_id='', caption='', access_token='', instagram_account_id=''):
    url = graph_url + instagram_account_id + '/media'
    container_id = ','.join(container_id)
    param = dict()
    print(container_id)
    param['access_token'] = access_token
    param['media_type'] = 'CAROUSEL'
    param['children'] = container_id
    param['caption'] = caption
    response = requests.post(url, params=param)
    response = response.json()
    return response['id']


def getInstagramUrlFromMediaId(media_id):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'
    shortened_id = ''

    while media_id > 0:
        remainder = media_id % 64
        # dual conversion sign gets the right ID for new posts
        media_id = (media_id - remainder) // 64
        # remainder should be casted as an integer to avoid a type error.
        shortened_id = alphabet[int(remainder)] + shortened_id

    return 'https://instagram.com/p/' + shortened_id + '/'


def func_get_url():
    print('\n access code url', access_url)
    code = input("\n enter the url")
    code = code.rsplit('access_token=')[1]
    code = code.rsplit('&data_access_expiration')[0]
    return code


def func_get_long_lived_access_token(access_token=''):
    url = graph_url + 'oauth/access_token'
    param = dict()
    param['grant_type'] = 'fb_exchange_token'
    param['client_id'] = client_id
    param['client_secret'] = client_secret
    param['fb_exchange_token'] = access_token
    response = requests.get(url=url, params=param)
    print("\n response", response)
    response = response.json()
    print("\n response", response)
    long_lived_access_tokken = response['access_token']
    return long_lived_access_tokken


def func_get_page_id(access_token=''):
    url = graph_url + 'me/accounts'
    param = dict()
    param['access_token'] = access_token
    response = requests.get(url=url, params=param)
    print("\n response", response)
    response = response.json()
    print("\n response", response)
    page_id = response['data'][0]['id']
    page_token = response['data'][0]['access_token']
    print("\n page_id", page_id)
    return page_id, page_token


def func_get_instagram_business_account(page_id='', access_token=''):
    url = graph_url + page_id
    param = dict()
    param['fields'] = 'instagram_business_account'
    param['access_token'] = access_token
    response = requests.get(url=url, params=param)
    print("\n response", response)
    response = response.json()
    print("\n response", response)
    try:
        instagram_account_id = response['instagram_business_account']['id']
    except:
        return {'error': 'Instagram account not linked'}
    return instagram_account_id


def get_post_data(media_id='', access_token=''):
    url = graph_url + media_id
    param = dict()
    param['fields'] = 'caption,like_count,media_url,owner,permalink'
    param['access_token'] = access_token
    response = requests.get(url=url, params=param)
    response = response.json()
    return response


def get_comment(ig_media_id='', access_token=''):
    url = graph_url + ig_media_id + '/comments'
    param = dict()
    param['access_token'] = access_token
    response = requests.get(url, param)
    response = response.json()
    return response


def get_status(media_id='', access_token=''):
    url = graph_url + media_id
    param = dict()
    param['fields'] = 'status'
    param['access_token'] = access_token
    response = requests.get(url=url, params=param)
    response = response.json()
    return response


def func_get_media_id(instagram_account_id='', access_token=''):
    url = graph_url + instagram_account_id + '/media'
    param = dict()
    param['access_token'] = access_token
    response = requests.get(url=url, params=param)
    response = response.json()
    media = []
    for i in response['data']:
        media_data = get_post_data(media_id=i['id'], access_token=access_token)
        media_data['comments'] = get_comment(i['id'], access_token)['data']
        media.append(media_data)
    return media


def get_limit(instagram_account_id, access_token):
    url = graph_url + instagram_account_id + '/content_publishing_limit'
    param = dict()
    param['fields'] = 'quota_usage,config'
    param['access_token'] = access_token
    response = requests.get(url=url, params=param)
    response = response.json()
    return response


def get_location_id():
    '''
    curl -i -X GET \
  "https://graph.facebook.com/pages/search?q=Facebook
  &fields=id,name,location,link
  &access_token={access-token}"
    '''
    url = "https://graph.facebook.com/pages/search"
    param = dict()
    param['q'] = 'Gliwice Mikołowska 4A'
    param['fields'] = 'id,name,location,link'
    param['access_token'] = access_token1
    response = requests.get(url=url, params=param)
    response = response.json()
    return response


def meta_demo():
    # r = get_location_id()
    page_id1, page_token1 = func_get_page_id(access_token1)
    page_id2, page_token2 = func_get_page_id(access_token2)
    insta_id = func_get_instagram_business_account(page_id=page_id1, access_token=page_token1)
    # print(get_limit(insta_id, access_token))
    # id = post_carousel(caption, [url, url2], insta_id, page_token)
    # id = publish_container(id, insta_id, page_token)
    # status = get_status(id, page_token)
    # print(status)
    id = post_image(caption, url, insta_id, page_token1, page_id1)
    id = publish_container(id['id'], insta_id, page_token1)
    id = post_image(caption, url, insta_id, page_token2, page_id2)
    id = publish_container(id['id'], insta_id, page_token2)
    # status = get_status(id['id'], page_token)
    # print(getInstagramUrlFromMediaId(int(id['id'])))
    # id = post_image(caption, url, insta_id, page_token)
    # print(getInstagramUrlFromMediaId(int(id['id'])))
    posts_data = func_get_media_id(instagram_account_id=insta_id, access_token=page_token)
    print(posts_data)



def debug(at):
    url = "https://graph.facebook.com/debug_token"
    response = requests.get(
        url,
        params={
            "access_token": f"494536885328838|09ad7aa99cb9a2b20b6c8e8126ca0043",
            "input_token": at,
        },
    )
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 400 and response.json().get("error").get("code") == 100:
            return {}
        else:
            # Reraise exception if it's not 400 with code 100
            raise e

    return response.json().get("data", {})


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    t1 = debug(access_token1)
    t2 = debug(access_token2)
    meta_demo()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

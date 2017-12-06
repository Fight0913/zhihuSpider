# -*- coding: utf-8 -*-
import scrapy
import json
from zhihuSpider.items import UserItem

# ssl._create_default_https_context = ssl._create_unverified_context()
# sys.setdefaultencoding('utf-8')

class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    # start_urls = ['https://www.zhihu.com/api/v4/members/cooncan/activities?limit=10&after_id=1511701115&desktop=True']

    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    follows_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'
    followers_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&offset={offset}&limit={limit}'

    start_user = 'tu-lun-jia-li-ya'
    user_include = 'locations,employments,gender,educations,business,voteup_count,thanked_Count,follower_count,following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,following_columns_count,answer_count,articles_count,pins_count,question_count,commercial_question_count,favorite_count,favorited_count,logs_count,marked_answers_count,marked_answers_text,message_thread_token,account_status,is_active,is_force_renamed,is_bind_sina,sina_weibo_url,sina_weibo_name,show_sina_weibo,is_blocking,is_blocked,is_following,is_followed,mutual_followees_count,vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,allow_message,industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics'
    follows_include = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'
    followers_include = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    def start_requests(self):
        # ip = '121.35.243.157:8080'
        # user
        yield scrapy.Request(self.user_url.format(user=self.start_user, include=self.user_include), callback=self.parse_user)
        # followers
        yield scrapy.Request(self.followers_url.format(user=self.start_user, include=self.followers_include, offset=0, limit=20), callback=self.parse_followers)
        # follows
        yield scrapy.Request(self.follows_url.format(user=self.start_user, include=self.follows_include, offset=0, limit=20), callback=self.parse_follows)

    def parse_user(self, response):
        if response.status == 200:
            response_json = json.loads(response.text)
            # print(response_json)
            item = UserItem()
            for field in item.fields:
                if field in item.fields:
                    item[field] = response_json.get(field)
            print(item)
            yield item

            yield scrapy.Request(
                self.followers_url.format(user=item.get('url_token'), include=self.followers_include, limit=20, offset=0),
                self.parse_followers)

            yield scrapy.Request(
                self.follows_url.format(user=item.get('url_token'), include=self.follows_include, limit=20, offset=0),
                self.parse_follows)
        else:
            print('response.status 异常')

    def parse_followers(self, response):
        response_json_text = json.loads(response.text)
        response_json_list = response_json_text['data']
        paging = response_json_text['paging']
        is_end = paging['is_end']
        next_page = paging['next']

        for response_json in response_json_list:
            yield scrapy.Request(self.user_url.format(user=response_json['url_token'], include=self.user_include),
                                 self.parse_user)

        if is_end == False:
            yield scrapy.Request(next_page, self.parse_followers)

    def parse_follows(self, response):

        response_json_text = json.loads(response.text)
        response_json_list = response_json_text['data']
        paging = response_json_text['paging']
        is_end = paging['is_end']
        next_page = paging['next']

        for response_json in response_json_list:
            yield scrapy.Request(self.user_url.format(user=response_json['url_token'], include=self.user_include), self.parse_user)

        if is_end == False:
                yield scrapy.Request(next_page, self.parse_follows)
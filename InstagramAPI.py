#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import random
import json
import hashlib
import hmac
import urllib
import uuid
import time
import os
import random
from tkinter import *

class InstagramAPI:
    API_URL = 'https://i.instagram.com/api/v1/'
    USER_AGENT = 'Instagram 9.2.0 Android (18/4.3; 320dpi; 720x1280; Xiaomi; HM 1SW; armani; qcom; en_US)'
    IG_SIG_KEY = '012a54f51c49aa8c5c322416ab1410909add32c966bbaa0fe3dc58ac43fd7ede'
    EXPERIMENTS = 'ig_android_progressive_jpeg,ig_creation_growth_holdout,ig_android_report_and_hide,ig_android_new_browser,ig_android_enable_share_to_whatsapp,ig_android_direct_drawing_in_quick_cam_universe,ig_android_huawei_app_badging,ig_android_universe_video_production,ig_android_asus_app_badging,ig_android_direct_plus_button,ig_android_ads_heatmap_overlay_universe,ig_android_http_stack_experiment_2016,ig_android_infinite_scrolling,ig_fbns_blocked,ig_android_white_out_universe,ig_android_full_people_card_in_user_list,ig_android_post_auto_retry_v7_21,ig_fbns_push,ig_android_feed_pill,ig_android_profile_link_iab,ig_explore_v3_us_holdout,ig_android_histogram_reporter,ig_android_anrwatchdog,ig_android_search_client_matching,ig_android_high_res_upload_2,ig_android_new_browser_pre_kitkat,ig_android_2fac,ig_android_grid_video_icon,ig_android_white_camera_universe,ig_android_disable_chroma_subsampling,ig_android_share_spinner,ig_android_explore_people_feed_icon,ig_explore_v3_android_universe,ig_android_media_favorites,ig_android_nux_holdout,ig_android_search_null_state,ig_android_react_native_notification_setting,ig_android_ads_indicator_change_universe,ig_android_video_loading_behavior,ig_android_black_camera_tab,liger_instagram_android_univ,ig_explore_v3_internal,ig_android_direct_emoji_picker,ig_android_prefetch_explore_delay_time,ig_android_business_insights_qe,ig_android_direct_media_size,ig_android_enable_client_share,ig_android_promoted_posts,ig_android_app_badging_holdout,ig_android_ads_cta_universe,ig_android_mini_inbox_2,ig_android_feed_reshare_button_nux,ig_android_boomerang_feed_attribution,ig_android_fbinvite_qe,ig_fbns_shared,ig_android_direct_full_width_media,ig_android_hscroll_profile_chaining,ig_android_feed_unit_footer,ig_android_media_tighten_space,ig_android_private_follow_request,ig_android_inline_gallery_backoff_hours_universe,ig_android_direct_thread_ui_rewrite,ig_android_rendering_controls,ig_android_ads_full_width_cta_universe,ig_video_max_duration_qe_preuniverse,ig_android_prefetch_explore_expire_time,ig_timestamp_public_test,ig_android_profile,ig_android_dv2_consistent_http_realtime_response,ig_android_enable_share_to_messenger,ig_explore_v3,ig_ranking_following,ig_android_pending_request_search_bar,ig_android_feed_ufi_redesign,ig_android_video_pause_logging_fix,ig_android_default_folder_to_camera,ig_android_video_stitching_7_23,ig_android_profanity_filter,ig_android_business_profile_qe,ig_android_search,ig_android_boomerang_entry,ig_android_inline_gallery_universe,ig_android_ads_overlay_design_universe,ig_android_options_app_invite,ig_android_view_count_decouple_likes_universe,ig_android_periodic_analytics_upload_v2,ig_android_feed_unit_hscroll_auto_advance,ig_peek_profile_photo_universe,ig_android_ads_holdout_universe,ig_android_prefetch_explore,ig_android_direct_bubble_icon,ig_video_use_sve_universe,ig_android_inline_gallery_no_backoff_on_launch_universe,ig_android_image_cache_multi_queue,ig_android_camera_nux,ig_android_immersive_viewer,ig_android_dense_feed_unit_cards,ig_android_sqlite_dev,ig_android_exoplayer,ig_android_add_to_last_post,ig_android_direct_public_threads,ig_android_prefetch_venue_in_composer,ig_android_bigger_share_button,ig_android_dv2_realtime_private_share,ig_android_non_square_first,ig_android_video_interleaved_v2,ig_android_follow_search_bar,ig_android_last_edits,ig_android_video_download_logging,ig_android_ads_loop_count_universe,ig_android_swipeable_filters_blacklist,ig_android_boomerang_layout_white_out_universe,ig_android_ads_carousel_multi_row_universe,ig_android_mentions_invite_v2,ig_android_direct_mention_qe,ig_android_following_follower_social_context'
    SIG_KEY_VERSION = '4'

    #username            # Instagram username
    #password            # Instagram password
    #debug               # Debug
    #uuid                # UUID
    #device_id           # Device ID
    #username_id         # Username ID
    #token               # _csrftoken
    #isLoggedIn          # Session status
    #rank_token          # Rank token
    #IGDataPath          # Data storage path

    def __init__(self, username, password, debug = False, IGDataPath = None):
        m = hashlib.md5()
        m.update(username.encode('utf-8') + password.encode('utf-8'))
        self.device_id = self.generateDeviceId(m.hexdigest())
        self.setUser(username, password)
        self.isLoggedIn = False
        self.LastResponse = None

    def setUser(self, username, password):
        self.username = username
        self.password = password

        self.uuid = self.generateUUID(True)

        # TODO save data to file...

    def login(self, force = False):
        if (not self.isLoggedIn or force):
            self.s = requests.Session()
            # if you need proxy make something like this:
            # self.s.proxies = {"https" : "http://proxyip:proxyport"}
            if (self.SendRequest('si/fetch_headers/?challenge_type=signup&guid=' + self.generateUUID(False), None, True)):

                data = {'phone_id'   : self.generateUUID(True),
                        '_csrftoken' : self.LastResponse.cookies['csrftoken'],
                        'username'   : self.username,
                        'guid'       : self.uuid,
                        'device_id'  : self.device_id,
                        'password'   : self.password,
                        'login_attempt_count' : '0'}

                if (self.SendRequest('accounts/login/', self.generateSignature(json.dumps(data)), True)):
                    self.isLoggedIn = True
                    self.username_id = self.LastJson["logged_in_user"]["pk"]
                    self.rank_token = "%s_%s" % (self.username_id, self.uuid)
                    self.token = self.LastResponse.cookies["csrftoken"]

                    self.syncFeatures()
                    self.autoCompleteUserList()
                    self.timelineFeed()
                    self.getv2Inbox()
                    self.getRecentActivity()
                    print ("Login success!\n")
                    return True;

    def syncFeatures(self):
        data = json.dumps({
        '_uuid'         : self.uuid,
        '_uid'          : self.username_id,
        'id'            : self.username_id,
        '_csrftoken'    : self.token,
        'experiments'   : self.EXPERIMENTS
        })
        return self.SendRequest('qe/sync/', self.generateSignature(data))

    def autoCompleteUserList(self):
        return self.SendRequest('friendships/autocomplete_user_list/')

    def timelineFeed(self):
        return self.SendRequest('feed/timeline/')

    def megaphoneLog(self):
        return self.SendRequest('megaphone/log/')

    def expose(self):
        data = json.dumps({
        '_uuid'        : self.uuid,
        '_uid'         : self.username_id,
        'id'           : self.username_id,
        '_csrftoken'   : self.token,
        'experiment'   : 'ig_android_profile_contextual_feed'
        })
        return self.SendRequest('qe/expose/', self.generateSignature(data))

    def logout(self):
        logout = self.SendRequest('accounts/logout/')
        # TODO Instagram.php 180-185

    def uploadPhoto(self, photo, caption = None, upload_id = None):
        # TODO Instagram.php 200-290
        return False

    def uploadVideo(self, video, caption = None):
        # TODO Instagram.php 290-415
        return False

    def direct_share(self, media_id, recipients, text = None):
        # TODO Instagram.php 420-490
        return False

    def configureVideo(upload_id, video, caption = ''):
        # TODO Instagram.php 490-530
        return False

    def configure(upload_id, photo, caption = ''):
        # TODO Instagram.php 530-570
        return False

    def editMedia(self, mediaId, captionText = ''):
        data = json.dumps({
        '_uuid'        : self.uuid,
        '_uid'         : self.username_id,
        '_csrftoken'   : self.token,
        'caption_text' : captionText
        })
        return self.SendRequest('media/'+ str(mediaId) +'/edit_media/', self.generateSignature(data))

    def removeSelftag(self, mediaId):
        data = json.dumps({
        '_uuid'        : self.uuid,
        '_uid'         : self.username_id,
        '_csrftoken'   : self.token
        })
        return self.SendRequest('media/'+ str(mediaId) +'/remove/', self.generateSignature(data))

    def mediaInfo(self, mediaId):
        data = json.dumps({
        '_uuid'        : self.uuid,
        '_uid'         : self.username_id,
        '_csrftoken'   : self.token,
        'media_id'     : mediaId
        })
        return self.SendRequest('media/'+ str(mediaId) +'/info/', self.generateSignature(data))

    def deleteMedia(self, mediaId):
        data = json.dumps({
        '_uuid'        : self.uuid,
        '_uid'         : self.username_id,
        '_csrftoken'   : self.token,
        'media_id'     : mediaId
        })
        return self.SendRequest('media/'+ str(mediaId) +'/delete/', self.generateSignature(data))

    def comment(self, mediaId, commentText):
        data = json.dumps({
        '_uuid'        : self.uuid,
        '_uid'         : self.username_id,
        '_csrftoken'   : self.token,
        'comment_text' : commentText
        })
        return self.SendRequest('media/'+ str(mediaId) +'/comment/', self.generateSignature(data))

    def deleteComment(self, mediaId, captionText, commentId):
        data = json.dumps({
        '_uuid'        : self.uuid,
        '_uid'         : self.username_id,
        '_csrftoken'   : self.token,
        'caption_text' : captionText
        })
        return self.SendRequest('media/'+ str(mediaId) +'/comment/'+ str(commentId) +'/delete/', self.generateSignature(data))

    def changeProfilePicture(self, photo):
        # TODO Instagram.php 705-775
        return False

    def removeProfilePicture(self):
        data = json.dumps({
        '_uuid'        : self.uuid,
        '_uid'         : self.username_id,
        '_csrftoken'   : self.token
        })
        return self.SendRequest('accounts/remove_profile_picture/', self.generateSignature(data))

    def setPrivateAccount(self):
        data = json.dumps({
        '_uuid'        : self.uuid,
        '_uid'         : self.username_id,
        '_csrftoken'   : self.token
        })
        return self.SendRequest('accounts/set_private/', self.generateSignature(data))

    def setPublicAccount(self):
        data = json.dumps({
        '_uuid'        : self.uuid,
        '_uid'         : self.username_id,
        '_csrftoken'   : self.token
        })
        return self.SendRequest('accounts/set_public/', self.generateSignature(data))

    def getProfileData(self):
        data = json.dumps({
        '_uuid'        : self.uuid,
        '_uid'         : self.username_id,
        '_csrftoken'   : self.token
        })
        return self.SendRequest('accounts/current_user/?edit=true', self.generateSignature(data))

    def editProfile(self, url, phone, first_name, biography, email, gender):
        data = json.dumps({
        '_uuid'        : self.uuid,
        '_uid'         : self.username_id,
        '_csrftoken'   : self.token,
        'external_url' : url,
        'phone_number' : phone,
        'username'     : self.username,
        'full_name'    : first_name,
        'biography'    : biography,
        'email'        : email,
        'gender'       : gender,
        })
        return self.SendRequest('accounts/edit_profile/', self.generateSignature(data))

    def getUsernameInfo(self, usernameId):
        return self.SendRequest('users/'+ str(usernameId) +'/info/')

    def getSelfUsernameInfo(self):
        return self.getUsernameInfo(self.username_id)

    def getRecentActivity(self):
        activity = self.SendRequest('news/inbox/?')
        # TODO Instagram.php 911-925
        return activity

    def getFollowingRecentActivity(self):
        activity = self.SendRequest('news/?')
        # TODO Instagram.php 935-945
        return activity

    def getv2Inbox(self):
        inbox = self.SendRequest('direct_v2/inbox/?')
        # TODO Instagram.php 950-960
        return inbox

    def getUserTags(self, usernameId):
        tags = self.SendRequest('usertags/'+ str(usernameId) +'/feed/?rank_token='+ str(self.rank_token) +'&ranked_content=true&')
        # TODO Instagram.php 975-985
        return tags

    def getSelfUserTags(self):
        return self.getUserTags(self.username_id)

    def tagFeed(self, tag):
        userFeed = self.SendRequest('feed/tag/'+ str(tag) +'/?rank_token=' + str(self.rank_token) + '&ranked_content=true&')
        # TODO Instagram.php 1000-1015
        return userFeed

    def getMediaLikers(self, mediaId):
        likers = self.SendRequest('media/'+ str(mediaId) +'/likers/?')
        # TODO Instagram.php 1025-1035
        return likers

    def getGeoMedia(self, usernameId):
        locations = self.SendRequest('maps/user/'+ str(usernameId) +'/')
        # TODO Instagram.php 1050-1060
        return locations

    def getSelfGeoMedia(self):
        return self.getGeoMedia(self.username_id)

    def fbUserSearch(self, query):
        query = self.SendRequest('fbsearch/topsearch/?context=blended&query='+ str(query) +'&rank_token='+ str(self.rank_token))
        # TODO Instagram.php 1080-1090
        return query

    def searchUsers(self, query):
        query = self.SendRequest('users/search/?ig_sig_key_version='+ str(self.SIG_KEY_VERSION)
                +'&is_typeahead=true&query='+ str(query) +'&rank_token='+ str(self.rank_token))
        # TODO Instagram.php 1100-1110
        return query

    def searchUsername(self, usernameName):
        query = self.SendRequest('users/'+ str(usernameName) +'/usernameinfo/')
        # TODO Instagram.php 1080-1090
        return query

    def syncFromAdressBook(self, contacts):
        return self.SendRequest('address_book/link/?include=extra_display_name,thumbnails', json.dumps(contacts))

    def searchTags(self, query):
        query = self.SendRequest('tags/search/?is_typeahead=true&q='+ str(query) +'&rank_token='+ str(self.rank_token))
        # TODO Instagram.php 1160-1170
        return query

    def getTimeline(self):
        query = self.SendRequest('feed/timeline/?rank_token='+ str(self.rank_token) +'&ranked_content=true&')
        # TODO Instagram.php 1180-1190
        return query

    def getUserFeed(self, usernameId, maxid = '', minTimestamp = None):
        # TODO Instagram.php 1200-1220
        return False

    def getSelfUserFeed(self):
        return self.getUserFeed(self.username_id)

    def getHashtagFeed(self, hashtagString, maxid = ''):
        # TODO Instagram.php 1230-1250
        return self.SendRequest('feed/tag/'+hashtagString+'/?max_id='+str(maxid)+'&rank_token='+self.rank_token+'&ranked_content=true&')

    def searchLocation(self, query):
        locationFeed = self.SendRequest('fbsearch/places/?rank_token='+ str(self.rank_token) +'&query=' + str(query))
        # TODO Instagram.php 1250-1270
        return locationFeed

    def getLocationFeed(self, locationId, maxid = ''):
        # TODO Instagram.php 1280-1300
        return self.SendRequest('feed/location/'+str(locationId)+'/?max_id='+maxid+'&rank_token='+self.rank_token+'&ranked_content=true&')

    def getPopularFeed(self):
        popularFeed = self.SendRequest('feed/popular/?people_teaser_supported=1&rank_token='+ str(self.rank_token) +'&ranked_content=true&')
        # TODO Instagram.php 1315-1325
        return popularFeed

    def getUserFollowings(self, usernameId, maxid = ''):
        return self.SendRequest('friendships/'+ str(usernameId) +'/following/?max_id='+ str(maxid)
            +'&ig_sig_key_version='+ self.SIG_KEY_VERSION +'&rank_token='+ self.rank_token)

    def getSelfUsersFollowing(self):
        return self.getUserFollowings(self.username_id)

    def getUserFollowers(self, usernameId, maxid = ''):
        return self.SendRequest('friendships/'+ str(usernameId) +'/followers/?max_id='+ str(maxid)
            +'&ig_sig_key_version='+ self.SIG_KEY_VERSION +'&rank_token='+ self.rank_token)

    def getSelfUserFollowers(self):
        return self.getUserFollowers(self.username_id)

    def like(self, mediaId):
        data = json.dumps({
        '_uuid'         : self.uuid,
        '_uid'          : self.username_id,
        '_csrftoken'    : self.token,
        'media_id'      : mediaId
        })
        return self.SendRequest('media/'+ str(mediaId) +'/like/', self.generateSignature(data))

    def unlike(self, mediaId):
        data = json.dumps({
        '_uuid'         : self.uuid,
        '_uid'          : self.username_id,
        '_csrftoken'    : self.token,
        'media_id'      : mediaId
        })
        return self.SendRequest('media/'+ str(mediaId) +'/unlike/', self.generateSignature(data))

    def getMediaComments(self, mediaId):
        return self.SendRequest('media/'+ mediaId +'/comments/?')

    def setNameAndPhone(self, name = '', phone = ''):
        data = json.dumps({
        '_uuid'         : self.uuid,
        '_uid'          : self.username_id,
        'first_name'    : name,
        'phone_number'  : phone,
        '_csrftoken'    : self.token
        })
        return self.SendRequest('accounts/set_phone_and_name/', self.generateSignature(data))

    def getDirectShare(self):
        return self.SendRequest('direct_share/inbox/?')

    def backup(self):
        # TODO Instagram.php 1470-1485
        return False

    def follow(self, userId):
        data = json.dumps({
        '_uuid'         : self.uuid,
        '_uid'          : self.username_id,
        'user_id'       : userId,
        '_csrftoken'    : self.token
        })

        return self.SendRequest('friendships/create/'+ str(userId) +'/', self.generateSignature(data))

    def unfollow(self, userId):
        data = json.dumps({
        '_uuid'         : self.uuid,
        '_uid'          : self.username_id,
        'user_id'       : userId,
        '_csrftoken'    : self.token
        })
        return self.SendRequest('friendships/destroy/'+ str(userId) +'/', self.generateSignature(data))

    def block(self, userId):
        data = json.dumps({
        '_uuid'         : self.uuid,
        '_uid'          : self.username_id,
        'user_id'       : userId,
        '_csrftoken'    : self.token
        })
        return self.SendRequest('friendships/block/'+ str(userId) +'/', self.generateSignature(data))

    def unblock(self, userId):
        data = json.dumps({
        '_uuid'         : self.uuid,
        '_uid'          : self.username_id,
        'user_id'       : userId,
        '_csrftoken'    : self.token
        })
        return self.SendRequest('friendships/unblock/'+ str(userId) +'/', self.generateSignature(data))

    def userFriendship(self, userId):
        data = json.dumps({
        '_uuid'         : self.uuid,
        '_uid'          : self.username_id,
        'user_id'       : userId,
        '_csrftoken'    : self.token
        })
        return self.SendRequest('friendships/show/'+ str(userId) +'/', self.generateSignature(data))

    def getLikedMedia(self,maxid=''):
        return self.SendRequest('feed/liked/?max_id='+str(maxid))

    def generateSignature(self, data):
        return 'ig_sig_key_version=' + self.SIG_KEY_VERSION + '&signed_body=' + hmac.new(self.IG_SIG_KEY.encode('utf-8'), data.encode('utf-8'), hashlib.sha256).hexdigest() + '.' + urllib.parse.quote(data)

    def generateDeviceId(self, seed):
        volatile_seed = "12345"
        m = hashlib.md5()
        m.update(seed.encode('utf-8') + volatile_seed.encode('utf-8'))
        return 'android-' + m.hexdigest()[:16]

    def generateUUID(self, type):
        #according to https://github.com/LevPasha/Instagram-API-python/pull/16/files#r77118894
        #uuid = '%04x%04x-%04x-%04x-%04x-%04x%04x%04x' % (random.randint(0, 0xffff),
        #    random.randint(0, 0xffff), random.randint(0, 0xffff),
        #    random.randint(0, 0x0fff) | 0x4000,
        #    random.randint(0, 0x3fff) | 0x8000,
        #    random.randint(0, 0xffff), random.randint(0, 0xffff),
        #    random.randint(0, 0xffff))
        generated_uuid = str(uuid.uuid4())
        if (type):
            return generated_uuid
        else:
            return generated_uuid.replace('-', '')

    def buildBody(bodies, boundary):
        # TODO Instagram.php 1620-1645
        return False

    def SendRequest(self, endpoint, post = None, login = False):
        if (not self.isLoggedIn and not login):
            raise Exception("Not logged in!\n")
            return;

        self.s.headers.update ({'Connection' : 'close',
                                'Accept' : '*/*',
                                'Content-type' : 'application/x-www-form-urlencoded; charset=UTF-8',
                                'Cookie2' : '$Version=1',
                                'Accept-Language' : 'en-US',
                                'User-Agent' : self.USER_AGENT})

        if (post != None): # POST
            response = self.s.post(self.API_URL + endpoint, data=post) # , verify=False
        else: # GET
            response = self.s.get(self.API_URL + endpoint) # , verify=False

        if response.status_code == 200:
            self.LastResponse = response
            self.LastJson = json.loads(response.text)
            return True
        else:
            print ("Request return " + str(response.status_code) + " error!")
            # for debugging
            try:
                self.LastResponse = response
                self.LastJson = json.loads(response.text)
            except:
                pass
            return False
            
    def getTotalFollowers(self,usernameId):
        followers = []
        next_max_id = ''
        while 1:
            self.getUserFollowers(usernameId,next_max_id)
            temp = self.LastJson

            for item in temp["users"]:
                followers.append(item)

            if temp["big_list"] == False:
                return followers            
            next_max_id = temp["next_max_id"]         

    def getTotalFollowings(self,usernameId):
        followers = []
        next_max_id = ''
        while 1:
            self.getUserFollowings(usernameId,next_max_id)
            temp = self.LastJson

            for item in temp["users"]:
                followers.append(item)

            if temp["big_list"] == False:
                return followers            
            next_max_id = temp["next_max_id"]  
    
    def getTotalSelfFollowers(self):
        return getTotalFollowers(self.username_id)
    
    def getTotalSelfFollowings(self):
        return getTotalFollowings(self.username_id)
        
    def getTotalLikedMedia(self,scan_rate = 1):
        next_id = ''
        liked_items = []
        for x in range(0,scan_rate):
            temp = self.getLikedMedia(next_id)
            next_id = temp["next_max_id"]
            for item in temp["items"]:
                liked_items.append(item)
        return liked_items
#-----------------------------------------------------------------------------------------------------------------  MON CODE :
    def likefct(self,event):
        print("Vous avez choisi la fonction like ")
        
        TempsActuel = self.time()
        strTempsActuel = str(TempsActuel)
        compte = open("comptage.txt","r")
        compteLect = compte.read()
        compteSepar = compteLect.split("x")
        lenCompteSepar = len(compteSepar)
        intLenCompteSepar = int(lenCompteSepar)
        compte.close()
                
        if TempsActuel == 3600:
            
            os.remove("comptage.txt")
            compte = open("comptage.txt","w")
            compte.close()
                          
            print ("entrez votre tag")
            tag = input()
            self.tagFeed(tag) # get media list by tag #instaffred
            media_id = self.LastJson # last response JSON
            TempsActuel = json.dumps(media_id)
        
            mik = (media_id["num_results"])
            TempsActuel = int(mik)
            bik = str(mik)
        

            if (TempsActuel>=60):
                for i in range(0,60):
                    self.comptage()
                    self.timeforce()
                    self.like(media_id["items"][i]["pk"]) # like first media
                    print(media_id["items"][i]["pk"])
                    time.sleep(10)
            else:
                print("il n'y a que :" + bik + " like à faire ")
                for i in range (0,TempsActuel):
                    self.comptage()
                    self.timeforce()
                    self.like(media_id["items"][i]["pk"]) # like first media
                    print(media_id["items"][i]["pk"])
                    time.sleep(10)
                    
            
        if TempsActuel < 3600 and intLenCompteSepar ==1 :
            
            print ("entrez votre tag, la campagne commencera lorsque la pause sera terminée")
            tag = input()
            pik = int(TempsActuel)
            time.sleep(pik)

            self.tagFeed(tag) # get media list by tag #instaffred
            media_id = self.LastJson # last response JSON
            TempsActuel = json.dumps(media_id)
        
            mik = (media_id["num_results"])
            TempsActuel = int(mik)
            bik = str(mik)
        

            if (TempsActuel>=60):
                for i in range(0,60):
                    self.comptage()
                    self.timeforce()
                    self.like(media_id["items"][i]["pk"]) # like first media
                    print(media_id["items"][i]["pk"])
                    time.sleep(10)
            else:
                print("il n'y a que :" + bik + " like à faire ")
                for i in range (0,TempsActuel):
                    self.comptage()
                    self.timeforce()
                    self.like(media_id["items"][i]["pk"]) # like first media
                    print(media_id["items"][i]["pk"])
                    time.sleep(10)

            
        if TempsActuel < 3600 and intLenCompteSepar !=1 :
            
            reste = 61 - intLenCompteSepar
            strRest = str(reste)
            intRest = int(reste)
            print("il vous reste "+strRest+" personnes à liké ou "+strTempsActuel+" secondes à attendre avant de débuter une nouvelle campagne")
            print ("entrez votre tag")
            tag = input()
            self.tagFeed(tag) # get media list by tag #instaffred
            media_id = self.LastJson # last response JSON
            TempsActuel = json.dumps(media_id)
        
            mik = (media_id["num_results"])
            TempsActuel = int(mik)
            bik = str(mik)
        

            if (TempsActuel>=60):
                for i in range(0,60):
                    self.comptage()
                    self.timeforce()
                    self.like(media_id["items"][i]["pk"]) # like first media
                    print(media_id["items"][i]["pk"])
                    time.sleep(10)
            else:
                val = min(TempsActuel,intRest)
                for i in range (0,val):
                    self.comptage()
                    self.timeforce()
                    self.like(media_id["items"][i]["pk"]) # like first media
                    print(media_id["items"][i]["pk"])
                    time.sleep(10)
                    
        print("Campagne like&comment finis")
        os.remove("comptage.txt")
        compte = open("comptage.txt","w")
        compte.close()
        
            
    def reglage(self,event):
        
        nombre1=(input("combien de secondes voulez vous attendre entre 2 follows ? "))
        nombre2=(input("combien de secondes voulez vous attendre entre 2 unfollows ? "))
        nombre3=(input("combien de secondes voulez vous attendre entre 2 campagnes? "))
        nombre4=(input("combien de campagne voulez vous faire?"))
        regles = open("reglages.txt","w")
        regles.write(nombre1 + "\n" + nombre2 + "\n" + nombre3 + "\n" + nombre4)
        regles.close()
        print("Réglage finis")

    def commenter(self,event):

        print("Vous avez choisi la fonction Commenter")
        
        TempsActuel = self.time()
        strTempsActuel = str(TempsActuel)
        compte = open("comptage.txt","r")
        compteLect = compte.read()
        compteSepar = compteLect.split("x")
        lenCompteSepar = len(compteSepar)
        intLenCompteSepar = int(lenCompteSepar)
        compte.close()
        
        if TempsActuel == 3600:

            os.remove("comptage.txt")
            compte = open("comptage.txt","w")
            compte.close()
            
            print ("entrez votre tag")
            tag = input()
            print ("entrez votre commentaire")
            commentaire = input()

            self.tagFeed(tag) # get media list by tag #instaffred
            media_id = self.LastJson # last response JSON
            TempsActuel = json.dumps(media_id)
            test = open("jsone.txt","w")
            test.write(TempsActuel)
            test.close()

            mik = (media_id["num_results"])
            TempsActuel = int(mik)
            bik = str(mik)

            if (TempsActuel>=60):
                for i in range(0,60):
                    self.comptage()
                    self.timeforce()
                    self.comment(media_id["items"][i]["pk"],commentaire) # like first media
                    print(media_id["items"][i]["pk"])
                    time.sleep(10)
            else:
                print("il n'y a que :" + bik + " images à commenter "+"\n")
                for i in range (0,TempsActuel):
                    self.comptage()
                    self.timeforce()
                    self.comment(media_id["items"][i]["pk"],commentaire) # like first media
                    print(media_id["items"][i]["pk"])
                    time.sleep(10)

            
        if TempsActuel < 3600 and intLenCompteSepar ==1 :
            
            print("entrez votre tag et votre commentaire, le programme commencera à la fin de la pause indiquée")
            print ("entrez votre tag")
            tag = input()
            print ("entrez votre commentaire")
            commentaire = input()
            pik = int(TempsActuel)

            self.tagFeed(tag) # get media list by tag #instaffred
            media_id = self.LastJson # last response JSON
            TempsActuel = json.dumps(media_id)
            test = open("jsone.txt","w")
            test.write(TempsActuel)
            test.close()

            mik = (media_id["num_results"])
            TempsActuel = int(mik)
            bik = str(mik)

            if (TempsActuel>=60):
                for i in range(0,60):
                    self.comptage()
                    self.timeforce()
                    self.comment(media_id["items"][i]["pk"],commentaire) # like first media
                    print(media_id["items"][i]["pk"])
                    time.sleep(10)
            else:
                print("il n'y a que :" + bik + " images à commenter "+"\n")
                for i in range (0,TempsActuel):
                    self.comptage()
                    self.timeforce()
                    self.comment(media_id["items"][i]["pk"],commentaire) # like first media
                    print(media_id["items"][i]["pk"])
                    time.sleep(10)

        if TempsActuel < 3600 and intLenCompteSepar !=1 :
            
            reste = 61 - intLenCompteSepar
            strRest = str(reste)
            intRest = int(reste)
            print("il vous reste "+strRest+" personnes à commenté ou "+strTempsActuel+" secondes à attendre avant de débuter une nouvelle campagne")
                            
            print ("entrez votre tag")
            tag = input()
            print ("entrez votre commentaire")
            commentaire = input()
            pik = int(TempsActuel)

            self.tagFeed(tag) # get media list by tag #instaffred
            media_id = self.LastJson # last response JSON
            TempsActuel = json.dumps(media_id)
            test = open("jsone.txt","w")
            test.write(TempsActuel)
            test.close()

            mik = (media_id["num_results"])
            TempsActuel = int(mik)
            bik = str(mik)

            if (TempsActuel>=60):
                for i in range(0,60):
                    self.comptage()
                    self.timeforce()
                    self.comment(media_id["items"][i]["pk"],commentaire) # like first media
                    print(media_id["items"][i]["pk"])
                    time.sleep(10)
            else:
                
                val = min(TempsActuel,intRest)
                for i in range (0,val):
                    self.comptage()
                    self.timeforce()
                    self.comment(media_id["items"][i]["pk"],commentaire) # like first media
                    print(media_id["items"][i]["pk"])
                    time.sleep(10)

        print("Campagne like&comment finis")
        os.remove("comptage.txt")
        compte = open("comptage.txt","w")
        compte.close()
            
                



    def ajout(self,event):

        os.remove("ajout.txt")
        os.remove("supprimer.txt")
        creation = open("ajout.txt","w")             # création du fichier où seront stockés les nouvelles personnes à follow
        creation.close()
        creationsup = open("supprimer.txt","w")             # Création du fichier où seront stockés les personnes à supprimer
        creationsup.close()



        print("combien de personne voulez vous ajouter?")
        nombre = int(input())
        nomb = str(nombre)
        for i in range (0,nombre):
            print("saisissez nom de la personne à follow : ")
            nom = input()
            self.searchUsername(nom)
            TempsActuel = self.LastJson
 
            ajout = open("ajout.txt","a+")
            identite = TempsActuel["user"]["pk"]
            tag = TempsActuel["user"]["username"]
            name = TempsActuel["user"]["full_name"]
            idmodif = str(identite)
            ajout.write(name + ";" + "@" + tag + ";" + idmodif + "\n")
            ajout.close()

        print("Supprimer à présent "+ nomb + "personne")
        text = open("nouveau.txt","r+")
        textread = text.read()
        separ = textread.split("\n")
        longeur = len(separ)
        text.close()

        recuperation = open("recuperation.txt","w")                 # Création d'un fichier de récupération dans le cas ou les données ne soient pas conforme
        for m in range(0,longeur):
            if m == 0 :
                recuperation.write(separ[m])
            else :
                recuperation.write("\n" + separ[m])
        recuperation.close()


        for b in range (0,longeur):
            print(str(b+1)+ " : " + separ[b])

        for p in range (0,nombre):

            print("saisissez un nombre de 1 à 60 qui correspondra à la personne à supprimer")
            no = input()
            verif = int(no)
            while (verif < 0 or verif > 60):
                print("Erreur recommencez saisie")
                print("saisissez un nombre de 1 à 60 qui correspondra à la personne à supprimer")
                no = input()
                verif = int(no)

            sup = open ("supprimer.txt","a+")
            bay = int(no)-1
            sup.write(separ[bay]+"\n")
            sup.close()
        verifnombre = int(nombre) - 1

        verif1 = open("ajout.txt","r")
        verif1lect = verif1.read()
        verif1separ = verif1lect.split("\n")
        lenverif1 = int(len(verif1separ))
        veri1 = list(set(verif1separ))
        ver1 = int(len(veri1))
        if lenverif1 != ver1 :
            print("Erreur vous avez entrez deux fois le même nom")

        verif2 = open("supprimer.txt","r")
        verif2lect = verif2.read()
        verif2separ = verif2lect.split("\n")
        lenverif2 = int(len(verif2separ))
        veri2 = list(set(verif2separ))
        ver2 = int(len(veri2))
        if lenverif2 != ver2 :
            print("Erreur vous avez supprimer deux fois la même personne")

        ajoutfin = open("ajout.txt","r")
        ajoutfinlect = ajoutfin.read()
        ajoutfinsepar = ajoutfinlect.split("\n")
        ajoutfin.close()

        suppfin = open("supprimer.txt","r")
        suppfinlect = suppfin.read()
        suppfinsepar = suppfinlect.split("\n")
        suppfin.close()

        creationfin = open("nouveau.txt","a+")
        creationfinlect = creationfin.read()
        for g in range (0,nombre):
            creationfin.write("\n" + ajoutfinsepar[g])
        creationfin.close()

        supprimfinal = open("nouveau.txt","r")
        supprimfinallect = supprimfinal.read()
        supprimfinalsepar = supprimfinallect.split("\n")
        for w in range (0,nombre):
            supprimfinalsepar.remove(suppfinsepar[w])
        leng = int(len(supprimfinalsepar))
        supprimfinal.close()

        os.remove("nouveau.txt")

        final = open("nouveau.txt","w+")

        for h in range(0,leng):
            if h == 0 :
                final.write(supprimfinalsepar[h])
            else:
                final.write("\n" + supprimfinalsepar[h])
        final.close()

        veriffinal = open("nouveau.txt","r")
        veriffinallect=veriffinal.read()
        veriffinalsepar = veriffinallect.split("\n")
        premier = len(veriffinalsepar)
        finalite = list(set(veriffinalsepar))
        deuxieme = len(finalite)
        veriffinal.close()
        if premier == deuxieme:
            print("Programme d'ajout terminé avec succés")
            os.remove("recuperation.txt")
        else:
            print("Erreur vous avez deux fois la même donnée votre fichier n'a pas été modifié")
            os.remove("nouveau.txt")
            os.rename("recuperation.txt","nouveau.txt")
    
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def comptage(self):
        compte = open("comptage.txt","a+")
        compte.write("x")
        compte.close()
        
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def fenetre(self):

        master = Tk()
        likecomment = PhotoImage(file="likecomment.png")
        commentaire = PhotoImage(file="commentaire.png")
        follow = PhotoImage(file="follow.png")
        like = PhotoImage(file="like.png")

        param = PhotoImage(file="reglage.png")
        ajout = PhotoImage(file="ajout.png")


        w = Canvas(master, width=940, height=600,bg="ivory")

        likebouton = w.create_image(0,0,anchor=NW,image=like)
        commentbouton = w.create_image(340,0,anchor=NW,image=commentaire)
        followbouton = w.create_image(0,340,anchor=NW,image=follow)
        likecommentbouton = w.create_image(680,0,anchor=NW, image=likecomment)
        parambouton = w.create_image(680,340,anchor=NW, image=param)
        ajoutbouton = w.create_image(340,340,anchor=NW, image=ajout)

        w.tag_bind(commentbouton,'<ButtonPress-1>', self.commenter)
        w.tag_bind(followbouton, '<ButtonPress-1>', self.lancer)
        w.tag_bind(likebouton, '<ButtonPress-1>', self.likefct)
        w.tag_bind(parambouton, '<ButtonPress-1>', self.reglage)
        w.tag_bind(likecommentbouton, '<ButtonPress-1>', self.likecomment)
        w.tag_bind(ajoutbouton, '<ButtonPress-1>', self.ajout)
        w.pack()

        mainloop()

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def likecomment(self,event):
        print("Vous avez choisi la fonction like et comment")
        TempsActuel = self.time()
        strTempsActuel = str(TempsActuel)
        compte = open("comptage.txt","r")
        compteLect = compte.read()
        compteSepar = compteLect.split("x")
        lenCompteSepar = len(compteSepar)
        intLenCompteSepar = int(lenCompteSepar)
        
        if TempsActuel == 3600 :

            os.remove("comptage.txt")
            compte = open("comptage.txt","w")
            compte.close()

            print ("entrez votre tag")
            tag = input()
            print ("entrez votre commentaire")
            commentaire = input()
            self.tagFeed(tag) # get media list by tag #instaffred
            media_id = self.LastJson # last response JSON
            TempsActuel = json.dumps(media_id)
            
            mik = (media_id["num_results"])
            TempsActuel = int(mik)
            bik = str(mik)
            

            if (TempsActuel>=60):
                for i in range(0,60):
                    self.comptage()
                    self.timeforce()
                    self.like(media_id["items"][i]["pk"]) # like first media
                    time.sleep(5)
                    self.comment(media_id["items"][i]["pk"],commentaire)
                    print(media_id["items"][i]["pk"])
                    time.sleep(10)
            else:
                print("il n'y a que :" + bik + " like à faire ")
                for i in range (0,TempsActuel):
                    self.comptage()
                    self.timeforce()
                    self.like(media_id["items"][i]["pk"]) # like first media
                    time.sleep(5)
                    self.comment(media_id["items"][i]["pk"],commentaire)
                    print(media_id["items"][i]["pk"])
                    time.sleep(10)


        if TempsActuel < 3600 and intLenCompteSepar ==1:
            
            print("Entrez votre tag et commentaire, le programme commencera dans "+strTempsActuel+" secondes")
            pik = int(TempsActuel)
            print ("entrez votre tag")
            tag = input()
            print ("entrez votre commentaire")
            commentaire = input()
            time.sleep(0)
            self.tagFeed(tag) # get media list by tag #instaffred
            media_id = self.LastJson # last response JSON
            TempsActuel = json.dumps(media_id)
            
            mik = (media_id["num_results"])
            TempsActuel = int(mik)
            bik = str(mik)
            

            if (TempsActuel>=60):
                for i in range(0,60):
                    self.comptage()
                    self.timeforce()
                    self.like(media_id["items"][i]["pk"]) # like first media
                    time.sleep(5)
                    self.comment(media_id["items"][i]["pk"],commentaire)
                    print(media_id["items"][i]["pk"])
                    time.sleep(10)
            else:
                print("il n'y a que :" + bik + " like à faire ")
                for i in range (0,TempsActuel):
                    self.comptage()
                    self.timeforce()
                    self.like(media_id["items"][i]["pk"]) # like first media
                    time.sleep(5)
                    self.comment(media_id["items"][i]["pk"],commentaire)
                    print(media_id["items"][i]["pk"])
                    time.sleep(10)

        if TempsActuel < 3600 and intLenCompteSepar !=1 :
            reste = 61 - intLenCompteSepar
            strRest = str(reste)
            intRest = int(reste)
            print("il vous reste "+strRest+" personnes à liké et commenté ou "+strTempsActuel+" secondes à attendre avant de débuter une nouvelle camagne")
            
            print ("entrez votre tag")
            tag = input()
            print ("entrez votre commentaire")
            commentaire = input()
            self.tagFeed(tag) # get media list by tag #instaffred
            media_id = self.LastJson # last response JSON
            TempsActuel = json.dumps(media_id)
            
            mik = (media_id["num_results"])
            TempsActuel = int(mik)
            bik = str(mik)

            if (TempsActuel>=60):
                for i in range(0,intRest):
                    self.comptage()
                    self.timeforce()
                    self.like(media_id["items"][i]["pk"]) # like first media
                    time.sleep(5)
                    self.comment(media_id["items"][i]["pk"],commentaire)
                    print(media_id["items"][i]["pk"])
                    time.sleep(10)
            else:
                val = min(TempsActuel,intRest)
                for i in range (0,val):
                    self.comptage()
                    self.timeforce()
                    self.like(media_id["items"][i]["pk"]) # like first media
                    time.sleep(5)
                    self.comment(media_id["items"][i]["pk"],commentaire)
                    print(media_id["items"][i]["pk"])
                    time.sleep(10)

        print("Campagne like&comment finis")
        os.remove("comptage.txt")
        compte = open("comptage.txt","w")
        
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def lancer(self,event):

        TempsActuel = self.time()
        strTempsActuel = str(TempsActuel)
        if TempsActuel == 3600:
            TempsActuel = 0

        comparaison1 = open("follow.txt","r")
        comparaison2 = open("unfollow.txt","r")
        compa1 = comparaison1.read()
        compa2 = comparaison2.read()
        split1 = compa1.split("\n")
        split2 = compa2.split("\n")

        max1 = int(len(split1))
        max2 = int(len(split2))
        comparaison1.close()
        comparaison2.close()


        var = max1 + max2
        if (var<60):
            boucle = 60 - var
            nombe = str(boucle)
            for i in range(0,nombe):
                print("saisissez nom de la personne à follow : ")
                nom = input()
                self.searchUsername(nom)
                TempsActuel = self.LastJson
 
                ajout = open("ajout.txt","a+")
                identite = TempsActuel["user"]["pk"]
                tag = TempsActuel["user"]["username"]
                name = TempsActuel["user"]["full_name"]
                idmodif = str(identite)
                ajout.write(name + ";" + "@" + tag + ";" + idmodif + "\n")
                ajout.close()
                
            ajoutfin = open("ajout.txt","r")
            ajoutfinlect = ajoutfin.read()
            ajoutfinsepar = ajoutfinlect.split("\n")
            ajoutfin.close()
            
            creationfin = open("nouveau.txt","a+")
            creationfinlect = creationfin.read()
            for g in range (0,nombre):
                creationfin.write("\n" + ajoutfinsepar[g])
            creationfin.close()
        
        verifFichier= open("unfollow.txt","r")
        verifFichierLecture = verifFichier.read()
        verifFichierLectureSplit = verifFichierLecture.split("/n")
        verifFichier.close()
        
        if verifFichierLectureSplit[0] == "" :
            ajout = open("nouveau.txt","r")
            ajoutlect = ajout.read()                                                                                # Changement de fichier de suivi
            ajoutsepar = ajoutlect.split("\n")
            ajout.close()

            remplacement = open("follow.txt","w")
            for g in range (0,60):
                if g == 0 :
                    remplacement.write(ajoutsepar[g])
                else :
                    remplacement.write("\n" + ajoutsepar[g])

            print("Mise à jour automatique des personnes à suivre effectuée")
            remplacement.close()

        
        nbrCampagneOuv = open("reglages.txt","r")
        nbrCampagneLect=nbrCampagneOuv.read()
        separ = nbrCampagneLect.split("\n")
        nombre = separ[3]
        nombre3 = int(nombre)

        if max1>max2:
            campagne = "follow"
        else:
            campagne = "unfollow"
        
        if (len(separ) == 4):                                                                   # VOIR SI L'APPLICATION EST BIEN PARAMETRE

            nbrCampagne = int(separ[3])

            if (split1[0]=="" or split2[0]==""):                                        # création d'une sécurité au cas ou le programme plante en cours de route.
                print("Veuillez attendre "+strTempsActuel+" secondes avant que la campagne se lance")
                time.sleep(TempsActuel)
            else:
                print("Pause de sécurité car le programme a planté au cours de la campagne : "+campagne)
                time.sleep(20)      
            
                
            if (max1 > max2):                                                                                      # supérieur ou égal pour le début car au lancement du programme les deux fichiers sont vides
                for i in range(0,nbrCampagne):
                    print("Début de la campagne follow :"+"\n")
                    self.campagneFollow()
                    print("Début de la campagne unfollow :"+"\n")
                    self.campagneUnfollow()
            else :
                for i in range(0,nbrCampagne):
                    print("Début de la campagne unfollow :"+"\n")
                    self.campagneUnfollow()
                    print("Début de la campagne follow :"+"\n")
                    self.campagneFollow()
                
        else:
            print("Erreur veuillez paramétré l application")

        

            
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------          
    def campagneFollowini(self) :

        reglage = open("reglages.txt","r")
        lect = reglage.read()
        virg = lect.split("\n")
        nombre2 = int(virg[1])
        nombre3 = int(virg[2])
        reglage.close()
        nombre1 = random.randint(9,12)
       
        
        Dossier_initial = open("donnee.txt", "r")   #ouvre le fichier data où sont stockés toutes les informations des personnes à suivre
        Dossier_init = Dossier_initial.read()
        Dossier_initial.close()
    
        #self.getSelfUsersFollowing()
        #midi = self.LastJson                                               # le json ne marche pas car il y a un temps d'attente entre la mise a jour de ses données et le programme
        #tik = json.dumps(midi)
        
        verification = open("unfollow.txt","r")
        veriflect = verification.read()
        verification.close()
        

        
        separ_ligne = Dossier_init.split("\n") # cette fonction SPLIT permet de créer une sorte de tableau avec des indices de 0 à n à chaque retour à la ligne.
        
        for i in range(0, len(separ_ligne)):  #parcour de la boucle de 0 à la longeur du tableau que l'on vien de créer.
            
            separ_virgule = separ_ligne[i].split(";") #on refait un split qui sépare les différentes données à chaque point virgule
                
            if (len(separ_virgule) == 3) and  separ_virgule[0] != ("") :
                    
                follow_a = separ_virgule[1]
                follow_name = separ_virgule[0] # indice 0 car on a le nom en première position
                follow_id = separ_virgule[2] # indice 2 car l'user_id est en  3 eme position
                    
                if follow_id in veriflect:
                    print(follow_name+" est déjà suivi")                        
                else:
                    unfollowSucess = open("unfollow.txt", "a+") # ouverture en mode lecture + écriture du fichier unfollow ou seront écrit les ID_user des personnes followés
                    follow = open ("follow.txt","a+") # ouverture en mode lecture + écriture du fichier follow raté ou seront écrit les ID_user des personnes qui n'ont pas pu être followés.
                    self.follow(follow_id) #on follow par ID

                    if self.LastResponse.status_code == 200 : # création de la vérification car dans la fct Follow de l'API si la personne a bien été follow elle renvoie un true
                
                        print (follow_name + " a été suivi")

                        unfollowSucess.write(follow_name+";"+follow_a+";"+follow_id+"\n") # commencement de la copie dans le fichier follow

                    
                    elif self.LastResponse.status_code == 404 :
                        print( "coordonnées Inconnues! données supprimées car votre ID n'est pas ou plus valide.")
                    else :
                        print (follow_name + " n'a pas pû être suivi")

                        follow.write(follow_name+";"+follow_a+";"+follow_id+"\n") #l'ID des personnes qui n'ont pas pu être follow se retrouvent ici.
                    unfollowSucess.close()
                    follow.close()        
                    time.sleep(nombre1)
            else:
                print("ERREUR DONNEE SUPPRIME CAR NON CONFORME : "+separ_ligne[i])

        vidage = open("donnee.txt","w")
        vidage.close()

                
            
            #ligneZero = separ_ligne[i]
            #ligneUne = separ_ligne[i+1]
            #separ_ligne[i] = ligneUne = separ_ligne[i+1]
            #separ_ligne.remove(separ_ligne[i])
            #ligneZero = ligneUne
            #print(ligneZero+ligneUne)
        
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def timeforce(self):
        tempsNouveau = time.time()

        strNouveauTemps = str(tempsNouveau)


        Nouveau = open("sauvegarde.txt","w")
        for i in range(0,10):
            Nouveau.write(strNouveauTemps[i])
        Nouveau.close()

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------        

    def time(self):
        
        tempsAncien = open("sauvegarde.txt","r")
        tempsAncienLect = tempsAncien.read()
        tempsAncienInt = int(tempsAncienLect)

        tempsNouveau = time.time()
        strNouveauTemps = str(tempsNouveau)

        tempsNouveauInt = int(tempsNouveau)
        nombre = tempsNouveauInt - tempsAncienInt
        nombreInt = int(nombre)
        pause = 3600 - nombre
        pauseStr = str(pause)
        
        if nombre >= 3600:
            Nouveau = open("sauvegarde.txt","w")
            for i in range(0,10):
                Nouveau.write(strNouveauTemps[i])
            Nouveau.close()
            pause = 3600
          
        return pause

    #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------  
        
    def campagneUnfollow(self) :

        reglage = open("reglages.txt","r")
        lect = reglage.read()
        virg = lect.split("\n")
        nombre1 = random.randint(9,12)
        nombre2 = int(virg[1])
        nombre3 = int(virg[2])
        reglage.close()

        donnee_source = open("unfollow.txt", "r") # on ouvre ensuite le fichier unfollow en mode read pour ne pas toucher à ses données.
        donnee_source_lecture = donnee_source.read()
        donnee_source.close()

        creation = open("followrate.txt","w")
        creation.close()

        verification = open("follow.txt","r")
        verif_lect = verification.read()
        verification.close()
        
        #self.getSelfUsersFollowing()
        #mido = self.LastJson
        #tiko = json.dumps(mido)

        
        separ_ligne = donnee_source_lecture.split("\n")# cette fonction SLIT permet de créer une sorte de tableau avec des indices de 0 à n à chaque retour à la ligne du fichier unfollow

        for j in range(0, len(separ_ligne)):  #parcour de la boucle de 0 à la longeur du tableau que l'on vien de créer. ici 3

            self.timeforce()
            
            separ_virgule = separ_ligne[j].split(";") #on refait un split qui sépare les différentes données à chaque point virgule
            

            
            if (len(separ_virgule) == 3) and separ_virgule[0] != ("") :                    #verification pour savoir SI LA DONNEE EST CONFORME
                
                
                unfollow_a = separ_virgule[1]
                unfollow_name = separ_virgule[0] # indice 0 car on a le nom en première position
                unfollow_id = separ_virgule[2] # indice 2 car l'user_id est en  3 eme position

                #if (unfollow_id not in tiko)
                        
                    #followSucess.write(unfollow_name+";"+unfollow_a+";"+unfollow_id+"\n") # commencement de la copie dans le fichier follow
                    #print(unfollow_name+" n'est déjà pas suivi ")
                    
                #else:
                if (unfollow_id in verif_lect):
                    print(unfollow_name+" n'était déjà pas suivi")
                        

                else:
                    followSucess = open("follow.txt", "a+") # ouverture en mode écriture du fichier follow ou seront écrit les données des personnes followés
                    followFail = open ("unfollowrate.txt","a+") # ouverture en mode écriture et lecture du fichier unfollow raté ou seront écrit les données des personnes qui n'ont pas pu être followés.
                
                    self.unfollow(unfollow_id) #on unfollow par ID
            
                    if self.LastResponse.status_code == 200 : # création de la vérification car dans la fct Follow de l'API si la personne a bien été follow elle renvoie un true

                        followSucess.write(unfollow_name+";"+unfollow_a+";"+unfollow_id+"\n") # commencement de la copie dans le fichier follow
                        print(unfollow_name+ " n'est plus suivi")

            
                    elif self.LastResponse.status_code == 404 :
                        print( "coordonnées Inconnues données supprimées.")
                    else :
                        print (unfollow_name + " n'a pû être désuivi")
                        followFail.write(unfollow_name+";"+unfollow_a+";"+unfollow_id+"\n")

                    followFail.close()
                    followSucess.close()  
                    time.sleep(nombre2)

            else:
                print("ERREUR DONNEE SUPPRIME CAR NON CONFORME")
                              
        os.remove("unfollow.txt")
        os.rename("unfollowrate.txt","unfollow.txt")
        time.sleep(1)
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        
        
        comparaison1 = open("follow.txt","r")
        comparaison2 = open("unfollow.txt","r")
        compa1 = comparaison1.read()
        compa2 = comparaison2.read()
        split1 = compa1.split("\n")
        split2 = compa2.split("\n")

        max1 = int(len(split1))
        max2 = int(len(split2))
        comparaison1.close()
        comparaison2.close()



                
        ajoutfin = open("ajout.txt","r")
        ajoutfinlect = ajoutfin.read()
        ajoutfinsepar = ajoutfinlect.split("\n")
        ajoutfin.close()
            
        creationfin = open("nouveau.txt","a+")
        creationfinlect = creationfin.read()
        for g in range (0,nombre):
            creationfin.write("\n" + ajoutfinsepar[g])
        creationfin.close()
        
        verifFichier= open("unfollow.txt","r")
        verifFichierLecture = verifFichier.read()
        verifFichierLectureSplit = verifFichierLecture.split("/n")
        verifFichier.close()
        
        if verifFichierLectureSplit[0] == "" :
            ajout = open("nouveau.txt","r")
            ajoutlect = ajout.read()                                                                                # Changement de fichier de suivi
            ajoutsepar = ajoutlect.split("\n")
            ajout.close()

            remplacement = open("follow.txt","w")
            for g in range (0,60):
                if g == 0 :
                    remplacement.write(ajoutsepar[g])
                else :
                    remplacement.write("\n" + ajoutsepar[g])

            print("Mise à jour automatique des personnes à suivre effectuée")
            remplacement.close()
            
        else :
            print("le changement prendra effet à la prochaine campagne car une personne n'a pas été défollowé correctement " )
            
                              
        sec = str(nombre3)
        print ("début de la pose de : "+sec+" secondes")
        time.sleep(nombre3)
        


    #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

 

    def campagneFollow(self):

                              
        reglage = open("reglages.txt","r")
        lect = reglage.read()
        virg = lect.split("\n")
        nombre1 = random.randint(9,12)
        nombre2 = int(virg[1])
        nombre3 = int(virg[2])
        sec = str(nombre3)
        reglage.close()



        donnee_source = open("follow.txt", "r") # on ouvre ensuite le fichier unfollow en mode read pour ne pas toucher à ses données.
        donnee_source_lecture= donnee_source.read()
        donnee_source.close()

        creation = open("followrate.txt","w")
        creation.close()

        verification = open("unfollow.txt","r")
        verif_lect = verification.read()
        verification.close()

        #self.getSelfUsersFollowing()
        #midi = self.LastJson
        #tik = json.dumps(midi)
        
        separ_ligne = donnee_source_lecture.split("\n")


        for i in range(0, len(separ_ligne)):  #parcour de la boucle de 0 à la longeur du tableau que l'on vien de créer.
            
            self.timeforce()
            separ_virgule = separ_ligne[i].split(";") #on refait un split qui sépare les différentes données à chaque point virgule
            
            if (len(separ_virgule) == 3) and separ_virgule[0] != ("") :                   #verification pour savoir s'il y a des données dans le fichier follow
                
                follow_a = separ_virgule[1]
                follow_name = separ_virgule[0] # indice 0 car on a le nom en première position
                follow_id = separ_virgule[2] # indice 2 car l'user_id est en  3 eme position

                #if (follow_id in midi):

                    #print(follow_name+" n'est déjà pas suivi ")
                    #unfollowSucess.write(follow_name+";"+follow_a+";"+follow_id+"\n")
                        
                        
                #else:
                if (follow_id in verif_lect):
                    print(follow_name+" est déja suivi")
                                  
                else:
                          
                    unfollowSucess = open("unfollow.txt", "a+") # ouverture en mode écriture du fichier unfollow ou seront écrit les ID_user des personnes followés
                    followrate = open ("followrate.txt","a+") # ouverture en mode écriture du fichier follow raté ou seront écrit les ID_user des personnes qui n'ont pas pu être followés.

                    self.follow(follow_id) #on follow par ID

                    if self.LastResponse.status_code == 200 : # création de la vérification car dans la fct Follow de l'API si la personne a bien été follow elle renvoie un true
                
                        print (follow_name + " a été suivi")

                        unfollowSucess.write(follow_name+";"+follow_a+";"+follow_id+"\n")

                    
                    elif self.LastResponse.status_code == 404 :
                        print( "coordonnées Inconnues données supprimées.")
                    else :
                        print (follow_name + " n'a pas pû être suivi")
                        followrate.write(follow_name+";"+follow_a+";"+follow_id+"\n")

                    followrate.close()
                    unfollowSucess.close()    
                    time.sleep(nombre1)
                    
            else:
                print("ERREUR DONNEE SUPPRIME CAR NON CONFORME")
                 
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------                                                        
        os.remove("follow.txt")
        os.rename("followrate.txt","follow.txt")
        sec = str(nombre3)
        print ("début de la pose de : "+sec+" secondes")
        time.sleep(nombre3)                                    # PAUSE DE 1H

    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class INSTA:

    def lancementApp(self):
    
        fen1 = Tk()

        ndc = StringVar()
        mdp = StringVar()
        txt1 = Label(fen1, text ='Nom de compte :')
        txt2 = Label(fen1, text ='Mot de passe :')
        entr1 = Entry(fen1, textvariable=ndc)
        entr2 = Entry(fen1,show='*', textvariable=mdp)

        can1 = Canvas(fen1, width =160, height =160)
        photo = PhotoImage(file ='connexion.png')
        item = can1.create_image(80, 80, image =photo)

        txt1.grid(row =1, sticky =E)
        txt2.grid(row =2, sticky =E)
        entr1.grid(row =1, column =2)
        entr2.grid(row =2, column =2)
        can1.grid(row =1, column =3, rowspan =3, padx =10, pady =5)

        bou2 = Button(fen1,text='valider',command = fen1.destroy)
        bou2.grid(row =3, sticky =E)

        fen1.mainloop()

        nomDeCompte = (ndc.get())
        motDePasse = (mdp.get())


        instanceClassInsta = InstagramAPI(nomDeCompte,motDePasse)
        instanceClassInsta.login()
    
        if instanceClassInsta.LastResponse.status_code !=200:
            print("Erreur connexion refusé")
            self.lancementApp()
        else:
            instanceClassInsta.fenetre()


main = INSTA()
main.lancementApp()

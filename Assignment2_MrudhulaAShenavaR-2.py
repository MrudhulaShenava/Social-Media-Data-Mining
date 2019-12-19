#!/usr/bin/env python
# coding: utf-8

# In[1]:


import twitter


# In[2]:


def oauth_login():
    CONSUMER_KEY = 'NPZbW3Praoi6hm4iMGZieufxF'
    CONSUMER_SECRET = 'cYTtV54sd9MQwTZk8lbsbMpxLXrH0UIaDYz0XA2ozwQV4D9IDo'
    OAUTH_TOKEN = '839530050-cPlBOP7fHKEq4sScO3MqH2AVBaIDNTwMxfyM2Gk2'
    OAUTH_TOKEN_SECRET = '3YJtuuGkQDMZzR9zzYMLN39ATCxOMz0b15fTo3IL9QkzV'
    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,CONSUMER_KEY, CONSUMER_SECRET)
    twitter_api = twitter.Twitter(auth=auth)
    return twitter_api
twitter_api = oauth_login()
print(twitter_api)


# In[3]:


import sys
import time
from urllib.error import URLError
from http.client import BadStatusLine
import json
import twitter


# In[4]:


def make_twitter_request(twitter_api_func, max_errors=10, *args, **kw):
    
    def handle_twitter_http_error(e, wait_period=2, sleep_when_rate_limited=True):
    
        if wait_period > 3600: # Seconds
            print('Too many retries. Quitting.', file=sys.stderr)
            raise e
            if e.e.code == 401:
                print('Encountered 401 Error (Not Authorized)', file=sys.stderr)
                return None
        elif e.e.code == 404:
            printnt('Encountered 404 Error (Not Found)', file=sys.stderr)
            return None
        elif e.e.code == 429: 
            print('Encountered 429 Error (Rate Limit Exceeded)', file=sys.stderr)
            if sleep_when_rate_limited:
                print("Retrying in 15 minutes...ZzZ...", file=sys.stderr)
                sys.stderr.flush()
                time.sleep(60*15 + 5)
                print('...ZzZ...Awake now and trying again.', file=sys.stderr)
                return 2
            else:
                raise e # Caller must handle the rate limiting issue 
        elif e.e.code in (500, 502, 503, 504):
            print('Encountered {0} Error. Retrying in {1} seconds' .format(e.e.code, wait_period), file=sys.stderr)
            time.sleep(wait_period)
            wait_period *= 3
            return wait_period
        else:
            raise e
            
    wait_period = 3 
    error_count = 0 

    while True:
        try:
            return twitter_api_func(*args, **kw)
        except twitter.api.TwitterHTTPError as e:
            error_count = 0 
            wait_period = handle_twitter_http_error(e, wait_period)
            if wait_period is None:
                return
        except URLError as e:
            error_count += 1
            time.sleep(wait_period)
            wait_period *= 3
            print("URLError encountered. Continuing.", file=sys.stderr)
            if error_count > max_errors:
                print("Too many consecutive errors...bailing out.", file=sys.stderr)
                raise
        except BadStatusLine as e:
            error_count += 1
            time.sleep(wait_period)
            wait_period *= 3
            print("BadStatusLine encountered. Continuing.", file=sys.stderr)
            if error_count > max_errors:
                print("Too many consecutive errors...bailing out.", file=sys.stderr)
                raise


# In[5]:


from functools import partial
from sys import maxsize as maxint


# In[6]:


def get_friends_followers_ids(twitter_api, screen_name=None, user_id=None,
                              friends_limit=maxint, followers_limit=maxint):
    #Must have either screen_name or user_id (logical xor)
    assert (screen_name != None) != (user_id != None),     "Must have screen_name or user_id, but not both"
    #5000 friends and follower ids
    get_friends_ids = partial(make_twitter_request, twitter_api.friends.ids, 
                              count=5000)
    get_followers_ids = partial(make_twitter_request, twitter_api.followers.ids, 
                                count=5000)

    friends_ids, followers_ids = [], []
    #api call to get friends and follower ids using partial
    for twitter_api_func, limit, ids, label in [
                    [get_friends_ids, friends_limit, friends_ids, "friends"], 
                    [get_followers_ids, followers_limit, followers_ids, "followers"]
                ]:
        
        if limit == 0: continue
        
        cursor = -1
        while cursor != 0:
        
            # Use make_twitter_request via the partially bound callable...
            if screen_name: 
                response = twitter_api_func(screen_name=screen_name, cursor=cursor)
            else: # user_id
                response = twitter_api_func(user_id=user_id, cursor=cursor)

            if response is not None:
                ids += response['ids']
                cursor = response['next_cursor']
        
            print('Fetched {0} total {1} ids for {2}'.format(len(ids),
                                                             label, (user_id or screen_name)),file=sys.stderr)
        
            # XXX: You may want to store data during each iteration to provide an 
            # an additional layer of protection from exceptional circumstances
        
            if len(ids) >= limit or response is None:
                break

    # Do something useful with the IDs, like store them to disk...
    #return no of friends and follower ids upto the limit asked
    return friends_ids[:friends_limit], followers_ids[:followers_limit]

# Sample usage

twitter_api = oauth_login()

friends_ids, followers_ids = get_friends_followers_ids(twitter_api, 
                                                       screen_name="sundarpichai", 
                                                       friends_limit=10, 
                                                       followers_limit=10)

print(friends_ids)
print(followers_ids)


# In[7]:


screen_name = 'sundarpichai'


# In[8]:


response = make_twitter_request(twitter_api.friends.ids,
                                screen_name=screen_name, count = 5000)
friends = response["ids"]


# In[9]:


#Finding reciprocal of friends
reciprocal_friends = set(friends)

reciprocal_friends


# In[10]:


def get_user_profile(twitter_api, screen_names=None, user_ids=None):
    assert (screen_names != None) != (user_ids != None),     "Must have screen_names or user_ids, but not both"
    
    items_to_info = {}

    items = screen_names or user_ids
    
    while len(items) > 0:

        # Process 100 items at a time per the API specifications for /users/lookup.
        # See http://bit.ly/2Gcjfzr for details.
        
        items_str = ','.join([str(item) for item in items[:100]])
        items = items[100:]

        if screen_names:
            response = make_twitter_request(twitter_api.users.lookup, 
                                            screen_name=items_str)
        else: # user_ids
            response = make_twitter_request(twitter_api.users.lookup, 
                                            user_id=items_str)
    
        for user_info in response:
            if screen_names:
                items_to_info[user_info['screen_name']] = user_info
            else: # user_ids
                items_to_info[user_info['id']] = user_info

    return items_to_info

# Sample usage

twitter_api = oauth_login()

print(get_user_profile(twitter_api, screen_names=["SocialWebMining", "sundarpichai"]))


# In[11]:


import pandas as pd
df = pd.DataFrame(columns=['ID','ReciprocalFriend'])
df.to_csv('ReciprocalFriend.csv', index=False)

# Our function
def save_followers(fid, reciprocal_friend):
    data_frame_rf = [[str(fid), str(i)] for i in reciprocal_friend]
    #print(data_frame_rf)
    df = pd.DataFrame(data_frame_rf, columns=['ID','ReciprocalFriend'])
    with open('ReciprocalFriend.csv', 'a') as f:
        df.to_csv(f,header=False, index=False)


# In[12]:


def crawl_followers(twitter_api, screen_name, limit=1000000, depth=2):
    
    # Resolve the ID for screen_name and start working with IDs for consistency
    seed_id = str(twitter_api.users.show(screen_name=screen_name)['id'])
    friends_ids, followers_ids = get_friends_followers_ids(twitter_api, user_id=seed_id,
                                 friends_limit=limit, followers_limit=limit)
    rp_friend = list(set(friends_ids) & set(followers_ids))
    top_five = get_user_profile(twitter_api, user_ids=rp_friend[:100])
    next_queue = top_five
    # Store a seed_id => _follower_ids mapping in MongoDB
    
    save_followers(seed_id, next_queue)
    
    d = 1
    # Note that in the example in the next cell,
    # we never enter this loop.
    while d < depth:
        print("Number of ", d,"- Distance node", len(next_queue))
        d += 1
        # Reset the next_queue so that we can
        # start building up the next level
        # of followers-of-followers
        (queue, next_queue) = (next_queue, [])
        # Loop through the current
        # level of followers
        for fid in queue:
            friends_ids, followers_ids = get_friends_followers_ids(twitter_api, user_id=fid,
                                friends_limit=limit, followers_limit=limit)
            # Store an ID with a string recording
            # IDs of followers of the user with ID "fid"
            rp_friend = list(set(friends_ids) & set(followers_ids))
            if (len(rp_friend) == 0):
                continue
            top_five = get_user_profile(twitter_api, user_ids=rp_friend[-100:])
            save_followers(str(fid), top_five)
            # Extending the list
            next_queue += top_five


# In[13]:


screen_name = 'TechnologyGuy'
crawl_followers(twitter_api, screen_name, depth=2, limit=5000)


# In[ ]:





# In[14]:


import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
# Create Graph from file
df = pd.read_csv("ReciprocalFriend.csv")
x_point = list(df[df.columns[0]].values)
y_point = list(df[df.columns[1]].values)
edges_list = []
for i in range(len(x_point)):
    edges_list.append((x_point[i], y_point[i]))
node_list = set(x_point+y_point)
RG = nx.Graph()
RG.add_nodes_from(node_list)
RG.add_edges_from(edges_list)
# Display some graph information such as number of nodes and edges
print ("Number of Nodes :", RG.number_of_nodes())
print ("Numebr of edges :", RG.number_of_edges())


# In[20]:


lmbds,vctrs = np.linalg.eig(L)
indx = [i for i in range(len(lmbds)) if lmbds[i] > .01 and lmbds[i] < .03]
RG_mbd = vctrs[:,indx]
print ("Number of Communities:", len(indx))


# In[21]:


est = KMeans(max_iter = 100000, n_clusters = len(indx), n_init = 200, init='k-means++')  
results_df['kmeans'] = est.fit(RG_mbd)
# y_pred[i] = ada.predict([X.iloc[i, :]])[0]
# Apply k-means
# est = KMeans(n_clusters=len(indx))
# est.fit(RG_mbd)


# In[23]:


pos = nx.spring_layout(RG)
nx.draw_networkx_nodes(RG,pos,
                       nodelist=node_list,
                       node_color='r',
                       node_size=100,
                   alpha=0.9)
nx.draw_networkx_edges(RG,pos)
plt.show()


# In[24]:


pos = nx.spring_layout(RG)
nx.draw_networkx_nodes(RG,pos,nodelist=node_list, node_color='b',
                       node_shape='o', node_size=1, alpha=1)
nx.draw_networkx_edges(RG,pos)
plt.show()


# In[25]:


print('The diameter is: ',nx.diameter(RG))


# In[26]:


print('The average distance between nodes is: ',nx.average_shortest_path_length(RG))


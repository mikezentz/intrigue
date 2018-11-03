import praw
import datetime
import pprint

# posts = [
#     {
#         'body': 'bob silent boy',
#         'score': 5,
#     },
#     {
#         'body': 'bob',
#         'score': 3,
#     },
#     {
#         'body': 'bob silent boy george',
#         'score': 1,
#     },
# ]
#
# search_terms = ['bob', 'silent boy', 'george']
#
# for post in posts:
#     post['contains'] = []
#     for term in search_terms:
#         if term in post['body']:
#             post['contains'].append(term)
#
# sorted_posts = sorted(posts, key=lambda x: len(x['contains']), reverse=True)
#
# # pprint.pprint(posts)
# # pprint.pprint(sorted_posts)
#
# for post in sorted_posts:
#     post['weight'] = (len(post['contains']) * .5) + (post['score'] * .5)
#     print(post['weight'])
#
# weighted_posts = sorted(sorted_posts, key=lambda x: x['weight'], reverse=True)


r = praw.Reddit(user_agent='testredditapi1',
                client_id='nZw0Z9BUaXsfew', client_secret="8y0h9Q-NzCyPjOgOxwOiaGt9iUM")

subreddits = ['all', 'ethereum', 'cryptocurrency',
              'blockchain', 'ethereumprojects', 'coindev', 'cryptotechnology', 'icocrypto', 'blockchainstartups']

searchterms = ['amberdata', 'contract', 'contracts',
               'integrity', 'analytics', 'realtime', 'api', 'etherscan', 'monitoring', 'saas', 'searching', 'analyzing', 'infrastructure', 'dapps', 'token utilization', 'security', 'audit', 'vulnerabilities', 'vulnerability', 'smart']


posts = []

for forum in subreddits:
    subreddit = r.subreddit(forum)
    for submission in subreddit.hot(limit=500):
        if not submission.selftext:
            continue
        for term in searchterms:
            if term in submission.title.casefold() or term in submission.selftext.casefold():
                posts.append({
                    "subreddit": forum,
                    "title": submission.title,
                    "score": submission.score,
                    "comments": submission.num_comments,
                    "link": submission.permalink,
                    "date": submission.created_utc,
                    "body": submission.selftext
                })

maxscore = 1
mostrecent = 1
mostcomments = 1
for post in posts:
    if post['score'] >= maxscore:
        maxscore = post['score']
    if post['date'] >= mostrecent:
        mostrecent = post['date']
    if post['comments'] >= mostcomments:
        mostcomments = post['comments']
    post['contains'] = []
    for term in searchterms:
        if term in post['body'].casefold() or term in post['title'].casefold():
            post['contains'].append(term)

# sorted_posts = sorted(posts, key=lambda x: len(x['contains']), reverse=True)

for post in posts:
    post['weight'] = (len(post['contains']) / len(searchterms)) * .75
    post['weight'] += (post['score'] / maxscore) * .05
    post['weight'] += (post['date'] / mostrecent) * .15
    post['weight'] += (post['comments'] / mostcomments) * .05

weighted_posts = sorted(posts, key=lambda x: x['weight'], reverse=True)

pprint.pprint(weighted_posts[:2])


#
# print(subreddit)
# count = 0
#
#
# results = []
#
# for submission in subreddit.hot(limit=500):
#     count += 1
#     # print(submission.title)
#     # print(submission.selftext)
#     # print()
#     if searchterm in submission.title or searchterm.title() in submission.title:
#         results.append({
#             "title": submission.title,
#             "score": submission.score,
#             "comments": submission.num_comments,
#             "link": submission.permalink,
#             "date": submission.created_utc
#         })
#
#         # print("title", submission.title)
#         # print("score", submission.score)
#         # print("comments", submission.num_comments)
#         # print("link", submission.permalink)
#         # print("date", datetime.datetime.utcfromtimestamp(
#         #     int(submission.created_utc)).strftime('%Y-%m-%d %H:%M:%S'))
#         # print()
#
# # print(results)
# print(results[0])

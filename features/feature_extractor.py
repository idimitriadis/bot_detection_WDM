from features import temporal_features as tf
from features import user_features as uf
from features import tools
from bot_data import get_user_label
from pymongo import MongoClient
from dotenv import load_dotenv
import pickle
import os

load_dotenv()

client = MongoClient(host=os.getenv("DB_HOST"), port=int(os.getenv("DB_PORT")),
                     username=os.getenv("DB_USERNAME"), password=os.getenv("DB_PASSWORD"), authSource=os.getenv("DB_AUTH_DB"))
db = client[os.getenv("DB_AUTH_DB")]
collection = db[os.getenv("COL")]

labels = get_user_label()

def get_user_features(tweets):
    user = tools.get_user_object(tweets)
    user_vector = {
        "user_id": uf.get_user_id(user),
        "user_name": uf.get_user_name(user),
        "user_screen_name": uf.get_user_screen_name(user),
        "followers_count": uf.get_followers_count(user),
        "followees_count": uf.get_friends_count(user),
        "followers_to_friends": uf.get_followers_to_friends(user),
        "tweets_count": uf.get_tweets_count(user),
        "listed_count": uf.get_listed_count(user),
        "favorites_count": uf.get_favourites_count(user),
        "default_profile": uf.is_default_profile(user),
        "default_profile_image": uf.has_default_profile_image(user),
        "verified": uf.is_verified(user),
        "location": uf.has_location(user),
        "url": uf.has_url(user),
        "description": uf.has_description(user),
        "name_length": uf.get_name_length(user),
        "screen_name_length": uf.get_screen_name_length(user),
        "description_length": uf.get_description_length(user),
        "numerics_in_name_count": uf.get_numbers_count_in_name(user),
        "numerics_in_screen_name_count": uf.get_numbers_count_in_screen_name(user),
        "hashtags_in_name": uf.has_hashtags_in_name(user),
        "hashtags_in_description": uf.has_hashtags_in_description(user),
        "urls_in_description": uf.has_urls_in_description(user),
        "bot_word_in_name": uf.has_bot_word_in_name(user),
        "bot_word_in_screen_name": uf.has_bot_word_in_screen_name(user),
        "bot_word_in_description": uf.has_bot_word_in_description(user),
        "tweet_posting_rate_per_day": uf.get_tweet_posting_rate_per_day(user),
        "favorite_rate_per_day": uf.get_favorite_rate_per_day(user),
        "description_sentiment": uf.get_description_sentiment(user),
        "description_emojis": uf.get_emojis_in_description(user)
    }
    return user_vector

def get_temporal_features(tweets):

    total_tweets_per_day_distro = tf.get_max_min_tweets_per_day(tweets)
    total_tweets_per_hour_distro = tf.get_max_min_tweets_per_hour(tweets)
    tweets_per_day_distro = tf.get_max_min_tweets_per_day(tweets)
    tweets_per_hour_distro = tf.get_max_min_tweets_per_hour(tweets)
    avg_time_between_tweets_distro = tf.get_average_time_between_tweets(tweets)
    temporal_features_vector = {
        "user_id": tools.get_user_id(tweets),
        "user_name": tools.get_user_name(tweets),
        "user_screen_name": tools.get_user_screen_name(tweets),
        "total_min_tweets_per_day": total_tweets_per_day_distro[0],
        "total_max_tweets_per_day": total_tweets_per_day_distro[1],
        "total_mean_tweets_per_day": total_tweets_per_day_distro[2],
        "total_median_tweets_per_day": total_tweets_per_day_distro[3],
        "total_std_tweets_per_day": total_tweets_per_day_distro[4],
        "total_skew_tweets_per_day": total_tweets_per_day_distro[5],
        "total_kurt_tweets_per_day": total_tweets_per_day_distro[6],
        "total_entropy_tweets_per_day": total_tweets_per_day_distro[7],
        "total_min_tweets_per_hour": total_tweets_per_hour_distro[0],
        "total_max_tweets_per_hour": total_tweets_per_hour_distro[1],
        "total_mean_tweets_per_hour": total_tweets_per_hour_distro[2],
        "total_median_tweets_per_hour": total_tweets_per_hour_distro[3],
        "total_std_tweets_per_hour": total_tweets_per_hour_distro[4],
        "total_skew_tweets_per_hour": total_tweets_per_hour_distro[5],
        "total_kurt_tweets_per_hour": total_tweets_per_hour_distro[6],
        "total_entropy_tweets_per_hour": total_tweets_per_hour_distro[7],
        "min_tweets_per_day": tweets_per_day_distro[0],
        "max_tweets_per_day": tweets_per_day_distro[1],
        "mean_tweets_per_day": tweets_per_day_distro[2],
        "median_tweets_per_day": tweets_per_day_distro[3],
        "std_tweets_per_day": tweets_per_day_distro[4],
        "skew_tweets_per_day": tweets_per_day_distro[5],
        "kurt_tweets_per_day": tweets_per_day_distro[6],
        "entropy_tweets_per_day": tweets_per_day_distro[7],
        "min_tweets_per_hour": tweets_per_hour_distro[0],
        "max_tweets_per_hour": tweets_per_hour_distro[1],
        "mean_tweets_per_hour": tweets_per_hour_distro[2],
        "median_tweets_per_hour": tweets_per_hour_distro[3],
        "std_tweets_per_hour": tweets_per_hour_distro[4],
        "skew_tweets_per_hour": tweets_per_hour_distro[5],
        "kurt_tweets_per_hour": tweets_per_hour_distro[6],
        "entropy_tweets_per_hour": tweets_per_hour_distro[7],
        "consecutive_days_of_no_activity": tf.get_consecutive_days_of_no_activity(tweets),
        "consecutive_days_of_activity": tf.get_consecutive_days_of_activity(tweets),
        "consecutive_hours_of_no_activity": tf.get_consecutive_hours_of_no_activity(tweets),
        "consecutive_hours_of_activity": tf.get_consecutive_hours_of_activity(tweets),
        "min_avg_time_between_tweets": avg_time_between_tweets_distro[0],
        "max_avg_time_between_tweets": avg_time_between_tweets_distro[1],
        "mean_avg_time_between_tweets": avg_time_between_tweets_distro[2],
        "median_avg_time_between_tweets": avg_time_between_tweets_distro[3],
        "std_avg_time_between_tweets": avg_time_between_tweets_distro[4],
        "skew_avg_time_between_tweets": avg_time_between_tweets_distro[5],
        "kurt_avg_time_between_tweets": avg_time_between_tweets_distro[6],
        "entropy_avg_time_between_tweets": avg_time_between_tweets_distro[7],
        "max_occurence_of_same_gap_in_seconds": tf.get_max_occurence_of_same_gap(tweets)
    }
    return temporal_features_vector

def get_all_features_train(user,tweets,labels):
    user_vector = get_user_features(tweets)
    temporal = get_temporal_features(tweets)
    total = {**user_vector, **temporal}
    total['label'] = labels[user['id_str']]
    return total

def create_training_set(labels):
    final_data=[]
    allUsers = labels.keys()
    for u in allUsers:
        userTweets = []
        iterator = collection.find({'user.id_str':u})
        if iterator.count()>0:
            for i in iterator:
                userTweets.append(i)
            user_dict = tools.get_user_object(userTweets)
            print (u)
            features = get_all_features_train(user_dict,userTweets,labels)
            final_data.append(features)
    pickle.dump(final_data,open('data','wb'))
    return final_data

# create_training_set(labels)



# authentication/social_helpers.py
from allauth.socialaccount.models import SocialAccount, SocialToken
import requests
from django.conf import settings

def get_social_metrics(user):
    """
    Try to fetch follower/subscriber counts from connected social accounts.
    Returns a dict: { 'instagram': int|None, 'facebook': int|None, 'youtube': int|None }
    """
    metrics = {'instagram': None, 'facebook': None, 'youtube': None}
    accounts = SocialAccount.objects.filter(user=user)

    for acc in accounts:
        provider = acc.provider  # 'facebook', 'instagram', 'google' (for YouTube) depending on your setup
        token_obj = SocialToken.objects.filter(account=acc).first()
        token = token_obj.token if token_obj else None

        # INSTAGRAM via Graph API: need ig user id -> acc.extra_data often contains instagram_business_account or id
        if provider in ('instagram', 'facebook'):
            # Many setups store the FB / IG ids in acc.extra_data:
            extra = acc.extra_data or {}
            # If this SocialAccount is a facebook page connection, it might contain 'id' or 'instagram_business_account'
            ig_id = None
            fb_id = None
            if provider == 'instagram':
                ig_id = extra.get('id') or extra.get('instagram_business_account', {}).get('id')
            elif provider == 'facebook':
                fb_id = extra.get('id')

            # Try Instagram follower count (IG user endpoint)
            if ig_id and token:
                try:
                    url = f"https://graph.facebook.com/v16.0/{ig_id}"
                    params = {"fields": "followers_count,username,account_type", "access_token": token}
                    r = requests.get(url, params=params, timeout=8)
                    data = r.json()
                    if 'followers_count' in data and data['followers_count'] is not None:
                        metrics['instagram'] = int(data['followers_count'])
                except Exception:
                    pass

            # Try Facebook Page followers
            if fb_id and token:
                try:
                    url = f"https://graph.facebook.com/v16.0/{fb_id}"
                    params = {"fields": "followers_count,fan_count", "access_token": token}
                    r = requests.get(url, params=params, timeout=8)
                    data = r.json()
                    # prefer followers_count, fallback to fan_count
                    if data.get('followers_count') is not None:
                        metrics['facebook'] = int(data['followers_count'])
                    elif data.get('fan_count') is not None:
                        metrics['facebook'] = int(data['fan_count'])
                except Exception:
                    pass

        # YOUTUBE via Google provider (allauth 'google')
        if provider in ('google', 'youtube'):
            if token:
                try:
                    # Using OAuth access token to get channel statistics for the authenticated user
                    url = "https://www.googleapis.com/youtube/v3/channels"
                    headers = {"Authorization": f"Bearer {token}"}
                    params = {"part": "statistics", "mine": "true", "maxResults": 1}
                    r = requests.get(url, headers=headers, params=params, timeout=8)
                    data = r.json()
                    items = data.get("items") or []
                    if items:
                        stats = items[0].get("statistics", {})
                        sub = stats.get("subscriberCount")
                        if sub is not None:
                            metrics['youtube'] = int(sub)
                except Exception:
                    pass

    return metrics

def categorize_influencer(metrics: dict):
    """
    Determine creator_type from metrics.
    Returns (category, top_platform, top_count)
    Category thresholds are configurable — adjust to match your business logic.
    Current thresholds (example):
      - Nano: <10,000
      - Micro: 10k - 100k
      - Macro: 100k - 1M
      - Mega: 1M - 5M
      - Mega A+: 5M - 10M
      - Celebrities: 10M - 50M
      - Premium Celebrities: 50M+
    """
    # choose the highest count across platforms
    platform, count = None, 0
    for p, c in metrics.items():
        if c and c > count:
            platform, count = p, c

    if count == 0:
        return ("Nano", None, 0)  # default if nothing available; you can also use 'Unknown' or force manual verification

    if count < 10_000:
        return ("Nano", platform, count)
    if count < 100_000:
        return ("Micro", platform, count)
    if count < 1_000_000:
        return ("Macro", platform, count)
    if count < 5_000_000:
        return ("Mega", platform, count)
    if count < 10_000_000:
        return ("Mega A+", platform, count)
    if count < 50_000_000:
        return ("Celebrities", platform, count)
    return ("Premium Celebrities", platform, count)

# config.py

from authomatic.providers import oauth2, oauth1, openid, gaeopenid

CONFIG = {
    
    'tw': { # Your internal provider name
           
        # Provider class
        'class_': oauth1.Twitter,
        
        # Twitter is an AuthorizationProvider so we need to set several other properties too:
        'consumer_key': '########################',
        'consumer_secret': '########################',
    },
    
    'fb': {
           
        'class_': oauth2.Facebook,
        
        # Facebook is an AuthorizationProvider too.
        'consumer_key': '254311618073113',
        'consumer_secret': 'ee2aa55d2ee8a98166d12448d0a3e618',
        
        # But it is also an OAuth 2.0 provider and it needs scope.
        'scope': ['user_about_me', 'email', 'user_location'],
    },
    
    'ya' : {
        'class_': oauth1.Yahoo,
        # Yahoo is an AuthorizationProvider too.
        
        # website: fantasycrystalball.com
        #'consumer_key': 'dj0yJmk9UXFyRk5hYWZNSnB1JmQ9WVdrOVlUQTFTek5uTjJrbWNHbzlNVGMwTURjNE1qTTJNZy0tJnM9Y29uc3VtZXJzZWNyZXQmeD00ZA--',
        #'consumer_secret': '8e0f1ee22c69acda1974992c361c0851ebc1ee1a',
        
        # mywebsite.com
        'consumer_key': 'dj0yJmk9Q0RNYUNNZVBTVGtOJmQ9WVdrOWRIcHhlSGd5TXpnbWNHbzlNVEEwTXpRME9EazJNZy0tJnM9Y29uc3VtZXJzZWNyZXQmeD04Zg--',
        'consumer_secret': 'a002d18b1e30837716aa23aa85f7952aafb7c35d',
        'short_name': 1
   },
    
    'gae_oi': {
           
        # OpenID provider based on Google App Engine Users API.
        # Works only on GAE and returns only the id and email of a user.
        # Moreover, the id is not available in the development environment!
        'class_': gaeopenid.GAEOpenID,
    },
    
    'oi': {
           
        # OpenID provider based on the python-openid library.
        # Works everywhere, is flexible, but requires more resources.
        'class_': openid.OpenID,
    }
}

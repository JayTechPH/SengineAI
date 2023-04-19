from facebook_bot.facebook_bot import facebook_bot
import json

if __name__=='__main__':
    with open ('config.json') as file:
        config = json.load(file)
        
        
    gcid = config['gcid']
    username = config['username']    
    password = config['password']
    morning = config['morning']
    evening = config['evening']
    afternoon = config['afternoon']
    night = config['night']
    
    
    facebook_bot(gcid, username, password, morning, evening, afternoon, night)
    
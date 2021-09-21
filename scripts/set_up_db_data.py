import random

# Models
from mydea.users.models import User
from mydea.socials.models import Request

def run():
    # Get all users    
    users = User.objects.all()
    # Verify all users
    for user in users:
        user.status.verified = True
        user.status.save(update_fields=["verified"]) 
        # Create requests for each user        
        # Create accepted requests for all user's following       
        followed_users = user.connection.following.all()
        for followed in followed_users:          
            request = Request(
                sender = user,
                receiver = followed,
                status = 'A'
            )           
            request.save()

        # Get the non-followed users
        non_followed_users = [
            u for u in list(users) if u not in list(followed_users) and u != user
        ]
        # Create sent request to n-number of non-followed users        
        n = 3; 
        rand_id_arr = []
        count_attempts = 0
        max_attempts = 50*len(non_followed_users)
        # Select 3 random users ids
        while(len(rand_id_arr) < n or count_attempts > max_attempts):
            count_attempts += 1
            rand_id = random.randrange(0, len(non_followed_users)) 
            if(rand_id not in rand_id_arr): # ensure non-duplicates
                rand_id_arr.append(rand_id)
        # Create requests
        for rand_id in rand_id_arr:               
            request = Request(
                sender = user,
                receiver = non_followed_users[rand_id],
                status = 'S'
            )           
            request.save()
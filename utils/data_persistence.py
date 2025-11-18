"""
Data persistence functions for saving and loading user data and ratings.
"""
import json
import os
from datetime import datetime

def save_user_data(user):
    """
    Save user demographic data to a JSON file.
    Creates user_data directory if it doesn't exist.
    """
    try:
        os.makedirs('user_data', exist_ok=True)

        filename = f"{user.user_id}.json"
        path = os.path.join('user_data', filename)

        data = user.to_dict()

        with open(path, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"[INFO] User data saved: {filename}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to save user data: {e}")
        return False

def save_rating(user_id, action_id, scale_values, action_not_recognized=False):
    """
    Save rating data to a JSON file.
    Creates user_ratings directory if it doesn't exist.

    Parameters:
    - user_id: User identifier
    - action_id: Action/video identifier
    - scale_values: Dictionary of scale titles to values
    - action_not_recognized: Boolean flag

    Returns:
    - True if save successful, False otherwise
    """
    try:
        os.makedirs('user_ratings', exist_ok=True)

        # Build rating data
        rating_data = {
            'user_id': user_id,
            'id': action_id,
            'action_not_recognized': action_not_recognized
        }

        # Add each scale's value
        for title, value in scale_values.items():
            # Use title as key (sanitized for JSON compatibility)
            key = title.lower().replace(' ', '_')
            rating_data[key] = value

        # Save to file
        filename = os.path.join('user_ratings', f"{user_id}_{action_id}.json")
        with open(filename, 'w') as f:
            json.dump(rating_data, f, indent=2)

        print(f"[INFO] Rating saved: {user_id}_{action_id}.json")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to save rating: {e}")
        return False

def user_exists(user_id):
    """
    Check if a user_id exists in the user_ratings directory.

    Parameters:
    - user_id: User identifier to check

    Returns:
    - True if user has at least one rating file, False otherwise
    """
    try:
        if not os.path.exists('user_ratings'):
            return False

        user_ratings_files = os.listdir('user_ratings')
        return any(f.startswith(f"{user_id}_") for f in user_ratings_files)
    except Exception as e:
        print(f"[ERROR] Failed to check user existence: {e}")
        return False

def get_rated_videos_for_user(user_id):
    """
    Get list of video IDs already rated by a user.

    Parameters:
    - user_id: User identifier

    Returns:
    - List of action IDs (without .mp4 extension)
    """
    try:
        if not os.path.exists('user_ratings'):
            return []

        files = os.listdir('user_ratings')
        rated_ids = []

        for f in files:
            if f.startswith(f"{user_id}_") and f.endswith('.json'):
                # Extract action_id from filename: {user_id}_{action_id}.json
                action_id = f.replace('.json', '').replace(f'{user_id}_', '')
                rated_ids.append(action_id)

        return rated_ids
    except Exception as e:
        print(f"[ERROR] Failed to get rated videos: {e}")
        return []

"""
Profile and high score management system.
"""

import json
import os
from datetime import datetime
from config import SCORES_FILE, PROFILES_FILE

class ProfileManager:
    """Manages player profiles and high scores."""
    
    def __init__(self):
        self.profiles = self._load_profiles()
        self.scores = self._load_scores()
        self.current_profile = None
    
    def _load_profiles(self):
        """Load profiles from file."""
        if os.path.exists(PROFILES_FILE):
            try:
                with open(PROFILES_FILE, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_profiles(self):
        """Save profiles to file."""
        with open(PROFILES_FILE, 'w') as f:
            json.dump(self.profiles, f, indent=2)
    
    def _load_scores(self):
        """Load high scores from file."""
        if os.path.exists(SCORES_FILE):
            try:
                with open(SCORES_FILE, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save_scores(self):
        """Save high scores to file."""
        with open(SCORES_FILE, 'w') as f:
            json.dump(self.scores, f, indent=2)
    
    def create_profile(self, name):
        """Create or load a player profile."""
        if not name or len(name.strip()) == 0:
            return False
        
        name = name.strip()
        
        if name not in self.profiles:
            self.profiles[name] = {
                'name': name,
                'created': datetime.now().isoformat(),
                'games_played': 0,
                'best_score': 0,
                'highest_level': 0
            }
            self._save_profiles()
        
        self.current_profile = name
        return True
    
    def get_profile(self, name):
        """Get profile data."""
        return self.profiles.get(name)
    
    def update_profile(self, score, level):
        """Update current profile with game results."""
        if not self.current_profile:
            return
        
        profile = self.profiles[self.current_profile]
        profile['games_played'] += 1
        
        if score > profile['best_score']:
            profile['best_score'] = score
        
        if level > profile['highest_level']:
            profile['highest_level'] = level
        
        self._save_profiles()
    
    def add_score(self, name, score, level):
        """Add a score to the high scores list."""
        score_entry = {
            'name': name,
            'score': score,
            'level': level,
            'date': datetime.now().isoformat()
        }
        
        self.scores.append(score_entry)
        
        # Sort by score (descending)
        self.scores.sort(key=lambda x: x['score'], reverse=True)
        
        # Keep only top 10
        self.scores = self.scores[:10]
        
        self._save_scores()
    
    def get_high_scores(self, limit=10):
        """Get top high scores."""
        return self.scores[:limit]
    
    def get_all_profiles(self):
        """Get list of all profile names."""
        return sorted(self.profiles.keys())
    
    def get_current_profile_name(self):
        """Get current profile name."""
        return self.current_profile
    
    def is_high_score(self, score):
        """Check if score qualifies as a high score."""
        if len(self.scores) < 10:
            return True
        return score > self.scores[-1]['score']

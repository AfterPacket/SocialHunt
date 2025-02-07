import requests
import time
import json
import argparse
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import quote_plus
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
import logging

def print_banner():
    """Print the application banner with ASCII art."""
    banner = """
\033[36m
███████╗ ██████╗  ██████╗██╗ █████╗ ██╗     ██╗  ██╗██╗   ██╗███╗   ██╗████████╗
██╔════╝██╔═══██╗██╔════╝██║██╔══██╗██║     ██║  ██║██║   ██║████╗  ██║╚══██╔══╝
███████╗██║   ██║██║     ██║███████║██║     ███████║██║   ██║██╔██╗ ██║   ██║   
╚════██║██║   ██║██║     ██║██╔══██║██║     ██╔══██║██║   ██║██║╚██╗██║   ██║   
███████║╚██████╔╝╚██████╗██║██║  ██║███████╗██║  ██║╚██████╔╝██║ ╚████║   ██║   
╚══════╝ ╚═════╝  ╚═════╝╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   
                                                                                  
           ┌─┐┌─┐┌─┐┬┌─┐┬    ┌┬┐┌─┐┌┬┐┌─┐┌─┐┌┬┐┬┬  ┬┌─┐
           └─┐│ ││  │├─┤│     ││├┤  │ ├┤ │   │ │└┐┌┘├┤ 
           └─┘└─┘└─┘┴┴ ┴┴─┘  ─┴┘└─┘ ┴ └─┘└─┘ ┴ ┴ └┘ └─┘\033[0m

\033[35m
                                    .---.
                               .---.|   |
                        _.---._|   ||   |
                      .'       |   ||   |
                     /     \\   |   ||   |
                    /    .-\\  |   ||   |
                   /  .-'   \\ |   ||   |
                  /.-'       \\|   ||   |
                 /           `\\   ||   |
                |               \\  ||   |
                |     ,     ,    \\ ||   |
                |    /|    /|     \\||   |
                |   / |   / |      `'   |
                |  /  |  /  |          /
                | /   | /   |         /
                |/    |/    |        /
                '     '     '       '\033[0m

   \033[33m[ Username Search Tool - Version 1.0 - Made by SecRas ]\033[0m
"""
    print(banner)

class UsernameSearch:
    def __init__(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('username_search.log'),
                logging.StreamHandler()
            ]
        )
        
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive"
        }

        # Initialize platforms dictionary
        self.platforms = {
            "instagram": {
                "url": "https://www.instagram.com/{}",
                "error_patterns": ["Sorry, this page isn't available.", "Page Not Found"],
                "success_patterns": ["profile picture", "Followers", "Following"]
            },
            "tiktok": {
                "url": "https://www.tiktok.com/@{}",
                "error_patterns": ["Couldn't find this account", "This account was not found"],
                "success_patterns": ["profile", "Following", "Followers", "Likes"]
            },
            "twitter": {
                "url": "https://nitter.net/{}",
                "error_patterns": ["User not found", "This account doesn't exist"],
                "success_patterns": ["Followers", "Following", "Tweets"]
            },
            "facebook": {
                "url": "https://www.facebook.com/{}",
                "error_patterns": ["Page Not Found", "Content Not Found"],
                "success_patterns": ["profile picture", "Timeline", "About"]
            },
            "youtube": {
                "url": "https://www.youtube.com/@{}",
                "error_patterns": ["404", "This channel does not exist"],
                "success_patterns": ["subscribers", "videos", "channel"]
            },
            "github": {
                "url": "https://github.com/{}",
                "error_patterns": ["Not Found", "404"],
                "success_patterns": ["repositories", "contributions", "followers"]
            },
            "reddit": {
                "url": "https://www.reddit.com/user/{}",
                "error_patterns": ["page not found", "Sorry, nobody on Reddit goes by that name"],
                "success_patterns": ["karma", "Cake day", "comments"]
            },
            "telegram": {
                "url": "https://t.me/{}",
                "error_patterns": ["If you have Telegram, you can contact"],
                "success_patterns": ["subscribers", "members", "online"]
            },
            "twitch": {
                "url": "https://www.twitch.tv/{}",
                "error_patterns": ["page not found"],
                "success_patterns": ["profile", "followers", "channel"]
            },
            "pinterest": {
                "url": "https://www.pinterest.com/{}",
                "error_patterns": ["Sorry! We couldn't find that page"],
                "success_patterns": ["followers", "following", "Pins"]
            },
            "steam": {
                "url": "https://steamcommunity.com/id/{}",
                "error_patterns": ["The specified profile could not be found"],
                "success_patterns": ["profile", "games", "badges"]
            },
            "snapchat": {
                "url": "https://www.snapchat.com/add/{}",
                "error_patterns": ["page could not be found"],
                "success_patterns": ["Add on Snapchat", "snapcode"]
            },
            "spotify": {
                "url": "https://open.spotify.com/user/{}",
                "error_patterns": ["page is not available"],
                "success_patterns": ["profile", "following", "followers"]
            },
            "soundcloud": {
                "url": "https://soundcloud.com/{}",
                "error_patterns": ["404", "We can't find that user"],
                "success_patterns": ["followers", "tracks", "following"]
            },
            "vimeo": {
                "url": "https://vimeo.com/{}",
                "error_patterns": ["Page not found", "404"],
                "success_patterns": ["followers", "following", "videos"]
            },
            "onlyfans": {
                "url": "https://onlyfans.com/{}",
                "error_patterns": ["page not found", "404 not found"],
                "success_patterns": ["profile", "subscribers", "posts"]
            },
            "deviantart": {
                "url": "https://www.deviantart.com/{}",
                "error_patterns": ["This is not the page you are looking for"],
                "success_patterns": ["watchers", "deviations"]
            },
            "behance": {
                "url": "https://www.behance.net/{}",
                "error_patterns": ["404", "Page not found"],
                "success_patterns": ["followers", "appreciations", "projects"]
            },
            "patreon": {
                "url": "https://www.patreon.com/{}",
                "error_patterns": ["Page not found", "404"],
                "success_patterns": ["patreon", "posts", "about"]
            },
            "linkedin": {
                "url": "https://www.linkedin.com/in/{}",
                "error_patterns": ["Page not found", "This page doesn't exist"],
                "success_patterns": ["profile", "Experience", "Education"]
            },
            "gab": {
                "url": "https://gab.com/{}",
                "error_patterns": ["Page not found", "404"],
                "success_patterns": ["followers", "following", "posts"]
            },
            "gettr": {
                "url": "https://gettr.com/user/{}",
                "error_patterns": ["User not found"],
                "success_patterns": ["followers", "following", "posts"]
            },
            "parler": {
                "url": "https://parler.com/{}",
                "error_patterns": ["404", "User not found"],
                "success_patterns": ["followers", "following", "posts"]
            },
            "truth": {
                "url": "https://truthsocial.com/@{}",
                "error_patterns": ["404", "page does not exist"],
                "success_patterns": ["truth social", "followers", "following"]
            },
            "rumble": {
                "url": "https://rumble.com/user/{}",
                "error_patterns": ["404", "Page not found"],
                "success_patterns": ["followers", "following", "videos"]
            },
            "bitchute": {
                "url": "https://www.bitchute.com/channel/{}",
                "error_patterns": ["404", "Channel not found"],
                "success_patterns": ["subscribers", "videos"]
            },
            "odysee": {
                "url": "https://odysee.com/@{}",
                "error_patterns": ["404", "Page not found"],
                "success_patterns": ["followers", "following", "posts"]
            },
            "4chan": {
                "url": "https://4chan.org/user/{}",
                "error_patterns": ["404", "not found"],
                "success_patterns": ["posts", "profile"]
            },
            "minds": {
                "url": "https://www.minds.com/{}",
                "error_patterns": ["404", "Channel not found"],
                "success_patterns": ["subscribers", "views", "posts"]
            },
            "flickr": {
                "url": "https://www.flickr.com/photos/{}",
                "error_patterns": ["Page not found", "Oops!"],
                "success_patterns": ["followers", "following", "photos"]
            },
            "xbox": {
                "url": "https://www.xbox.com/en-US/live/gamer/{}",
                "error_patterns": ["page not found", "something went wrong"],
                "success_patterns": ["gamertag", "profile", "games"]
            },
            "psn": {
                "url": "https://psnprofiles.com/{}",
                "error_patterns": ["user not found", "404"],
                "success_patterns": ["Level", "Trophies", "Games"]
            },
            "discord": {
                "url": "https://discord.com/users/{}",
                "error_patterns": ["not found", "page not found"],
                "success_patterns": ["user profile", "Joined Discord", "Bio"]
            },
            "threads": {
                "url": "https://www.threads.net/@{}",
                "error_patterns": ["page isn't available", "content isn't available"],
                "success_patterns": ["profile", "followers", "threads"]
            },
            "medium": {
                "url": "https://medium.com/@{}",
                "error_patterns": ["404", "Page not found"],
                "success_patterns": ["followers", "following", "profile"]
            },
            "substack": {
                "url": "https://{}.substack.com",
                "error_patterns": ["404", "page doesn't exist"],
                "success_patterns": ["subscribe", "posts", "archive"]
            }
        }

    def check_username(self, platform, username):
        """Check username availability on a platform."""
        try:
            url = self.platforms[platform]["url"].format(quote_plus(username))
            
            # Platform-specific headers
            headers = self.headers.copy()
            
            # Platform-specific configurations
            if platform == "tiktok":
                headers["User-Agent"] = "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15"
                headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9"
            elif platform == "instagram":
                headers["User-Agent"] = "Instagram 219.0.0.12.117 Android"
                headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9"
            
            # Make request with appropriate timeout
            timeout = 20 if platform in ["instagram", "tiktok", "facebook"] else 10
            response = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
            content = response.text.lower()
            
            # Check for success and error patterns
            success_patterns = self.platforms[platform]["success_patterns"]
            error_patterns = self.platforms[platform]["error_patterns"]
            
            # Default to not found
            found = False
            
            # Special handling for specific platforms
            if platform == "tiktok" and "@" + username.lower() in content:
                found = True
            elif platform == "github" and "users/" + username.lower() in content:
                found = True
            elif platform == "instagram" and "profile picture" in content:
                found = True
            else:
                # Check for success patterns
                if any(pattern.lower() in content for pattern in success_patterns):
                    found = True
                
                # Check for error patterns
                if any(pattern.lower() in content for pattern in error_patterns):
                    found = False
            
            return {
                "platform": platform,
                "username": username,
                "url": url,
                "found": found,
                "status_code": response.status_code,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logging.error(f"Error checking {platform} for username {username}: {str(e)}")
            return {
                "platform": platform,
                "username": username,
                "url": url,
                "found": None,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    def search_username(self, username, platforms=None):
        """Search username across platforms."""
        if platforms is None:
            platforms = list(self.platforms.keys())
        else:
            platforms = [p for p in platforms if p in self.platforms]
        
        logging.info(f"Starting search for username '{username}' across {len(platforms)} platforms")
        
        results = []
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(self.check_username, platform, username) 
                      for platform in platforms]
            
            for future in futures:
                result = future.result()
                results.append(result)
                time.sleep(2)  # Rate limiting
        
        return results

    def export_results(self, results, format="csv"):
        """Export results to file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format == "csv":
            df = pd.DataFrame(results)
            filename = f"username_search_{timestamp}.csv"
            df.to_csv(filename, index=False)
        else:
            filename = f"username_search_{timestamp}.json"
            with open(filename, "w") as f:
                json.dump(results, f, indent=4)
        
        return filename

def main():
    """Main function to run the username search tool."""
    print_banner()
    
    parser = argparse.ArgumentParser(description="Search username across multiple platforms")
    parser.add_argument("username", help="Username to search")
    parser.add_argument("--platforms", nargs="+", help="Specific platforms to search")
    parser.add_argument("--format", choices=["csv", "json"], default="csv",
                        help="Export format (csv or json)")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Enable verbose output")
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    searcher = UsernameSearch()
    print(f"\nSearching for username: {args.username}")
    print("=" * 50)

    results = searcher.search_username(args.username, args.platforms)
    
    for result in results:
        platform = result["platform"]
        if result.get("found") is None:
            status = "?" # Error occurred
            status_msg = f"Error: {result.get('error', 'Unknown error')}"
        else:
            status = "✓" if result.get("found") else "✗"
            status_msg = result["url"]
        
        print(f"{platform:12} [{status}] - {status_msg}")
    
    output_file = searcher.export_results(results, args.format)
    print(f"\nResults exported to: {output_file}")
    print(f"Detailed logs available in: username_search.log")

if __name__ == "__main__":
    main()

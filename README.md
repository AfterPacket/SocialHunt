# SocialHunt
A comprehensive social media username search tool that checks username availability across multiple platforms.

## Features
- Checks 30+ social media platforms
- Fast, concurrent checking
- Export results to CSV or JSON
- Detailed logging
- Platform-specific detection methods
- Rate limiting protection

## Supported Platforms
- Social Networks (Instagram, TikTok, Twitter, Facebook, etc.)
- Video Platforms (YouTube, Twitch, Vimeo, etc.)
- Creative Platforms (DeviantArt, Behance, etc.)
- Gaming (Steam, Xbox, PSN)
- Messaging (Discord, Telegram, Snapchat)
- Alternative Social (Gab, GETTR, Truth Social, etc.)
- Professional (LinkedIn, GitHub, Medium)
- Content Creator (OnlyFans, Patreon)

## Installation
1. Clone the repository:
```bash
git clone https://github.com/yourusername/SocialHunt.git
cd SocialHunt
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install requirements:
```bash
pip install -r requirements.txt
```

## Usage
Basic usage:
```bash
python SocialHunt.py username123
```

Search specific platforms:
```bash
python SocialHunt.py username123 --platforms twitter instagram github
```

Export as JSON:
```bash
python SocialHunt.py username123 --format json
```

Enable verbose output:
```bash
python SocialHunt.py username123 --verbose
```

## Output
The tool will:
1. Display results in the terminal
2. Export detailed results to CSV/JSON
3. Create a log file with debug information

## Requirements
- Python 3.6+
- requests
- pandas
- beautifulsoup4

## Disclaimer
This tool is provided for educational and informational purposes only. The creators and contributors of SocialHunt take no responsibility for any misuse or damage caused by this tool. Users are solely responsible for ensuring the legality and ethics of their usage. No warranties or liabilities are provided. Use at your own risk.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
MIT License

Copyright (c) [2025] [AfterPacket]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to use,
copy, modify, merge, and/or distribute copies of the Software for 
non-commercial purposes only, subject to the following conditions:

1. The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

2. The Software may not be used for commercial purposes without express written 
permission from the copyright holder.

3. Any modifications to the Software must be clearly marked as such and must not
be misrepresented as being the original Software.

4. Redistributions of the Software must retain the above copyright notice, this
list of conditions, and the following disclaimer.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

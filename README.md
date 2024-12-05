# Twitter DM Media Downloader

This Python script extracts and downloads media (images, GIFs, and videos) from Twitter/X Direct Messages (DMs). It uses Selenium to simulate browser activity and handle authentication and requests to ensure private media files are accessible.

## Features

- **Real-time Media Extraction**: Captures URLs of images, GIFs, and videos from DMs as you scroll.
- **Authentication**: Uses your browser's cookies to authenticate requests.
- **Separate Media Storage**: Downloads images and GIFs to the `IMG` folder and videos to the `VID` folder.
- **m3u8 Conversion**: Converts `.m3u8` video streams to `.mp4` using FFmpeg.
- **Error Handling**: Includes robust debugging for troubleshooting issues.



## Requirements

- **Python 3.8+**
- **Chrome-Testing** or **Chromium**
- **ChromeDriver** (matching your browser version)
- **NPM** (to install ChromeDriver and Chrome-Testing)
- **FFmpeg** (for video conversion)

### Python Dependencies

Install required Python libraries using:

```bash
pip install selenium requests ffmpeg
```

## Installation
### 1. Clone the Repository

```bash
git clone https://github.com/KoriKosmos/Twitter-DM-Media-Downloader.git
cd Twitter-DM-Media-Downloader
```

### 2. Download ChromeDriver

```bash
npm install @puppeteer/browsers
npx @puppeteer/browsers install chrome@stable
npx @puppeteer/browsers install chromedriver@stable
```

## Usage

### 1. Edit login.py and extract.py
Edit `chrome_path` and `chromedriver_path` to point to the binaries you downloaded with npm earlier.

(Optionally) Point the `dm_url` under the main function in extract.py to point to a specific DM (e.g `https://x.com/messages/123-xyz`).

### 2. Login and Save Cookies
Run the script to log in to Twitter/X and save your session cookies.
Follow the prompts to log in manually in the browser.:

```bash
python login.py
```

### 3. Begin downloading

```bash
python extract.py
```

- Scroll through messages until you reach the point you wish to start extracting from.
- Press Enter in the terminal to start the script.
- Scroll through messages to trigger media loading and subsequent extraction.
- The process will automatically convert the network stream m3u8 container into mp4.

### 4. View Downloads
**Images** and **GIFs**: Saved in the `IMG` folder.

**Videos (.mp4)**: Saved in the `VID` folder.



## Notes
- Ensure your Twitter/X account has access to the media in the DMs.
- FFmpeg must be installed and accessible from the command line.
- The script is for personal use only. Do not use it for unauthorized purposes.


## Troubleshooting
### 1. 404 Errors
- Ensure your cookies are valid and up-to-date.
- Verify the resource exists by pasting the URL into your browser.
### 2. ChromeDriver Version Mismatch
- Update ChromeDriver to match your browser version.
### 3. FFmpeg Errors
- Ensure FFmpeg is installed and correctly added to your PATH.

## License
This project is licensed under the GNU General Public License v3.0.

## Contributing
Feel free to open issues or submit pull requests for improvements or additional features!

## Support
If you would like to show your appreciation, please send a few bucks my way on [Ko-fi](https://ko-fi.com/korikosmos)

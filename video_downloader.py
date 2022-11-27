from pytube import YouTube

VIDEO_URL = "https://www.youtube.com/watch?v=CS0XfdRCUhk"
youtubeDownloader = YouTube(VIDEO_URL)
youtubeDownloader = youtubeDownloader.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
youtubeDownloader.download("/Users/hmh/OneDrive/Documents/Airtel-IQ/")

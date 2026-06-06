Place a looping MP4 file named `background.mp4` here to enable the site video background.

If you prefer to use a hosted video, edit `srt_flower_marchent/templates/srt_flower_marchent/base.html` and replace the <source> src with the hosted URL, for example:

    <source src="https://example.com/path/to/video.mp4" type="video/mp4">

Notes:
- Keep the file reasonably sized for web delivery (under ~10MB recommended for testing).
- For production consider using adaptive streaming or a CDN.

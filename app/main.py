import os
# pyrefly: ignore [missing-import]
from fastapi import FastAPI
# pyrefly: ignore [missing-import]
from fastapi.middleware.cors import CORSMiddleware
# pyrefly: ignore [missing-import]
from fastapi.staticfiles import StaticFiles
# pyrefly: ignore [missing-import]
from fastapi.responses import HTMLResponse
from app.api.router import api_router

app = FastAPI(title="Jronix Video Downloader API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

# Mount static directory for APK downloads
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/download-app", response_class=HTMLResponse)
def download_app():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Download App</title>
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; text-align: center; padding: 50px 20px; background-color: #f9fafb; color: #111827; }
            .container { max-width: 500px; margin: 0 auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
            h1 { font-size: 24px; margin-bottom: 10px; }
            p { color: #4b5563; margin-bottom: 20px; line-height: 1.5; }
            .btn { display: inline-block; background-color: #3b82f6; color: white; padding: 12px 24px; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 16px; margin-top: 10px; transition: background-color 0.2s; }
            .btn:hover { background-color: #2563eb; }
            .spinner { border: 3px solid #f3f3f3; border-top: 3px solid #3b82f6; border-radius: 50%; width: 24px; height: 24px; animation: spin 1s linear infinite; margin: 0 auto 15px auto; }
            @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
            .manual-links { margin-top: 30px; font-size: 14px; text-align: left; border-top: 1px solid #e5e7eb; padding-top: 20px; }
            .manual-links a { color: #3b82f6; text-decoration: none; display: block; margin-bottom: 8px; }
            .manual-links a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <div class="container">
            <div id="loading" class="spinner"></div>
            <h1 id="title">Preparing Download...</h1>
            <p id="desc">We are detecting the best version for your device.</p>
            <a id="download-btn" href="/static/apks/app-universal-release.apk" class="btn" style="display: none;">Download Anyway</a>
            
            <div class="manual-links">
                <p><strong>Manual Downloads:</strong></p>
                <a href="/static/apks/app-arm64-v8a-release.apk">Download for modern phones (64-bit ARM) - ~28MB</a>
                <a href="/static/apks/app-armeabi-v7a-release.apk">Download for older phones (32-bit ARM) - ~25MB</a>
                <a href="/static/apks/app-universal-release.apk">Download Universal (All Devices) - ~61MB</a>
            </div>
        </div>

        <script>
            setTimeout(() => {
                let downloadLink = "/static/apks/app-universal-release.apk"; 
                
                if (navigator.userAgentData) {
                    navigator.userAgentData.getHighEntropyValues(["architecture", "bitness"])
                        .then(ua => {
                            if (ua.architecture === "arm") {
                                if (ua.bitness === "64") {
                                    downloadLink = "/static/apks/app-arm64-v8a-release.apk";
                                } else {
                                    downloadLink = "/static/apks/app-armeabi-v7a-release.apk";
                                }
                            } else if (ua.architecture === "x86") {
                                downloadLink = "/static/apks/app-x86_64-release.apk";
                            }
                            triggerDownload(downloadLink);
                        }).catch(() => {
                            triggerDownload("/static/apks/app-arm64-v8a-release.apk"); 
                        });
                } else {
                    triggerDownload("/static/apks/app-arm64-v8a-release.apk");
                }
            }, 800);

            function triggerDownload(link) {
                document.getElementById('loading').style.display = 'none';
                document.getElementById('title').innerText = 'Download Started!';
                document.getElementById('desc').innerText = 'If your download doesn\\'t start automatically, please click the button below.';
                
                const btn = document.getElementById('download-btn');
                btn.style.display = 'inline-block';
                btn.href = link;
                btn.innerText = 'Click here to download manually';
                
                window.location.href = link;
            }
        </script>
    </body>
    </html>
    """

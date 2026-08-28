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
        <title>Download Jronix Video Downloader</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
        <style>
            :root {
                --primary: #4F46E5;
                --primary-hover: #4338CA;
                --bg-gradient: linear-gradient(135deg, #0F172A 0%, #1E1B4B 100%);
                --card-bg: rgba(255, 255, 255, 0.05);
                --card-border: rgba(255, 255, 255, 0.1);
                --text-main: #F8FAFC;
                --text-muted: #94A3B8;
            }
            body { 
                font-family: 'Inter', sans-serif; 
                text-align: center; 
                margin: 0;
                padding: 40px 20px; 
                background: var(--bg-gradient);
                color: var(--text-main);
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
            }
            .brand-logo {
                width: 80px;
                height: 80px;
                background: linear-gradient(135deg, #6366F1, #EC4899);
                border-radius: 20px;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 0 auto 24px auto;
                box-shadow: 0 10px 25px rgba(99, 102, 241, 0.4);
            }
            .brand-logo svg { width: 40px; height: 40px; fill: white; }
            .container { 
                max-width: 480px; 
                width: 100%;
                background: var(--card-bg);
                backdrop-filter: blur(20px);
                -webkit-backdrop-filter: blur(20px);
                border: 1px solid var(--card-border);
                padding: 40px 30px; 
                border-radius: 24px; 
                box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
                box-sizing: border-box;
            }
            h1 { font-size: 26px; font-weight: 700; margin: 0 0 12px 0; letter-spacing: -0.5px; }
            p { color: var(--text-muted); font-size: 15px; margin: 0 0 28px 0; line-height: 1.6; }
            .btn { 
                display: inline-flex;
                align-items: center;
                justify-content: center;
                gap: 8px;
                background: linear-gradient(135deg, #6366F1, #4F46E5);
                color: white; 
                padding: 14px 28px; 
                text-decoration: none; 
                border-radius: 12px; 
                font-weight: 600; 
                font-size: 16px; 
                transition: all 0.3s ease;
                box-shadow: 0 8px 20px rgba(79, 70, 229, 0.3);
                width: 100%;
                box-sizing: border-box;
                border: 1px solid rgba(255,255,255,0.1);
            }
            .btn:hover { 
                transform: translateY(-2px);
                box-shadow: 0 12px 25px rgba(79, 70, 229, 0.4);
                background: linear-gradient(135deg, #4F46E5, #4338CA);
            }
            .btn svg { width: 20px; height: 20px; }
            .spinner { 
                width: 48px; 
                height: 48px; 
                border: 4px solid rgba(255,255,255,0.1); 
                border-top: 4px solid #6366F1; 
                border-radius: 50%; 
                animation: spin 1s cubic-bezier(0.5, 0.1, 0.4, 0.9) infinite; 
                margin: 0 auto 24px auto; 
            }
            @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
            .manual-links { 
                margin-top: 36px; 
                font-size: 13px; 
                text-align: left; 
                border-top: 1px solid var(--card-border); 
                padding-top: 24px; 
            }
            .manual-links-title {
                color: var(--text-main);
                font-weight: 600;
                margin-bottom: 12px;
                font-size: 14px;
            }
            .manual-links a { 
                color: var(--text-muted); 
                text-decoration: none; 
                display: flex; 
                align-items: center;
                gap: 8px;
                padding: 10px;
                border-radius: 8px;
                background: rgba(255,255,255,0.03);
                margin-bottom: 8px; 
                transition: all 0.2s;
                border: 1px solid transparent;
            }
            .manual-links a:hover { 
                color: white; 
                background: rgba(255,255,255,0.08);
                border-color: rgba(255,255,255,0.1);
            }
            .badge {
                background: rgba(99, 102, 241, 0.2);
                color: #818CF8;
                padding: 2px 8px;
                border-radius: 4px;
                font-size: 11px;
                font-weight: 600;
                margin-left: auto;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="brand-logo" id="logo-container" style="display: none;">
                <!-- Jronix Logo Icon -->
                <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM10 16.5V7.5L16 12L10 16.5Z"/>
                </svg>
            </div>
            <div id="loading" class="spinner"></div>
            
            <h1 id="title">Preparing Download...</h1>
            <p id="desc">We're finding the best optimized version of Jronix for your specific device.</p>
            
            <a id="download-btn" href="/static/apks/app-universal-release.apk" class="btn" style="display: none;">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
                Download Anyway
            </a>
            
            <div class="manual-links">
                <div class="manual-links-title">Other Versions</div>
                <a href="/static/apks/app-arm64-v8a-release.apk">
                    <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z"></path></svg>
                    Modern Phones (64-bit)
                    <span class="badge">~28MB</span>
                </a>
                <a href="/static/apks/app-armeabi-v7a-release.apk">
                    <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z"></path></svg>
                    Older Phones (32-bit)
                    <span class="badge">~25MB</span>
                </a>
                <a href="/static/apks/app-universal-release.apk">
                    <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
                    Universal (All Devices)
                    <span class="badge">~61MB</span>
                </a>
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
            }, 1200);

            function triggerDownload(link) {
                document.getElementById('loading').style.display = 'none';
                document.getElementById('logo-container').style.display = 'flex';
                
                document.getElementById('title').innerText = 'Jronix is Downloading!';
                document.getElementById('desc').innerText = 'If the download didn\\'t start automatically, tap the button below.';
                
                const btn = document.getElementById('download-btn');
                btn.style.display = 'inline-flex';
                btn.href = link;
                btn.innerHTML = '<svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg> Click here to download';
                
                window.location.href = link;
            }
        </script>
    </body>
    </html>
    """

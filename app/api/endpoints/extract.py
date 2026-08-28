# pyrefly: ignore [missing-import]
from fastapi import APIRouter, HTTPException
# pyrefly: ignore [missing-import]
from pydantic import BaseModel
from app.models.video import VideoInfo
from app.services.extractor.factory import ExtractorFactory

router = APIRouter()

class ExtractRequest(BaseModel):
    url: str

@router.post("/extract", response_model=VideoInfo)
async def extract_video_info(request: ExtractRequest):
    try:
        extractor = ExtractorFactory.get_extractor(request.url)
        info = extractor.extract()
        if not info.success:
            raise HTTPException(status_code=400, detail=info.error_message)
        return info
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

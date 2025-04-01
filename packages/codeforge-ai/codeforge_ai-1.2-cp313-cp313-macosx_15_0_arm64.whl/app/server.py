import os
from typing import Dict, Any, List, Tuple, Optional
import traceback
import tiktoken
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from langserve import add_routes
from app.agents.agent import agent_executor
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
import uvicorn
from app.agents.agent_converse import stream_response

from app.utils.code_util import use_git_to_apply_code_diff, correct_git_diff
from app.utils.directory_util import get_ignored_patterns
from app.utils.logging_utils import logger
from app.utils.gitignore_parser import parse_gitignore_patterns
from app.utils.markdown_utils import parse_markdown_to_json  # New import
from app.utils.mertrics_utils import put_metric
from botocore.exceptions import ClientError


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="../templates/static"), name="static")
templates = Jinja2Templates(directory="../templates")
add_routes(app, agent_executor, disabled_endpoints=["playground"], path="/codeforgeai")


class AttachmentContent(BaseModel):
    fileName: str
    content: Any
    type: str



@app.post("/codeforge-ai/stream")
async def stream_chat(
        input_data: dict,
):
    """Streaming endpoint that supports both text-only and multimodal inputs"""
    response = StreamingResponse(
        stream_response(input_data["input"]),
        media_type='text/event-stream'
    )

    return response



@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request
    })


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse('../templates/favicon.ico')


def get_folder_structure(directory: str, ignored_patterns: List[Tuple[str, str]], max_depth: int) -> Dict[str, Any]:
    should_ignore_fn = parse_gitignore_patterns(ignored_patterns)

    def count_tokens(file_path: str) -> int:
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                return len(tiktoken.get_encoding("cl100k_base").encode(content))
        except Exception as e:
            print(f"Skipping file {file_path} due to error: {e}")
            return 0

    def get_structure(current_dir: str, current_depth: int):
        if current_depth > max_depth:
            return None

        current_structure = {}
        for entry in os.listdir(current_dir):
            if entry.startswith('.'):
                continue
            entry_path = os.path.join(current_dir, entry)
            if os.path.islink(entry_path):
                continue
            if os.path.isdir(entry_path):
                if not should_ignore_fn(entry_path):
                    sub_structure = get_structure(entry_path, current_depth + 1)
                    if sub_structure is not None:
                        token_count = sum(sub_structure[key]['token_count'] for key in sub_structure)
                        current_structure[entry] = {'token_count': token_count, 'children': sub_structure}
            else:
                if not should_ignore_fn(entry_path):
                    token_count = count_tokens(entry_path)
                    current_structure[entry] = {'token_count': token_count}

        return current_structure

    folder_structure = get_structure(directory, 1)
    return folder_structure


@app.get("/api/folders")
async def get_folders():
    user_codebase_dir = os.environ["CODEFORGEAI_USER_CODEBASE_DIR"]
    max_depth = int(os.environ.get("CODEFORGEAI_MAX_DEPTH"))
    ignored_patterns: List[Tuple[str, str]] = get_ignored_patterns(user_codebase_dir)
    return get_folder_structure(user_codebase_dir, ignored_patterns, max_depth)


@app.get('/api/default-included-folders')
def get_default_included_folders():
    return {'defaultIncludedFolders': []}


class ApplyChangesRequest(BaseModel):
    diff: str
    filePath: str


@app.post('/api/apply-changes')
async def apply_changes(request: ApplyChangesRequest):
    try:
        logger.info(f"Received request to apply changes to file: {request.filePath}")
        logger.info(f"Diff content: \n{request.diff}")
        user_codebase_dir = os.environ.get("CODEFORGEAI_USER_CODEBASE_DIR")
        if not user_codebase_dir:
            raise ValueError("CODEFORGEAI_USER_CODEBASE_DIR environment variable is not set")
        file_path = os.path.join(user_codebase_dir, request.filePath)
        corrected_diff = correct_git_diff(request.diff, file_path)
        logger.info(f"corrected diff content: \n{corrected_diff}")
        use_git_to_apply_code_diff(corrected_diff)
        return {'message': 'Changes applied successfully'}
    except Exception as e:
        logger.error(f"Error applying changes: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


class AgentInput(BaseModel):
    chat_history: List[Tuple[str, str]]
    question: str
    config: Dict[str, List[str]]
    attachments: Optional[List[AttachmentContent]] = None


# New endpoint to get prompt libraries
@app.get("/api/prompt-libraries")
async def get_prompt_library():
    try:
        prompt_libraries = ["default"]

        config = {
            "promptLibraries": prompt_libraries
        }
        prompt_library: Dict[str, List[Dict[str, str]]] = {}

        prompts_dir = os.path.join(os.path.dirname(__file__), "prompts")
        default_dir = os.path.join(prompts_dir, "default")

        for category in os.listdir(default_dir):
            category_path = os.path.join(default_dir, category)
            if os.path.isdir(category_path):
                prompt_library[category] = [
                    parse_markdown_to_json(os.path.join(category_path, markdown_file))
                    for markdown_file in sorted(os.listdir(category_path))
                    if markdown_file.endswith('.md')]

        return {"config": config, "promptLibraries": {"default": prompt_library}}
    except Exception as e:
        logger.error(f"Error loading prompt library: {str(e)}")
        raise HTTPException(status_code=500, detail="Error loading prompt library")


@app.post("/api/metrics")
async def record_metric(metric_data: Dict[str, Any]):
    try:
        metric_name = metric_data.get("metricName", "UnknownMetric")
        dimensions = metric_data.get("dimensions", [])
        user = os.environ["USER"]
        logger.info(f"Recording metric: {metric_name} with dimensions: {dimensions}")

        if not dimensions:
            if metric_name == "InvocationMetric":
                dimensions = [{
                    'Name': "InvokingUser",
                    "Value": user
                }]
            else:
                dimensions = [{'Name': 'metricCategory', 'Value': 'Uncategorized'}]

        try:
            put_metric(metric_name, dimensions, 1, 'Count')
        except ClientError as e:
            logger.error(f"CloudWatch ClientError: {e}")
            raise HTTPException(status_code=500, detail=f"CloudWatch Error: {str(e)}")
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Error recording metric: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Error recording metric")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


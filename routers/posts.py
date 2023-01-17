from typing import List

from fastapi import APIRouter, HTTPException, Path

from models import Post, PostUpdate

router = APIRouter()

# temporary list of posts, until actual DB introduced
db: List[Post] = [
    Post(
        id=1,
        title="First post",
        content="Where's your crown, King Nothing?"
    ),
    Post(
        id=2,
        title="Secon post",
        content="So hold me until it sleeps"
    ),
]


def get_object_or_404(post_id):
    """Look if post exists in db and return post entry. Raises 404 error otherwise."""
    for post in db:
        if post.id == post_id:
            return post
    raise HTTPException(
        status_code=404, detail=f"post with id: {post_id} does not exist"
    )


@router.get("/api/v1/posts")
async def fetch_posts():
    """Return list of posts."""
    return db


@router.post("/api/v1/posts")
async def register_post(post: Post):
    """Add new post entry."""
    db.append(post)
    return {"id": post.id}


@router.delete("/api/v1/posts/{post_id}")
async def delete_post(
    post_id: int = Path(None, description="The ID of post you want to delete")
):
    """Delete existing post."""
    post = get_object_or_404(post_id)
    if post is not None:
        db.remove(post)


@router.put("/api/v1/posts/{post_id}")
async def update_post(
    data: PostUpdate,
    post_id: int = Path(None, description="The ID of post you want to update"),
):
    """Update post data."""
    post = get_object_or_404(post_id)
    if post is not None:
        if data.title is not None:
            post.title = data.title
        if data.content is not None:
            post.content = data.content

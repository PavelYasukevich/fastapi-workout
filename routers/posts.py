import os

import psycopg
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Path, status
from psycopg import sql
from psycopg.rows import dict_row

from models import Post, PostUpdate

load_dotenv()

router = APIRouter()


def connect():
    """Connect to database"""
    DBNAME = os.environ.get("DBNAME")
    DB_USER = os.environ.get("DB_USER")

    try:
        conn = psycopg.connect(f"dbname={DBNAME} user={DB_USER}")
        print("Sucsessful connection to DB")
    except Exception as error:
        print(f"Failed to connect. Error: {error}")
    else:
        return conn


conn = connect()
cur = conn.cursor(row_factory=dict_row)


def get_object_or_404(post_id: int) -> Post | None:
    """Look if post exists in db and return post entry. Raises 404 error otherwise."""
    post = cur.execute(
        """SELECT * FROM posts WHERE id=%s""", (str(post_id),)
    ).fetchone()
    if post is not None:
        return post
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post with id: {post_id} does not exist",
    )


@router.get("/api/v1/posts")
async def fetch_posts():
    """Return list of posts."""
    return cur.execute("""SELECT * FROM posts""").fetchall()


@router.post("/api/v1/posts", status_code=status.HTTP_201_CREATED)
async def register_post(post: Post) -> Post:
    """Add new post entry."""
    new_post = cur.execute(
        """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
        (post.title, post.content, str(post.published)),
    ).fetchone()
    conn.commit()
    return new_post


@router.delete("/api/v1/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int = Path(None, description="The ID of post you want to delete")
) -> None:
    """Delete existing post."""
    post = get_object_or_404(post_id)
    if post is not None:
        cur.execute("""DELETE FROM posts WHERE id=%s""", (str(post_id),))
        conn.commit()


@router.put("/api/v1/posts/{post_id}")
async def update_post(
    data: PostUpdate,
    post_id: int = Path(None, description="The ID of post you want to update"),
) -> Post | None:
    """Update post data."""
    post = get_object_or_404(post_id)
    if post is not None:
        data = data.dict(exclude_unset=True)
        for key, value in data.items():
            cur.execute(
                sql.SQL("""UPDATE posts SET {} = %s WHERE id=%s""").format(
                    sql.Identifier(key)
                ),
                (value, str(post_id)),
            )
        conn.commit()
        updated_post = get_object_or_404(post_id)
        return updated_post

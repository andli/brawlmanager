# session_backend.py
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from app.db import SessionLocal
from app.models import Session as DBSession
import uuid
from datetime import datetime, timedelta, timezone

class PostgresSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Initialize the session state
        request.state.session = {}

        # Retrieve the session cookie
        session_id = request.cookies.get('session')
        if not session_id:
            session_id = str(uuid.uuid4())

        # Load session data from the database
        with SessionLocal() as db:
            session_row = db.query(DBSession).filter(DBSession.session_id == session_id).first()
            if session_row and not session_row.is_expired():
                request.state.session = session_row.session_data

        # Proceed with the request
        response = await call_next(request)

        # Save session data if modified
        with SessionLocal() as db:
            session_entry = DBSession(
                session_id=session_id,
                session_data=request.state.session,
                expires_at=datetime.now(timezone.utc) + timedelta(days=1)
            )
            db.merge(session_entry)
            db.commit()

        # Set cookie in the response
        response.set_cookie(
            key='session',
            value=session_id,
            httponly=True,
            samesite='none',
            secure=True  # Ensure your app is served over HTTPS
        )

        return response
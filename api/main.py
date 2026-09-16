from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel, Field

app = FastAPI(title="Collection")
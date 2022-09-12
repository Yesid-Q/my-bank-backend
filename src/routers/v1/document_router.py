from uuid import UUID
from typing import List

from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from tortoise.exceptions import IntegrityError

from src.models.document_model import DocumentModel
from src.schemas.document_schema import DocumentRequest, DocumentResponse

document_router = APIRouter(
    prefix='/document',
    tags=['document']
)


@document_router.get(
    '',
    name='All Documents.',
    status_code=status.HTTP_200_OK,
    response_model=List[DocumentResponse]
)
async def get_all():
    documents = await DocumentModel.filter(deleted_at__not_isnull=False)
    return documents


@document_router.post(
    '',
    name='Create Document.',
    status_code=status.HTTP_201_CREATED,
    response_model=DocumentResponse
)
async def create_document(document_data: DocumentRequest):
    try:
        document = await DocumentModel.create(**document_data.dict())
    except IntegrityError as err:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f'{err}')
    return document


@document_router.get(
    '/{id}',
    name='Get by Id Document.',
    status_code=status.HTTP_200_OK,
    response_model=DocumentResponse
)
async def get_document(id: UUID):
    document = await DocumentModel.get_or_none(pk=id)
    if document is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Not found document with id {id}')
    return document


@document_router.put(
    '/{id}',
    name='Update Document.',
    status_code=status.HTTP_202_ACCEPTED,
    response_model=DocumentResponse
)
async def get_document(id: UUID, document_data: DocumentRequest):
    check = await DocumentModel.get_or_none(pk=id)
    if check is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Not found document with id {id}')
    try:
        await DocumentModel.filter(pk=id).update(**document_data.dict())
        document = await DocumentModel.filter(pk=id).first()
    except IntegrityError as err:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f'{err}')

    return document


@document_router.delete(
    '/{id}',
    name='Delete Document.',
    status_code=status.HTTP_204_NO_CONTENT
)
async def get_document(id: UUID):
    document = await DocumentModel.get_or_none(pk=id)
    if document is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Not found document with id {id}')
    await document.delete()
    return


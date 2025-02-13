import aiofiles
import pytest

from infomaniak_ai.openai.audio.transcriptions import transcribe, ResponseFormat, Model
from infomaniak_ai.session import Session


@pytest.mark.parametrize("testfile", ["tests/resources/audio.mp3"])
@pytest.mark.asyncio
async def test_transcribe(testfile, dummyenvvar, mock_api_call):
    async with Session() as session:
        async with aiofiles.open(testfile, "rb") as audiofile:
            content = await audiofile.read()
            text, filename, file_content = await transcribe(
                session=session, audio=content, response_format=ResponseFormat.TEXT
            )

    assert "Jeanne" in text


@pytest.mark.real_api_calls
@pytest.mark.parametrize("testfile", ["tests/resources/audio.mp3"])
@pytest.mark.asyncio
async def test_transcribe_real(testfile, dotenvvar):
    async with Session() as session:
        async with aiofiles.open(testfile, "rb") as audiofile:
            content = await audiofile.read()
            text, filename, file_content = await transcribe(
                session=session, audio=content, response_format=ResponseFormat.TEXT
            )

    assert "Jeanne" in text

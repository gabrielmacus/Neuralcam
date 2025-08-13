from math import floor
import os
import subprocess
import time
import av
from testcontainers.core.container import DockerContainer
from src.Contexts.SharedKernel.Infrastructure.Services.ConsoleLogger import ConsoleLogger
import pytest
from src.Contexts.Recording.RecordingSessions.Domain.ValueObjects.OutputPath import (
    OutputPath,
)
from src.Contexts.Recording.RecordingSessions.Domain.ValueObjects.RecordingSessionDuration import (
    RecordingSessionDuration,
)
from src.Contexts.Recording.RecordingSessions.Domain.ValueObjects.Uri import Uri
from src.Contexts.Recording.RecordingSessions.Infrastructure.Services.PyAvVideoRecorder import (
    PyAvVideoRecorder,
)
from tests.Contexts.Recording.RecordingSessions.Domain.Mothers.RecordingSessionMother import (
    RecordingSessionMother,
)


def then_video_exists(output_path: OutputPath):
    assert os.path.exists(output_path.value)
    assert os.path.getsize(output_path.value) > 0


def then_video_has_duration(output_path: OutputPath, expected_seconds: int):
    """Verifica que el video tenga la duración esperada en segundos (con tolerancia de ±1 segundo)"""
    container = av.open(output_path.value)
    try:
        # Obtener la duración en segundos
        if container.duration is None:
            raise ValueError("No se pudo obtener la duración del video")

        duration_seconds = float(container.duration) / av.time_base

        # Verificar con tolerancia de ±1 segundo para tener en cuenta pequeñas variaciones
        tolerance = 1.0
        assert (
            floor(abs(duration_seconds - expected_seconds)) <= tolerance
        ), f"Duración esperada: {expected_seconds}s ±{tolerance}s, pero obtuvo: {duration_seconds:.2f}s"
    finally:
        container.close()


@pytest.fixture
def recorder():
    logger = ConsoleLogger()
    return PyAvVideoRecorder(logger)


@pytest.fixture
def rtsp_stream_uri():
    return "rtsp://admin:solar2022@200.85.178.42/cam/realmonitor?channel=1&subtype=1"


@pytest.mark.integration
def test_should_record_video(recorder: PyAvVideoRecorder, rtsp_stream_uri: str):
    # Given
    output_path = OutputPath("/app/recordings/test.mkv")
    uri = Uri(rtsp_stream_uri)
    duration = RecordingSessionDuration(3)

    # When
    recorder.record(
        uri,
        output_path,
        duration,
    )

    # Then
    then_video_exists(output_path)
    then_video_has_duration(output_path, duration.value)

    # Cleanup
    os.remove(output_path.value)


@pytest.mark.integration
def test_should_throw_exception_when_rtsp_uri_not_found(recorder: PyAvVideoRecorder):
    # Given
    output_path = OutputPath("/app/recordings/test.mkv")
    uri = Uri("rtsp://127.0.0.1")
    duration = RecordingSessionDuration(3)

    # Then
    with pytest.raises(av.ConnectionRefusedError):
        recorder.record(uri, output_path, duration)

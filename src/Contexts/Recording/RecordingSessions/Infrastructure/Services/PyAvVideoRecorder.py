from __future__ import annotations

import time
from datetime import datetime
from pathlib import Path
import av.logging
from typing_extensions import override

import av
from av.container.output import OutputContainer
from src.Contexts.Recording.RecordingSessions.Domain.ValueObjects.RecordingSessionDuration import (
    RecordingSessionDuration,
)
from src.Contexts.Recording.RecordingSessions.Domain.Contracts.VideoRecorder import VideoRecorder
from src.Contexts.Recording.RecordingSessions.Domain.ValueObjects.OutputPath import OutputPath
from src.Contexts.Recording.RecordingSessions.Domain.ValueObjects.Uri import Uri
from src.Contexts.SharedKernel.Domain.LoggerInterface import LoggerInterface


class PyAvVideoRecorder(VideoRecorder):

    def __init__(self, logger: LoggerInterface):
        self.__logger = logger

    def __get_input_options(self):
        timeout_microseconds = 30 * 1000000  # TODO: read from env
        return {"rtsp_transport": "tcp", "timeout": str(timeout_microseconds)}

    def __handle_packet(
        self, packet: av.Packet, out_stream: av.VideoStream, output: OutputContainer
    ):
        # We need to skip the "flushing" packets that `demux` generates.
        if packet.dts is None:
            return
        packet.stream = out_stream
        output.mux(packet)

    def __duration_reached(self, dts: int | None, recording_seconds: int):
        if dts is None:
            return False
        return int(dts / 1000) >= recording_seconds

    @override
    def record(
        self,
        uri: Uri,
        output_path: OutputPath,
        duration_seconds: RecordingSessionDuration,
    ):
        input = av.open(uri.value, format="rtsp", options=self.__get_input_options())
        output = av.open(output_path.value, mode="w")
        try:
            in_stream = input.streams.video[0]
            out_stream: av.VideoStream = output.add_stream_from_template(in_stream)
            for packet in input.demux(in_stream):
                self.__handle_packet(packet, out_stream, output)
                if self.__duration_reached(packet.dts, duration_seconds.value):
                    break

        except av.HTTPBadRequestError as e:
            self.__logger.error(f"Error de autenticación: {e}")
            raise e
        except av.HTTPNotFoundError as e:
            self.__logger.error(f"Stream no encontrado: {e}")
            raise e
        except Exception as e:
            self.__logger.error(f"Error desconocido al grabar el video: {e}")
            raise e
        finally:
            input.close()
            output.close()

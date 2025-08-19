from __future__ import annotations

import json
import threading
from typing import Any, Callable, Dict, Optional

from kafka import KafkaConsumer as PyKafkaConsumer
from kafka.errors import KafkaError

from src.Contexts.SharedKernel.Domain.DomainEvent import DomainEvent
from src.Contexts.SharedKernel.Domain.LoggerInterface import LoggerInterface


class KafkaConsumer:
    """
    Consumer de Kafka que escucha mensajes y los convierte en eventos de dominio.
    """

    def __init__(
        self,
        bootstrap_servers: str,
        group_id: str,
        logger: LoggerInterface,
        auto_offset_reset: str = "earliest",
        enable_auto_commit: bool = True,
        value_deserializer: Optional[Callable[[bytes], Any]] = None,
    ):
        self._bootstrap_servers = bootstrap_servers
        self._group_id = group_id
        self._logger = logger
        self._auto_offset_reset = auto_offset_reset
        self._enable_auto_commit = enable_auto_commit
        self._value_deserializer = value_deserializer or self._json_deserializer
        self._consumer: Optional[PyKafkaConsumer] = None
        self._event_handlers: Dict[str, Callable[[DomainEvent], None]] = {}
        self._running = False
        self._consume_thread: Optional[threading.Thread] = None

    @staticmethod
    def _json_deserializer(data: bytes) -> dict:
        """Deserializador por defecto que convierte JSON a diccionario."""
        return json.loads(data.decode("utf-8"))

    def subscribe(self, topics: list[str]) -> None:
        """
        Se suscribe a los topics especificados.

        Args:
            topics: Lista de topics a los que suscribirse
        """
        try:
            self._consumer = PyKafkaConsumer(
                *topics,
                bootstrap_servers=self._bootstrap_servers,
                group_id=self._group_id,
                auto_offset_reset=self._auto_offset_reset,
                enable_auto_commit=self._enable_auto_commit,
                value_deserializer=self._value_deserializer,
            )
            self._logger.info(f"Suscrito a topics: {topics}")
        except KafkaError as e:
            self._logger.error(f"Error al suscribirse a topics {topics}: {e}")
            raise

    def register_event_handler(self, event_name: str, handler: Callable[[DomainEvent], None]) -> None:
        """
        Registra un manejador para un tipo específico de evento.

        Args:
            event_name: Nombre del evento (ej: "recording_session.finished")
            handler: Función que maneja el evento
        """
        self._event_handlers[event_name] = handler
        self._logger.debug(f"Registrado handler para evento: {event_name}")

    def start_consuming(self) -> None:
        """Inicia el consumo de mensajes en un thread separado."""
        if self._running:
            self._logger.warn("El consumer ya está ejecutándose")
            return

        if not self._consumer:
            raise ValueError("Debe suscribirse a topics antes de iniciar el consumo")

        self._running = True
        self._consume_thread = threading.Thread(target=self._consume_messages, daemon=True)
        self._consume_thread.start()
        self._logger.info("Consumer iniciado")

    def stop_consuming(self) -> None:
        """Detiene el consumo de mensajes."""
        if not self._running:
            return

        self._running = False
        if self._consume_thread:
            self._consume_thread.join(timeout=5.0)
        
        if self._consumer:
            self._consumer.close()
            
        self._logger.info("Consumer detenido")

    def _consume_messages(self) -> None:
        """Método interno que consume mensajes en loop."""
        try:
            while self._running and self._consumer:
                # Poll con timeout para permitir interrupciones
                message_batch = self._consumer.poll(timeout_ms=1000)
                
                for topic_partition, messages in message_batch.items():
                    for message in messages:
                        try:
                            self._process_message(message)
                        except Exception as e:
                            self._logger.error(
                                f"Error procesando mensaje de {topic_partition}: {e}"
                            )
        except Exception as e:
            self._logger.error(f"Error en el loop de consumo: {e}")
        finally:
            self._running = False

    def _process_message(self, message) -> None:
        """
        Procesa un mensaje individual y ejecuta el handler correspondiente.

        Args:
            message: Mensaje de Kafka
        """
        try:
            # El mensaje viene deserializado por el deserializador configurado
            event_data = message.value
            event_name = event_data.get("event_name")
            
            if not event_name:
                self._logger.warn(f"Mensaje sin event_name: {event_data}")
                return

            handler = self._event_handlers.get(event_name)
            if not handler:
                self._logger.debug(f"No hay handler para evento: {event_name}")
                return

            # Crear un evento simple basado en los datos del mensaje
            domain_event = SimpleDomainEvent(event_name, event_data)
            handler(domain_event)
            
            self._logger.debug(f"Procesado evento: {event_name}")

        except Exception as e:
            self._logger.error(f"Error procesando mensaje: {e}")

    def is_running(self) -> bool:
        """Indica si el consumer está ejecutándose."""
        return self._running


class SimpleDomainEvent(DomainEvent):
    """Evento de dominio simple para encapsular mensajes de Kafka."""
    
    def __init__(self, event_name: str, data: dict):
        self._event_name = event_name
        self.data = data

    @property
    def event_name(self) -> str:
        return self._event_name
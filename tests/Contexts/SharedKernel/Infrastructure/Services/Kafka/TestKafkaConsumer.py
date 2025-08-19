import json
import threading
import time
from typing import List
from unittest.mock import MagicMock

import pytest
from kafka import KafkaProducer
from testcontainers.kafka import KafkaContainer

from src.Contexts.SharedKernel.Domain.DomainEvent import DomainEvent
from src.Contexts.SharedKernel.Infrastructure.Services.ConsoleLogger import ConsoleLogger
from src.Contexts.SharedKernel.Infrastructure.Services.Kafka.KafkaConsumer import KafkaConsumer


@pytest.fixture(scope="function")
def kafka_container():
    """Fixture que proporciona un contenedor de Kafka para las pruebas."""
    with KafkaContainer() as kafka:
        yield kafka


@pytest.fixture
def logger():
    """Fixture que proporciona un logger para las pruebas."""
    return ConsoleLogger()


@pytest.fixture
def kafka_consumer(kafka_container, logger):
    """Fixture que proporciona un KafkaConsumer configurado."""
    bootstrap_servers = kafka_container.get_bootstrap_server()
    consumer = KafkaConsumer(
        bootstrap_servers=bootstrap_servers,
        group_id="test-group",
        logger=logger,
        auto_offset_reset="earliest"
    )
    yield consumer
    # Cleanup
    consumer.stop_consuming()


@pytest.fixture
def kafka_producer(kafka_container):
    """Fixture que proporciona un KafkaProducer para enviar mensajes de prueba."""
    bootstrap_servers = kafka_container.get_bootstrap_server()
    producer = KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )
    yield producer
    producer.close()


@pytest.mark.integration
def test_kafka_consumer_should_subscribe_to_topics_successfully(kafka_consumer):
    """
    Given: Un KafkaConsumer configurado
    When: Se suscribe a una lista de topics
    Then: Debería suscribirse exitosamente sin errores
    """
    # Given
    topics = ["test-topic-1", "test-topic-2"]
    
    # When
    kafka_consumer.subscribe(topics)
    
    # Then
    assert kafka_consumer._consumer is not None
    assert set(kafka_consumer._consumer.subscription()) == set(topics)


@pytest.mark.integration
def test_kafka_consumer_should_register_event_handlers(kafka_consumer):
    """
    Given: Un KafkaConsumer configurado
    When: Se registra un handler para un evento específico
    Then: El handler debería quedar registrado correctamente
    """
    # Given
    event_name = "test.event"
    handler = MagicMock()
    kafka_consumer.subscribe(["test-topic"])
    
    # When
    kafka_consumer.register_event_handler(event_name, handler)
    
    # Then
    assert event_name in kafka_consumer._event_handlers
    assert kafka_consumer._event_handlers[event_name] == handler


@pytest.mark.integration
def test_kafka_consumer_should_consume_and_process_messages(kafka_consumer, kafka_producer):
    """
    Given: Un KafkaConsumer suscrito a un topic con un handler registrado
    When: Se envía un mensaje al topic
    Then: El handler debería ser llamado con el evento correspondiente
    """
    # Given
    topic = "test-events"
    event_name = "test.event"
    event_data = {"event_name": event_name, "data": {"id": "123", "name": "test"}}
    
    handler = MagicMock()
    kafka_consumer.subscribe([topic])
    kafka_consumer.register_event_handler(event_name, handler)
    
    # When
    kafka_consumer.start_consuming()
    time.sleep(0.5)  # Tiempo para que inicie el consumer
    
    kafka_producer.send(topic, event_data)
    kafka_producer.flush()
    
    # Wait for message processing
    time.sleep(2)
    kafka_consumer.stop_consuming()
    
    # Then
    handler.assert_called_once()
    called_event = handler.call_args[0][0]
    assert isinstance(called_event, DomainEvent)
    assert called_event.event_name == event_name
    assert called_event.data == event_data


@pytest.mark.integration
def test_kafka_consumer_should_handle_multiple_messages(kafka_consumer, kafka_producer):
    """
    Given: Un KafkaConsumer con handler registrado
    When: Se envían múltiples mensajes
    Then: Todos los mensajes deberían ser procesados
    """
    # Given
    topic = "test-multiple-events"
    event_name = "multiple.test.event"
    message_count = 5
    
    handler = MagicMock()
    kafka_consumer.subscribe([topic])
    kafka_consumer.register_event_handler(event_name, handler)
    kafka_consumer.start_consuming()
    time.sleep(0.5)
    
    # When
    for i in range(message_count):
        event_data = {"event_name": event_name, "data": {"id": str(i), "message": f"test-{i}"}}
        kafka_producer.send(topic, event_data)
    
    kafka_producer.flush()
    time.sleep(3)  # Tiempo para procesar todos los mensajes
    kafka_consumer.stop_consuming()
    
    # Then
    assert handler.call_count == message_count


@pytest.mark.integration
def test_kafka_consumer_should_ignore_messages_without_event_name(kafka_consumer, kafka_producer):
    """
    Given: Un KafkaConsumer configurado
    When: Se envía un mensaje sin event_name
    Then: El mensaje debería ser ignorado y no debería llamar ningún handler
    """
    # Given
    topic = "test-invalid-events"
    handler = MagicMock()
    
    kafka_consumer.subscribe([topic])
    kafka_consumer.register_event_handler("any.event", handler)
    kafka_consumer.start_consuming()
    time.sleep(0.5)
    
    # When
    invalid_message = {"data": {"some": "data"}}  # Sin event_name
    kafka_producer.send(topic, invalid_message)
    kafka_producer.flush()
    
    time.sleep(2)
    kafka_consumer.stop_consuming()
    
    # Then
    handler.assert_not_called()


@pytest.mark.integration
def test_kafka_consumer_should_ignore_messages_with_no_registered_handler(kafka_consumer, kafka_producer):
    """
    Given: Un KafkaConsumer sin handlers registrados
    When: Se envía un mensaje válido
    Then: El mensaje debería ser ignorado sin errores
    """
    # Given
    topic = "test-no-handler"
    event_data = {"event_name": "unhandled.event", "data": {"id": "123"}}
    
    kafka_consumer.subscribe([topic])
    kafka_consumer.start_consuming()
    time.sleep(0.5)
    
    # When
    kafka_producer.send(topic, event_data)
    kafka_producer.flush()
    
    time.sleep(2)
    kafka_consumer.stop_consuming()
    
    # Then - No debería haber errores (verificado por no excepciones)
    assert True  # Si llegamos aquí, no hubo errores


@pytest.mark.integration
def test_kafka_consumer_should_handle_malformed_json_messages_gracefully(kafka_consumer, kafka_producer):
    """
    Given: Un KafkaConsumer configurado
    When: Se envía un mensaje con JSON malformado
    Then: El consumer debería continuar funcionando sin fallar
    """
    # Given
    topic = "test-malformed-json"
    handler = MagicMock()
    
    kafka_consumer.subscribe([topic])
    kafka_consumer.register_event_handler("test.event", handler)
    kafka_consumer.start_consuming()
    time.sleep(0.5)
    
    # When - Enviar JSON malformado directamente
    producer_raw = KafkaProducer(
        bootstrap_servers=kafka_consumer._bootstrap_servers,
        value_serializer=lambda v: v  # Sin serialización JSON
    )
    
    producer_raw.send(topic, b'{"invalid": json}')  # JSON inválido
    producer_raw.flush()
    producer_raw.close()
    
    # Enviar mensaje válido después para verificar que el consumer sigue funcionando
    valid_message = {"event_name": "test.event", "data": {"id": "valid"}}
    kafka_producer.send(topic, valid_message)
    kafka_producer.flush()
    
    time.sleep(2)
    kafka_consumer.stop_consuming()
    
    # Then - El consumer debería haber procesado solo el mensaje válido
    handler.assert_called_once()


@pytest.mark.integration
def test_kafka_consumer_should_start_and_stop_correctly(kafka_consumer):
    """
    Given: Un KafkaConsumer suscrito a un topic
    When: Se inicia y detiene el consumer
    Then: Los estados deberían cambiar correctamente
    """
    # Given
    kafka_consumer.subscribe(["test-lifecycle"])
    
    # When - Iniciar
    kafka_consumer.start_consuming()
    
    # Then - Debería estar ejecutándose
    assert kafka_consumer.is_running() is True
    
    # When - Detener
    kafka_consumer.stop_consuming()
    
    # Then - No debería estar ejecutándose
    assert kafka_consumer.is_running() is False


@pytest.mark.integration
def test_kafka_consumer_should_not_start_without_subscription(kafka_consumer):
    """
    Given: Un KafkaConsumer sin suscripción a topics
    When: Se intenta iniciar el consumer
    Then: Debería lanzar una excepción
    """
    # Given - Sin suscripción
    
    # When/Then
    with pytest.raises(ValueError, match="Debe suscribirse a topics antes de iniciar el consumo"):
        kafka_consumer.start_consuming()


@pytest.mark.integration
def test_kafka_consumer_should_handle_double_start_gracefully(kafka_consumer):
    """
    Given: Un KafkaConsumer ya iniciado
    When: Se intenta iniciar nuevamente
    Then: Debería manejar la situación sin errores
    """
    # Given
    kafka_consumer.subscribe(["test-double-start"])
    kafka_consumer.start_consuming()
    
    # When - Intentar iniciar de nuevo
    kafka_consumer.start_consuming()  # No debería lanzar excepción
    
    # Then
    assert kafka_consumer.is_running() is True
    
    # Cleanup
    kafka_consumer.stop_consuming()


@pytest.mark.integration
def test_kafka_consumer_should_handle_handler_exceptions_gracefully(kafka_consumer, kafka_producer):
    """
    Given: Un KafkaConsumer con un handler que lanza excepción
    When: Se procesa un mensaje
    Then: El consumer debería continuar funcionando después de la excepción
    """
    # Given
    topic = "test-handler-exception"
    event_name = "exception.test"
    
    def failing_handler(event: DomainEvent):
        raise Exception("Handler failed")
    
    successful_handler = MagicMock()
    
    kafka_consumer.subscribe([topic])
    kafka_consumer.register_event_handler(event_name, failing_handler)
    kafka_consumer.register_event_handler("success.event", successful_handler)
    kafka_consumer.start_consuming()
    time.sleep(0.5)
    
    # When
    # Enviar mensaje que causará excepción
    failing_message = {"event_name": event_name, "data": {"will": "fail"}}
    kafka_producer.send(topic, failing_message)
    
    # Enviar mensaje que debería funcionar
    success_message = {"event_name": "success.event", "data": {"will": "succeed"}}
    kafka_producer.send(topic, success_message)
    
    kafka_producer.flush()
    time.sleep(2)
    kafka_consumer.stop_consuming()
    
    # Then - El handler exitoso debería haber sido llamado
    successful_handler.assert_called_once()


# Helper functions para encapsular código común

def given_kafka_consumer_with_handler(kafka_consumer, topic: str, event_name: str):
    """Helper para configurar un consumer con handler."""
    handler = MagicMock()
    kafka_consumer.subscribe([topic])
    kafka_consumer.register_event_handler(event_name, handler)
    return handler


def given_consumer_is_running(kafka_consumer):
    """Helper para iniciar el consumer y esperar que esté listo."""
    kafka_consumer.start_consuming()
    time.sleep(0.5)


def when_message_is_sent(kafka_producer, topic: str, message: dict):
    """Helper para enviar un mensaje."""
    kafka_producer.send(topic, message)
    kafka_producer.flush()


def then_handler_should_have_been_called_with_event(handler, expected_event_name: str):
    """Helper para verificar que el handler fue llamado con el evento esperado."""
    handler.assert_called_once()
    called_event = handler.call_args[0][0]
    assert isinstance(called_event, DomainEvent)
    assert called_event.event_name == expected_event_name


def then_consumer_should_process_message_successfully(kafka_consumer, handler):
    """Helper para esperar y verificar el procesamiento exitoso."""
    time.sleep(2)
    kafka_consumer.stop_consuming()
    return handler.called
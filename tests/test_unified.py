import unittest
from unittest.mock import MagicMock, patch

from src.trivialapi.unified.core import (HRIS, KMS, Connection, Custom,
                                         Messaging, Repo, Task, Unified)


class TestUnified(unittest.TestCase):
    def setUp(self):
        self.token = "test_token"
        self.unified = Unified(self.token)

    @patch("src.trivialapi.unified.core._request")
    def test_connection(self, mock_request):
        connection = self.unified.connection("test_connection_id")
        self.assertIsInstance(connection, Connection)
        self.assertEqual(connection.connection_id, "test_connection_id")

    @patch("src.trivialapi.unified.core._request")
    def test_messaging(self, mock_request):
        messaging = self.unified.messaging("test_connection_id")
        self.assertIsInstance(messaging, Messaging)
        self.assertEqual(messaging.connection_id, "test_connection_id")

    @patch("src.trivialapi.unified.core._request")
    def test_task(self, mock_request):
        task = self.unified.task("test_connection_id")
        self.assertIsInstance(task, Task)
        self.assertEqual(task.connection_id, "test_connection_id")

    @patch("src.trivialapi.unified.core._request")
    def test_hris(self, mock_request):
        hris = self.unified.hris("test_connection_id")
        self.assertIsInstance(hris, HRIS)
        self.assertEqual(hris.connection_id, "test_connection_id")

    @patch("src.trivialapi.unified.core._request")
    def test_kms(self, mock_request):
        kms = self.unified.kms("test_connection_id")
        self.assertIsInstance(kms, KMS)
        self.assertEqual(kms.connection_id, "test_connection_id")

    @patch("src.trivialapi.unified.core._request")
    def test_repo(self, mock_request):
        repo = self.unified.repo("test_connection_id", "test_org_id")
        self.assertIsInstance(repo, Repo)
        self.assertEqual(repo.connection_id, "test_connection_id")
        self.assertEqual(repo.org_id, "test_org_id")

    @patch("src.trivialapi.unified.core._request_raw")
    def test_custom(self, mock_request_raw):
        custom = self.unified.custom("test_connection_id")
        self.assertIsInstance(custom, Custom)
        self.assertEqual(custom.connection_id, "test_connection_id")


class TestConnection(unittest.TestCase):
    def setUp(self):
        self.req = MagicMock()
        self.connection = Connection(self.req, "test_connection_id")

    def test_info(self):
        self.connection.info()
        self.req.assert_called_once_with("unified/connection/test_connection_id")

    def test_delete(self):
        self.connection.delete()
        self.req.assert_called_once_with(
            "unified/connection/test_connection_id", method="DELETE"
        )


class TestMessaging(unittest.TestCase):
    def setUp(self):
        self.req = MagicMock()
        self.messaging = Messaging(self.req, "test_connection_id")

    def test_channels(self):
        self.messaging.channels()
        self.req.assert_called_once_with("messaging/test_connection_id/channel")

    def test_messages(self):
        self.messaging.messages("test_channel_id")
        self.req.assert_called_once_with(
            "messaging/test_connection_id/message",
            params={"channel_id": "test_channel_id"},
        )

    def test_send(self):
        self.messaging.send("test_channel_id", "subject", "message", "html_message")
        self.req.assert_called_once_with(
            "messaging/test_connection_id/message",
            method="POST",
            params={
                "channel_id": "test_channel_id",
                "subject": "subject",
                "message": "message",
                "message_html": "html_message",
            },
        )


# Similar test classes should be created for Task, HRIS, KMS, Repo, and Custom classes

if __name__ == "__main__":
    unittest.main()

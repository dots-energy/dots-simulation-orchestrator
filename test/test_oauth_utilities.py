import unittest
from unittest.mock import patch
from fastapi import HTTPException
from jose import JWTError

from simulation_orchestrator.rest.oauth.OAuthUtilities import get_current_user, UserInDB


class TestOAuthUtilities(unittest.TestCase):
    def test_get_current_user_when_auth_disabled(self):
        """Test that get_current_user returns anonymous user when USE_AUTH is False."""
        with patch('simulation_orchestrator.rest.oauth.OAuthUtilities.oauth2_scheme') as mock_oauth:
            mock_oauth.return_value = None
            with patch('simulation_orchestrator.rest.oauth.OAuthUtilities.USE_AUTH', False):
                result = get_current_user(None)
                self.assertIsInstance(result, UserInDB)
                self.assertEqual(result.username, "anonymous")
                self.assertEqual(result.hashed_password, "")
                self.assertFalse(result.disabled)

    def test_get_current_user_when_auth_enabled_and_token_none(self):
        """Test that get_current_user raises HTTPException when USE_AUTH is True and token is None."""
        with patch('simulation_orchestrator.rest.oauth.OAuthUtilities.oauth2_scheme') as mock_oauth:
            mock_oauth.return_value = None
            with patch('simulation_orchestrator.rest.oauth.OAuthUtilities.USE_AUTH', True):
                with self.assertRaises(HTTPException) as context:
                    get_current_user(None)
                self.assertEqual(context.exception.status_code, 401)
                self.assertIn("Could not validate credentials", context.exception.detail)

    def test_get_current_user_when_auth_enabled_and_invalid_token(self):
        """Test that get_current_user raises HTTPException when USE_AUTH is True and token is invalid."""
        with patch('simulation_orchestrator.rest.oauth.OAuthUtilities.oauth2_scheme') as mock_oauth:
            mock_oauth.return_value = "invalid_token"
            with patch('simulation_orchestrator.rest.oauth.OAuthUtilities.USE_AUTH', True):
                with patch('simulation_orchestrator.rest.oauth.OAuthUtilities.jwt.decode') as mock_decode:
                    mock_decode.side_effect = JWTError("Invalid token")
                    with self.assertRaises(HTTPException) as context:
                        get_current_user("invalid_token")
                    self.assertEqual(context.exception.status_code, 401)
                    self.assertIn("Could not validate credentials", context.exception.detail)

    def test_get_current_user_when_auth_enabled_and_valid_token(self):
        """Test that get_current_user returns the user when USE_AUTH is True and token is valid."""
        with patch('simulation_orchestrator.rest.oauth.OAuthUtilities.oauth2_scheme') as mock_oauth:
            mock_oauth.return_value = "valid_token"
            with patch('simulation_orchestrator.rest.oauth.OAuthUtilities.USE_AUTH', True):
                with patch('simulation_orchestrator.rest.oauth.OAuthUtilities.jwt.decode') as mock_decode:
                    mock_decode.return_value = {"sub": "DotsUser"}
                    with patch('simulation_orchestrator.rest.oauth.OAuthUtilities.get_user') as mock_get_user:
                        mock_user = UserInDB(username="DotsUser", hashed_password="hash hash", disabled=False)
                        mock_get_user.return_value = mock_user
                        result = get_current_user("valid_token")
                        self.assertEqual(result, mock_user)
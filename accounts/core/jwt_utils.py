import logging
import time
import uuid
from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.core.cache import cache
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

logger = logging.getLogger(__name__)


class TokenManager:
    """Gestion des tokens JWT."""

    @staticmethod
    def generate_token(user):
        """Génère un token JWT pour un utilisateur donné."""

        try:
            refresh = RefreshToken.for_user(user)
            jti = str(uuid.uuid4())

            refresh["jti"] = jti
            refresh["username"] = user.username
            refresh["email"] = user.email
            refresh["is_staff"] = user.is_staff
            refresh["is_verified"] = user.is_verified
            refresh["type"] = "refresh"

            access_token = refresh.access_token
            access_token["jti"] = str(uuid.uuid4())
            access_token["type"] = "access"

            # get token expiry settings
            access_expiry = settings.SIMPLE_JWT.get(
                "ACCESS_TOKEN_LIFETIME", timedelta(minutes=15)
            )
            refresh_expiry = settings.SIMPLE_JWT.get(
                "REFRESH_TOKEN_LIFETIME", timedelta(days=14)
            )

            # store tokens in cache for potential revocation
            TokenManager._store_token_metadata(
                user.id, jti, "refresh", refresh_expiry.total_seconds()
            )

            # return full token package
            return {
                "access": str(access_token),
                "refresh": str(refresh),
                "token_type": "Bearer",
                "access_expires_in": int(access_expiry.total_seconds()),
                "refresh_expires_in": int(refresh_expiry.total_seconds()),
                "user_id": user.id,
                "issued_at": int(time.time()),
            }
        except Exception as e:
            logger.error(f"Error generating token for user {user.id}: {str(e)}")
            return None

    @staticmethod
    def refresh_token(refresh_token_str):
        """Rafraîchit un token JWT donné."""
        try:
            token = RefreshToken(refresh_token_str)

            jti = token.get('jti')
            if not jti or TokenManager.is_token_blacklisted(jti):
                logger.warning(
                    f"Attempt to refresh blacklisted or invalid token: {jti}"
                )
                raise TokenError("Token is blacklisted or invalid")
            user_id = token.get("user_id")
            from accounts.models import User

            try:
                user = User.objects.get(id=user_id)
            except:
                logger.warning(f"User not found for token refresh: {user_id}")
                raise TokenError("Invalid token ")

            if not user.is_active:
                logger.warning(
                    f"Inactive user attempted token refresh: {user.matricule}"
                )
                TokenManager.blacklist_token(jti)
                raise TokenError("User is inactive")
            if settings.SIMPLE_JWT.get("ROTATE_REFRESH_TOKENS", True):
                # Blacklist the old token
                TokenManager.blacklist_token(jti)
                # Generate a new token pair
                return TokenManager.generate_token(user)
        except TokenError as e:
            logger.error(f"TokenError while refreshing token: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"unexpected error during token refresh: {str(e)}")
            raise TokenError(f"Failed to refresh token: {str(e)}")

    @staticmethod
    def validate_token(token_str):
        """Valide un token JWT donné.
        return tuple ( is_valid, user_id, token_type)
        """
        try:
            """first use pyjwt to decode and verify the token"""
            unverified = jwt.decode(
                token_str,
                options={"verify_signature": False},
            )
            algorithms = unverified.get(
                "algorithms", settings.SIMPLE_JWT.get("ALGORITHM", "HS256")
            )
            # now properly decode
            decoded = jwt.decode(
                token_str,
                settings.SIMPLE_JWT.get("SIGNING_KEY", settings.SECRET_KEY),
                algorithms=[algorithms],
                options={"verify_signature": True},
            )

            # check token type

            token_type = decoded.get("token_type", decoded.get("type", "access"))
            user_id = decoded.get("user_id")
            jti = decoded.get("jti")

            # check if token is blacklisted
            if jti and TokenManager.is_token_blacklisted(jti):
                logger.warning(f"Attempt to use blacklisted token: {jti}")
                return False, None, None

            # check expiration
            exp_timestamp = decoded.get("exp", 0)
            if exp_timestamp < time.time():
                logger.debug(
                    f"Token has expired at : {datetime.fromtimestamp(exp_timestamp).isoformat()}"
                )
                return False, None, None
            return True, user_id, token_type
        except jwt.PyJWKError as e:
            logger.error(f"token validation error: {str(e)}")
            return False, None, None
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired")
            return None
        except jwt.InvalidTokenError as e:
            logger.error(f"Invalid token error: {str(e)}")
            return None

    @staticmethod
    def _store_token_metadata(user_id, jti, token_type, expiry_seconds):
        """Stocke les métadonnées du token dans le cache pour la révocation."""
        try:
            # verifie si on utilise redis ou cache memoire
            if hasattr(cache, "client"):
                # redis implementation
                user_tokens_key = f"user_tokens: {user_id}"
                pipe = cache.client.pipeline()
                pipe.sadd(user_tokens_key, jti)
                pipe.expire(user_tokens_key, int(expiry_seconds))
                pipe.execute()
            else:
                # memory cache implementation
                user_tokens_key = f"user_tokens_{user_id}"
                existing_tokens = cache.get(user_tokens_key, set())

                if not isinstance(existing_tokens, set):
                    existing_tokens = set()
                existing_tokens.add(jti)
                cache.set(user_tokens_key, existing_tokens, timeout=int(expiry_seconds))
        except Exception as e:
            logger.error(f"Error storing token metadata: {str(e)}")

    @staticmethod
    def is_token_blacklisted(jti):
        """Vérifie si un token est dans la liste noire."""
        if not jti:
            return False
        blacklist_key = f"blacklisted_tokens:{jti}"
        return cache.get(blacklist_key) is not None

    @staticmethod
    def blacklist_token(jti):
        if not jti:
            return False
        blacklist_key = f"blacklisted_tokens:{jti}"
        cache.set(
            blacklist_key,
            True,
            timeout=settings.SIMPLE_JWT.get("BLACKLIST_TIMEOUT", 86400),
        )

    @staticmethod
    def blacklist_all_user_tokens(user_id):
        """Met tous les tokens d'un utilisateur dans la liste noire."""
        try:
            user_tokens_key = f"user_tokens:{user_id}"
            if hasattr(cache, "client"):
                # reddis implementation
                actives_tokens = cache.client.smembers(user_tokens_key)
                if not actives_tokens:
                    return 0
                # blackliste chaque token
                for jti in actives_tokens:
                    (
                        TokenManager.blacklist_token(jti.decode("utf-8"))
                        if isinstance(jti, bytes)
                        else jti
                    )
                # supprime la liste des tokens actifs
                cache.client.delete(user_tokens_key)
                return len(actives_tokens)
            else:
                # implementation generic pour LocMemCache
                token_set = cache.get(user_tokens_key, set())
                if not token_set:
                    return 0
                for jti in token_set:
                    TokenManager.blacklist_token(jti)
                # supprime la liste des tokens actifs
                cache.delete(user_tokens_key)
                return len(token_set)
        except Exception as e:
            logger.error(f"Error blacklisting tokens for user {user_id}: {str(e)}")
            return 0

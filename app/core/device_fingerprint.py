"""
Device Fingerprint Manager

Manages device fingerprints for Telegram accounts using TLAPI library.
Provides generation, rotation, and validation of device fingerprints.
"""

from datetime import datetime
from typing import Optional, Dict, List, TYPE_CHECKING
import logging

from app.tlapi import API, APIData

if TYPE_CHECKING:
    from app.models.account import Account

logger = logging.getLogger(__name__)


class DeviceFingerprintManager:
    """
    Manager for device fingerprints using TLAPI.

    Provides official Telegram API credentials and realistic device fingerprints
    to avoid detection and account linking.
    """

    # Available API presets from TLAPI
    AVAILABLE_PRESETS = [
        "TelegramAndroid",
        "TelegramIOS",
        "TelegramDesktop",
        "TelegramMacOS",
        "TelegramAndroidX",
        "TelegramAndroidBeta",
        "TelegramWeb_Z",
        "TelegramWeb_K",
        "Webogram",
    ]

    @staticmethod
    def get_available_presets() -> List[str]:
        """Get list of available API presets."""
        return DeviceFingerprintManager.AVAILABLE_PRESETS.copy()

    @staticmethod
    def generate_api(account: "Account", preset_name: Optional[str] = None) -> APIData:
        """
        Generate API configuration with device fingerprint for an account.

        Args:
            account: Account model instance
            preset_name: Override API preset (default: use account.api_preset)

        Returns:
            APIData: Generated API configuration with device fingerprints

        Raises:
            ValueError: If preset name is invalid
        """
        # Determine preset to use
        preset = preset_name or account.api_preset or "TelegramAndroid"

        # Validate preset
        if preset not in DeviceFingerprintManager.AVAILABLE_PRESETS:
            logger.warning(f"Invalid preset '{preset}', falling back to TelegramAndroid")
            preset = "TelegramAndroid"

        # Get API class
        try:
            api_class = getattr(API, preset)
        except AttributeError:
            logger.error(f"Preset '{preset}' not found in TLAPI, using TelegramAndroid")
            api_class = API.TelegramAndroid

        # If account already has complete fingerprint data, use it
        if (account.device_model and
            account.system_version and
            account.app_version):

            logger.info(
                f"Using existing fingerprint for {account.phone_number}: "
                f"{account.device_model} {account.system_version}"
            )

            # Create APIData with existing data
            # Note: We need to get the base API to get api_id and api_hash
            base_api = api_class
            return APIData(
                api_id=account.api_id or base_api.api_id,
                api_hash=account.api_hash or base_api.api_hash,
                device_model=account.device_model,
                system_version=account.system_version,
                app_version=account.app_version,
                lang_code=account.lang_code or "en",
                system_lang_code=account.system_lang_code or "en"
            )

        # Generate new fingerprint
        unique_id = account.device_unique_id or account.phone_number

        logger.info(
            f"Generating new fingerprint for {account.phone_number} "
            f"with preset '{preset}' and unique_id '{unique_id}'"
        )

        # Generate using TLAPI
        generated_api = api_class.Generate(unique_id=unique_id)

        logger.info(
            f"Generated fingerprint: {generated_api.device_model} "
            f"{generated_api.system_version} - {generated_api.app_version}"
        )

        return generated_api

    @staticmethod
    def apply_fingerprint_to_account(
        account: "Account",
        api_data: APIData,
        save_to_db: bool = False
    ) -> None:
        """
        Apply generated fingerprint to account model.

        Args:
            account: Account model instance
            api_data: Generated API data with fingerprints
            save_to_db: Whether to commit changes to database
        """
        # Update account fields
        account.device_model = api_data.device_model
        account.system_version = api_data.system_version
        account.app_version = api_data.app_version
        account.lang_code = api_data.lang_code
        account.system_lang_code = api_data.system_lang_code

        # Update API credentials if using official API
        if account.use_official_api:
            account.api_id = api_data.api_id
            account.api_hash = api_data.api_hash

        # Update rotation timestamp
        account.fingerprint_last_rotated = datetime.utcnow()

        logger.info(
            f"Applied fingerprint to account {account.phone_number}: "
            f"{api_data.device_model} {api_data.system_version}"
        )

        if save_to_db:
            from app.services.database import get_session
            with get_session() as session:
                session.add(account)
                session.commit()
                logger.info(f"Saved fingerprint to database for {account.phone_number}")

    @staticmethod
    def rotate_fingerprint(
        account: "Account",
        new_preset: Optional[str] = None,
        save_to_db: bool = False
    ) -> APIData:
        """
        Rotate (regenerate) device fingerprint for an account.

        Args:
            account: Account model instance
            new_preset: New API preset to use (default: keep current)
            save_to_db: Whether to commit changes to database

        Returns:
            APIData: Newly generated API configuration
        """
        # Update preset if provided
        if new_preset:
            if new_preset not in DeviceFingerprintManager.AVAILABLE_PRESETS:
                raise ValueError(f"Invalid preset: {new_preset}")
            account.api_preset = new_preset

        # Change unique_id to force new generation
        # Append timestamp to ensure different fingerprint
        import time
        old_unique_id = account.device_unique_id or account.phone_number
        account.device_unique_id = f"{old_unique_id}_{int(time.time())}"

        logger.info(
            f"Rotating fingerprint for {account.phone_number} "
            f"from {account.device_model} to new device"
        )

        # Generate new fingerprint
        new_api = DeviceFingerprintManager.generate_api(account)

        # Apply to account
        DeviceFingerprintManager.apply_fingerprint_to_account(
            account,
            new_api,
            save_to_db=save_to_db
        )

        return new_api

    @staticmethod
    def validate_fingerprint(account: "Account") -> Dict[str, bool]:
        """
        Validate that account has complete and valid fingerprint.

        Args:
            account: Account model instance

        Returns:
            Dict with validation results
        """
        results = {
            "has_device_model": bool(account.device_model),
            "has_system_version": bool(account.system_version),
            "has_app_version": bool(account.app_version),
            "has_lang_code": bool(account.lang_code),
            "has_valid_preset": account.api_preset in DeviceFingerprintManager.AVAILABLE_PRESETS,
            "is_complete": False,
        }

        # Check if complete
        results["is_complete"] = all([
            results["has_device_model"],
            results["has_system_version"],
            results["has_app_version"],
            results["has_lang_code"],
        ])

        return results

    @staticmethod
    def get_fingerprint_summary(account: "Account") -> str:
        """
        Get human-readable summary of account's fingerprint.

        Args:
            account: Account model instance

        Returns:
            String summary of fingerprint
        """
        if not account.device_model:
            return "No fingerprint configured"

        last_rotated = ""
        if account.fingerprint_last_rotated:
            last_rotated = f" (rotated {account.fingerprint_last_rotated.strftime('%Y-%m-%d')})"

        return (
            f"{account.device_model} | {account.system_version} | "
            f"{account.app_version} | {account.api_preset}{last_rotated}"
        )

    @staticmethod
    def ensure_fingerprint(account: "Account", save_to_db: bool = False) -> APIData:
        """
        Ensure account has a fingerprint, generating one if needed.

        Args:
            account: Account model instance
            save_to_db: Whether to commit changes to database

        Returns:
            APIData: Existing or newly generated API configuration
        """
        validation = DeviceFingerprintManager.validate_fingerprint(account)

        if validation["is_complete"]:
            # Already has complete fingerprint, return it
            return DeviceFingerprintManager.generate_api(account)

        # Generate new fingerprint
        logger.info(f"Account {account.phone_number} missing fingerprint, generating...")
        api_data = DeviceFingerprintManager.generate_api(account)

        # Apply to account
        DeviceFingerprintManager.apply_fingerprint_to_account(
            account,
            api_data,
            save_to_db=save_to_db
        )

        return api_data

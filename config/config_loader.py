import os
import yaml
from dotenv import load_dotenv
import logging

load_dotenv(override=True) # Load environment variables from .env file, allowing overrides

class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _get_val(self, env_key, config_key, default=None):
        """Helper to get value from env or config with placeholder detection."""
        val = os.getenv(env_key)
        if val is None:
            val = self._config.get(config_key)
        
        # If the value is a literal placeholder like "${VARIABLE}", treat it as not set
        if isinstance(val, str) and val.startswith("${") and val.endswith("}"):
            return default
        
        return val if val is not None else default

    def _load_config(self):
        config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
        try:
            with open(config_path, 'r') as f:
                self._config = yaml.safe_load(f)
        except FileNotFoundError:
            logging.warning(f"Warning: config.yaml not found at {config_path}. Using environment variables only.")
            self._config = {}
        except Exception as e:
            logging.error(f"Error loading config.yaml: {e}")
            self._config = {}

        # Database and API Keys
        self.DATABASE_URL = self._get_val("DATABASE_URL", "database_url")
        self.GEMINI_API_KEY = self._get_val("GEMINI_API_KEY", "gemini_api_key")
        self.TWILIO_ACCOUNT_SID = self._get_val("TWILIO_ACCOUNT_SID", "twilio_account_sid")
        self.TWILIO_AUTH_TOKEN = self._get_val("TWILIO_AUTH_TOKEN", "twilio_auth_token")
        self.TWILIO_WHATSAPP_NUMBER = self._get_val("TWILIO_WHATSAPP_NUMBER", "twilio_whatsapp_number")

        # General App Settings
        self.APP_SECRET_KEY = self._get_val("APP_SECRET_KEY", "app_secret_key", "super_secret_key_dev")
        self.LOG_LEVEL = self._get_val("LOG_LEVEL", "log_level", "INFO")
        
        # File Upload Settings
        self.RESUME_UPLOAD_FOLDER = self._config.get("resume_upload_folder", "uploads/resumes")
        self.JD_UPLOAD_FOLDER = self._config.get("jd_upload_folder", "uploads/jds")
        self.TEMP_BULK_UPLOAD_FOLDER = self._config.get("temp_bulk_upload_folder", "uploads/temp_bulk")

        # ATS Settings
        self.ats_weights = self._config.get("ats_weights", {})
        self.ATS_SHORTLIST_THRESHOLD = float(self._get_val("ATS_SHORTLIST_THRESHOLD", "ats_shortlist_threshold", 70.0))
        
        # Concurrency Settings
        self.MAX_WORKERS_RESUME_PROCESSING = int(self._get_val("MAX_WORKERS_RESUME_PROCESSING", "max_workers_resume_processing", 8))
        self.MAX_WORKERS_WHATSAPP_SENDING = int(self._get_val("MAX_WORKERS_WHATSAPP_SENDING", "max_workers_whatsapp_sending", 5))

        # --- NEW: Email Notification (SMTP) Settings ---
        self.SMTP_SERVER = self._get_val("SMTP_SERVER", "smtp_server")
        self.SMTP_PORT = int(self._get_val("SMTP_PORT", "smtp_port", 587))
        self.SMTP_SENDER_EMAIL = self._get_val("SMTP_SENDER_EMAIL", "smtp_sender_email")
        self.SMTP_USERNAME = self._get_val("SMTP_USERNAME", "smtp_username")
        self.SMTP_PASSWORD = self._get_val("SMTP_PASSWORD", "smtp_password")
        self.HR_RECIPIENT_EMAIL = self._get_val("HR_RECIPIENT_EMAIL", "hr_recipient_email")

config = Config()
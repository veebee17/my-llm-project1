#!/usr/bin/env python3
"""
API Configuration Utilities

This module provides utilities for loading and managing API keys and configurations
from environment variables in a secure and consistent manner.
"""

import os
from typing import Optional, Dict, Any
import warnings

try:
    from dotenv import load_dotenv
except ImportError:
    warnings.warn("python-dotenv not installed. Install with: pip install python-dotenv")
    load_dotenv = None

try:
    import streamlit as st
    STREAMLIT_AVAILABLE = True
except ImportError:
    STREAMLIT_AVAILABLE = False


class APIConfig:
    """
    Centralized API configuration management for various AI services.
    """
    
    def __init__(self, env_file: Optional[str] = None):
        """
        Initialize API configuration.
        
        Args:
            env_file: Optional path to .env file. If None, uses default locations.
        """
        self.env_file = env_file
        self._load_environment()
    
    def _load_environment(self):
        """Load environment variables from .env file if available."""
        if load_dotenv and self.env_file:
            load_dotenv(self.env_file)
        elif load_dotenv:
            # Try to load from common locations
            env_paths = ['.env', '../.env', '../../.env']
            for path in env_paths:
                if os.path.exists(path):
                    load_dotenv(path)
                    break
    
    def _get_env_var(self, key: str, default: Optional[str] = None, required: bool = False) -> Optional[str]:
        """
        Get environment variable with optional default and validation.
        Supports both environment variables and Streamlit secrets.
        
        Args:
            key: Environment variable name
            default: Default value if not found
            required: Whether the variable is required
            
        Returns:
            Variable value or default
            
        Raises:
            ValueError: If required variable is not found
        """
        value = None
        
        # First try Streamlit secrets if available
        if STREAMLIT_AVAILABLE:
            try:
                # Try to get from Streamlit secrets
                if hasattr(st, 'secrets') and 'api_keys' in st.secrets:
                    value = st.secrets.api_keys.get(key)
            except Exception:
                pass  # Fall back to environment variables
        
        # Fall back to environment variables
        if value is None:
            value = os.getenv(key, default)
        
        if required and not value:
            raise ValueError(f"Required environment variable '{key}' not found")
        
        return value
    
    # API Key Getters
    def get_openai_key(self) -> Optional[str]:
        """Get OpenAI API key."""
        return self._get_env_var('OPENAI_API_KEY')
    
    def get_openai_org_id(self) -> Optional[str]:
        """Get OpenAI organization ID."""
        return self._get_env_var('OPENAI_ORG_ID')
    
    def get_gemini_key(self) -> Optional[str]:
        """Get Google Gemini API key."""
        return self._get_env_var('GOOGLE_API_KEY')
    
    def get_google_project_id(self) -> Optional[str]:
        """Get Google Cloud project ID."""
        return self._get_env_var('GOOGLE_PROJECT_ID')
    
    def get_groq_key(self) -> Optional[str]:
        """Get Groq API key."""
        return self._get_env_var('GROQ_API_KEY')
    
    def get_anthropic_key(self) -> Optional[str]:
        """Get Anthropic API key."""
        return self._get_env_var('ANTHROPIC_API_KEY')
    
    def get_huggingface_token(self) -> Optional[str]:
        """Get Hugging Face token."""
        return self._get_env_var('HUGGINGFACE_TOKEN')
    
    def get_wandb_key(self) -> Optional[str]:
        """Get Weights & Biases API key."""
        return self._get_env_var('WANDB_API_KEY')
    
    # Model Configuration
    def get_default_models(self) -> Dict[str, str]:
        """Get default model configurations for each provider."""
        return {
            'openai': 'gpt-3.5-turbo',
            'gemini': 'gemini-2.5-flash',
            'groq': 'llama-3.1-8b-instant',
            'anthropic': 'claude-3-5-haiku-20241022'
        }
    
    # Client Getters
    def get_openai_client(self):
        """Get configured OpenAI client."""
        try:
            import openai
            api_key = self.get_openai_key()
            if not api_key:
                warnings.warn("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
                return None
            
            client = openai.OpenAI(
                api_key=api_key,
                organization=self.get_openai_org_id()
            )
            return client
        except ImportError:
            warnings.warn("OpenAI library not installed. Install with: pip install openai")
            return None
    
    def get_gemini_client(self):
        """Get configured Google Gemini client."""
        try:
            import google.generativeai as genai
            api_key = self.get_gemini_key()
            if not api_key:
                warnings.warn("Google API key not found. Set GOOGLE_API_KEY environment variable.")
                return None
            
            genai.configure(api_key=api_key)
            return genai
        except ImportError:
            warnings.warn("Google Generative AI library not installed. Install with: pip install google-generativeai")
            return None
    
    def get_groq_client(self):
        """Get configured Groq client."""
        try:
            from groq import Groq
            api_key = self.get_groq_key()
            if not api_key:
                warnings.warn("Groq API key not found. Set GROQ_API_KEY environment variable.")
                return None
            
            client = Groq(api_key=api_key)
            return client
        except ImportError:
            warnings.warn("Groq library not installed. Install with: pip install groq")
            return None
    
    def get_anthropic_client(self):
        """Get configured Anthropic client."""
        try:
            import anthropic
            api_key = self.get_anthropic_key()
            if not api_key:
                warnings.warn("Anthropic API key not found. Set ANTHROPIC_API_KEY environment variable.")
                return None
            
            client = anthropic.Anthropic(api_key=api_key)
            return client
        except ImportError:
            warnings.warn("Anthropic library not installed. Install with: pip install anthropic")
            return None
    
    def validate_configuration(self) -> Dict[str, bool]:
        """
        Validate API configuration and return status for each service.
        
        Returns:
            Dictionary with service names as keys and boolean status as values
        """
        return {
            'openai': bool(self.get_openai_key()),
            'gemini': bool(self.get_gemini_key()),
            'groq': bool(self.get_groq_key()),
            'anthropic': bool(self.get_anthropic_key()),
            'huggingface': bool(self.get_huggingface_token()),
            'wandb': bool(self.get_wandb_key())
        }
    
    def print_configuration_status(self):
        """Print the current configuration status."""
        status = self.validate_configuration()
        print("API Configuration Status:")
        print("-" * 30)
        for service, configured in status.items():
            status_text = "✓ Configured" if configured else "✗ Not configured"
            print(f"{service.capitalize():12}: {status_text}")


# Convenience functions
def get_api_config() -> APIConfig:
    """Get a default APIConfig instance."""
    return APIConfig()


def quick_setup_check():
    """Quick setup check for API configuration."""
    config = APIConfig()
    config.print_configuration_status()


if __name__ == "__main__":
    quick_setup_check()
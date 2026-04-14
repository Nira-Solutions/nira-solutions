"""Init Sentry — appelé au démarrage de l'API FastAPI et des scripts."""
import os


def init_sentry(service: str = "agents") -> None:
    dsn = os.environ.get("SENTRY_DSN")
    if not dsn:
        return
    try:
        import sentry_sdk
        from sentry_sdk.integrations.fastapi import FastApiIntegration
        from sentry_sdk.integrations.starlette import StarletteIntegration
        sentry_sdk.init(
            dsn=dsn,
            environment=os.environ.get("NIRA_ENV", "production"),
            traces_sample_rate=0.1,
            profiles_sample_rate=0.1,
            integrations=[StarletteIntegration(), FastApiIntegration()],
            release=f"{service}@{os.environ.get('RAILWAY_DEPLOYMENT_ID', 'local')}",
        )
    except ImportError:
        pass  # sentry-sdk optionnel

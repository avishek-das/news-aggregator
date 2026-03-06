"""Daily fetch job — run as: python -m app.jobs.fetch_sources"""
import asyncio
import logging

from app.adapters import get_adapter
from app.repositories.sources import find_active, record_success, record_failure
from app.repositories.items import upsert

logger = logging.getLogger(__name__)


async def run_fetch_job() -> None:
    sources = find_active()
    logger.info("Starting fetch job for %d active sources", len(sources))

    for source in sources:
        adapter_name: str = source.fetch_config.get("adapter", "")
        try:
            adapter = get_adapter(adapter_name, source.id, source.fetch_config)
            items = await adapter.fetch()
            count = upsert(items, str(source.id))
            record_success(str(source.id), count)
            logger.info("Source '%s': fetched %d items (%d new)", source.name, len(items), count)
        except Exception as exc:
            logger.error("Source '%s' failed: %s", getattr(source, "name", source.id), exc)
            record_failure(str(source.id), str(exc))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(run_fetch_job())

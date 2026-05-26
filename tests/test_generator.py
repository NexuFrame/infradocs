from pathlib import Path

import pytest

from infradocs.config import InfraDocsConfig
from infradocs.generator import SiteGenerator

SAMPLE = Path(__file__).parent.parent / "sample-data"


@pytest.fixture
def tmp_config(tmp_path):
    return InfraDocsConfig(
        site_name="Test Site",
        input_dir=str(SAMPLE),
        output_dir=str(tmp_path / "output"),
        theme="dark",
        logo="",
        footer="Test Footer",
    )


def test_build_creates_output_dir(tmp_config, tmp_path):
    gen = SiteGenerator(tmp_config)
    gen.build()
    assert (tmp_path / "output").exists()


def test_build_creates_index(tmp_config, tmp_path):
    gen = SiteGenerator(tmp_config)
    gen.build()
    assert (tmp_path / "output" / "index.html").exists()

from pathlib import Path

from app.services.generator_parser import parse_mgnd


def test_parses_real_uruguay_generator_rows() -> None:
    generators = parse_mgnd(Path("data/UY_SDDP/mgndur.dat"))
    assert len(generators) >= 80
    assert any(generator.name == "UPM S.A. BIC" for generator in generators)
    assert all(generator.coordinate_status == "not-provided" for generator in generators)
    assert all(generator.source_line > 2 for generator in generators)

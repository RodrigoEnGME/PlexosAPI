from pathlib import Path

from app.services.generator_parser import parse_mgnd


def test_parses_real_uruguay_generator_rows() -> None:
    generators = parse_mgnd(Path("data/UY_SDDP/mgndur.dat"))
    assert len(generators) >= 80
    assert any(generator.name == "UPM S.A. BIC" for generator in generators)
    assert all(generator.coordinate_status == "not-provided" for generator in generators)
    assert all(generator.source_line > 2 for generator in generators)


def test_parses_mgnd_rows_without_plant_type() -> None:
    generators = parse_mgnd(Path("data/PA_202503_R25_1050_Gatun_en_BC02/mgndni.dat"))
    trini = [item for item in generators if item.name == "NI-Trini SOL"]

    assert [(item.source_line, item.capacity_mw) for item in trini] == [(3, 76.38), (5, 101.38), (6, 126.38)]
